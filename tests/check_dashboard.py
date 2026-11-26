#!/usr/bin/env python3
"""
Integrity checks for the consolidated root dashboard.

Fails non-zero on any violation. Four families:

  A. Provenance   — every verified ledger row has a value and a known source id;
                    every blank row points at a flagged item that exists; every
                    source URL is https and on the official allowlist.
  B. Links        — every internal href resolves to a file, and every fragment to
                    a real id on that page. External links must be allowlisted.
  C. Privacy      — no street address, parcel number, postal code, phone, email or
                    SSN pattern anywhere in the published pages or the data file,
                    and no identifier field smuggled into the data layer.
  D. Calculator   — the calculator script must stay inert: no network, no storage,
                    no cookies, no external script, no form action.

Run:  python3 tests/check_root.py
"""
import json
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "root.json"

ALLOWED_HOSTS = {
    "www.sec.gov", "sec.gov", "www.investor.gov",
    "investors.jackinthebox.com",  # issuer-primary earnings and calendar
    "www.nist.gov", "www.cde.ca.gov", "planning.lacity.gov", "wagesla.lacity.gov", "www.occ.gov",
    "www.bls.gov", "data.bls.gov",
    "www.census.gov", "api.census.gov",
    "www.irs.gov",
    "www.ftb.ca.gov",
    "www.dir.ca.gov",
    "dof.ca.gov",
    "dot.ca.gov",
    "fred.stlouisfed.org",
    "www.fema.gov", "msc.fema.gov",
    "www.usgs.gov", "earthquake.usgs.gov",
    "osfm.fire.ca.gov", "www.fire.ca.gov",
    "www.conservation.ca.gov", "maps.conservation.ca.gov",
    "www.boe.ca.gov",
    "www.insurance.ca.gov",
    "home.treasury.gov", "www.treasury.gov",
    "www.federalreserve.gov",
    "lacity.gov", "finance.lacity.gov",
    "rrcc.lacounty.gov", "assessor.lacounty.gov",
    "dq.cde.ca.gov",
}

HTML_FILES = sorted(p.name for p in ROOT.glob("*.html"))
fails = []
warns = []

# ---------------------------------------------------------------- data layer
D = json.loads(DATA.read_text(encoding="utf-8"))
sources = {s["id"]: s for s in D["sources"]}
flag_ids = {f["id"] for f in D["flagged"]}

for s in D["sources"]:
    u = urlsplit(s["url"])
    if u.scheme != "https":
        fails.append(f"source {s['id']}: not https -> {s['url']}")
    if (u.hostname or "").lower() not in ALLOWED_HOSTS:
        fails.append(f"source {s['id']}: host not allowlisted -> {u.hostname}")

for f in D["findings"]:
    if f["sourceId"] not in sources:
        fails.append(f"finding {f['id']}: unknown source id {f['source']}")
    if f["status"] == "verified" and not f["value"].strip():
        fails.append(f"finding {f['id']}: marked verified with an empty value")
    if f["status"] != "verified":
        if f["value"].strip():
            fails.append(f"finding {f['id']}: unverified row carries a value -> {f['value']!r}")
        m = re.search(r"F-\d{2}", f["note"])
        if not m:
            fails.append(f"finding {f['id']}: blank row does not point at a flag")
        elif m.group(0) not in flag_ids:
            fails.append(f"finding {f['id']}: points at missing flag {m.group(0)}")

if not any(f["status"] == "verified" for f in D["findings"]):
    fails.append("no verified findings at all")

# no identifier-ish keys in the data layer
BANNED_KEYS = {"address", "street", "apn", "parcel_number", "parcel_id", "owner_name",
               "tenant_entity", "zip", "phone", "email", "ssn"}


def walk(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            if k.lower() in BANNED_KEYS:
                fails.append(f"data layer: banned identifier key {path}.{k}")
            walk(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]")


walk(D)

# ------------------------------------------------------------------- parsing
class Page(HTMLParser):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.refs = []
        self.ids = set()
        self.in_table = 0
        self.row = None
        self.rows = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag in ("a", "link", "script"):
            url = a.get("href") or a.get("src")
            if url:
                self.refs.append(url)
        if tag == "table":
            self.in_table += 1
        if tag == "tr" and self.in_table:
            self.row = {"cells": 0, "external": False, "verified_pill": False}
        if tag in ("td", "th") and self.row is not None:
            self.row["cells"] += 1
        if tag == "a" and self.row is not None:
            url = a.get("href") or ""
            if url.startswith("https://"):
                self.row["external"] = True

    def handle_endtag(self, tag):
        if tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        if tag == "table" and self.in_table:
            self.in_table -= 1


pages = {}
for name in HTML_FILES:
    p = Page(name)
    p.feed((ROOT / name).read_text(encoding="utf-8"))
    pages[name] = p

# --------------------------------------------------------------------- links
for name, p in pages.items():
    for url in p.refs:
        u = urlsplit(url)
        if u.scheme in ("http", "mailto", "tel"):
            fails.append(f"{name}: insecure or non-https link -> {url}")
            continue
        if u.scheme == "https":
            host = (u.hostname or "").lower()
            if host not in ALLOWED_HOSTS:
                fails.append(f"{name}: external host not allowlisted -> {host}")
            continue
        target = u.path
        if not target:
            if u.fragment and unquote(u.fragment) not in p.ids:
                fails.append(f"{name}: broken fragment #{u.fragment}")
            continue
        if target.startswith("assets/"):
            if not (ROOT / target).is_file():
                fails.append(f"{name}: missing asset -> {target}")
            continue
        f = (ROOT / unquote(target))
        if not f.exists():
            fails.append(f"{name}: broken internal link -> {target}")
            continue
        if u.fragment and target in pages:
            if unquote(u.fragment) not in pages[target].ids:
                fails.append(f"{name}: broken anchor -> {target}#{u.fragment}")

# ---------------------------------------------------------------- provenance
for name in pages:
    text = (ROOT / name).read_text(encoding="utf-8")
    for block in re.findall(r"<tr>(.*?)</tr>", text, re.S):
        if ">Verified<" in block and "https://" not in block:
            snippet = re.sub(r"<[^>]+>", " ", block)
            snippet = re.sub(r"\s+", " ", snippet).strip()[:90]
            fails.append(f"{name}: row shows a Verified badge but carries no source link -> {snippet}")

# every page must link the privacy policy and carry the no-winner rule
for name, p in pages.items():
    text = (ROOT / name).read_text(encoding="utf-8")
    if "privacy.html" not in text:
        fails.append(f"{name}: does not link the privacy policy")
    if "No winner selected" not in text:
        fails.append(f"{name}: missing the 'No winner selected' disclosure")

# ------------------------------------------------------------------- privacy
PATTERNS = [
    ("postal code", re.compile(r"\b9\d{4}(?:-\d{4})?\b")),
    ("street address", re.compile(r"\b\d{1,5}\s+(?:[NSEW]\.?\s+)?[A-Z][a-z]+\s+(?:St|Ave|Blvd|Rd|Dr|Ln|Way|Ct|Pl|Pkwy)\b")),
    ("parcel number", re.compile(r"\b\d{3,4}-\d{3}-\d{3}\b")),
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b")),
    ("phone", re.compile(r"\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b")),
    ("ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("conflict marker", re.compile(r"^(?:<{7}|={7}|>{7})(?: .*)?$", re.M)),
]

SCAN = [ROOT / n for n in HTML_FILES] + [DATA, ROOT / "README.md", ROOT / "assets" / "calc.js"]
for f in SCAN:
    if not f.is_file():
        continue
    text = f.read_text(encoding="utf-8", errors="ignore")
    for label, rx in PATTERNS:
        for m in rx.finditer(text):
            hit = m.group(0)
            start = max(0, m.start() - 70)
            ctx = text[start:m.start()]
            if "/" in ctx and ("http" in ctx or "www." in ctx):
                continue  # inside a URL, not an identifier
            fails.append(f"{f.name}: {label} pattern -> {hit!r}")

# ---------------------------------------------------------------- calculator
calc = ROOT / "calculator.html"
if not calc.is_file():
    fails.append("calculator.html is missing")
else:
    text = calc.read_text(encoding="utf-8")
    script_blobs = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", text, re.S))
    js_file = (ROOT / "assets" / "calc.js").read_text(encoding="utf-8")
    for label, blob in (("inline script", script_blobs), ("calc.js", js_file)):
        for bad in ["fetch(", "XMLHttpRequest", "localStorage", "sessionStorage",
                    "document.cookie", "sendBeacon", "new Image(", "import(", "WebSocket",
                    "IndexedDB", "serviceWorker"]:
            if bad in blob:
                fails.append(f"calculator {label}: forbidden capability -> {bad}")
    for m in re.finditer(r'<script[^>]*src="([^"]+)"', text):
        if m.group(1) != "assets/calc.js":
            fails.append(f"calculator.html: unexpected external script -> {m.group(1)}")
    if re.search(r'<form[^>]*action="[^"]+"', text):
        fails.append("calculator.html: form posts somewhere")
    if not (ROOT / "assets" / "calc.js").is_file():
        fails.append("assets/calc.js is missing")

# --------------------------------------------------------------- dead assets
for asset in sorted((ROOT / "assets").glob("*")):
    if asset.name in {"style.css", "calc.js", "app.js"}:  # app.js is the tested source for generated calc.js
        continue
    if not any(asset.name in (ROOT / n).read_text(encoding="utf-8") for n in HTML_FILES):
        warns.append(f"assets/{asset.name}: not referenced by any page")

# -------------------------------------------------------------------- report
verified = sum(1 for f in D["findings"] if f["status"] == "verified")
print(f"pages: {len(pages)}  ledger rows: {len(D['findings'])} ({verified} verified)  "
      f"sources: {len(sources)}  flags: {len(flag_ids)}")
if warns:
    print(f"\n{len(warns)} warning(s):")
    for w in warns:
        print("  ~ " + w)
if fails:
    print(f"\nFAIL — {len(fails)} violation(s):")
    for f in fails:
        print("  ! " + f)
    sys.exit(1)
print("\nOK — provenance, links, privacy patterns and calculator inertness all pass.")
