"""Large Sahab Explains: classy information reels (dark speakeasy look, gold line-art, slow lounge music).

    python3 kit/classy/make_classy.py kit/classy/specs/explainNN.json   -> reels/ExplainNN_<slug>.mp4 + reels/ExplainNN_Cover.jpg
"""
import json, os, shutil, subprocess, sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
from tabla_lib import Kit, place, SR

OUT = os.path.join(HERE, '..', '..', 'reels') if os.path.isdir(os.path.join(HERE, '..', '..', 'reels')) else os.path.join(HERE, 'out')
FPS = 30


def midi(n): return 440 * 2 ** ((n - 69) / 12)


def ep(f, dur, v, rng):
    """Soft electric piano: FM bell attack over a warm sine body, gentle tremolo."""
    n = int(SR * dur); t = np.arange(n) / SR
    idx = 1.4 * np.exp(-t / .25)
    y = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t)) + .25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / .4)
    env = (1 - np.exp(-t / .006)) * np.exp(-t / (dur * .55))
    trem = 1 + .12 * np.sin(2 * np.pi * 4.3 * t + rng.uniform(0, 6))
    return v * y * env * trem


def bass(f, dur, v):
    n = int(SR * dur); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / .15)
    return v * y * (1 - np.exp(-t / .004)) * np.exp(-t / .55)


def brush(rng, dur=.35, v=.12):
    n = int(SR * dur); t = np.arange(n) / SR
    y = sosfilt(butter(2, [2500, 9000], btype='band', fs=SR, output='sos'), rng.standard_normal(n))
    return v * y * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5


def ride(rng, v=.06):
    n = int(SR * .5); t = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * t) for f in (5300, 6900, 8100)) / 3 + .3 * rng.standard_normal(n)
    return v * sosfilt(butter(2, 4000, btype='high', fs=SR, output='sos'), y) * np.exp(-t / .18)


def whoosh(rng, dur=.6, v=.10):
    n = int(SR * dur); t = np.arange(n) / SR
    y = sosfilt(butter(2, [400, 2200], btype='band', fs=SR, output='sos'), rng.standard_normal(n))
    return v * y * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2


def ting(rng, v=.08):
    n = int(SR * 1.2); t = np.arange(n) / SR
    return v * sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, a, d in [(2093, 1, .5), (3136, .5, .35), (4186, .3, .25)])


def tick(rng, v=.10):
    n = int(SR * .09); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 1250 * t) * np.exp(-t / .018) + .5 * sosfilt(butter(2, [1500, 5000], btype='band', fs=SR, output='sos'), rng.standard_normal(n)) * np.exp(-t / .008)
    return v * y


def ding(rng, v=.16):
    n = int(SR * 2.0); t = np.arange(n) / SR
    return v * sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, a, d in [(1318.5, 1, .9), (1975.5, .55, .6), (2637, .35, .4), (3951, .15, .25)])


def clink(rng, v=.10):
    n = int(SR * .6); t = np.arange(n) / SR
    f0 = rng.uniform(2500, 3000)
    return v * sum(a * np.sin(2 * np.pi * f0 * m * t) * np.exp(-t / d) for m, a, d in [(1, 1, .16), (1.48, .6, .11), (2.11, .4, .08), (2.93, .25, .05)])


PROGS = {   # (bass root, chord voicing) per bar
    'D': [(50, [66, 69, 73, 76]), (47, [62, 66, 69, 73]), (52, [62, 66, 67, 71]), (45, [61, 66, 67, 71])],   # Dmaj9 Bm9 Em9 A13
    'Eb': [(48, [63, 67, 70, 74]), (53, [63, 67, 68, 72]), (46, [62, 67, 68, 72]), (51, [62, 65, 67, 70])],  # Cm9 Fm9 Bb13 Ebmaj9
    'F': [(53, [64, 67, 69, 72]), (50, [60, 64, 65, 69]), (55, [62, 65, 69, 70]), (48, [64, 69, 70, 74])],   # Fmaj9 Dm9 Gm9 C13
}


def build_times(spec):
    """Cards carry their own 'dur'; the opener and outro have fixed lengths."""
    if all('dur' in c for c in spec['cards']):
        a = spec.get('open', 3.0); cards = []
        for c in spec['cards']:
            cards.append([round(a, 2), round(a + c['dur'], 2)]); a += c['dur']
        spec['times'] = {'cards': cards, 'outro': [round(a, 2), round(a + spec.get('outro_dur', 4.0), 2)]}
        spec['total'] = spec['times']['outro'][1]
    return spec


def lounge(spec, wav_path):
    T = spec['times']; total = spec['total']
    rng = np.random.default_rng(int(spec.get('seed', 3)))
    k = Kit(sa=293.66, seed=5)
    n = int(SR * (total + .2))
    keys = np.zeros(n); low = np.zeros(n); kit = np.zeros(n); fx = np.zeros(n)
    bpm = spec.get('bpm', 76); beat = 60 / bpm; bar = 4 * beat; sw = beat * .66      # swing eighth
    sh = spec.get('shift', 0)
    prog = [(r + sh, [m + sh for m in ch]) for r, ch in PROGS[spec.get('prog', 'D')]]
    t0 = 0.0; b = 0
    while t0 < total:
        root, chord = prog[b % 4]
        for at, vv in ((0, .22), (beat * 1 + sw, .15), (beat * 3, .12)):          # gentle comping
            for j, m in enumerate(chord):
                place(keys, ep(midi(m), bar * .9, vv, rng), t0 + at + j * .012)
        line = [root, root + 7, root + 12 if b % 2 else root + 4, root + 5]          # walking bass
        for q, m in enumerate(line):
            place(low, bass(midi(m - 12 if m > 52 else m), beat * .95, .55), t0 + q * beat)
        for q in range(4):
            place(kit, ride(rng), t0 + q * beat); place(kit, ride(rng, .035), t0 + q * beat + sw)
            if q % 2 == 1: place(kit, brush(rng), t0 + q * beat)
        if b % 2 == 0: place(kit, k.bol('Tin', .25), t0)                            # a desi wink, very soft
        if b % 4 == 3: place(kit, k.bol('Ge', .22), t0 + beat * 3.5)
        t0 += bar; b += 1
    for (a, _), c in zip(T['cards'], spec['cards']):
        typ = c.get('type', 'drink'); place(fx, whoosh(rng), a - .35)
        if typ in ('drink', 'info', 'recipe'): place(fx, ting(rng), a + .8)
        if typ == 'recipe':
            for k in range(len(c['rows'])): place(fx, tick(rng, .05), a + 1.0 + k * .45)
        if typ == 'myth': place(fx, k.bol('Ge', .30), a + 1.7); place(fx, ting(rng), a + 2.15)
        if typ == 'quiz':
            for q in (1.6, 2.6, 3.6): place(fx, tick(rng), a + q)
            place(fx, ding(rng), a + 4.6)
        if typ == 'beat':
            for j in range(c.get('glasses', 0) - c.get('from', 0)): place(fx, clink(rng), a + .45 + j * .2 + .18)
        if typ == 'verdict': place(fx, ting(rng), a + .6); place(fx, k.bol('Na', .25), a + 2.0)
    place(fx, whoosh(rng), T['outro'][0] - .35)
    nz = lambda x: x / (np.max(np.abs(x)) + 1e-9)
    mix = .55 * nz(keys) + .45 * nz(low) + .22 * nz(kit) + .30 * nz(fx)
    f = int(SR * 1.2); mix[:int(SR * .4)] *= np.linspace(.4, 1, int(SR * .4)); mix[-f:] *= np.linspace(1, 0, f)
    st = np.stack([mix, np.roll(mix, int(.011 * SR))], 1); st = st / np.max(np.abs(st)) * .85
    wavfile.write(wav_path, SR, (st * 32767).astype(np.int16))


def main(path):
    spec = build_times(json.load(open(path))); os.makedirs(OUT, exist_ok=True)
    work = f'/tmp/classy_{spec["id"]}'; shutil.rmtree(work, ignore_errors=True); os.makedirs(work + '/f')
    wav = os.path.join(work, 'mix.wav'); lounge(spec, wav)
    from playwright.sync_api import sync_playwright
    nfr = int(round(spec['total'] * FPS))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto('file://' + os.path.join(HERE, 'classy.html')); pg.wait_for_timeout(700)
        warn = pg.evaluate('s => window.load(s)', spec)
        if warn: print('LAYOUT WARNINGS:', warn)
        for i in range(nfr):
            pg.evaluate(f'window.render({i / FPS}, {i})')
            pg.screenshot(path=f'{work}/f/{i:04d}.jpg', type='jpeg', quality=92)
        pg.evaluate('window.cover()'); pg.wait_for_timeout(200)
        pg.screenshot(path=os.path.join(OUT, f'{spec["id"]}_Cover.jpg'), type='jpeg', quality=93)
        b.close()
    mp4 = os.path.join(OUT, f'{spec["id"]}_{spec["slug"]}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{work}/f/%04d.jpg', '-i', wav,
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
                    '-af', 'loudnorm=I=-18:TP=-2:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
                    '-shortest', '-movflags', '+faststart', mp4], check=True)
    print(mp4)


if __name__ == '__main__':
    main(sys.argv[1])
