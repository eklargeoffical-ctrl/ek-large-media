"""Ek Large carousel maker.  python3 make_carousel.py specs/car_xxx.json  ->  ../carousels/<id>/<id>_01.png ...
Spec: {id, series (shown in the header), date, caption, slides:[{type: cover|point|list|end, ...}]}
  cover {hindi?, title, sub?, face?}   point {kicker?, title, body?, face? | icon?, bg?}
  list {title, items[]}                end {kicker?, title, body?, cta}
"""
import json, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))


def main(spec_path):
    spec = json.load(open(spec_path))
    out = os.path.join(HERE, '..', 'carousels', spec['id'])
    os.makedirs(out, exist_ok=True)
    files = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        pg.goto('file://' + os.path.join(HERE, 'carousel.html'))
        pg.wait_for_timeout(700)
        n = pg.evaluate('s => window.build(s)', spec)
        pg.wait_for_timeout(300)
        for i in range(n):
            f = os.path.join(out, f"{spec['id']}_{i + 1:02d}.png")
            pg.locator(f'#s{i}').screenshot(path=f)
            files.append(os.path.abspath(f))
        b.close()
    with open(os.path.join(out, 'caption.txt'), 'w') as fh:
        fh.write(spec.get('caption', ''))
    print(json.dumps({'slides': files, 'caption': os.path.abspath(os.path.join(out, 'caption.txt'))}))


if __name__ == '__main__':
    main(sys.argv[1])
