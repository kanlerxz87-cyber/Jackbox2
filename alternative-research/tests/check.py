from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

class Checker(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]; self.row=None; self.in_body=False
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='tbody': self.in_body=True
        if tag=='tr' and self.in_body: self.row=[]
        if tag=='a' and self.row is not None: self.row.append(attrs.get('href',''))
        if tag in ('a','link','script'):
            url=attrs.get('href') or attrs.get('src')
            if url and not urlparse(url).scheme and not url.startswith('#'):
                assert Path(url).is_file(), f'missing local link: {url}'
    def handle_endtag(self, tag):
        if tag=='tr' and self.row is not None:
            assert any(url.startswith('https://') for url in self.row), 'table row missing source'
            self.rows.append(self.row); self.row=None
        if tag=='tbody': self.in_body=False

for path in Path('.').glob('*.html'):
    p=Checker(); p.feed(path.read_text()); print(path, len(p.rows), 'sourced rows')
assert len(list(Path('.').glob('*.html'))) == 8
