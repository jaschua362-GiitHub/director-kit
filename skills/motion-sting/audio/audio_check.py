"""Verify a sting's audio without listening: loudness, loudness-over-time, band balance, spectrogram.

    python audio_check.py sfx.wav [--sections 0:2.2:seed 2.6:4:roast 4:5.3:flight 5.3:6.5:cup 6.5:10:logo]

Prints integrated LUFS + true peak (ffmpeg ebur128), an RMS bar per 250 ms (does the energy follow the
story?), and per-section energy in <60 / 60–250 / 250–2k / 2k+ Hz (is the low end swamping it?).
Writes <wav>_spectrogram.png — read it to confirm each cue lands on its beat.

Targets: −14 to −16 LUFS integrated for social; peak ≤ −1 dBFS; in dense sections keep <60 Hz below
about −12 dB relative, or it booms on headphones and vanishes on phones.
"""
import argparse, re, subprocess, wave
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('wav')
ap.add_argument('--sections', nargs='*', default=[], help='start:end:name')
a = ap.parse_args()

r = subprocess.run(['ffmpeg', '-hide_banner', '-i', a.wav, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                   capture_output=True, text=True).stderr
summ = r[r.rfind('Summary'):]
I = re.search(r'I:\s+(-?[\d.]+) LUFS', summ); P = re.search(r'Peak:\s+(-?[\d.]+) dBFS', summ)
print(f'Integrated {I.group(1) if I else "?"} LUFS   true peak {P.group(1) if P else "?"} dBFS')

w = wave.open(a.wav); sr, n, sw = w.getframerate(), w.getnframes(), w.getsampwidth()
raw = np.frombuffer(w.readframes(n), np.uint8)
if sw == 3:
    b = raw.reshape(-1, w.getnchannels(), 3).astype(np.int32)
    x = b[..., 0] | (b[..., 1] << 8) | (b[..., 2] << 16); x = np.where(x >= 2 ** 23, x - 2 ** 24, x) / 2 ** 23
else:
    x = np.frombuffer(raw.tobytes(), np.int16).reshape(-1, w.getnchannels()) / 32768
m = x.mean(1)

print('\nRMS per 250 ms')
for s in np.arange(0, n / sr, .25):
    seg = m[int(s * sr):int((s + .25) * sr)]
    db = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9)
    print(f'{s:5.2f}s {db:6.1f} dB ' + '#' * int(max(0, (60 + db) / 1.5)))

if a.sections:
    print('\nsection        <60  60-250  250-2k    2k+   (dB rel. section total)')
    for spec in a.sections:
        s0, s1, name = spec.split(':')
        seg = m[int(float(s0) * sr):int(float(s1) * sr)]
        S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2; f = np.fft.rfftfreq(len(seg), 1 / sr); tot = S.sum()
        print(f'{name:<12}' + ''.join(f'{10 * np.log10(S[(f >= lo) & (f < hi)].sum() / tot + 1e-12):8.1f}'
                                      for lo, hi in ((20, 60), (60, 250), (250, 2000), (2000, 20000))))

out = a.wav.rsplit('.', 1)[0] + '_spectrogram.png'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', a.wav, '-lavfi',
                'showspectrumpic=s=2000x500:legend=1:scale=log:fscale=log:color=intensity,format=rgb24', out])
print(f'\nspectrogram -> {out}')
