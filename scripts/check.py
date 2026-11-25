from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import subprocess
root=Path(__file__).resolve().parent.parent
class Check(HTMLParser):
 def __init__(self, name): super().__init__(); self.name=name; self.in_table=False; self.in_row=False; self.in_head=False; self.row_source=False; self.errors=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='table': self.in_table=True
  if tag=='thead': self.in_head=True
  if tag=='tr' and self.in_table and not self.in_head: self.in_row=True; self.row_source=False
  if tag=='a':
   href=a.get('href','')
   if self.in_row and href.startswith('https://'): self.row_source=True
   if href and not urlsplit(href).scheme and not href.startswith('#') and not (root / self.name.parent / href.split('#')[0]).exists(): self.errors.append('broken local link: '+href)
  if tag in ('script','link'):
   path=a.get('src') or a.get('href','')
   if path and not urlsplit(path).scheme and not (root/path).exists(): self.errors.append('missing asset: '+path)
 def handle_endtag(self,tag):
  if tag=='tr' and self.in_row:
   if not self.row_source: self.errors.append('table row missing primary-source link')
   self.in_row=False
  if tag=='thead': self.in_head=False
  if tag=='table': self.in_table=False
subprocess.run(['python3',str(root/'scripts/build.py')],check=True)
errors=[]
for p in sorted(root.glob('*.html')):
 c=Check(p.relative_to(root)); c.feed(p.read_text()); errors += [str(p.name)+': '+e for e in c.errors]
for path in [root/'assets/app.js', root/'assets/style.css']:
 s=path.read_text().lower()
 for forbidden in ['localstorage','sessionstorage','fetch(', 'xmlhttprequest', '@import']:
  if forbidden in s: errors.append(str(path.name)+': forbidden '+forbidden)
if errors: raise SystemExit('\n'.join(errors))
print('PASS: local links, table source links, assets and privacy checks')
