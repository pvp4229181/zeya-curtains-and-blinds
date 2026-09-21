from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]/'zeya-website'
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for key in ('href','src'):
            url=a.get(key,''); p=urlsplit(url)
            if url and not p.scheme and p.path:
                assert (ROOT/unquote(p.path)).is_file(), (self.page,url)
        if tag=='img': assert a.get('alt'), self.page
for page in ROOT.glob('*.html'):
    parser=Links(); parser.page=page.name; parser.feed(page.read_text(encoding='utf8'))
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog
# Slugs, not rows: Motorized Curtains is listed in two groups but is one page.
expected={catalog.slug(n) for g in catalog.GROUPS.values() for n,d,b in g}
assert len(list(ROOT.glob('product-*.html')))==len(expected)
total=len(list(ROOT.glob('*.html')))
print(f'All {total} pages: local links, images and product count passed.')
