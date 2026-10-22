"""Preview key frames of a classy spec: opener, every card fully revealed, outro and cover, as one contact sheet."""
import json, os, sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_classy import build_times
OUT = sys.argv[2] if len(sys.argv) > 2 else 'prev'
os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for path in sys.argv[1].split(','):
        spec = build_times(json.load(open(path)))
        pg.goto('file://' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'classy.html')); pg.wait_for_timeout(500)
        warn = pg.evaluate('s => window.load(s)', spec)
        if warn: print(spec['id'], 'WARN', warn)
        T = spec['times']; shots = [0.0] + [b_ - .6 for a, b_ in T['cards']] + [spec['total'] - .3]
        ims = []
        for k, t in enumerate(shots):
            pg.evaluate(f'window.render({t}, {int(t*30)})'); f = f'{OUT}/{spec["id"]}_{k:02d}.jpg'; pg.screenshot(path=f, type='jpeg', quality=85); ims.append(f)
        pg.evaluate('window.cover()'); pg.wait_for_timeout(100); f = f'{OUT}/{spec["id"]}_cover.jpg'; pg.screenshot(path=f, type='jpeg', quality=88); ims.append(f)
        w = 360; h = 640; n = len(ims); cols = min(n, 5); rows = (n + cols - 1) // cols
        sheet = Image.new('RGB', (cols * w, rows * h), 'black')
        for k, f in enumerate(ims): sheet.paste(Image.open(f).resize((w, h)), ((k % cols) * w, (k // cols) * h))
        sheet.save(f'{OUT}/{spec["id"]}_sheet.jpg', quality=88); print(spec['id'], 'total', spec['total'])
    b.close()
