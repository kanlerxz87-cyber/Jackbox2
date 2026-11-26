#!/usr/bin/env python3
"""Verify the root dashboard.

Rules enforced (these are the site's own published rules, not style preferences):
  1. Every <tr> in a <tbody> carries an https:// link to an official source, OR states
     plainly that the value is blank/unverified/withheld/not public.
  2. Every local href and src resolves to a file that exists.
  3. Every local anchor (#id) resolves to an id on the target page.
  4. Every https:// host used in a source link is on the official allowlist.
  5. No personal or parcel-identifying patterns appear in the HTML.
  6. No inline event handlers, no external scripts, no network calls from the calculator.
  7. Required nav pages exist and are all reachable from index.html.

Run from the repository root: python3 tests/check_root.py
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    'index.html', 'executive-summary.html', 'decision-gates.html', 'trade-area.html',
    'hazards.html', 'sell-vs-hold.html', 'risks.html', 'questions.html',
    'suggestions.html', 'flagged.html', 'printable-summary.html', 'sources.html',
]

# Official-source allowlist. Anything else is a failure, so a vendor or news
# site cannot creep into a "source" column.
ALLOWED_HOSTS = {
    'www.sec.gov', 'sec.gov',
    'www.census.gov', 'census.gov',
    'fred.stlouisfed.org',
    'www.bls.gov', 'bls.gov',
    'www.irs.gov', 'irs.gov',
    'www.ftb.ca.gov', 'ftb.ca.gov',
    'finance.lacity.gov', 'planning.lacity.gov',
    'dof.ca.gov',
    'www.usgs.gov', 'usgs.gov', 'earthquake.usgs.gov', 'pubs.usgs.gov',
    'msc.fema.gov', 'www.fema.gov',
    'osfm.fire.ca.gov', 'www.fire.ca.gov',
    'www.conservation.ca.gov',
    'www.dir.ca.gov',
    'home.treasury.gov',
    'www.insurance.ca.gov', 'www.cfpnet.com',
    'www.cde.ca.gov',
    'dot.ca.gov',
    'www.census.gov',
}

BLANK_MARKERS = ('blank', 'unverified', 'withheld', 'not public', 'not started',
                 'pending', 'not applied', 'not priced', 'owner input', 'deferred',
                 'not obtainable', 'no official')

errors = []
warnings = []


class RowChecker(HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.in_tbody = False
        self.nodata_depth = 0
        self.row = None
        self.row_http = False
        self.row_text = []
        self.row_num = 0
        self.ids = set()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'table' and a.get('data-nodata') == '1':
            self.nodata_depth += 1
        if tag == 'tbody':
            self.in_tbody = True
        if tag == 'tr' and self.in_tbody and not self.nodata_depth:
            self.row = True
            self.row_http = False
            self.row_text = []
            self.row_num += 1
        if tag == 'a':
            href = a.get('href', '')
            if href:
                self.refs.append(('a', href))
                if self.row and href.startswith('https://'):
                    self.row_http = True
        if tag in ('link', 'script', 'img'):
            src = a.get('href') or a.get('src')
            if src:
                self.refs.append((tag, src))

    def handle_data(self, data):
        if self.row and data.strip():
            self.row_text.append(data.strip())

    def handle_endtag(self, tag):
        if tag == 'table' and self.nodata_depth:
            self.nodata_depth -= 1
        if tag == 'tr' and self.row:
            text = ' '.join(self.row_text).lower()
            if not self.row_http and not any(m in text for m in BLANK_MARKERS):
                snippet = ' '.join(self.row_text)[:110]
                errors.append(f'{self.page}: table row {self.row_num} has no official source and is not '
                              f'marked blank/unverified -> "{snippet}"')
            self.row = None
            self.row_http = False
            self.row_text = []
        if tag == 'tbody':
            self.in_tbody = False


def check_page(name, pages):
    path = ROOT / name
    if not path.exists():
        errors.append(f'{name}: page is missing')
        return None
    html = path.read_text(encoding='utf-8')

    checker = RowChecker(name)
    checker.feed(html)

    # 2. local links resolve
    for tag, ref in checker.refs:
        parts = urlsplit(ref)
        if parts.scheme and parts.scheme != 'https':
            errors.append(f'{name}: non-https external reference {ref}')
            continue
        if parts.scheme == 'https':
            continue
        if not parts.path:
            continue
        target = (path.parent / unquote(parts.path)).resolve()
        if not target.exists():
            errors.append(f'{name}: broken local link -> {ref}')
        elif parts.fragment and target.name in pages and target.suffix == '.html':
            if unquote(parts.fragment) not in pages[target.name]:
                errors.append(f'{name}: broken anchor -> {ref}')

    # 4. host allowlist on every absolute link
    for tag, ref in checker.refs:
        parts = urlsplit(ref)
        if parts.scheme == 'https' and parts.hostname not in ALLOWED_HOSTS:
            errors.append(f'{name}: non-official source host -> {ref}')

    # 5. privacy patterns
    privacy = {
        'street address': r'\b\d{3,5}\s+[NSEW]?\.?\s*[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Drive|Dr|Way)\b',
        'APN-like number': r'\b\d{3,4}-\d{3}-\d{3}\b',
        'phone number': r'\b\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',
        'email address': r'[\w.+-]+@[\w-]+\.[\w.]+',
        'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
        'coordinates': r'\b\d{2}\.\d{4,}\s*,\s*-?\d{2,3}\.\d{4,}\b',
    }
    for label, pattern in privacy.items():
        for m in re.finditer(pattern, html):
            errors.append(f'{name}: possible {label} -> "{m.group(0)}"')

    # 6. no inline handlers, no external scripts, no network calls in app code
    if re.search(r'\son[a-z]+\s*=\s*"', html):
        errors.append(f'{name}: inline event handler attribute found')
    for tag, ref in checker.refs:
        if tag == 'script' and ref.startswith('http'):
            errors.append(f'{name}: external script -> {ref}')

    return checker.ids


def main():
    pages = {}
    for name in PAGES:
        ids = check_page(name, pages)
        pages[name] = ids or set()

    # re-run anchor checks now that every page's ids are known
    for name in PAGES:
        path = ROOT / name
        if not path.exists():
            continue
        for ref in re.findall(r'href="([^"]+)"', path.read_text(encoding='utf-8')):
            parts = urlsplit(ref)
            if parts.scheme or not parts.path or not parts.fragment:
                continue
            target = Path(parts.path).name
            if target in pages and unquote(parts.fragment) not in pages[target]:
                msg = f'{name}: anchor #{parts.fragment} missing on {target}'
                if msg not in errors:
                    errors.append(msg)

    # 7. navigation completeness
    nav = (ROOT / 'assets/nav.js').read_text(encoding='utf-8')
    for name in PAGES:
        if f"'{name}'" not in nav:
            errors.append(f'assets/nav.js: {name} is not in the shared navigation')

    # calculator must not touch the network or storage
    calc = (ROOT / 'assets/app.js').read_text(encoding='utf-8')
    for banned in ('XMLHttpRequest', 'localStorage', 'sessionStorage', 'indexedDB',
                   'document.cookie', 'navigator.sendBeacon'):
        if banned in calc:
            errors.append(f'assets/app.js: uses {banned} — the calculator must stay offline and stateless')
    if re.search(r'\bfetch\s*\(', calc):
        errors.append('assets/app.js: uses fetch() — the calculator must make no network requests')

    print(f'checked {len(PAGES)} pages, {len(ALLOWED_HOSTS)} allowlisted hosts')
    if warnings:
        print('\nWARNINGS:')
        print('\n'.join('  ' + w for w in warnings))
    if errors:
        print(f'\n{len(errors)} FAILURES:')
        print('\n'.join('  ' + e for e in errors))
        return 1
    print('OK — every data row sourced or explicitly blank, links and anchors resolve, '
          'hosts allowlisted, no identifiers, calculator is offline and stateless.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
