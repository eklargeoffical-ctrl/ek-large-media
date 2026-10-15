"""Ek Large tabla kit v2: tabla-led, quirky, minimal. Original synthesis, no samples.

Design rules (owner feedback, 15 Oct): tabla is the star; a catchy repeating hook;
playful bayan "wobbles" (pitch glides) for the quirky feel; background only a faint, slow drone;
quieter master (about -17 LUFS) with no heavy compression.
"""
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100


class Kit:
    def __init__(self, sa=293.66, seed=1):
        self.sa = sa
        self.rng = np.random.default_rng(seed)

    # ---------- helpers ----------
    def t(self, d):
        return np.arange(int(SR * d)) / SR

    def bp(self, x, lo, hi):
        return sosfilt(butter(2, [lo, hi], btype='band', fs=SR, output='sos'), x)

    def lp(self, x, f):
        return sosfilt(butter(2, f, btype='low', fs=SR, output='sos'), x)

    def hp(self, x, f):
        return sosfilt(butter(2, f, btype='high', fs=SR, output='sos'), x)

    # ---------- dayan (treble drum) ----------
    def na(self, v=1.0, ring=0.40):
        """Open, singing stroke on the rim. ring = decay of the fundamental."""
        t = self.t(ring * 2.2)
        y = np.zeros_like(t)
        for n, a, d in [(1, 1.0, ring), (2, .45, ring * .5), (3, .32, ring * .32), (4, .16, ring * .2), (5, .08, ring * .14)]:
            y += a * np.exp(-t / d) * np.sin(2 * np.pi * self.sa * n * (1 + .0015 * n) * t + self.rng.uniform(0, 6.28))
        y += self.hp(self.rng.standard_normal(len(t)), 3000) * np.exp(-t / .003) * .35
        return v * y

    def tin(self, v=1.0):
        """Softer, shorter Na."""
        return self.na(v * .8, ring=.16)

    def tun(self, v=1.0):
        """Round open tone in the centre: pure, singing, a little lower."""
        t = self.t(.9)
        y = np.sin(2 * np.pi * self.sa * t) * np.exp(-t / .35) + .25 * np.sin(2 * np.pi * self.sa * 2 * t) * np.exp(-t / .12)
        return v * y * .9

    def ti(self, v=1.0):
        """Dry, closed tap: the 'Ti' of Tirakita."""
        t = self.t(.09)
        y = self.bp(self.rng.standard_normal(len(t)), 1500, 4800) * np.exp(-t / .014) * .8
        y += np.sin(2 * np.pi * self.sa * 2.03 * t) * np.exp(-t / .02) * .35
        return v * y

    # ---------- bayan (bass drum) ----------
    def ge(self, v=1.0, glide=0.0, dur=.75):
        """Open bass. glide>0 = the palm presses during the note, pitch bends up: the quirky 'wobble'."""
        t = self.t(dur)
        base = 88.0
        bend = glide * (1 - np.exp(-t / .11))  # rises then holds
        if glide > 0:
            bend += glide * .25 * np.sin(2 * np.pi * 5.5 * t) * np.exp(-t / .25)  # little wiggle
        f = base + 28 * (1 - np.exp(-t / .06)) + bend
        ph = 2 * np.pi * np.cumsum(f) / SR
        y = np.sin(ph) * np.exp(-t / .30) + .22 * np.sin(2 * ph) * np.exp(-t / .12)
        y += self.lp(self.rng.standard_normal(len(t)), 260) * np.exp(-t / .01) * .6
        return v * y

    def ka(self, v=1.0):
        """Flat, closed slap on the bass drum."""
        t = self.t(.08)
        y = self.bp(self.rng.standard_normal(len(t)), 140, 900) * np.exp(-t / .016)
        y += np.sin(2 * np.pi * 150 * t) * np.exp(-t / .025) * .5
        return v * y * .9

    # ---------- composite bols ----------
    def bol(self, name, v=1.0):
        parts = {
            'Dha': lambda: [self.na(v * .8), self.ge(v * .9)],
            'Dhin': lambda: [self.tin(v * .8), self.ge(v * .85)],
            'Dhaa': lambda: [self.na(v * .8), self.ge(v * .95, glide=60, dur=1.0)],   # quirky wobble accent
            'Na': lambda: [self.na(v)],
            'Tin': lambda: [self.tin(v)],
            'Tun': lambda: [self.tun(v)],
            'Ge': lambda: [self.ge(v)],
            'Gee': lambda: [self.ge(v, glide=55, dur=.9)],                            # wobble alone
            'Ti': lambda: [self.ti(v)],
            'Ra': lambda: [self.ti(v * .65)],
            'Ki': lambda: [self.ka(v * .8)],
            'Ka': lambda: [self.ka(v)],
            'Ta': lambda: [self.ti(v * 1.1)],
        }[name]()
        n = max(len(p) for p in parts)
        y = np.zeros(n)
        for p in parts:
            y[:len(p)] += p
        return y

    # ---------- the only background: a faint, slow drone ----------
    def drone(self, length_s, period=4.0):
        """Two notes (Sa and low Pa) swelling very slowly; meant to sit far behind the tabla."""
        n = int(SR * length_s)
        out = np.zeros(n)
        t0 = 0.0
        notes = [self.sa / 2, self.sa / 2 * 0.75]
        k = 0
        while t0 < length_s:
            f0 = notes[k % 2]
            tt = self.t(period * 1.6)
            y = sum((1 / h ** 1.4) * np.sin(2 * np.pi * f0 * h * tt + self.rng.uniform(0, 6.28)) for h in range(1, 9))
            env = np.sin(np.pi * np.clip(tt / (period * 1.6), 0, 1)) ** 2  # slow swell in and out
            y = self.lp(y * env, 1800)
            i = int(t0 * SR)
            j = min(n, i + len(y))
            out[i:j] += y[:j - i]
            t0 += period
            k += 1
        return out / (np.max(np.abs(out)) + 1e-9)


def place(buf, sig, t0, g=1.0):
    i = max(0, int(round(t0 * SR)))
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += g * sig[:j - i]


def master(tabla, drone, out_path, drone_db=-24.0, fade=0.8):
    """Tabla up front, drone far back, gentle room, no brick-wall squashing."""
    rng = np.random.default_rng(9)
    tabla = tabla / (np.max(np.abs(tabla)) + 1e-9)
    g = 10 ** (drone_db / 20)
    L = tabla + g * drone
    R = tabla + g * np.roll(drone, int(.015 * SR))
    tt = np.arange(int(SR * .5)) / SR
    ir = rng.standard_normal(len(tt)) * np.exp(-tt / .09)
    ir = sosfilt(butter(2, 5000, btype='low', fs=SR, output='sos'), ir)
    ir /= np.sqrt(np.sum(ir ** 2))
    L = L + .08 * fftconvolve(L, ir)[:len(L)]
    R = R + .08 * fftconvolve(R, ir[::-1].copy())[:len(R)]
    st = np.stack([L, R], 1)
    f = int(SR * fade)
    st[-f:] *= np.linspace(1, 0, f)[:, None]
    st = st / np.max(np.abs(st)) * .8
    wavfile.write(out_path, SR, (st * 32767).astype(np.int16))
