#!/usr/bin/env python3
"""Offline integrity/privacy/provenance check for the privacy-first dashboard."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]
errors = []
allowed_hosts = {
    "assessor.lacounty.gov", "data.census.gov", "docs.github.com", "github.com",
    "earthquake.usgs.gov", "labormarketinfo.edd.ca.gov", "ladot.lacity.gov",
    "msc.fema.gov", "osfm.fire.ca.gov", "planning.lacity.gov", "www.bea.gov",
    "www.bls.gov", "www.cde.ca.gov", "www.census.gov", "www.cisa.gov",
    "www.conservation.ca.gov", "www.consumerfinance.gov", "www.envirostor.dtsc.ca.gov",
    "www.federalreserve.gov", "www.fema.gov", "www.ftb.ca.gov", "www.ftc.gov",
    "www.insurance.ca.gov", "www.irs.gov", "www.metro.net", "www.nist.gov",
    "www.sec.gov", "www.usgs.gov", "zimas.lacity.org",
}

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.refs = []
        self.row = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "tr":
            self.row = {"has_cell": False, "official": False}
        if tag == "td" and self.row is not None:
            self.row["has_cell"] = True
        if tag in ("a", "link", "script"):
            url = attrs.get("href") or attrs.get("src")
            if not url:
                return
            if self.row is not None and url.startswith("https://"):
                self.row["official"] = True
            self.refs.append(url)

    def handle_endtag(self, tag):
        if tag == "tr" and self.row is not None:
            if self.row["has_cell"] and not self.row["official"]:
                errors.append(f"{self.path.name}: data row lacks an external official/context source")
            self.row = None

pages = {}
for path in sorted(ROOT.glob("*.html")):
    parser = Page(path)
    text = path.read_text(encoding="utf-8")
    parser.feed(text)
    pages[path.resolve()] = parser
    # Fail on common high-risk identifier patterns. Placeholders are allowed.
    patterns = {
        "SSN-like value": r"\b\d{3}-\d{2}-\d{4}\b",
        "email address": r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "phone number": r"\b(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b",
        "LA County APN-like value": r"\b\d{4}-\d{3}-\d{3}\b",
        "numbered street address": r"\b\d{1,6}\s+[A-Z][A-Za-z0-9 .'-]{1,40}\s(?:Street|St\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Road|Rd\.?)\b",
    }
    for label, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            errors.append(f"{path.name}: possible {label}")

for path, parser in pages.items():
    for url in parser.refs:
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc:
            if parsed.scheme != "https" or parsed.hostname not in allowed_hosts:
                errors.append(f"{path.name}: unapproved external source {url}")
            continue
        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        if not target.is_relative_to(ROOT) or not target.exists():
            errors.append(f"{path.name}: broken local link {url}")
        elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
            errors.append(f"{path.name}: broken local anchor {url}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"{len(pages)} privacy-first pages: local links, table provenance, source hosts, and identifier patterns checked.")
