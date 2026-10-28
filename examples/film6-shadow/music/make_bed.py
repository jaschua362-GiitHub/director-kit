"""Cut a full-length score into the v02 bed: intro + drop timed to the run, dead stop at the decoy turn, then the
track's own ending under the recognition scene.

Usage: python make_bed.py A   |   python make_bed.py B
"""
import pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from assemble_v02 import EDL, FF

HERE = pathlib.Path(__file__).resolve().parent
# drop = loud entry measured in the RMS curve (s); tail = start of the closing section (s); src length (s)
SCORES = {"A": ("score_A_cyberpunk_taiko.mp3", 16.0, 170.5, 189.0),
          "B": ("score_B_darksynth.mp3", 15.0, 139.5, 158.0),
          "C": ("score_C_japanese_fusion.mp3", 9.0, 168.5, 187.0),
          "D": ("score_D_ninja_digital.mp3", 18.0, 203.0, 222.0)}
GAP = 1.2   # near-silence at the decoy reveal (one glitch tone added later in the SFX pass)


def main():
    key = sys.argv[1]
    src, drop, tail, length = SCORES[key]
    t, starts = 0.0, []
    for row in EDL:
        starts.append(t); t += row[2] - row[1]
    run = starts[6]                                   # Aiko springs off: second T04 segment
    turn = starts[[r[0] for r in EDL].index("T19")]   # decoy appears
    off = drop - run
    rest = t - turn - GAP
    out = HERE / f"bed_{key}.wav"
    fc = (f"[0:a]atrim={off:.2f}:{off + turn:.2f},asetpts=PTS-STARTPTS,afade=t=out:st={turn - 0.08:.2f}:d=0.08[a];"
          f"anullsrc=r=44100:cl=stereo,atrim=0:{GAP}[g];"
          f"[0:a]atrim={max(tail, length - rest):.2f}:{length:.2f},asetpts=PTS-STARTPTS,afade=t=in:d=0.4[c];"
          f"[a][g][c]concat=n=3:v=0:a=1[o]")
    subprocess.run([str(FF), "-loglevel", "error", "-y", "-i", str(HERE / src), "-filter_complex", fc, "-map", "[o]",
                    "-ar", "48000", str(out)], check=True)
    print(out.name, f"drop at {run:.1f}s, cut at {turn:.1f}s, total {t:.1f}s")


if __name__ == "__main__":
    main()
