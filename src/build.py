"""Build 웹_3안/BLUFF_3안_Brand.html from template.html.

Inlines the BLUFF logo paths and embeds the paintings as data URIs: WebGL cannot read image files
when the page is opened straight from disk (file://), so the pictures travel inside the HTML.
Run:  python -E build.py
"""
import base64
import json
import re
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / 'assets'
# order on the wall (the three works BLUFF paints over), resized to 1100 px
PAINTINGS = [
    ('mona', '모나리자', '레오나르도 다 빈치'),
    ('van', '자화상', '빈센트 반 고흐'),
    ('david', '다비드', '미켈란젤로'),
]

svg = (HERE / 'logo.svg').read_text(encoding='utf-8')
paths = [re.sub(r'\s(fill|id)="[^"]*"', '', p) for p in re.findall(r'<path\b[^>]*/>', svg, flags=re.S)]
items = []
for key, title, artist in PAINTINGS:
    f = ASSETS / f'{key}.webp'
    w, h = Image.open(f).size
    items.append({'key': key, 'title': title, 'artist': artist, 'w': w, 'h': h,
                  'src': 'data:image/webp;base64,' + base64.b64encode(f.read_bytes()).decode()})
html = (HERE / 'template.html').read_text(encoding='utf-8')
html = html.replace('{{LOGO_PATHS}}', ''.join(paths)).replace('{{PAINTINGS}}', json.dumps(items, ensure_ascii=False))
# the 1안 footer, shared with 웹_2안; inside 3안 its Brand link and Back to top return to the first screen
footer = (HERE.parent.parent / '웹_2안' / 'shared' / 'footer.html').read_text(encoding='utf-8')
footer = footer.replace('href="BLUFF_2안_Brand.html"', 'href="#top" data-top').replace('href="BLUFF_2안_Products.html"', 'href="BLUFF_3안_Products.html" data-products')
html = html.replace('{{FOOTER}}', footer.replace('<span>Popup AR</span>', '<a href="BLUFF_3안_PopupAR.html">Popup AR</a>'))
(HERE.parent / 'BLUFF_3안_Brand.html').write_text(html, encoding='utf-8')
print('built', sum(len(i['src']) for i in items) // 1024, 'KB of images')
