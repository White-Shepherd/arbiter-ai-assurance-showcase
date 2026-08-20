#!/usr/bin/env python3
"""Validate local links, HTML structure, and public-content boundaries."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = [*ROOT.glob("*.md"), *ROOT.glob("docs/**/*.md"), *ROOT.glob("site/**/*")]
TEXT_SUFFIXES = {".css", ".html", ".md", ".txt", ".vtt"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
MARKDOWN_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
EXPOSURE_PATTERNS = {
    "Windows user path": re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
    "Unix user path": re.compile(r"/Users/[^/\s]+/"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "private key": re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
}


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.references.append(values[attribute])


def local_target(source: Path, reference: str) -> tuple[Path | None, str]:
    parsed = urlsplit(reference.strip().strip("<>"))
    if parsed.scheme or parsed.netloc or reference.startswith(("mailto:", "data:")):
        return None, ""
    path = unquote(parsed.path)
    target = source if not path else (source.parent / path).resolve()
    return target, unquote(parsed.fragment)


def markdown_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    counts: dict[str, int] = {}
    for heading in MARKDOWN_HEADING.findall(path.read_text(encoding="utf-8")):
        slug = heading.lower().strip()
        slug = re.sub(r"[`*_{}\[\]()<>#+.!,:;?'\"]", "", slug)
        slug = re.sub(r"\s+", "-", slug)
        suffix = counts.get(slug, 0)
        counts[slug] = suffix + 1
        ids.add(slug if suffix == 0 else f"{slug}-{suffix}")
    return ids


def validate_reference(source: Path, reference: str, ids: set[str], errors: list[str]) -> None:
    target, fragment = local_target(source, reference)
    if target is None:
        return
    if not target.is_relative_to(ROOT):
        errors.append(f"{source.relative_to(ROOT)}: local target escapes repository {reference!r}")
        return
    if not target.exists():
        errors.append(f"{source.relative_to(ROOT)}: missing local target {reference!r}")
        return
    if source.suffix == ".html" and fragment and target == source and fragment not in ids:
        errors.append(f"{source.relative_to(ROOT)}: missing HTML fragment #{fragment}")
    if fragment and target.suffix.lower() == ".md" and fragment not in markdown_ids(target):
        errors.append(f"{source.relative_to(ROOT)}: missing Markdown fragment {reference!r}")


def main() -> int:
    errors: list[str] = []
    checked_links = 0

    for source in sorted(path for path in PUBLIC_FILES if path.is_file()):
        if source.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = source.read_text(encoding="utf-8")

        for label, pattern in EXPOSURE_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{source.relative_to(ROOT)}: possible {label}")

        if source.suffix.lower() == ".md":
            for reference in MARKDOWN_LINK.findall(text):
                checked_links += 1
                validate_reference(source, reference, set(), errors)

        if source.suffix.lower() == ".html":
            parser = DocumentParser()
            parser.feed(text)
            duplicates = sorted({value for value in parser.ids if parser.ids.count(value) > 1})
            for duplicate in duplicates:
                errors.append(f"{source.relative_to(ROOT)}: duplicate id {duplicate!r}")
            ids = set(parser.ids)
            for reference in parser.references:
                checked_links += 1
                validate_reference(source, reference, ids, errors)

    if errors:
        print("Public documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Public documentation validation passed ({checked_links} link references checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
