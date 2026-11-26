#!/usr/bin/env python3
"""Offline checks for the canonical public dashboard; not a substitute for source review."""
from html.parser import HTMLParser
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]
spec = spec_from_file_location('root_build', ROOT / 'tests/root_build.py')
builder = module_from_spec(spec)
spec.loader.exec_module(builder)
PAGES = [ROOT / href for _, items in builder.NAV for href, _ in items]
ERRORS = []


def allowed(url):
    parsed = urlsplit(url)
    host = (parsed.hostname or '').lower()
    return parsed.scheme == 'https' and (host.endswith('.gov') or host == 'fred.stlouisfed.org' or host == 'investors.jackinthebox.com')


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.refs = []
        self.ids = set()
        self.labels = set()
        self.fields = set()
        self.row = None
        self.row_count = 0
        self.text = []
        self.scripts = []
        self.referrer = False

    def fail(self, message):
        ERRORS.append(f'{self.path.name}: {message}')

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            if a['id'] in self.ids:
                self.fail(f'duplicate id {a["id"]}')
            self.ids.add(a['id'])
        if tag == 'meta' and a.get('name') == 'referrer' and a.get('content') == 'no-referrer':
            self.referrer = True
        if tag in ('form', 'iframe', 'object', 'embed'):
            self.fail(f'forbidden public submission or embedded resource: {tag}')
        if tag == 'label' and a.get('for'):
            self.labels.add(a['for'])
        if tag in ('input', 'textarea'):
            if not a.get('id'):
                self.fail('input without id')
            else:
                self.fields.add(a['id'])
            if a.get('name') or 'value' in a:
                self.fail('input must not have submission name or a default value')
        if tag == 'tr':
            self.row = {'cells': 0, 'sources': []}
        if tag == 'td' and self.row is not None:
            self.row['cells'] += 1
        if tag in ('a', 'link', 'script', 'img'):
            url = a.get('href') if tag in ('a', 'link') else a.get('src')
            if not url:
                return
            self.refs.append(url)
            p = urlsplit(url)
            if tag == 'a' and p.scheme:
                if not allowed(url):
                    self.fail(f'unapproved external link: {url}')
                if a.get('referrerpolicy') != 'no-referrer':
                    self.fail(f'external link missing no-referrer policy: {url}')
                if self.row is not None and allowed(url):
                    self.row['sources'].append(url)
            if tag in ('link', 'script', 'img') and (p.scheme or p.netloc):
                self.fail(f'automatic external resource: {url}')
            if tag == 'script':
                self.scripts.append(url)

    def handle_endtag(self, tag):
        if tag == 'tr' and self.row is not None:
            if self.row['cells']:
                self.row_count += 1
                if not self.row['sources']:
                    self.fail('table row has no official / primary source link')
            self.row = None

    def handle_data(self, data):
        self.text.append(data)


pages = {}
for path in PAGES:
    if not path.exists():
        ERRORS.append(f'missing canonical page: {path.name}')
        continue
    parsed = Page(path)
    parsed.feed(path.read_text(encoding='utf-8'))
    pages[path.resolve()] = parsed
    if not parsed.referrer:
        parsed.fail('missing no-referrer page policy')
    if parsed.fields - parsed.labels:
        parsed.fail('input without associated label: ' + ', '.join(sorted(parsed.fields - parsed.labels)))
    visible = ' '.join(parsed.text)
    checks = {
        'email address': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        'SSN-like number': r'\b\d{3}-\d{2}-\d{4}\b',
        'phone-like number': r'\b(?:\+1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',
        'street-like address': r'\b\d{1,5}\s+(?:[A-Za-z]+\s+){1,4}(?:Street|St\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Road|Rd\.?)\b',
    }
    for description, regex in checks.items():
        if re.search(regex, visible, re.I):
            parsed.fail(f'possible personal {description}; manual review required')

for path, parsed in pages.items():
    for url in parsed.refs:
        p = urlsplit(url)
        if p.scheme or p.netloc:
            continue
        target = (path.parent / unquote(p.path)).resolve() if p.path else path
        if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
            parsed.fail(f'broken local reference: {url}')
        elif p.fragment and target in pages and unquote(p.fragment) not in pages[target].ids:
            parsed.fail(f'broken local anchor: {url}')

js = (ROOT / 'assets/app.js').read_text(encoding='utf-8')
if (ROOT / 'assets/calc.js').read_text(encoding='utf-8') != js:
    ERRORS.append('generated worksheet engine differs from its reviewed source')
if re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon|localStorage|sessionStorage|indexedDB)\b|document\s*\.\s*cookie', js):
    ERRORS.append('worksheet contains a network or persistent-storage capability')

# A clean build must produce the checked-in, publishable HTML exactly.
with TemporaryDirectory() as tmp:
    builder.ROOT = Path(tmp)
    builder.build()
    for path in PAGES:
        generated = Path(tmp) / path.name
        if not generated.is_file() or generated.read_bytes() != path.read_bytes():
            ERRORS.append(f'{path.name}: checked-in page differs from root_build.py output')

if ERRORS:
    print('\n'.join(ERRORS))
    raise SystemExit(1)
print(f'{len(pages)} canonical pages; {sum(p.row_count for p in pages.values())} sourced table rows; local links, labels, privacy patterns, inert worksheet and reproducible build passed.')
print('External availability, source truth, anonymity against re-identification, and legacy dashboard correctness require separate review.')
