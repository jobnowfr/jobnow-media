"""Procedural lo-fi / ambient background music, generated locally (no third-party audio, no rights issues).

usage: python3 music.py out.wav seconds [seed]
The seed picks the chord progression, tempo and voicing, so each video gets its own track.
"""
import sys
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile

SR = 44100

PROGRESSIONS = [
    # (chords as midi notes, bass root)
    [([53, 57, 60, 64], 41), ([52, 55, 59, 62], 40), ([50, 53, 57, 60], 38), ([48, 52, 55, 59], 36)],   # Fmaj7 Em7 Dm7 Cmaj7
    [([50, 53, 57, 60], 38), ([55, 59, 62, 65], 43), ([48, 52, 55, 59], 36), ([45, 48, 52, 55], 33)],   # Dm7 G7 Cmaj7 Am7
    [([45, 48, 52, 55], 33), ([53, 57, 60, 64], 41), ([48, 52, 55, 59], 36), ([55, 59, 62, 65], 43)],   # Am7 Fmaj7 Cmaj7 G7
    [([48, 52, 55, 59], 36), ([45, 48, 52, 55], 33), ([50, 53, 57, 60], 38), ([55, 59, 62, 66], 43)],   # Cmaj7 Am7 Dm7 Gmaj7
]


def make(out, dur, seed=1):
    rng = np.random.default_rng(seed)
    bpm = int(rng.integers(76, 92))
    beat = 60 / bpm
    bar = 4 * beat
    prog = PROGRESSIONS[seed % len(PROGRESSIONS)]
    transpose = int(rng.integers(-2, 3))
    N = int(SR * (dur + 3))
    mix = np.zeros((N, 2))

    def midi(m):
        return 440 * 2 ** ((m + transpose - 69) / 12)

    def add(sig, t0, gain=1.0, pan=0.0):
        i = int(round(t0 * SR))
        if i < 0:
            sig = sig[-i:]
            i = 0
        if i >= N or len(sig) == 0:
            return
        sig = sig[: N - i]
        l = np.cos((pan + 1) * np.pi / 4)
        r = np.sin((pan + 1) * np.pi / 4)
        mix[i:i + len(sig), 0] += sig * gain * l
        mix[i:i + len(sig), 1] += sig * gain * r

    def env(n, a, d, s_level, r, sustain_len):
        a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
        s_n = max(0, int(sustain_len * SR) - a_n - d_n)
        e = np.concatenate([np.linspace(0, 1, max(a_n, 1)), np.linspace(1, s_level, max(d_n, 1)),
                            np.full(s_n, s_level), np.linspace(s_level, 0, max(r_n, 1))])
        return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))

    def ep_note(f, length):
        n = int((length + 1.2) * SR)
        t = np.arange(n) / SR
        s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 1.6)
             + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3.0)
             + 0.12 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 6.0)
             + 0.06 * np.sin(2 * np.pi * 7.1 * f * t) * np.exp(-t * 18.0))
        s *= (1 + 0.08 * np.sin(2 * np.pi * 4.2 * t))
        rel = np.ones(n)
        k = int(length * SR)
        rel[k:] = np.linspace(1, 0, n - k)
        return s * rel * np.minimum(1, t / 0.004)

    def pad_note(f, length):
        n = int((length + 1.5) * SR)
        t = np.arange(n) / SR
        s = sum(np.sin(2 * np.pi * f * (1 + det) * t + rng.uniform(0, 6.28)) for det in (-0.004, 0, 0.0035))
        s += 0.3 * sum(np.sin(2 * np.pi * 2 * f * (1 + det) * t) for det in (-0.002, 0.002))
        return s * env(n, 0.9, 0.5, 0.75, 1.4, length) / 3

    def kick():
        n = int(0.45 * SR)
        t = np.arange(n) / SR
        f = 52 + 70 * np.exp(-t * 28)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)

    def hat(open_=False):
        n = int((0.25 if open_ else 0.06) * SR)
        s = sosfilt(butter(4, 7000, 'hp', fs=SR, output='sos'), rng.standard_normal(n))
        return s * np.exp(-np.arange(n) / SR * (14 if open_ else 60))

    def snare():
        n = int(0.3 * SR)
        t = np.arange(n) / SR
        s = sosfilt(butter(2, [1200, 6000], 'bp', fs=SR, output='sos'), rng.standard_normal(n))
        return 0.6 * s * np.exp(-t * 18) + 0.4 * np.sin(2 * np.pi * 185 * t) * np.exp(-t * 25)

    comp = [(0, 1.0), (1.5, 0.7), (3, 0.8)] if seed % 2 else [(0, 1.0), (2, 0.75), (3.5, 0.6)]
    t = 0.0
    ci = 0
    while t < dur + 1:
        notes, root = prog[ci % 4]
        L = 2 * bar
        for m in notes:
            add(pad_note(midi(m), L), t, 0.05, rng.uniform(-0.5, 0.5))
        for b in range(2):
            for pos, vel in comp:
                tt = t + b * bar + pos * beat + rng.uniform(-0.012, 0.012)
                for j, m in enumerate(notes):
                    add(ep_note(midi(m + 12), beat * 0.9), tt + j * 0.008, 0.055 * vel, -0.25 + j * 0.17)
        for b in range(2):
            for pos, ln in ((0, 1.4), (2.5, 1.0)):
                n = int((ln * beat + 0.3) * SR)
                tt_ = np.arange(n) / SR
                bs = np.sin(2 * np.pi * midi(root) * tt_) * env(n, 0.01, 0.2, 0.7, 0.2, ln * beat)
                add(bs, t + b * bar + pos * beat, 0.16)
        if t >= 2 * bar - 0.01:
            for b in range(2):
                base = t + b * bar
                for pos in (0, 2.5):
                    add(kick(), base + pos * beat, 0.28)
                for pos in (1, 3):
                    add(snare(), base + pos * beat + 0.02, 0.07, 0.1)
                for k8 in range(8):
                    add(hat(k8 == 7), base + k8 * 0.5 * beat + (0.03 if k8 % 2 else 0), 0.035 if k8 % 2 else 0.05, 0.3)
        t += L
        ci += 1

    mix = sosfilt(butter(2, 5200, 'lp', fs=SR, output='sos'), mix, axis=0)
    ir_n = int(1.6 * SR)
    ir = rng.standard_normal((ir_n, 2)) * np.exp(-np.arange(ir_n) / SR * 3.2)[:, None]
    for c in range(2):
        ir[:, c] /= np.abs(ir[:, c]).sum() ** 0.5 * 9
    wet = np.stack([fftconvolve(mix[:, c], ir[:, c])[:N] for c in range(2)], axis=1)
    mix = mix + 0.35 * wet
    mix += (rng.random((N, 1)) < 0.0004) * rng.standard_normal((N, 1)) * 0.06
    mix += sosfilt(butter(2, 3000, 'hp', fs=SR, output='sos'), rng.standard_normal((N, 1)) * 0.004, axis=0)
    mix = mix[: int(dur * SR)]
    fi, fo = int(1.0 * SR), int(2.5 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)[:, None]
    mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
    mix = mix / np.max(np.abs(mix)) * 0.7
    wavfile.write(out, SR, (mix * 32767).astype(np.int16))
    return out


if __name__ == '__main__':
    make(sys.argv[1], float(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    print('wrote', sys.argv[1])
