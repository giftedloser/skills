#!/usr/bin/env python3
"""Evidence-backed repository hygiene audit for repo-polisher."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback.
    tomllib = None  # type: ignore[assignment]


PACKAGE_FILES = [
    "package.json",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "Cargo.toml",
    "go.mod",
    "composer.json",
    "Dockerfile",
    "*.csproj",
]

README_SECTIONS = {
    "install": ["install", "installation", "setup"],
    "usage": ["usage", "quick start", "getting started", "run"],
    "configuration": ["configuration", "config", "environment", "env vars"],
    "development": ["development", "developing", "local development", "contributing"],
    "testing": ["test", "testing", "quality"],
}

README_SECTION_DOC_FALLBACKS = {
    "install": ["docs/installation.md", "docs/setup.md", "docs/quick-start.md"],
    "configuration": ["docs/installation.md", "docs/configuration.md", "docs/setup.md"],
    "testing": ["tests/README.md", "docs/testing.md", "docs/development.md"],
}

PLACEHOLDER_MARKERS = [
    "todo",
    "fixme",
    "lorem ipsum",
    "your project",
    "project name",
    "coming soon",
    "tbd",
    "insert ",
    "replace me",
]

SECRET_PATTERNS = [
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "id_rsa",
    "id_dsa",
    "credentials.json",
    "service-account*.json",
]

SAFE_SECRET_TEMPLATE_SUFFIXES = (
    ".example",
    ".sample",
    ".template",
    ".dist",
)

GITIGNORE_EXPECTATIONS = {
    "node": ["node_modules", "dist", "coverage", ".env"],
    "python": ["__pycache__", ".pytest_cache", ".venv", "dist", ".env"],
    "rust": ["target"],
    "go": ["bin", "coverage", ".env"],
    "docker": [".env"],
    "terraform": [".terraform", "*.tfstate"],
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def read_toml(path: Path) -> dict[str, Any] | None:
    if tomllib is None:
        return None
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError):
        return None
    return data if isinstance(data, dict) else None


def has_any(root: Path, patterns: list[str]) -> bool:
    return any(list(root.glob(pattern)) for pattern in patterns)


def detect_stack(root: Path) -> list[str]:
    markers = {
        "node": ["package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json"],
        "python": ["pyproject.toml", "requirements.txt", "setup.py", "setup.cfg"],
        "rust": ["Cargo.toml"],
        "go": ["go.mod"],
        "docker": ["Dockerfile", "docker-compose.yml", "compose.yml"],
        "terraform": ["main.tf", "versions.tf", "providers.tf", "*.tf"],
        "powershell": ["*.ps1", "*.psm1", "*.psd1"],
        "dotnet": ["*.csproj", "*.sln"],
    }
    return [name for name, patterns in markers.items() if has_any(root, patterns)]


def heading_titles(markdown: str) -> list[str]:
    return [
        match.group(1).strip().lower()
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", markdown, flags=re.MULTILINE)
    ]


def markdown_links(markdown: str) -> set[str]:
    links: set[str] = set()
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", markdown):
        link = match.group(1).split("#", 1)[0].strip()
        if link and not re.match(r"^[a-z]+://", link):
            links.add(link.replace("\\", "/").lstrip("./"))
    return links


def section_covered_by_linked_doc(root: Path, links: set[str], section: str, aliases: list[str]) -> bool:
    for doc in README_SECTION_DOC_FALLBACKS.get(section, []):
        if doc not in links:
            continue
        text = read_text(root / doc)
        if text and any(alias in heading for heading in heading_titles(text) for alias in aliases):
            return True
    return False


def add(findings: dict[str, Any], severity: str, area: str, message: str, evidence: str, recommendation: str) -> None:
    findings[severity].append(
        {
            "area": area,
            "message": message,
            "evidence": evidence,
            "recommendation": recommendation,
        }
    )


def audit_readme(root: Path, findings: dict[str, Any], package: dict[str, Any] | None) -> None:
    readme_path = root / "README.md"
    if not readme_path.exists():
        add(
            findings,
            "critical",
            "README",
            "missing README.md",
            "README.md was not found at the repository root.",
            "Create a factual README with overview, install, usage, configuration, development, and testing sections.",
        )
        return

    readme = read_text(readme_path)
    stripped = readme.strip()
    headings = heading_titles(readme)
    links = markdown_links(readme)
    lower = readme.lower()

    if len(stripped) < 800:
        add(
            findings,
            "recommended",
            "README",
            "README.md is too thin for a professional handoff",
            f"README.md contains {len(stripped)} non-whitespace characters.",
            "Expand it with a grounded project summary, install/run commands, configuration notes, and development workflow.",
        )

    missing_sections: list[str] = []
    for section, aliases in README_SECTIONS.items():
        has_heading = any(any(alias in heading for alias in aliases) for heading in headings)
        has_linked_doc = section_covered_by_linked_doc(root, links, section, aliases)
        if not has_heading and not has_linked_doc:
            missing_sections.append(section)
    if missing_sections:
        add(
            findings,
            "recommended",
            "README",
            "README.md is missing common operating sections",
            "Missing section groups: " + ", ".join(missing_sections),
            "Add only the sections that are supported by the repository contents and mark uncertain commands as optional.",
        )

    for marker in PLACEHOLDER_MARKERS:
        if marker in lower:
            add(
                findings,
                "polish",
                "README",
                "README.md may contain placeholder copy",
                f"Matched marker: {marker}",
                "Replace template wording with specific, maintainable project copy.",
            )
            break

    if package and package.get("name"):
        package_name = str(package["name"]).removeprefix("@").split("/")[-1].replace("-", " ")
        first_heading = headings[0] if headings else ""
        description = str(package.get("description") or "").lower()
        documented_alias = bool(
            package_name
            and package_name.lower() in lower
            and (
                "user-facing" in lower
                or "public name" in lower
                or "app name" in lower
                or first_heading in description
            )
        )
        if package_name and package_name.lower() not in first_heading and not documented_alias:
            add(
                findings,
                "polish",
                "README",
                "README title may not match package metadata",
                f"package.json name is {package['name']!r}; first README heading is {first_heading!r}.",
                "Keep the public project name consistent unless the mismatch is intentional.",
            )


def audit_package(root: Path, findings: dict[str, Any]) -> dict[str, Any] | None:
    package_path = root / "package.json"
    package = read_json(package_path) if package_path.exists() else None

    if package_path.exists() and package is None:
        add(
            findings,
            "critical",
            "package.json",
            "package.json is not valid JSON",
            "json.loads failed for package.json.",
            "Fix JSON syntax before editing package metadata or scripts.",
        )
        return None

    if package is not None:
        for field in ["description", "license", "repository"]:
            if not package.get(field):
                add(
                    findings,
                    "recommended",
                    "package.json",
                    f"package.json missing {field}",
                    f"The {field!r} field is absent or empty.",
                    "Fill this from existing repo facts; ask before choosing a license if none is declared.",
                )

        scripts = package.get("scripts") if isinstance(package.get("scripts"), dict) else {}
        if scripts and not any(name in scripts for name in ["test", "lint", "check", "typecheck", "build"]):
            add(
                findings,
                "polish",
                "package.json",
                "package scripts lack obvious quality commands",
                "Found scripts: " + ", ".join(sorted(scripts.keys())),
                "Document available quality commands in README or add conventional aliases if they already exist in tooling.",
            )
        if (root / "tests").exists() and scripts and not any(name in scripts for name in ["test", "test:unit", "test:e2e", "check"]):
            add(
                findings,
                "recommended",
                "package.json",
                "tests exist but package scripts do not expose a test command",
                "Found tests/ directory; package.json scripts are: " + ", ".join(sorted(scripts.keys())),
                "Add a conventional test script or document the exact manual test entry point in README.",
            )

    pyproject_path = root / "pyproject.toml"
    pyproject = read_toml(pyproject_path) if pyproject_path.exists() else None
    project = pyproject.get("project", {}) if isinstance(pyproject, dict) else {}
    if pyproject_path.exists() and tomllib is not None and pyproject is None:
        add(
            findings,
            "critical",
            "pyproject.toml",
            "pyproject.toml could not be parsed",
            "tomllib failed to parse pyproject.toml.",
            "Fix TOML syntax before relying on Python package metadata.",
        )
    if isinstance(project, dict) and project:
        for field in ["description", "license"]:
            if not project.get(field):
                add(
                    findings,
                    "recommended",
                    "pyproject.toml",
                    f"pyproject project metadata missing {field}",
                    f"[project].{field} is absent or empty.",
                    "Fill this from existing project facts; ask before choosing a license if none is declared.",
                )

    if not has_any(root, PACKAGE_FILES):
        add(
            findings,
            "polish",
            "metadata",
            "no recognized package or build metadata found",
            "No package/build file matched: " + ", ".join(PACKAGE_FILES),
            "If this repo is distributed or built, add the conventional metadata file for its ecosystem.",
        )

    return package


def audit_gitignore(root: Path, stack: list[str], findings: dict[str, Any]) -> None:
    gitignore_path = root / ".gitignore"
    if not gitignore_path.exists():
        add(
            findings,
            "recommended",
            ".gitignore",
            "missing .gitignore",
            ".gitignore was not found at the repository root.",
            "Add stack-appropriate ignores for dependencies, build output, caches, logs, local env files, and OS/editor noise.",
        )
        return

    text = read_text(gitignore_path).lower()
    missing: list[str] = []
    for stack_name in stack:
        for expected in GITIGNORE_EXPECTATIONS.get(stack_name, []):
            if expected.lower() not in text:
                missing.append(expected)
    if missing:
        add(
            findings,
            "recommended",
            ".gitignore",
            ".gitignore may miss stack-specific generated files",
            "Missing expected patterns: " + ", ".join(sorted(set(missing))),
            "Add safe ignore patterns without excluding source files, lockfiles, or deployment manifests.",
        )


def audit_docs(root: Path, findings: dict[str, Any]) -> None:
    for doc in ["CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md"]:
        path = root / doc
        if not path.exists():
            add(
                findings,
                "polish",
                "docs",
                f"missing {doc}",
                f"{doc} was not found at the repository root.",
                "Create it when the repo is public, collaborative, versioned, or distributed; keep placeholders clearly marked.",
            )
        elif any(marker in read_text(path).lower() for marker in PLACEHOLDER_MARKERS):
            add(
                findings,
                "polish",
                "docs",
                f"{doc} may contain placeholder copy",
                f"{doc} matched a common placeholder marker.",
                "Replace template text with repo-specific instructions or remove unsupported claims.",
            )

    if not (root / ".github" / "pull_request_template.md").exists():
        add(
            findings,
            "polish",
            "GitHub",
            "missing pull request template",
            ".github/pull_request_template.md was not found.",
            "Add a concise template with summary, testing, risk, and checklist fields for collaborative repos.",
        )

    issue_template_dir = root / ".github" / "ISSUE_TEMPLATE"
    if not issue_template_dir.exists() or not list(issue_template_dir.glob("*")):
        add(
            findings,
            "polish",
            "GitHub",
            "missing issue templates",
            ".github/ISSUE_TEMPLATE is absent or empty.",
            "Add bug and feature templates if the repository accepts external or cross-team issues.",
        )


def audit_license(root: Path, findings: dict[str, Any], package: dict[str, Any] | None) -> None:
    license_files = [path for path in [root / "LICENSE", root / "LICENSE.md", root / "LICENSE.txt"] if path.exists()]
    package_license = package.get("license") if package else None

    if not license_files and not package_license:
        add(
            findings,
            "recommended",
            "license",
            "no license detected",
            "No LICENSE file or package.json license field was found.",
            "Ask the maintainer which license to use; do not choose one without explicit direction.",
        )
    elif package_license and not license_files:
        add(
            findings,
            "polish",
            "license",
            "package metadata declares a license but no license file exists",
            f"package.json license is {package_license!r}.",
            "Add the matching license text if the repository is distributed publicly.",
        )


def audit_risky_files(root: Path, findings: dict[str, Any]) -> None:
    risky: list[str] = []
    for pattern in SECRET_PATTERNS:
        for path in root.glob(pattern):
            if not path.is_file():
                continue
            name = path.name.lower()
            if name.endswith(SAFE_SECRET_TEMPLATE_SUFFIXES) or ".example." in name or ".sample." in name:
                continue
            risky.append(str(path.relative_to(root)))
    if risky:
        add(
            findings,
            "critical",
            "sensitive files",
            "possible secret or credential files are present",
            "Matched files: " + ", ".join(sorted(risky)[:20]),
            "Verify whether these are safe fixtures. If they contain secrets, rotate credentials and remove them from history.",
        )


def audit(root: Path) -> dict[str, Any]:
    root = root.resolve()
    stack = detect_stack(root)
    findings: dict[str, Any] = {
        "root": str(root),
        "stack": stack,
        "critical": [],
        "recommended": [],
        "polish": [],
    }

    package = audit_package(root, findings)
    audit_readme(root, findings, package)
    audit_gitignore(root, stack, findings)
    audit_license(root, findings, package)
    audit_docs(root, findings)
    audit_risky_files(root, findings)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit repository documentation and hygiene.")
    parser.add_argument("root", nargs="?", default=os.environ.get("REPO_ROOT", "."))
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.exists() or not root.is_dir():
        print(f"error: repository root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    print(json.dumps(audit(root), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
