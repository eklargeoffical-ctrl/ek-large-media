"""Ek Large reel maker.  python3 make_reel.py specs/reel04.json  ->  ../reels/<id>_<slug>.mp4 and <id>_Cover.jpg

One spec drives both picture and music, so every visual beat lands on a tabla stroke.
Spec keys: id, slug, taal ('keherwa' 16 steps/bar | 'dadra' 12 steps/bar), bar (seconds), sa (Hz), seed,
groove ('bounce' | 'strut' | 'sneak'), scenes [ {type: hook|card|tier|list|end, bars, ...} ].
"""
import json, os, subprocess, sys, shutil
import numpy as np
from tabla_lib import Kit, place, master, SR

HERE = os.path.dirname(os.path.abspath(__file__))
REELS = os.path.join(HERE, '..', 'reels')
FPS = 30
TAIL = 1.4

# ---------------- groove library ----------------
G16 = {
    'bounce': (
        [(0, 'Dha', 1.0), (3, 'Ge', .55), (4, 'Na', .8), (6, 'Ti', .5), (7, 'Ta', .6), (8, 'Dhin', .9), (10, 'Na', .7), (12, 'Ge', .6), (14, 'Ti', .45), (15, 'Ra', .45)],
        [(0, 'Dha', 1.0), (2, 'Dha', .7), (6, 'Na', .75), (8, 'Dhaa', .95), (11, 'Na', .6), (12, 'Tin', .6), (14, 'Ki', .5), (15, 'Ta', .55)]),
    'strut': (
        [(0, 'Dha', 1.0), (4, 'Na', .8), (6, 'Dha', .75), (8, 'Tin', .7), (10, 'Na', .65), (11, 'Na', .5), (12, 'Ge', .7), (14, 'Na', .6)],
        [(0, 'Dha', 1.0), (3, 'Dha', .7), (6, 'Gee', .85), (10, 'Tin', .6), (12, 'Na', .7), (13, 'Ti', .45), (14, 'Ra', .45), (15, 'Ta', .55)]),
    'sneak': (
        [(0, 'Dha', .95), (4, 'Tin', .6), (6, 'Na', .6), (8, 'Dha', .8), (12, 'Tin', .6), (14, 'Na', .55)],
        [(0, 'Dha', .95), (4, 'Tin', .55), (7, 'Ge', .5), (8, 'Gee', .8), (12, 'Tin', .55), (14, 'Ki', .45), (15, 'Ta', .5)]),
}
G12 = {
    'bounce': (
        [(0, 'Dha', 1.0), (2, 'Dhin', .7), (4, 'Na', .65), (6, 'Dha', .85), (8, 'Tin', .6), (9, 'Ti', .4), (10, 'Na', .65)],
        [(0, 'Dha', 1.0), (2, 'Tin', .5), (3, 'Ge', .5), (4, 'Na', .65), (6, 'Gee', .8), (8, 'Tin', .6), (10, 'Na', .6), (11, 'Ra', .4)]),
    'strut': (
        [(0, 'Dha', 1.0), (3, 'Na', .6), (4, 'Na', .7), (6, 'Dha', .85), (9, 'Tin', .6), (10, 'Na', .6)],
        [(0, 'Dha', 1.0), (2, 'Dha', .6), (4, 'Na', .65), (6, 'Gee', .85), (9, 'Tin', .55), (10, 'Ki', .45), (11, 'Ta', .5)]),
    'sneak': (
        [(0, 'Dha', .9), (4, 'Tin', .5), (6, 'Na', .6), (8, 'Tin', .5), (10, 'Na', .5)],
        [(0, 'Dha', .9), (3, 'Ge', .45), (4, 'Tin', .5), (6, 'Gee', .75), (8, 'Tin', .5), (10, 'Na', .5)]),
}
TEASE16 = [(0, 'Gee', .9), (8, 'Na', .7), (11, 'Na', .5), (12, 'Tin', .5)]
TEASE12 = [(0, 'Tin', .45), (4, 'Tin', .4), (6, 'Ge', .35), (8, 'Tin', .45), (10, 'Tin', .35)]
FILL16 = [(i, s, .55 + .025 * i) for i, s in enumerate(['Ti', 'Ra', 'Ki', 'Ta'] * 2)] + [(8, 'Dha', .85), (10, 'Na', .6), (12, 'Ti', .55), (13, 'Ra', .55), (14, 'Ki', .6), (15, 'Ta', .65)]
FILL12 = [(0, 'Dha', .9), (2, 'Dhin', .7), (4, 'Na', .6), (6, 'Ti', .5), (7, 'Ra', .45), (8, 'Ki', .5), (9, 'Ta', .55), (10, 'Ti', .5), (11, 'Ta', .6)]


def timeline(spec):
    steps = 16 if spec.get('taal', 'keherwa') == 'keherwa' else 12
    bar = float(spec['bar'])
    st = bar / steps
    beat = 4 if steps == 16 else 3
    t = 0.0
    out = []
    for i, sc in enumerate(spec['scenes']):
        s = dict(sc)
        s['start'] = round(t, 4)
        s['end'] = round(t + sc['bars'] * bar, 4)
        s['events'] = [] if sc['type'] == 'hook' else [s['start']]  # every scene after the hook opens on a wobble accent
        if s['type'] == 'hook':
            s['subAt'] = round(bar * 0.5, 4)
        if s['type'] == 'card':
            s['bodyAt'] = round(st * beat, 4)
            if s.get('stamp'):
                s['stampAt'] = round(s['start'] + bar, 4)  # stamp lands on the scene's second downbeat
                s['events'].append(s['stampAt'])
        if s['type'] == 'tier':
            s['rowAt'] = [round(s['start'] + (k + 1) * beat * st * 2, 4) for k in range(len(s['rows']))]
            s['events'] += s['rowAt']
        if s['type'] == 'list':
            s['itemAt'] = [round(s['start'] + (k + 2) * beat * st, 4) for k in range(len(s['items']))]
            s['ctaAt'] = round(s['start'] + (len(s['items']) + 3) * beat * st, 4)
            s['events'] += s['itemAt'] + [s['ctaAt']]
        if s['type'] == 'end':
            final = s['end']
            s['l1At'] = round(final - 12 * st, 4)
            s['l2At'] = round(final - 6 * st, 4)
            s['sealAt'] = round(final, 4)
        out.append(s)
        t = s['end']
    return {'steps': steps, 'bar': bar, 'step': st, 'total': round(t + TAIL, 4), 'final': round(t, 4), 'scenes': out}


def music(spec, tl, wav_path):
    steps, bar, st = tl['steps'], tl['bar'], tl['step']
    k = Kit(sa=float(spec.get('sa', 261.63)), seed=int(spec.get('seed', 1)))
    rng = np.random.default_rng(int(spec.get('seed', 1)) + 7)
    g = (G16 if steps == 16 else G12)[spec.get('groove', 'bounce')]
    tease = TEASE16 if steps == 16 else TEASE12
    fill = FILL16 if steps == 16 else FILL12
    n = int(SR * tl['total'])
    tabla = np.zeros(n)
    final = tl['final']
    tihai_start = final - 16 * st
    events = sorted(set(e for s in tl['scenes'] for e in s['events'] if e < tihai_start - 1e-3))
    hits = {}
    for s in tl['scenes']:
        nb = int(round((s['end'] - s['start']) / bar))
        for b in range(nb):
            b0 = s['start'] + b * bar
            if s['type'] == 'hook':
                pat = tease
            elif s['type'] == 'end' or b == nb - 1 and s is not tl['scenes'][-1] and tl['scenes'][tl['scenes'].index(s) + 1]['type'] == 'end':
                pat = g[0] if s['type'] == 'end' else fill
            else:
                pat = g[b % 2]
            for step, bol, v in pat:
                tt = round(b0 + step * st, 4)
                hits[tt] = (bol, v)
    for e in events:  # accents on every visual event
        e = round(e, 4)
        nearest = min(hits, key=lambda x: abs(x - e)) if hits else None
        if nearest is not None and abs(nearest - e) < st * .5:
            del hits[nearest]
        hits[e] = ('Dhaa', 1.0)
    hits = {t: h for t, h in hits.items() if t < tihai_start - 1e-3}
    for t, (bol, v) in hits.items():
        place(tabla, k.bol(bol, v * rng.uniform(.93, 1.04)), t + rng.uniform(-.004, .004))
    # tihai: (Ti Ra Ki Ta Dha) x3 with one-slot gaps; Dhas at final-12, final-6 steps; the last Dha is the final sam
    slot = 0
    for rep in range(3):
        for s_ in ['Ti', 'Ra', 'Ki', 'Ta', 'Dha']:
            if rep == 2 and s_ == 'Dha':
                break
            place(tabla, k.bol(s_, (.6 + .08 * rep) if s_ != 'Dha' else (.9 + .05 * rep)), tihai_start + slot * st)
            slot += 1
        slot += 1
    place(tabla, k.bol('Dhaa', 1.0), final)
    drone = k.drone(tl['total'], period=bar * 2)
    raw = wav_path.replace('.wav', '_raw.wav')
    master(tabla, drone, raw, drone_db=float(spec.get('drone_db', -26)))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-af', 'loudnorm=I=-17:TP=-2:LRA=11', '-ar', '44100', wav_path], check=True)


def frames(tl, out_dir, cover_path, cover_t):
    from playwright.sync_api import sync_playwright
    os.makedirs(out_dir, exist_ok=True)
    n = int(round(tl['total'] * FPS))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto('file://' + os.path.join(HERE, 'reel.html'))
        pg.wait_for_timeout(700)
        pg.evaluate('tl => window.load(tl)', tl)
        pg.wait_for_timeout(300)
        for i in range(n):
            pg.evaluate(f'window.render({i / FPS})')
            pg.screenshot(path=os.path.join(out_dir, f'f{i:04d}.jpg'), type='jpeg', quality=93)
        pg.evaluate(f'window.render({cover_t})')
        pg.screenshot(path=cover_path, type='jpeg', quality=92)
        b.close()
    return n


def main(spec_path, keep_frames=False):
    spec = json.load(open(spec_path))
    tl = timeline(spec)
    work = os.path.join('/tmp', 'eklarge_' + spec['id'])
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    os.makedirs(REELS, exist_ok=True)
    wav = os.path.join(work, 'music.wav')
    music(spec, tl, wav)
    hook = tl['scenes'][0]
    cover = os.path.join(REELS, f"{spec['id']}_Cover.jpg")
    frames(tl, os.path.join(work, 'frames'), cover, min(hook['end'] - .2, hook['start'] + 1.4))
    mp4 = os.path.join(REELS, f"{spec['id']}_{spec['slug']}.mp4")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(work, 'frames', 'f%04d.jpg'), '-i', wav,
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart',
                    '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-shortest', mp4], check=True)
    json.dump(tl, open(os.path.join(work, 'timeline.json'), 'w'), indent=1)
    print(json.dumps({'mp4': os.path.abspath(mp4), 'cover': os.path.abspath(cover), 'seconds': tl['total'], 'work': work}))
    if not keep_frames:
        shutil.rmtree(os.path.join(work, 'frames'), ignore_errors=True)


def preview(spec_path, times, out_png):
    """Render a contact sheet of key frames (no music, no video) for a quick visual check."""
    from playwright.sync_api import sync_playwright
    spec = json.load(open(spec_path))
    tl = timeline(spec)
    shots = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto('file://' + os.path.join(HERE, 'reel.html'))
        pg.wait_for_timeout(700)
        pg.evaluate('tl => window.load(tl)', tl)
        for t in times:
            pg.evaluate(f'window.render({t})')
            f = f'/tmp/pv_{spec["id"]}_{t:06.2f}.png'
            pg.screenshot(path=f)
            shots.append(f)
        b.close()
    subprocess.run(['montage', *shots, '-tile', f'{min(len(shots), 5)}x', '-geometry', '270x480+6+6', '-background', '#444', out_png], check=True)
    return tl


if __name__ == '__main__':
    if '--preview' in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index('--preview') + 1].split(',')]
        tl = preview(sys.argv[1], ts, sys.argv[sys.argv.index('--preview') + 2])
        print(json.dumps([(s['type'], s['start'], s['end']) for s in tl['scenes']]))
    else:
        main(sys.argv[1], keep_frames='--keep' in sys.argv)
