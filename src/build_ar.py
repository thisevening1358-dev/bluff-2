"""Build 웹_3안/BLUFF_3안_PopupAR.html from template_ar.html.

The popup model (E안, BLUFF CASE FILE) is built in the browser from boxes; only the paintings in World A and the
bags in the exit-hall shop are pictures. They are shrunk and embedded as data URIs so the page also works from disk.
Run:  python -E build_ar.py
"""
import base64
import io
import json
import re
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def shrink(path, width):
    im = Image.open(path)
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=82)
    return {'src': 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode(), 'w': im.width, 'h': im.height}


art = {
    # the three works on the World A gallery wall
    'paintings': [shrink(HERE.parent / 'assets' / f'{k}.webp', 520) for k in ('van', 'mona', 'david')],
    # QUAZIC CHIPS on the BLUFF SHOP tables
    'bags': [shrink(ROOT / '웹_2안' / 'assets' / f'bag_{k}.webp', 260) for k in ('mona', 'van', 'david')],
}
svg = (HERE / 'logo.svg').read_text(encoding='utf-8')
paths = [re.sub(r'\s(fill|id)="[^"]*"', '', p) for p in re.findall(r'<path\b[^>]*/>', svg, flags=re.S)]
html = (HERE / 'template_ar.html').read_text(encoding='utf-8')
html = html.replace('{{LOGO_PATHS}}', ''.join(paths)).replace('{{ART}}', json.dumps(art))
out = HERE.parent / 'BLUFF_3안_PopupAR.html'
out.write_text(html, encoding='utf-8')
print('built', out.name, len(html) // 1024, 'KB')
