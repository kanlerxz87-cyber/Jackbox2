#!/usr/bin/env python3
"""Validate local links, table provenance and public artifacts without network access."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
root = Path(__file__).resolve().parents[1] / 'docs'
errors = []
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.path = path; self.row = None; self.refs=[]; self.ids=set(); self.in_td=False
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag == 'tr': self.row={'cell':False,'official':False}
        if tag == 'td' and self.row is not None: self.row['cell']=True
        if tag in ('a','link','script'):
            url=a.get('href') or a.get('src')
            if not url: return
            if self.row is not None and url.startswith('https://'): self.row['official']=True
            self.refs.append(url)
    def handle_endtag(self,tag):
        if tag == 'tr' and self.row is not None:
            if self.row['cell'] and not self.row['official']: errors.append(f'{self.path.name}: table row without external source')
            self.row=None
pages={}
for path in root.glob('*.html'):
    parser=Page(path);parser.feed(path.read_text());pages[path]=parser
for path, parser in pages.items():
    for url in parser.refs:
        u=urlsplit(url)
        if u.scheme or u.netloc: continue
        target=(path.parent / unquote(u.path)).resolve() if u.path else path
        if not target.is_relative_to(root.resolve()) or not target.exists(): errors.append(f'{path.name}: broken local link {url}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids: errors.append(f'{path.name}: broken anchor {url}')
json.loads((root/'data/verified.json').read_text())
if errors: print('\n'.join(errors)); raise SystemExit(1)
print(f'{len(pages)} pages: local links and table provenance checked; JSON valid. External availability is not checked.')
