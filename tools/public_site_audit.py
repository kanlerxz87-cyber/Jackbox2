#!/usr/bin/env python3
"""Offline integrity audit for the public GitHub Pages tree.

This tool deliberately separates three things that are often conflated:

* local publication integrity (links, anchors, insecure assets, conflict markers);
* provenance signals (whether a static table row includes an official-source URL);
* substantive verification (which still requires opening the official record and,
  for private property facts, a secure adviser workflow).

It makes no network request and never treats a linked URL as proof of an underlying
fact. The designated current public decision surface is ``central-la-2026/``. Older
self-contained dashboards remain published for traceability and are reported as
archival limitations rather than silently promoted as current evidence.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

# Official issuers and government/official-program hosts that appear in the public
# dashboards. This is an offline provenance allowlist, not an availability check.
OFFICIAL_HOST_SUFFIXES = (
    "sec.gov", "census.gov", "bls.gov", "irs.gov", "ftb.ca.gov", "dir.ca.gov",
    "dof.ca.gov", "fema.gov", "usgs.gov", "fire.ca.gov", "osfm.fire.ca.gov",
    "conservation.ca.gov", "boe.ca.gov", "treasury.gov", "federalreserve.gov",
    "freddiemac.com", "fred.stlouisfed.org", "metro.net", "planning.lacity.gov",
    "lacity.gov", "lacounty.gov", "scag.ca.gov", "dot.ca.gov", "edd.ca.gov",
    "cde.ca.gov", "lausd.org", "leginfo.legislature.ca.gov", "oehha.ca.gov",
    "insurance.ca.gov", "epa.gov", "consumerfinance.gov", "cisa.gov",
    "investors.jackinthebox.com",
)

PUBLIC_DIRS = (
    "assets", "site", "data", "docs", "privacy-first", "alternative-research",
    "central-la-2026", "audit",
)
TEXT_SUFFIXES = {".html", ".css", ".js", ".mjs", ".json", ".md"}

# This is a deliberately conservative safety net. It is not represented as a full
# DLP solution and does not replace human review of any new public copy.
PRIVATE_PATTERNS = (
    ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("email address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("US phone number", re.compile(r"\b(?:\+1[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]\d{4}\b")),
    ("parcel number", re.compile(r"\b\d{3,4}-\d{3}-\d{3}\b")),
    ("street address", re.compile(
        r"\b\d{1,6}\s+(?:[NSEW]\.?\s+)?[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+){0,4}\s+"
        r"(?:Street|St\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Road|Rd\.?|Drive|Dr\.?|Lane|Ln\.?|Way|Place|Pl\.?)\b"
    )),
    # A bare five-digit number is not reliable: official financial datasets can
    # legitimately contain values such as 97,387. Match only an explicitly labelled
    # postal field; street-address matching above remains a separate safeguard.
    ("California ZIP code", re.compile(r"\b(?:zip|postal(?:\s+code)?)\s*[:#-]?\s*(?:9\d{4}(?:-\d{4})?)\b", re.I)),
)


@dataclass
class Ref:
    tag: str
    attr: str
    url: str
    line: int


@dataclass
class TableRow:
    line: int
    hrefs: list[str] = field(default_factory=list)


class PageParser(HTMLParser):
    """Collect references, IDs, and static ``tbody`` row citations."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[Ref] = []
        self.ids: set[str] = set()
        self.tbody_depth = 0
        self.current_row: TableRow | None = None
        self.rows: list[TableRow] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        for attr in ("href", "src"):
            if values.get(attr):
                self.refs.append(Ref(tag, attr, values[attr] or "", self.getpos()[0]))
                if self.current_row is not None and attr == "href":
                    self.current_row.hrefs.append(values[attr] or "")
        if tag == "tbody":
            self.tbody_depth += 1
        elif tag == "tr" and self.tbody_depth:
            self.current_row = TableRow(self.getpos()[0])

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # HTMLParser does not call handle_starttag for self-closing tags.
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr" and self.current_row is not None:
            self.rows.append(self.current_row)
            self.current_row = None
        elif tag == "tbody":
            self.tbody_depth = max(0, self.tbody_depth - 1)


def is_official_url(url: str) -> bool:
    parsed = urlsplit(url)
    if parsed.scheme != "https":
        return False
    host = (parsed.hostname or "").lower().removeprefix("www.")
    return any(host == suffix or host.endswith("." + suffix) for suffix in OFFICIAL_HOST_SUFFIXES)


def dashboard_key(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if len(rel.parts) == 1:
        return "root-current" if rel.name == "index.html" else "root-legacy"
    first = rel.parts[0]
    if first == "audit":
        return "audit-metadata"
    return first


def iter_public_text_files() -> list[Path]:
    files: set[Path] = set()
    for path in ROOT.glob("*.html"):
        files.add(path)
    for name in ("README.md", "COORDINATION.md"):
        candidate = ROOT / name
        if candidate.exists():
            files.add(candidate)
    for dirname in PUBLIC_DIRS:
        base = ROOT / dirname
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                files.add(path)
    return sorted(files)


def local_target(page: Path, url: str) -> tuple[Path | None, str]:
    """Return the resolved workspace file and decoded fragment for a relative URL."""
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or url.startswith("//"):
        return None, ""
    if url.startswith("#"):
        return page, unquote(parsed.fragment)
    if url.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None, unquote(parsed.fragment)
    raw_path = unquote(parsed.path)
    if not raw_path:
        return page, unquote(parsed.fragment)
    # The site is intentionally relative-path only. A leading slash would escape the
    # project base path when Pages serves it under /Jackbox2/.
    if raw_path.startswith("/"):
        return ROOT / "__invalid_absolute_path__", unquote(parsed.fragment)
    return (page.parent / raw_path).resolve(), unquote(parsed.fragment)


def is_under_root(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT.resolve())
        return True
    except ValueError:
        return False


def scan_privacy(path: Path, text: str, errors: list[str]) -> None:
    # Official URL query strings may include digits that resemble a ZIP. Links are
    # separately audited; strip them before looking for content-level identifiers.
    content = re.sub(r"https?://[^\s\"'<>()]+", "[URL]", text)
    for label, pattern in PRIVATE_PATTERNS:
        for match in pattern.finditer(content):
            errors.append(f"[PRIVACY] {path.relative_to(ROOT)}: {label} pattern {match.group(0)!r}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    parsed_pages: dict[Path, PageParser] = {}
    source_rows: Counter[str] = Counter()
    official_rows: Counter[str] = Counter()
    nonofficial_rows: dict[str, list[tuple[Path, int]]] = defaultdict(list)

    all_text = iter_public_text_files()
    for path in all_text:
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"^(?:<<<<<<<|=======|>>>>>>>)", text, re.MULTILINE):
            errors.append(f"[CONFLICT] {path.relative_to(ROOT)} contains a Git conflict marker")
        scan_privacy(path, text, errors)
        if path.suffix.lower() != ".html":
            continue
        parser = PageParser()
        try:
            parser.feed(text)
            parser.close()
        except Exception as exc:  # defensive: malformed HTML must be visible
            errors.append(f"[HTML] {path.relative_to(ROOT)} could not be parsed: {exc}")
            continue
        parsed_pages[path.resolve()] = parser
        key = dashboard_key(path)
        source_rows[key] += len(parser.rows)
        for row in parser.rows:
            if any(is_official_url(url) for url in row.hrefs):
                official_rows[key] += 1
            else:
                nonofficial_rows[key].append((path, row.line))

        # Browser-facing code must not load an external script or stylesheet. Source
        # links are allowed only as explicit reader-clicked anchors.
        for ref in parser.refs:
            url = ref.url.strip()
            if not url:
                continue
            lower = url.lower()
            if "localhost" in lower or "127.0.0.1" in lower:
                errors.append(f"[LOCALHOST] {path.relative_to(ROOT)}:{ref.line} -> {url}")
            if lower.startswith("http://"):
                errors.append(f"[HTTP] {path.relative_to(ROOT)}:{ref.line} -> {url}")
            if ref.tag == "script" and ref.attr == "src" and lower.startswith(("http://", "https://", "//")):
                errors.append(f"[EXTERNAL SCRIPT] {path.relative_to(ROOT)}:{ref.line} -> {url}")
            if ref.tag == "link" and ref.attr == "href" and lower.startswith(("http://", "https://", "//")):
                errors.append(f"[EXTERNAL STYLESHEET] {path.relative_to(ROOT)}:{ref.line} -> {url}")

            target, fragment = local_target(path, url)
            if target is None:
                continue
            if not is_under_root(target):
                errors.append(f"[ESCAPING LINK] {path.relative_to(ROOT)}:{ref.line} -> {url}")
                continue
            if not target.exists():
                errors.append(f"[BROKEN LINK] {path.relative_to(ROOT)}:{ref.line} -> {url}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsed_pages.get(target.resolve())
                # Target might not have been parsed yet; parse on demand.
                if target_parser is None:
                    candidate = PageParser()
                    candidate.feed(target.read_text(encoding="utf-8", errors="replace"))
                    candidate.close()
                    parsed_pages[target.resolve()] = candidate
                    target_parser = candidate
                if fragment not in target_parser.ids:
                    errors.append(f"[BROKEN ANCHOR] {path.relative_to(ROOT)}:{ref.line} -> {url}")

    # The current root portal must not promote the archived analytical copy or pick a
    # decision winner. The current Central LA dashboard is separately runtime-tested
    # by CI because most of its rows are client-side rendered.
    root_index = ROOT / "index.html"
    root_text = root_index.read_text(encoding="utf-8")
    if 'href="site/index.html"' in root_text:
        errors.append("[CURRENT ROUTE] root index promotes archived site/index.html")
    if re.search(r"\b(?:recommend(?:ed|ation)?|favor(?:s|ed)?)\s+(?:selling|sell|renew(?:al)?)\b", root_text, re.I):
        errors.append("[CURRENT ROUTE] root index appears to select a sale/renewal outcome")
    if "central-la-2026/index.html" not in root_text or "central-la-2026/flagged-review.html" not in root_text:
        errors.append("[CURRENT ROUTE] root index does not expose the current dashboard and flags")

    # Only the designated current surface and the independent alternative are held
    # to full static-row coverage here. Historical root/docs/privacy artifacts are
    # retained for traceability and explicitly reported below when they contain
    # workflow rows rather than direct evidence rows.
    required_current = ("root-current", "central-la-2026", "alternative-research")
    for key in required_current:
        missing = nonofficial_rows.get(key, [])
        if missing:
            examples = ", ".join(f"{p.relative_to(ROOT)}:{line}" for p, line in missing[:5])
            errors.append(f"[TABLE PROVENANCE] {key} has {len(missing)} static tbody row(s) without an official URL: {examples}")

    for page in (ROOT / "site").glob("*.html"):
        text = page.read_text(encoding="utf-8")
        if "ARCHIVED ANALYTICAL WORKSPACE" not in text:
            errors.append(f"[ARCHIVE MARKER] {page.relative_to(ROOT)} lacks the archival no-decision notice")

    # These are transparent limitations, not a disguised pass/fail condition. The
    # affected artifacts are marked archival and are not promoted by the root portal.
    for key in ("root-legacy", "site", "docs", "privacy-first"):
        if nonofficial_rows.get(key):
            warnings.append(
                f"{key}: {len(nonofficial_rows[key])} of {source_rows[key]} static table row(s) lack a direct official URL; "
                "retained as archival/process material and documented on audit/index.html."
            )

    print("PUBLIC SITE AUDIT — offline local checks only")
    print(f"HTML pages parsed: {len(parsed_pages)}")
    print("Static table-row provenance (direct official URL / total):")
    for key in sorted(source_rows):
        print(f"  - {key}: {official_rows[key]}/{source_rows[key]}")
    if warnings:
        print("Known archival limitations:")
        for item in warnings:
            print("  ~ " + item)
    if errors:
        print(f"PUBLIC SITE AUDIT: FAIL ({len(errors)} error(s))", file=sys.stderr)
        for item in errors:
            print("  ! " + item, file=sys.stderr)
        return 1
    print("PUBLIC SITE AUDIT: PASS (with the archival limitations shown above)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
