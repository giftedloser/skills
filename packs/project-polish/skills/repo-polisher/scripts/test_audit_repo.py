#!/usr/bin/env python3
"""Small regression check for audit_repo.py."""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.dont_write_bytecode = True

from audit_repo import audit


def write(root: Path, path: str, content: str | bytes = "") -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        target.write_bytes(content)
    else:
        target.write_text(content, encoding="utf-8")


def main() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        write(root, "README.md", "# Tiny\n\nDoes one job.\n")
        result = audit(root)
        assert result["confirmed_issues"] == [], result
        assert result["repository_surface"] == [], result

        for path in (
            "docs/a&b.md",
            "docs/a_(b).md",
            "docs/guide with space.md",
            "docs/shortcut.md",
            "img/one.png",
            "img/two.png",
            "img/unquoted.png",
        ):
            write(root, path)
        write(
            root,
            "README.md",
            """# Tiny

`[inline example](missing-inline.md)`

```md
[fenced example](missing-fenced.md)
```

<!-- [old link](missing-comment.md) -->
[unused]: missing-unused.md
[Duplicate][duplicate]
[duplicate]: docs/shortcut.md
[duplicate]: missing-duplicate.md
\\[Escaped shortcut]
[Escaped shortcut]: missing-escaped-shortcut.md
[Indented]

    [ignored](missing-indented-inline.md)
    [Indented]: missing-indented-reference.md

[Shortcut]
[Shortcut]: docs/shortcut.md
[Multiline
link](docs/shortcut.md)
[Parentheses](docs/a_(b).md)
[Escaped parentheses](docs/a_\\(b\\).md)
[Markdown entity](docs/a&amp;b.md)
[Spaces](<docs/guide with space.md>)
[Root-relative site URL](/docs)
<a href="docs/guide with space.md">Guide</a>
<a href="docs/a&amp;b.md">Entity</a>
<img src=img/unquoted.png>
<source srcset="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP, img/two.png 2x">
Plain prose ](missing-prose.md)
""",
        )
        result = audit(root)
        assert result["confirmed_issues"] == [], result
        assert result["readme"]["local_references"] == [
            "docs/a&b.md",
            "docs/a_(b).md",
            "docs/guide with space.md",
            "docs/shortcut.md",
            "img/two.png",
            "img/unquoted.png",
        ], result

        (root / "img/two.png").unlink()
        with (root / "README.md").open("a", encoding="utf-8") as readme:
            readme.write('<a href="docs/missing.html">Missing</a>\n')
        result = audit(root)
        assert result["confirmed_issues"] == [
            {"kind": "broken_local_reference", "path": "README.md", "detail": "docs/missing.html"},
            {"kind": "broken_local_reference", "path": "README.md", "detail": "img/two.png"},
        ], result

        write(root, "package.json", b"\xff")
        write(root, "pyproject.toml", b"\xff")
        result = audit(root)
        unreadable = {
            issue["path"] for issue in result["confirmed_issues"] if issue["kind"] == "unreadable_manifest"
        }
        assert unreadable == {"package.json", "pyproject.toml"}, result

    with TemporaryDirectory() as directory:
        root = Path(directory)
        write(root, "README.md", '# Broken URL\n\n<a href="http://[">Broken</a>\n')
        result = audit(root)
        assert len(result["confirmed_issues"]) == 1, result
        assert result["confirmed_issues"][0]["kind"] == "malformed_reference", result

        write(root, "package.json", "[]")
        write(root, "composer.json", "{")
        write(root, "Cargo.toml", "[")
        result = audit(root)
        manifest_issues = {
            (issue["kind"], issue["path"])
            for issue in result["confirmed_issues"]
            if issue["path"] in {"package.json", "composer.json", "Cargo.toml"}
        }
        assert manifest_issues == {
            ("invalid_manifest", "package.json"),
            ("unreadable_manifest", "composer.json"),
            ("unreadable_manifest", "Cargo.toml"),
        }, result

    with TemporaryDirectory() as directory:
        root = Path(directory)
        write(root, "docs/existing.md")
        write(
            root,
            "README.md",
            "# Duplicate\n\n[Guide][duplicate]\n\n[duplicate]: docs/missing-first.md\n[duplicate]: docs/existing.md\n",
        )
        result = audit(root)
        assert result["confirmed_issues"] == [
            {"kind": "broken_local_reference", "path": "README.md", "detail": "docs/missing-first.md"}
        ], result

    with TemporaryDirectory() as directory:
        root = Path(directory)
        write(
            root,
            "README.md",
            """# Real heading

```md
<!--
# Fenced heading
```

<pre>[example](missing-pre.md)</pre>
[After fence](docs/missing-after.md)
""",
        )
        result = audit(root)
        assert result["readme"]["headings"] == ["Real heading"], result
        assert result["confirmed_issues"] == [
            {"kind": "broken_local_reference", "path": "README.md", "detail": "docs/missing-after.md"}
        ], result

    with TemporaryDirectory() as directory:
        root = Path(directory)
        write(root, "README.md", "# T\n\n`[Rendered link](missing.md)``\n")
        result = audit(root)
        assert result["readme"]["local_references"] == ["missing.md"], result

        write(root, "README.md", "# Before\n\n``` `\n[Rendered link](missing.md)\n\n# After\n")
        result = audit(root)
        assert result["readme"]["local_references"] == ["missing.md"], result
        assert result["readme"]["headings"] == ["Before", "After"], result

        write(root, "README.md", "   ### Indented ATX\n\nSetext heading\n---\n")
        result = audit(root)
        assert result["readme"]["headings"] == ["Indented ATX", "Setext heading"], result

        write(root, "README.md", "Paragraph before a list:\n\n- first\n- second\n")
        result = audit(root)
        assert result["readme"]["headings"] == [], result

        write(root, "README.md", "- `FIRST`\n- `SECOND`\n")
        result = audit(root)
        assert result["readme"]["headings"] == [], result

    with TemporaryDirectory() as directory:
        root = Path(directory)
        write(root, "docs/guide.md")
        write(root, "img/logo.png")
        write(root, "README.md", "[Guide](docs/guide.md) ![Logo](img/logo.png)\n")
        result = audit(root)
        assert result["readme"]["local_references"] == ["docs/guide.md", "img/logo.png"], result
        assert result["confirmed_issues"] == [], result

        write(root, "README.md", "- Item\n\n    [Guide](docs/missing-list.md)\n")
        result = audit(root)
        assert result["confirmed_issues"] == [
            {"kind": "broken_local_reference", "path": "README.md", "detail": "docs/missing-list.md"}
        ], result

    with TemporaryDirectory() as directory:
        root = Path(directory)
        result = audit(root)
        assert result["readme"] is None and result["confirmed_issues"] == [], result
        write(root, "README.markdown", "# Alternate\n\n[Missing](docs/missing.md)\n")
        result = audit(root)
        assert result["confirmed_issues"] == [
            {"kind": "broken_local_reference", "path": "README.markdown", "detail": "docs/missing.md"}
        ], result

    print("audit_repo regression check passed")


if __name__ == "__main__":
    main()
