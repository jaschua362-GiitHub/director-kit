"""Mix a supplied music track with the synthesised SFX and master to -14 LUFS / -1.5 dBTP.

    python mix.py audio/track.wav audio/sfx.wav audio/mix.wav [--sfx-db -4] [--lufs -14] [--peak -1.5]

Why not single-pass loudnorm: on 10-30 s files it stays in dynamic mode and misses the target by
several LU (measured -17.2 for a -14 request). This measures, applies one gain, then a true-peak
limiter, then re-measures and prints the result. Output: 48 kHz stereo 24-bit WAV.
"""
import argparse, re, subprocess, sys


def ff(args):
    r = subprocess.run(['ffmpeg', '-y', '-v', 'error'] + args, capture_output=True, text=True)
    if r.returncode: sys.exit('ffmpeg failed:\n' + r.stderr)


def measure(path):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind('Summary:'):]
    i = float(re.search(r'I:\s*(-?[\d.]+)', tail)[1])
    p = re.search(r'Peak:\s*(-?[\d.]+|-inf)', tail)[1]
    return i, float(p) if p != '-inf' else -99.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('music'); ap.add_argument('sfx'); ap.add_argument('out')
    ap.add_argument('--sfx-db', type=float, default=-4, help='SFX level relative to the music')
    ap.add_argument('--lufs', type=float, default=-14)
    ap.add_argument('--peak', type=float, default=-1.5)
    a = ap.parse_args()
    tmp = a.out + '.premix.wav'
    ff(['-i', a.music, '-i', a.sfx, '-filter_complex',
        f'[0:a]aformat=channel_layouts=stereo[m];[1:a]aformat=channel_layouts=stereo,volume={a.sfx_db}dB[s];'
        '[m][s]amix=inputs=2:normalize=0:duration=longest',
        '-ar', '48000', '-c:a', 'pcm_f32le', tmp])
    i0, _ = measure(tmp)
    gain = a.lufs - i0
    lim = 10 ** ((a.peak - .3) / 20)          # 0.3 dB margin: resampling back to 48 kHz adds inter-sample peaks
    for _ in range(2):                        # 2nd pass makes up the loudness the limiter shaved off
        ff(['-i', tmp, '-af', f'volume={gain:.2f}dB,aresample=192000,alimiter=limit={lim:.4f}:level=disabled:attack=1:release=50,'
            'aresample=48000', '-c:a', 'pcm_s24le', a.out])
        i1, p1 = measure(a.out)
        if abs(a.lufs - i1) < .2: break
        gain += a.lufs - i1
    import os; os.remove(tmp)
    print(f'[mix] premix {i0:.1f} LUFS, gain {gain:+.1f} dB -> {i1:.1f} LUFS, true peak {p1:.1f} dBFS  ({a.out})')


if __name__ == '__main__':
    main()
