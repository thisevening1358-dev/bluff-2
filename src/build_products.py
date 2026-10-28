"""Build 웹_3안/BLUFF_3안_Products.html from template_products.html.

The paintings (웹_3안/assets) and the QUAZIC CHIPS bags and soda cans (웹_2안/assets) travel inside the HTML as
data URIs, so the WebGL paper also works when the file is opened straight from disk.
Run:  python -E build_products.py
"""
import base64
import json
import re
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ART = HERE.parent / 'assets'
SHOP = ROOT / '웹_2안' / 'assets'

# same keys as the brand page, so a ball handed over from there finds its own painting here
PRODUCTS = [
    dict(key='mona', flavor='Herb', claim='허브 향이 진하게 밴 스낵.', big='0 kcal', bigLab='열량',
         truth='향은 진하지만 열량과 나트륨은 0입니다.', work='레오나르도 다 빈치, 모나리자'),
    dict(key='van', flavor='Blue Cheese', claim='꼬릿하고 짭짤한 블루치즈 맛.', big='0 mg', bigLab='나트륨',
         truth='짭짤한 이름이지만 염분은 없습니다.', work='빈센트 반 고흐, 자화상'),
    dict(key='david', flavor='Original Hot', claim='혀가 얼얼하게 매운맛.', big='0%', bigLab='캡사이신',
         truth='매운 이름이지만 얼얼함은 없습니다.', work='미켈란젤로, 다비드'),
]
# Soda facts are printed on the cans: 355 ml, 0 kcal, 0 mg sodium.
CANS = ['Cherry Hot Tonic', 'Acid Lime Fizz', 'Blue Cheese Cola', 'Red Sansho Tonic', 'Counterfeit Lime']


def uri(f):
    return 'data:image/webp;base64,' + base64.b64encode(f.read_bytes()).decode()


for p in PRODUCTS:
    bag = SHOP / f"bag_{p['key']}.webp"
    p['bw'], p['bh'] = Image.open(bag).size
    p['paint'], p['bag'] = uri(ART / f"{p['key']}.webp"), uri(bag)

picks = ''.join(f'<button type="button" aria-pressed="false">{p["flavor"]}</button>' for p in PRODUCTS)
cans = ''.join(f'''<button class="can" type="button" aria-label="BLUFF SODA {n}, 355 ml, 0 kcal, 나트륨 0 mg">
      <span class="body"><span class="contact" aria-hidden="true"></span><img src="{uri(SHOP / f'can{i + 1}.webp')}" alt="" width="322" height="724"></span>
      <span class="cap"><b>{n}</b><i>355 ML</i></span></button>''' for i, n in enumerate(CANS))

svg = (HERE / 'logo.svg').read_text(encoding='utf-8')
paths = [re.sub(r'\s(fill|id)="[^"]*"', '', p) for p in re.findall(r'<path\b[^>]*/>', svg, flags=re.S)]
footer = (ROOT / '웹_2안' / 'shared' / 'footer.html').read_text(encoding='utf-8')
footer = footer.replace('href="BLUFF_2안_Brand.html"', 'href="BLUFF_3안_Brand.html"').replace('href="BLUFF_2안_Products.html"', 'href="#top" data-top')

html = (HERE / 'template_products.html').read_text(encoding='utf-8')
html = (html.replace('{{LOGO_PATHS}}', ''.join(paths)).replace('{{FOOTER}}', footer.replace('<span>Popup AR</span>', '<a href="BLUFF_3안_PopupAR.html">Popup AR</a>'))
        .replace('{{PICKS}}', picks).replace('{{CANS}}', cans)
        .replace('{{PRODUCTS}}', json.dumps(PRODUCTS, ensure_ascii=False)))
out = HERE.parent / 'BLUFF_3안_Products.html'
out.write_text(html, encoding='utf-8')
print('built', out.name, len(html) // 1024, 'KB')
