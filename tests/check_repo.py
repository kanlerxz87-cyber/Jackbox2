#!/usr/bin/env python3
"""Repo-wide integration check: conflict markers, all HTML links, root table provenance, PII, and root calculator isolation."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

# 1. Conflict markers across tracked text files
# Byte-built so this file does not itself contain the sequence it looks for.
_M = "<" * 7 + " "
_E = "=" * 7
_G = ">" * 7 + " "
CONFLICT_RE = re.compile(r"^(?:" + re.escape(_M) + r"|" + re.escape(_E) + r"\s*$|" + re.escape(_G) + r")", re.MULTILINE)
for p in sorted(ROOT.rglob("*")):
    if ".git" in p.parts or not p.is_file():
        continue
    if p.suffix.lower() not in {".html", ".md", ".json", ".js", ".css", ".py", ".mjs", ".yml", ".yaml", ".txt"}:
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    if CONFLICT_RE.search(text):
        errors.append(f"conflict marker found in {p.relative_to(ROOT)}")

# 2. All HTML local links + no insecure http:// links across the entire repo
LINK_RE = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)
html_files = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
for html in html_files:
    text = html.read_text(encoding="utf-8", errors="ignore")
    for m in LINK_RE.finditer(text):
        url = m.group(1)
        if url.startswith(("https://", "#", "mailto:", "javascript:")):
            continue
        if url.startswith("http://"):
            errors.append(f"insecure http:// link in {html.relative_to(ROOT)}: {url}")
            continue
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (html.parent / unquote(parsed.path)).resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.exists():
            errors.append(f"broken local link in {html.relative_to(ROOT)}: {url}")

# 3. Every table row in root *.html must have an https:// official source link
class RootTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.row = None
        self.unsourced = 0
        self.nodata = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table" and a.get("data-nodata") == "1":
            self.nodata += 1
        if tag == "tr" and not self.nodata:
            self.row = {"td": False, "https": False}
        if tag == "td" and self.row is not None:
            self.row["td"] = True
        if tag == "a" and self.row is not None:
            if a.get("href", "").startswith("https://"):
                self.row["https"] = True

    def handle_endtag(self, tag):
        if tag == "table" and self.nodata:
            self.nodata -= 1
        if tag == "tr" and self.row is not None:
            if self.row["td"] and not self.row["https"]:
                self.unsourced += 1
            self.row = None

root_pages = sorted(ROOT.glob("*.html"))
for page in root_pages:
    p = RootTableParser()
    p.feed(page.read_text(encoding="utf-8"))
    if p.unsourced:
        errors.append(f"root {page.name}: {p.unsourced} table row(s) without an https:// official source link")

# 4. PII pattern scan across repository
PII_PATTERNS = [
    ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("US phone", re.compile(r"\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b")),
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b")),
    ("APN", re.compile(r"\b\d{4}-\d{3}-\d{3}\b")),
    ("street address", re.compile(r"\b\d{1,5}\s+(?:[NSEW]\.?\s+)?[A-Z][a-z]+\s+(?:St|Ave|Blvd|Rd|Dr|Ln|Way|Ct|Pl|Pkwy)\b")),
]
for p in sorted(ROOT.rglob("*")):
    if ".git" in p.parts or not p.is_file():
        continue
    if p.suffix.lower() not in {".html", ".json", ".js", ".md"}:
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    for label, rx in PII_PATTERNS:
        for m in rx.finditer(text):
            ctx = text[max(0, m.start() - 80):m.start() + 40]
            if "http" in ctx and "/" in ctx:
                continue
            errors.append(f"PII pattern ({label}) in {p.relative_to(ROOT)}: {m.group(0)!r}")

# 5. Root calculator must remain offline / storage-free
app_js = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
for forbidden in ["fetch(", "XMLHttpRequest", "localStorage", "sessionStorage", "document.cookie", "navigator.sendBeacon"]:
    if forbidden in app_js:
        errors.append(f"assets/app.js contains forbidden API: {forbidden}")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print(f"Root + repo-wide integration check PASS: {len(root_pages)} root pages, {len(html_files)} total HTML files, 0 conflict markers, 0 broken links, 0 PII hits.")
