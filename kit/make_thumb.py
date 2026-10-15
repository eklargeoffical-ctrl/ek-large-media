"""Ek Large reel thumbnail (cover) maker.

    python3 make_thumb.py specs/reel09.json [specs/reel10.json ...]  ->  ../reels/<id>_Thumb.jpg

Each spec needs "id" and a "thumb" object. The thumbnail is a separate poster, never a frame of the video.
  thumb {kicker (series, caps), no? (issue number), hindi?, title (HTML, <em> = italic accent, 2-6 words),
         sub? (one short line), face (wink|dis|shock) | icon (neat|rocks|splash|highball|patiala|water|bottle),
         side? (small icon beside the face), stamp? (rotated sticker text), stampColor?, size?, max? (title px),
         bg (ox|ink|oak|amber|cream)}
1080x1920. Everything important sits in the centre 1080x1440, which is what the Instagram profile grid shows.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REELS = os.path.join(HERE, '..', 'reels')


def main(paths):
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto('file://' + os.path.join(HERE, 'thumb.html'))
        pg.wait_for_timeout(700)
        for sp in paths:
            spec = json.load(open(sp))
            pg.evaluate('th => window.build(th)', spec['thumb'])
            pg.wait_for_timeout(150)
            f = os.path.abspath(os.path.join(REELS, f"{spec['id']}_Thumb.jpg"))
            pg.locator('#t').screenshot(path=f, type='jpeg', quality=93)
            out.append(f)
        b.close()
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main(sys.argv[1:])
