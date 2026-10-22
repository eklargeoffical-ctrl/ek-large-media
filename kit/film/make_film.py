"""Large Sahab Productions film maker (no voiceover; on-screen text, desi-trap beat and sound effects carry the joke).

    python3 make_film.py specs/film05.json            -> reels/Film05_<slug>.mp4 + reels/Film05_Thumb.jpg
    python3 make_film.py specs/film05.json --audio    (sound only, for a quick listen)

See FORMAT.md for the spec, the 13.6-second clock and the writing rules.
"""
import json, os, shutil, subprocess, sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from tabla_lib import Kit, place, SR

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'reels')
FPS = 30


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], btype='band', fs=SR, output='sos'), x)


def boom(rng, v=1.0):
    n = int(SR * .9); t = np.arange(n) / SR
    f = 40 + 55 * np.exp(-t / .09)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .32)
    nz = sosfilt(butter(2, 1800, fs=SR, output='sos'), rng.standard_normal(n)) * np.exp(-t / .05) * .5
    return v * (s + nz)


def whoosh(rng, dur=.32, v=.5):
    n = int(SR * dur); t = np.arange(n) / SR
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    noise = rng.standard_normal(n)
    out = np.zeros(n); seg = n // 8
    for i in range(8):                          # rising band sweep
        lo = 300 * (1.45 ** i); a, b = i * seg, min(n, (i + 2) * seg)
        out[a:b] += bp(noise[a:b], lo, lo * 2.2) * np.hanning(b - a)
    return v * out * env / (np.max(np.abs(out)) + 1e-9)


def clink(rng, v=.35):
    n = int(SR * .7); t = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f * rng.uniform(.985, 1.015) * t) * np.exp(-t / d)
            for f, a, d in [(2650, 1, .32), (3980, .7, .22), (5230, .5, .16), (6900, .3, .1)])
    return v * y * (1 - np.exp(-t / .002))


def scratch(rng, v=.6):
    n = int(SR * .42); t = np.arange(n) / SR
    fc = 900 + 700 * np.sin(2 * np.pi * 6.5 * t) * np.exp(-t / .3)
    x = rng.standard_normal(n); y = np.zeros(n); y1 = y2 = 0.0; r = .985
    for i in range(n):                          # swept two-pole resonator = vinyl scratch
        w = 2 * np.pi * fc[i] / SR
        y0 = x[i] + 2 * r * np.cos(w) * y1 - r * r * y2
        y[i] = y0; y2, y1 = y1, y0
    y = y / (np.max(np.abs(y)) + 1e-9)
    return v * y * np.exp(-t / .25)


def load_voice(path):
    if path.endswith('.wav'):
        sr, a = wavfile.read(path)
    else:
        tmp = '/tmp/_vo.wav'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), tmp], check=True)
        sr, a = wavfile.read(tmp)
    a = a.astype(np.float64)
    if a.ndim > 1: a = a.mean(1)
    if sr != SR:
        idx = np.arange(0, len(a), sr / SR); a = np.interp(idx, np.arange(len(a)), a)
    return a / (np.max(np.abs(a)) + 1e-9)


def k808(rng, f0, dur=.9, v=1.0):
    """Sub bass with a short pitch drop and soft saturation so phones can hear it."""
    n = int(SR * dur); t = np.arange(n) / SR
    f = f0 * (1 + 1.6 * np.exp(-t / .03))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (dur * .45))
    return v * np.tanh(2.2 * y) / np.tanh(2.2)


def clap(rng, v=.7):
    n = int(SR * .25); t = np.arange(n) / SR
    env = sum(np.exp(-np.clip(t - d, 0, None) / .012) * (t >= d) for d in (0, .011, .022)) * .4 + np.exp(-t / .07) * .8
    return v * bp(rng.standard_normal(n), 900, 5200) * env


def hat(rng, v=.18, open_=False):
    n = int(SR * (.18 if open_ else .05)); t = np.arange(n) / SR
    y = sosfilt(butter(2, 7500, btype='high', fs=SR, output='sos'), rng.standard_normal(n))
    return v * y * np.exp(-t / (.06 if open_ else .012))


def riser(rng, dur, v=.35):
    n = int(SR * dur); t = np.arange(n) / SR
    out = np.zeros(n); seg = n // 10; noise = rng.standard_normal(n)
    for i in range(10):
        lo = 250 * (1.4 ** i); a, b = i * seg, min(n, (i + 2) * seg)
        out[a:b] += bp(noise[a:b], lo, lo * 2) * np.hanning(b - a)
    return v * out * (t / dur) ** 2 / (np.max(np.abs(out)) + 1e-9)


def soundtrack(spec, wav_path):
    """Desi trap: 808 bass, clap, light hats, and the tabla as the signature hook. Sound effects carry the jokes."""
    T = spec['times']; total = spec['total']
    rng = np.random.default_rng(int(spec.get('seed', 7)))
    k = Kit(sa=spec.get('sa', 293.66), seed=int(spec.get('seed', 7)))
    n = int(SR * (total + .1))
    drums = np.zeros(n); bass = np.zeros(n); tab = np.zeros(n); fx = np.zeros(n)
    bar = T['beats'][0][1] - T['beats'][0][0]
    s16 = bar / 16
    root = spec.get('root', 73.42)                       # D2
    prog = [1, 1, 0.794, 0.749]                          # D D Bb A

    def tabla(t0, pattern, g=1.0):
        for step, b, v in pattern:
            place(tab, k.bol(b, v * rng.uniform(.93, 1.04)), t0 + step * s16 + rng.uniform(-.003, .003), g)

    def beat_bar(t0, i, full=True):
        f = root * prog[i % 4]
        place(bass, k808(rng, f, bar * .55), t0)
        place(bass, k808(rng, f, bar * .3, .8), t0 + 10 * s16)
        if full:
            place(bass, k808(rng, f * 1.335, bar * .2, .6), t0 + 14 * s16)
            place(drums, clap(rng), t0 + 8 * s16)
            for st in range(0, 16, 2):
                place(drums, hat(rng, .16 if st % 4 else .2), t0 + st * s16)
            if i % 2 == 1:
                for st in range(12, 16):
                    place(drums, hat(rng, .12), t0 + st * s16 + s16 / 2)
        tabla(t0, [(0, 'Dha', .9), (3, 'Na', .55), (6, 'Tin', .5), (7, 'Na', .45), (12, 'Ge', .5), (13, 'Na', .5)])

    # 0: title slam
    place(fx, boom(rng, 1.0), 0.0); place(bass, k808(rng, root, 1.1, 1.0), 0.0); place(tab, k.bol('Dhaa', 1.0), 0.0)
    place(tab, k.bol('Dha', .8), .3)
    # night: no drums, tabla tiptoe and a riser into the first beat
    a, b = T['night']
    tabla(a, [(0, 'Tin', .45), (4, 'Ge', .4), (8, 'Tin', .45), (12, 'Ge', .35), (14, 'Tin', .35)])
    place(fx, riser(rng, b - a), a)
    tt = a + .1; j = 0
    while tt < b - .1:                                   # clock tick-tock keeps the night card moving
        n_ = int(SR * .03); x = np.arange(n_) / SR
        place(fx, np.sin(2 * np.pi * (2400 if j % 2 == 0 else 1800) * x) * np.exp(-x / .006) * .5, tt)
        tt += .2; j += 1
    # three beats: full groove, a hit on each cut, a clink per glass
    for i, (a, b) in enumerate(T['beats']):
        beat_bar(a, i, True)
        place(fx, boom(rng, .5), a)
    for bt in spec['beats']:
        for p in bt['pop']:
            place(fx, clink(rng, .3), p)
    # Large Sahab: everything stops on a record scratch; one low note under his line; a hit when the line lands
    s0 = T['sahab'][0]
    place(fx, scratch(rng), s0 - .05)
    place(bass, k808(rng, root * .749, 1.6, .7), spec['sahab']['at'])
    place(fx, boom(rng, .7), spec['sahab']['at'])
    # end card: the drop, two bars, tihai on the tabla landing on the last frame (loops to the title slam)
    e0 = T['end'][0]
    place(fx, boom(rng, 1.0), e0)
    t = e0; i = 0
    while t < total - .05:
        beat_bar(t, i, True); t += bar; i += 1
    land = total - .02; slot = s16 * .75; seq = []
    for rep in range(3):
        seq += [('Ti', .55 + .07 * rep), ('Ra', .55 + .07 * rep), ('Ki', .6 + .07 * rep), ('Ta', .65 + .07 * rep), ('Dha', .9 + .05 * rep)]
        if rep < 2: seq.append(None)
    t0 = land - slot * (len(seq) - 1)
    for j, x in enumerate(seq):
        if x and j < len(seq) - 1: place(tab, k.bol(x[0], x[1]), t0 + j * slot)
    # whooshes into every cut
    for c in [T['night'][0]] + [x[0] for x in T['beats']] + [s0, e0]:
        place(fx, whoosh(rng, v=.45), c - .2)
    # silence the groove under the verdict (it stops dead on the scratch)
    g = np.ones(n); g[int(s0 * SR):int(e0 * SR)] = 0
    g = np.convolve(g, np.ones(441) / 441, mode='same')
    nz = lambda x: x / (np.max(np.abs(x)) + 1e-9)
    mix = (.62 * nz(bass) + .42 * nz(drums)) * g + .55 * nz(tab) + .5 * nz(fx)
    mix = np.tanh(mix * 1.3) / np.tanh(1.3)
    st = np.stack([mix, np.roll(mix, int(.006 * SR))], 1)
    st = st / np.max(np.abs(st)) * .89
    wavfile.write(wav_path, SR, (st * 32767).astype(np.int16))


def mouth_curve(spec):
    """Large Sahab's mouth opening per frame, from the loudness of his voice line."""
    sl = next((l for l in spec.get('vo', []) if l['id'].startswith('S') and l.get('file')), None)
    if not sl: return []
    a = np.abs(load_voice(sl['file'])); hop = SR // FPS
    env = np.array([a[i:i + hop].mean() for i in range(0, len(a), hop)])
    env = env / (env.max() + 1e-9)
    return [round(float(min(1, x * 1.6)) if x > .08 else 0, 3) for x in env]


def main(path, audio_only=False):
    spec = json.load(open(path))
    os.makedirs(OUT, exist_ok=True)
    work = f'/tmp/film_{spec["id"]}'; shutil.rmtree(work, ignore_errors=True); os.makedirs(work + '/f')
    wav = os.path.join(work, 'mix.wav')
    soundtrack(spec, wav)
    if audio_only:
        shutil.copy(wav, os.path.join(OUT, f'{spec["id"]}_audio.wav')); print('audio', wav); return
    spec['mouth'] = mouth_curve(spec)
    from playwright.sync_api import sync_playwright
    nfr = int(round(spec['total'] * FPS))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto('file://' + os.path.join(HERE, 'film.html')); pg.wait_for_timeout(700)
        pg.evaluate('s => window.load(s)', spec)
        for i in range(nfr):
            pg.evaluate(f'window.render({i / FPS}, {i})')
            pg.screenshot(path=f'{work}/f/{i:04d}.jpg', type='jpeg', quality=93)
        # thumbnail: the end-card poster, fully settled
        pg.evaluate(f'window.render({spec["times"]["end"][0] + 1.5}, 99999)')
        pg.screenshot(path=os.path.join(OUT, f'{spec["id"]}_Thumb.jpg'), type='jpeg', quality=93)
        b.close()
    mp4 = os.path.join(OUT, f'{spec["id"]}_{spec["slug"]}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{work}/f/%04d.jpg', '-i', wav,
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '23', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-shortest', '-movflags', '+faststart', mp4], check=True)
    print(mp4)


if __name__ == '__main__':
    main(sys.argv[1], audio_only='--audio' in sys.argv)
