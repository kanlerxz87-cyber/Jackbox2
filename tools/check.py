#!/usr/bin/env python3
"""
Integrity checks for the site. Fails non-zero on any violation.

Two families of check:
  A. Link integrity      — every internal href resolves to a file; every external href is https
                           and points at a host on the approved official-source allowlist.
  B. Privacy / safety    — no identifier patterns in the built site or the data layer, and the
                           calculator must contain no network or storage capability.

Run:  python3 tools/check.py
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DATA = ROOT / "data"

fails, warns = [], []

# ------------------------------------------------------------------ A. links
PAGES = {p.name for p in SITE.glob("*.html")}
ASSETS = {p.name for p in (SITE / "assets").glob("*")} if (SITE / "assets").is_dir() else set()

# Official-source hosts that may be cited. Anything else is either a mistake or a
# breach of the "official sources only" rule.
ALLOWED_HOSTS = {
    "www.sec.gov", "sec.gov",
    "www.bls.gov", "data.bls.gov",
    "www.census.gov", "api.census.gov",
    "www.irs.gov",
    "www.ftb.ca.gov",
    "www.dir.ca.gov",
    "dof.ca.gov",
    "fred.stlouisfed.org",
    "www.fema.gov", "msc.fema.gov",
    "www.usgs.gov", "earthquake.usgs.gov",
    "osfm.fire.ca.gov", "www.fire.ca.gov",
    "www.conservation.ca.gov", "maps.conservation.ca.gov",
    "www.boe.ca.gov",
    "calfire.box.com", "calfire.app.box.com",
    "experience.arcgis.com", "oehha.ca.gov",
    "www.treasury.gov", "www.federalreserve.gov", "www.freddiemac.com",
}

HREF = re.compile(r'href="([^"]+)"')

for page in sorted(SITE.glob("*.html")):
    text = page.read_text(encoding="utf-8")
    for href in HREF.findall(text):
        if href.startswith("#") or href.startswith("mailto:"):
            continue
        if href.startswith("http://"):
            fails.append(f"{page.name}: insecure http link -> {href}")
            continue
        if href.startswith("https://"):
            host = re.sub(r"^https://", "", href).split("/")[0].lower()
            if host not in ALLOWED_HOSTS:
                fails.append(f"{page.name}: non-allowlisted external host {host} -> {href}")
            continue
        # relative
        target = href.split("#")[0].split("?")[0]
        if not target:
            continue
        if target.startswith("assets/"):
            if target.split("/")[-1] not in ASSETS:
                fails.append(f"{page.name}: missing asset {target}")
        elif target.endswith(".html"):
            if target not in PAGES:
                fails.append(f"{page.name}: broken internal link -> {target}")
        else:
            if not (SITE / target).exists():
                fails.append(f"{page.name}: broken relative link -> {target}")

# every nav target must exist
nav_targets = set()
for page in SITE.glob("*.html"):
    nav_targets |= {h for h in HREF.findall(page.read_text(encoding="utf-8")) if h.endswith(".html") and "/" not in h}
for t in sorted(nav_targets):
    if t not in PAGES:
        fails.append(f"nav/link target missing page: {t}")

# ------------------------------------------------------------------ B. privacy
PATTERNS = [
    ("ZIP code", re.compile(r"\b\d{5}-\d{4}\b|\b9\d{4}\b(?!\d)")),
    ("street address", re.compile(r"\b\d{1,5}\s+(?:[NSEW]\.?\s+)?[A-Z][a-z]+\s+(?:St|Ave|Blvd|Rd|Dr|Ln|Way|Ct|Pl|Pkwy)\b")),
    ("parcel number", re.compile(r"\b\d{3,4}-\d{3}-\d{3}\b")),
    ("email address", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b")),
    ("US phone number", re.compile(r"\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b")),
    ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
]

SCAN_DIRS = [SITE, DATA]
ALLOW_EMAIL_DOMAINS = {"example.com", "example.org"}

for d in SCAN_DIRS:
    for f in d.rglob("*"):
        if not f.is_file() or f.suffix not in {".html", ".json", ".css", ".md", ".js", ".txt"}:
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        for name, rx in PATTERNS:
            for m in rx.finditer(text):
                hit = m.group(0)
                if name == "email address" and hit.split("@")[-1] in ALLOW_EMAIL_DOMAINS:
                    continue
                # government URLs are not identifiers; skip matches inside a URL
                start = max(0, m.start() - 60)
                ctx = text[start:m.start()]
                if "http" in ctx and "/" in ctx:
                    continue
                fails.append(f"{f.relative_to(ROOT)}: {name} pattern -> {hit!r}")

# calculator must be inert
calc = SITE / "calculator.html"
if calc.exists():
    c = calc.read_text(encoding="utf-8")
    # Only the executable script blocks matter; the surrounding prose legitimately names
    # these APIs when explaining that they are absent.
    script_blobs = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", c, re.S))
    for forbidden in ["fetch(", "XMLHttpRequest", "localStorage", "sessionStorage",
                      "document.cookie", "navigator.sendBeacon", "new Image(", "import("]:
        if forbidden in script_blobs:
            fails.append(f"calculator.html: forbidden capability in script -> {forbidden}")
    if re.search(r'<form[^>]*action="[^"]+"', c):
        fails.append("calculator.html: form posts somewhere")
    for m in re.finditer(r'<script[^>]*src="([^"]+)"', c):
        fails.append(f"calculator.html: external script -> {m.group(1)}")
else:
    fails.append("calculator.html is missing")

# JSON integrity + no unknown source ids
sources = {s["id"] for s in json.loads((DATA / "sources.json").read_text())["sources"]}
for jf in sorted(DATA.glob("*.json")):
    raw = jf.read_text(encoding="utf-8")
    try:
        json.loads(raw)
    except Exception as exc:
        fails.append(f"{jf.name}: invalid JSON -> {exc}")
        continue
    for m in re.finditer(r'"source"\s*:\s*"([^"]*)"', raw):
        for sid in [p.strip() for p in re.split(r"[/,]", m.group(1)) if p.strip()]:
            if sid not in sources:
                fails.append(f"{jf.name}: cites unknown source id {sid}")

# every page must carry the privacy statement
for page in SITE.glob("*.html"):
    t = page.read_text(encoding="utf-8")
    if "privacy.html" not in t:
        warns.append(f"{page.name}: no link to the privacy policy")

# no empty nav reference
for page in SITE.glob("*.html"):
    if "<nav" not in page.read_text(encoding="utf-8"):
        warns.append(f"{page.name}: no navigation")

# ------------------------------------------------------------------ report
print(f"pages checked: {len(PAGES)}  assets: {len(ASSETS)}  source ids: {len(sources)}")
if warns:
    print(f"\n{len(warns)} warning(s):")
    for w in warns:
        print("  ~ " + w)
if fails:
    print(f"\nFAIL — {len(fails)} violation(s):")
    for f in fails:
        print("  ! " + f)
    sys.exit(1)
print("\nOK — links resolve, hosts allowlisted, no identifier patterns, calculator inert.")
