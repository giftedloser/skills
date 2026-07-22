#!/usr/bin/env python3
"""Collect repository-presentation evidence without prescribing generic polish."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html import unescape as html_unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11.
    tomllib = None  # type: ignore[assignment]


MANIFESTS = (
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "composer.json",
    "setup.py",
    "setup.cfg",
    "Dockerfile",
)
SURFACE_FILES = (
    "LICENSE",
    "LICENSE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "CODE_OF_CONDUCT.md",
)
VISUAL_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
SKIP_DIRS = {".git", ".venv", "dist", "node_modules", "target", "vendor"}
README_SUFFIXES = {"", ".md", ".markdown", ".mdown", ".mkdn", ".rst", ".adoc", ".asciidoc", ".asc", ".org", ".txt"}
MARKDOWN_README_SUFFIXES = {"", ".md", ".markdown", ".mdown", ".mkdn"}
MARKDOWN_ESCAPABLE = frozenset(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""")
ATX_HEADING = re.compile(r"^[ \t]{0,3}#{1,6}[ \t]+(.+?)(?:[ \t]+#+[ \t]*)?$", re.MULTILINE)
SETEXT_HEADING = re.compile(r"^[ \t]{0,3}([^\n]+?)[ \t]*\n[ \t]{0,3}(?:=+|-+)[ \t]*$", re.MULTILINE)
HTML_COMMENT = re.compile(r"<!--.*?(?:-->|$)", re.DOTALL)
RAW_HTML_BLOCK = re.compile(r"<(pre|code|script|style)\b[^>]*>.*?(?:</\1\s*>|$)", re.IGNORECASE | re.DOTALL)
REFERENCE_DEFINITION = re.compile(r"^\s*\[([^\]]+)\]:\s*(.+?)\s*$", re.MULTILINE)
REFERENCE_USAGE = re.compile(r"(?<!\\)!?\[([^\]]+)\]\[([^\]]*)\]")
SHORTCUT_REFERENCE = re.compile(r"(?<!\\)!?\[([^\]]+)\](?![\[(]|\s*:)")
LIST_ITEM = re.compile(r"^[ \t]{0,3}(?:[-+*]|\d+[.)])[ \t]+")


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def relative_files(root: Path, suffixes: set[str], issues: list[dict[str, str]]) -> list[str]:
    files: list[str] = []

    def record_error(error: OSError) -> None:
        issues.append({"kind": "unreadable_path", "path": error.filename or ".", "detail": str(error)})

    for directory, names, filenames in os.walk(root, onerror=record_error):
        names[:] = [name for name in names if name.lower() not in SKIP_DIRS]
        base = Path(directory)
        for name in filenames:
            path = base / name
            if path.suffix.lower() in suffixes:
                files.append(path.relative_to(root).as_posix())
    return sorted(files)


def readme_candidates(root: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in root.iterdir()
            if path.is_file() and path.stem.casefold() == "readme" and path.suffix.casefold() in README_SUFFIXES
        ),
        key=lambda path: (path.name.lower() != "readme.md", path.name.lower()),
    )


def strip_nonrendered(markdown: str) -> str:
    """Remove comments and code where Markdown-looking text is not a link."""
    output: list[str] = []
    fence_char = ""
    fence_length = 0
    indented_code = False
    previous_blank = True
    list_content_indent: int | None = None

    for line in markdown.splitlines(keepends=True):
        fence = re.match(r"^[ \t]{0,3}(`{3,}|~{3,})", line)
        if fence_char:
            if re.match(rf"^[ \t]{{0,3}}{re.escape(fence_char)}{{{fence_length},}}[ \t]*(?:\r?\n)?$", line):
                fence_char = ""
            continue
        if fence:
            marker = fence.group(1)
            if marker[0] == "`" and "`" in line[fence.end() :]:
                fence = None
            else:
                fence_char, fence_length = marker[0], len(marker)
                continue
        if not line.strip():
            if not indented_code:
                output.append(line)
            previous_blank = True
            continue
        list_item = LIST_ITEM.match(line)
        if list_item:
            list_content_indent = len(line[: list_item.end()].expandtabs(4))
            indented_code = False
            previous_blank = False
            output.append(line)
            continue
        indent = len(line) - len(line.lstrip(" \t"))
        if list_content_indent is not None and indent >= list_content_indent:
            if indent >= list_content_indent + 4 and (indented_code or previous_blank):
                indented_code = True
                continue
            indented_code = False
            previous_blank = False
            output.append(line)
            continue
        if list_content_indent is not None and previous_blank:
            list_content_indent = None
        if (line.startswith("    ") or line.startswith("\t")) and (indented_code or previous_blank):
            indented_code = True
            continue
        indented_code = False
        previous_blank = False
        output.append(line)

    rendered = "".join(output)
    rendered = RAW_HTML_BLOCK.sub("", rendered)
    rendered = HTML_COMMENT.sub("", rendered)
    return strip_inline_code(rendered)


def strip_inline_code(markdown: str) -> str:
    """Remove code spans only when opening and closing runs are exactly equal."""
    output: list[str] = []
    position = 0
    while position < len(markdown):
        opening = markdown.find("`", position)
        if opening < 0:
            output.append(markdown[position:])
            break
        output.append(markdown[position:opening])
        run_end = opening
        while run_end < len(markdown) and markdown[run_end] == "`":
            run_end += 1
        marker = markdown[opening:run_end]
        search = run_end
        closing = -1
        while True:
            candidate = markdown.find(marker, search)
            if candidate < 0:
                break
            after = candidate + len(marker)
            if (candidate == 0 or markdown[candidate - 1] != "`") and (
                after == len(markdown) or markdown[after] != "`"
            ):
                closing = candidate
                break
            search = candidate + 1
        if closing < 0:
            output.append(marker)
            position = run_end
        else:
            output.append("code")
            position = closing + len(marker)
    return "".join(output)


def heading_titles(markdown: str) -> list[str]:
    headings = [(match.start(), match.group(1).strip()) for match in ATX_HEADING.finditer(markdown)]
    headings.extend((match.start(), match.group(1).strip()) for match in SETEXT_HEADING.finditer(markdown))
    return [title for _, title in sorted(headings)]


def is_escaped(text: str, position: int) -> bool:
    slashes = 0
    position -= 1
    while position >= 0 and text[position] == "\\":
        slashes += 1
        position -= 1
    return slashes % 2 == 1


def link_label_opening(text: str, closing: int) -> int:
    """Find the unmatched opening bracket in the current paragraph."""
    unix_boundary = text.rfind("\n\n", 0, closing)
    windows_boundary = text.rfind("\r\n\r\n", 0, closing)
    boundary = max(
        unix_boundary + 2 if unix_boundary >= 0 else 0,
        windows_boundary + 4 if windows_boundary >= 0 else 0,
    )
    nested = 0
    for position in range(closing - 1, boundary - 1, -1):
        if is_escaped(text, position):
            continue
        if text[position] == "]":
            nested += 1
        elif text[position] == "[":
            if nested == 0:
                return position
            nested -= 1
    return -1


def unescape_markdown(value: str) -> str:
    result: list[str] = []
    position = 0
    while position < len(value):
        if value[position] == "\\" and position + 1 < len(value) and value[position + 1] in MARKDOWN_ESCAPABLE:
            position += 1
        result.append(value[position])
        position += 1
    return "".join(result)


def inline_destinations(markdown: str) -> list[str]:
    """Parse Markdown inline destinations, including balanced parentheses."""
    targets: list[str] = []
    position = 0
    while True:
        opening = markdown.find("](", position)
        if opening < 0:
            return targets
        position = opening + 2
        label_opening = link_label_opening(markdown, opening)
        if label_opening < 0 or is_escaped(markdown, label_opening) or is_escaped(markdown, opening):
            continue
        while position < len(markdown) and markdown[position].isspace():
            position += 1
        if position >= len(markdown):
            continue
        if markdown[position] == "<":
            closing = markdown.find(">", position + 1)
            if closing >= 0:
                targets.append(markdown[position + 1 : closing])
                position = closing + 1
            continue

        start = position
        depth = 0
        escaped = False
        while position < len(markdown):
            char = markdown[position]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == "(":
                depth += 1
            elif char == ")":
                if depth == 0:
                    break
                depth -= 1
            elif char.isspace() and depth == 0:
                break
            position += 1
        if position > start:
            targets.append(markdown[start:position])


def reference_destinations(markdown: str) -> list[str]:
    def label(value: str) -> str:
        return " ".join(value.casefold().split())

    definitions: dict[str, str] = {}
    for name, raw in REFERENCE_DEFINITION.findall(markdown):
        value = raw.strip()
        if value.startswith("<") and ">" in value:
            value = value[1 : value.index(">")]
        else:
            value = value.split(maxsplit=1)[0]
        definitions.setdefault(label(name), value)

    used = {label(name or text) for text, name in REFERENCE_USAGE.findall(markdown)}
    used.update(label(name) for name in SHORTCUT_REFERENCE.findall(markdown))
    return [definitions[name] for name in sorted(used) if name in definitions]


def srcset_destinations(value: str) -> list[str]:
    """Split common srcset forms while keeping data-URI commas intact."""
    candidates = (
        re.split(r"(?<=[0-9][wx]),\s*|,(?=\s)", value)
        if "data:" in value.casefold()
        else value.split(",")
    )
    return [
        candidate.strip().rsplit(maxsplit=1)[0]
        if re.search(r"\s+[0-9.]+[wx]\s*$", candidate)
        else candidate.strip()
        for candidate in candidates
        if candidate.strip()
    ]


class ReferenceHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name.casefold(): value for name, value in attrs if value is not None}
        if tag.casefold() == "a" and "href" in attributes:
            self.targets.append(attributes["href"])
        if tag.casefold() in {"img", "source"}:
            if "src" in attributes:
                self.targets.append(attributes["src"])
            if "srcset" in attributes:
                self.targets.extend(srcset_destinations(attributes["srcset"]))


def html_destinations(markdown: str) -> list[str]:
    parser = ReferenceHTMLParser()
    parser.feed(markdown)
    parser.close()
    return parser.targets


def local_targets(markdown: str) -> tuple[set[str], list[dict[str, str]]]:
    candidates = [
        *inline_destinations(markdown),
        *reference_destinations(markdown),
        *html_destinations(markdown),
    ]
    targets: set[str] = set()
    issues: list[dict[str, str]] = []
    for target in candidates:
        target = unescape_markdown(html_unescape(target.strip()))
        try:
            parsed = urlsplit(target)
        except ValueError as error:
            issues.append({"kind": "malformed_reference", "path": "README", "detail": f"{target}: {error}"})
            continue
        if not target or target.startswith(("#", "/")) or parsed.scheme or parsed.netloc:
            continue
        path = unquote(parsed.path).replace("\\", "/")
        if path:
            targets.add(path)
    return targets, issues


def inspect_manifest(path: Path, issues: list[dict[str, str]]) -> dict[str, Any]:
    facts: dict[str, Any] = {"path": path.name}
    if path.name in {"package.json", "composer.json"}:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            issues.append({"kind": "unreadable_manifest", "path": path.name, "detail": str(error)})
            return facts
        if not isinstance(data, dict):
            issues.append({"kind": "invalid_manifest", "path": path.name, "detail": "Expected a JSON object."})
            return facts
        facts.update({key: data[key] for key in ("name", "description", "version", "license") if data.get(key)})
        if path.name == "package.json":
            facts["scripts"] = sorted(data.get("scripts", {})) if isinstance(data.get("scripts"), dict) else []
    elif path.name in {"pyproject.toml", "Cargo.toml"} and tomllib is not None:
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
            issues.append({"kind": "unreadable_manifest", "path": path.name, "detail": str(error)})
            return facts
        section = "project" if path.name == "pyproject.toml" else "package"
        project = data.get(section) if isinstance(data, dict) else None
        if isinstance(project, dict):
            facts.update({key: project[key] for key in ("name", "description", "version", "license") if project.get(key)})
    return facts


def audit(root: Path) -> dict[str, Any]:
    root = root.resolve()
    issues: list[dict[str, str]] = []
    readmes = readme_candidates(root)
    readme_fact: dict[str, Any] | None = None

    if readmes:
        readme = readmes[0]
        text = read_text(readme)
        if text is None:
            issues.append({"kind": "unreadable_readme", "path": readme.name, "detail": "The file could not be read."})
        else:
            rendered = strip_nonrendered(text)
            headings = heading_titles(rendered)
            if readme.suffix.casefold() in MARKDOWN_README_SUFFIXES:
                target_set, reference_issues = local_targets(rendered)
                targets = sorted(target_set)
                for issue in reference_issues:
                    issue["path"] = readme.name
                issues.extend(reference_issues)
            else:
                targets = []
            readme_fact = {
                "path": readme.name,
                "characters": len(text.strip()),
                "headings": headings,
                "local_references": targets,
            }
            for target in targets:
                resolved = (readme.parent / target).resolve()
                try:
                    resolved.relative_to(root)
                except ValueError:
                    issues.append({"kind": "reference_outside_repo", "path": readme.name, "detail": target})
                else:
                    if not resolved.exists():
                        issues.append({"kind": "broken_local_reference", "path": readme.name, "detail": target})

    manifests = [inspect_manifest(root / name, issues) for name in MANIFESTS if (root / name).is_file()]
    workflows = sorted(path.relative_to(root).as_posix() for path in (root / ".github" / "workflows").glob("*.y*ml"))
    visuals = relative_files(root, VISUAL_SUFFIXES, issues)

    return {
        "root": str(root),
        "readme": readme_fact,
        "other_readmes": [path.name for path in readmes[1:]],
        "manifests": manifests,
        "repository_surface": [name for name in SURFACE_FILES if (root / name).is_file()],
        "workflows": workflows,
        "visual_asset_count": len(visuals),
        "visual_assets": visuals[:100],
        "visual_assets_truncated": len(visuals) > 100,
        "confirmed_issues": issues,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Collect evidence for repository presentation work.")
    parser.add_argument("root", nargs="?", default=os.environ.get("REPO_ROOT", "."))
    args = parser.parse_args(argv)
    root = Path(args.root)
    if not root.is_dir():
        print(f"error: repository root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2
    print(json.dumps(audit(root), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
