"""craft_check: the Lab's gate checks, one subcommand per mechanical lesson.

Run from the Lab root with the Lab's Python:
    python -I -X utf8 tools/craft_check.py <check> [args]
    python -I -X utf8 tools/craft_check.py <check> --help

Every check prints one line per item ("PASS ..." / "FAIL ...") with the measured
number, then a summary line, and exits 0 on pass, 1 on fail, 2 on a usage or
read error. Local and free: OpenCV, numpy and the standard library only. No
paid call, no upload, no ffmpeg (App Control blocks it from agent sessions).
Nothing is written except the contact sheets of `edges`, which go to --out
(default: a temp folder), never beside the input.

What each check measures, its threshold and the film that taught it:
tools/CRAFT_CHECK.md. Tests: python -I -X utf8 tools/craft_check_tests/run_tests.py
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np

try:
    import cv2
except ImportError:  # every video check needs it; the others do not
    cv2 = None

TOOLS = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(TOOLS)


# ---------------------------------------------------------------- shared helpers
class CheckError(Exception):
    """A usage or read problem: exit 2, not a pass or a fail."""


def need_cv2():
    if cv2 is None:
        raise CheckError("OpenCV (cv2) is not importable in this Python")


def open_video(path):
    need_cv2()
    if not os.path.isfile(path):
        raise CheckError("no such file: %s" % path)
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise CheckError("cannot decode: %s" % path)
    return cap


def iter_frames(path):
    cap = open_video(path)
    try:
        while True:
            ok, f = cap.read()
            if not ok:
                break
            yield f
    finally:
        cap.release()


def small_gray(f, width):
    h, w = f.shape[:2]
    hh = max(2, int(round(h * width / w)))
    return cv2.cvtColor(cv2.resize(f, (width, hh), interpolation=cv2.INTER_AREA),
                        cv2.COLOR_BGR2GRAY).astype(np.float32)


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as e:
        raise CheckError("cannot read %s: %s" % (path, e))


def load_edl_shots(path):
    """Lab EDL (roughcut/EDL_*.json): {"fps", "shots": [{"id", "t_in", "frames", ...}]}.
    t_in is the shot's first frame in the cut (no lead-in black); "offset" shifts all."""
    e = load_json(path)
    shots = e.get("shots") if isinstance(e, dict) else e
    if not isinstance(shots, list):
        raise CheckError("%s has no shots list" % path)
    off = int(e.get("offset", 0)) if isinstance(e, dict) else 0
    out = []
    for i, s in enumerate(shots):
        try:
            out.append((str(s.get("id", i + 1)), int(s["t_in"]) + off, int(s["frames"])))
        except (KeyError, TypeError, ValueError):
            raise CheckError("shot %d in %s needs t_in and frames" % (i, path))
    return e if isinstance(e, dict) else {}, out


def parse_window(text):
    m = re.fullmatch(r"\s*(\d+)\s*-\s*(\d+)\s*", text or "")
    if not m or int(m.group(2)) <= int(m.group(1)):
        raise CheckError("window must look like A-B with B > A (source frames [A, B))")
    return int(m.group(1)), int(m.group(2))


def finish(fails, total, what):
    if fails:
        print("RESULT FAIL: %d of %d %s failed" % (fails, total, what))
        return 1
    print("RESULT PASS: %d of %d %s passed" % (total, total, what))
    return 0


# ---------------------------------------------------------------- 1. motion
def frame_diffs(path, width):
    """Mean absolute grey difference (0-255) between consecutive frames at `width` px."""
    prev, d = None, []
    for f in iter_frames(path):
        g = small_gray(f, width)
        if prev is not None:
            d.append(float(np.abs(g - prev).mean()))
        prev = g
    if prev is None:
        raise CheckError("no frames decoded from %s" % path)
    return np.array(d)


def cmd_motion(a):
    d = frame_diffs(a.video, a.width)
    n = len(d) + 1
    if a.edl:
        _, shots = load_edl_shots(a.edl)
    elif a.window:
        s, e = parse_window(a.window)
        shots = [("window %d-%d" % (s, e), s, e - s)]
    else:
        shots = [("whole file", 0, n)]
    fails = 0
    print("motion: %s, %d frames, median frame difference at %d px, threshold %.2f"
          % (os.path.basename(a.video), n, a.width, a.threshold))
    for sid, t0, nf in shots:
        seg = d[t0:t0 + nf - 1]          # differences inside the shot only, never across its cuts
        if t0 + nf > n or len(seg) < 2:
            print("FAIL %-10s frames %d-%d outside the file (%d frames)" % (sid, t0, t0 + nf, n))
            fails += 1
            continue
        med = float(np.median(seg))
        held = int((seg < a.held).sum())
        ok = med >= a.threshold
        fails += not ok
        print("%s %-10s frames %4d-%-4d median %.3f%s%s" % (
            "PASS" if ok else "FAIL", sid, t0, t0 + nf, med,
            "" if ok else "  <- frozen or near-still (under %.2f)" % a.threshold,
            "  (%d repeated frames)" % held if held else ""))
    return finish(fails, len(shots), "shots")


# ---------------------------------------------------------------- 2. anchors
FIRST_KEYS = ("image", "first_image", "first_frame", "start_image", "start_frame", "image_url", "first_frame_image")
LAST_KEYS = ("last_image", "end_image", "last_frame", "end_frame", "tail_image", "image_tail", "last_frame_image")
SAME_NOTE = re.compile(r"first\s+and\s+last|both\s+ends|same\s+(?:image|plate|frame)\s+(?:at|for|as)\s+(?:both|first\s+and\s+last)", re.I)
EMPTY = (None, "", "none", "null", "false")


def split_anchor(v):
    """'plates/fixed/B2-f01.png (note) -> https://...' -> (local path or None, url or None, raw)."""
    if v is None or (isinstance(v, str) and v.strip().lower() in EMPTY) or v is False:
        return None
    if not isinstance(v, str):
        return ("<%s>" % type(v).__name__, None, str(v))
    s = v.strip()
    local, url = s, None
    if "->" in s:
        local, url = [p.strip() for p in s.split("->", 1)]
    elif re.match(r"https?://", s):
        local, url = None, s
    if local is not None:
        local = re.sub(r"\s*\(.*\)\s*$", "", local).strip() or None
    if url:
        url = url.split()[0]
    return (local, url, s)


def resolve_local(p, bases):
    if not p or p.startswith("<"):
        return None
    if os.path.isabs(p) and os.path.isfile(p):
        return p
    for b in bases:
        q = os.path.normpath(os.path.join(b, p))
        if os.path.isfile(q):
            return q
    return None


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pixel_diff(p, q):
    need_cv2()
    a, b = cv2.imread(p), cv2.imread(q)
    if a is None or b is None:
        return None
    a, b = small_gray(a, 320), small_gray(b, 320)
    if a.shape != b.shape:
        b = cv2.resize(b, (a.shape[1], a.shape[0]), interpolation=cv2.INTER_AREA)
    return float(np.abs(a - b).mean())


def find_jobs(o, path=""):
    """Yield (path, dict) for every dict that names a first frame, a last frame or a plate."""
    if isinstance(o, dict):
        if any(k in o for k in FIRST_KEYS + LAST_KEYS + ("plate",)):
            yield path or "<root>", o
        for k, v in o.items():
            if isinstance(v, (dict, list)) and k not in ("params_used",):
                for x in find_jobs(v, (path + "." if path else "") + str(k)):
                    yield x
    elif isinstance(o, list):
        for i, v in enumerate(o):
            for x in find_jobs(v, "%s[%d]" % (path, i)):
                yield x


def judge_anchor_job(job, bases, same_px):
    """Return (ok, text). Fails when first and last are the same image."""
    params = job.get("params") if isinstance(job.get("params"), dict) else job
    first = next((split_anchor(params[k]) for k in FIRST_KEYS if k in params and split_anchor(params[k])), None)
    last = next((split_anchor(params[k]) for k in LAST_KEYS if k in params and split_anchor(params[k])), None)
    notes = " ".join(str(v) for v in list(job.values()) + list(params.values()) if isinstance(v, str))
    if SAME_NOTE.search(notes):
        return False, "record says the same plate was used at both ends: %r" % SAME_NOTE.search(notes).group(0)
    if first is None and last is None and "plate" in job:
        return False, ("UNSURE: names a plate (%s) but not the frame arguments sent; record image and "
                       "last_image (null for none)" % str(job["plate"])[:48])
    if last is None:
        return True, "first frame only"
    if first is None:
        return True, "last frame only (no first frame named)"
    (fl, fu, _), (ll, lu, _) = first, last
    if fu and lu and fu == lu:
        return False, "same upload URL at both ends"
    if fl and ll and os.path.normcase(os.path.normpath(fl)) == os.path.normcase(os.path.normpath(ll)):
        return False, "same file at both ends: %s" % fl
    pf, pl = resolve_local(fl, bases), resolve_local(ll, bases)
    if pf and pl:
        if sha256(pf) == sha256(pl):
            return False, "identical files (SHA-256) at both ends"
        d = pixel_diff(pf, pl)
        if d is not None and d < same_px:
            return False, "first and last differ by only %.2f grey levels at 320 px (under %.1f): the same picture" % (d, same_px)
        return True, "distinct frames, mean difference %.2f at 320 px" % (d if d is not None else -1)
    if fu and lu:
        return True, "distinct upload URLs (local files not found, so compared by URL only)"
    return True, "distinct names (not compared by pixels: files not found)"


def cmd_anchors(a):
    if a.first or a.last:
        jobs = [("command line", {"image": a.first, "last_image": a.last})]
        bases = [os.getcwd(), LAB]
    else:
        if not a.record:
            raise CheckError("give a job record (JSON) or --first/--last")
        rec = load_json(a.record)
        jobs = list(find_jobs(rec))
        if a.job:
            jobs = [j for j in jobs if j[0] == a.job or j[0].endswith("." + a.job)]
        if not jobs:
            raise CheckError("no generation job with a frame argument found in %s%s" % (a.record, " for " + a.job if a.job else ""))
        d = os.path.dirname(os.path.abspath(a.record))
        bases = [d]
        while d and os.path.dirname(d) != d and len(bases) < 6:   # up to the film folder and the Lab root
            d = os.path.dirname(d)
            bases.append(d)
        bases += [os.path.join(b, "plates") for b in bases[:4]] + [os.getcwd(), LAB]
    fails = 0
    print("anchors: first and last frame must not be the same image (first frame only by default)")
    for path, job in jobs:
        ok, text = judge_anchor_job(job, bases, a.same_px)
        fails += not ok
        print("%s %-34s %s" % ("PASS" if ok else "FAIL", path[:34], text))
    return finish(fails, len(jobs), "jobs")


# ---------------------------------------------------------------- 3. edges
def affine_step(g0, g1, mask, orb, bf):
    k0, d0 = orb.detectAndCompute(g0, mask)
    k1, d1 = orb.detectAndCompute(g1, mask)
    if d0 is None or d1 is None:
        return None
    m = bf.match(d0, d1)
    if len(m) < 30:
        return None
    p0 = np.float32([k0[x.queryIdx].pt for x in m])
    p1 = np.float32([k1[x.trainIdx].pt for x in m])
    A, _ = cv2.estimateAffine2D(p0, p1, ransacReprojThreshold=1.0)
    return A


def corner_motion(A, w, h):
    pts = np.float32([[0, 0], [w, 0], [0, h], [w, h], [w / 2, h / 2]])
    return pts @ A[:, :2].T + A[:, 2] - pts


def contact_sheet(frames, idx, out, cols=4):
    rows = (len(frames) + cols - 1) // cols
    h, w = frames[0].shape[:2]
    sheet = np.full((rows * h, cols * w, 3), 16, np.uint8)
    for k, (f, i) in enumerate(zip(frames, idx)):
        r, c = divmod(k, cols)
        tile = f.copy()
        cv2.putText(tile, "f%d" % i, (24, 72), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (0, 0, 0), 9, cv2.LINE_AA)
        cv2.putText(tile, "f%d" % i, (24, 72), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 255), 3, cv2.LINE_AA)
        sheet[r * h:(r + 1) * h, c * w:(c + 1) * w] = tile
    cv2.imwrite(out, sheet, [cv2.IMWRITE_JPEG_QUALITY, 92])


def cmd_edges(a):
    need_cv2()
    frames = list(iter_frames(a.video))
    n = len(frames)
    if n < 2 * a.n + 4:
        raise CheckError("%s has %d frames; need at least %d" % (a.video, n, 2 * a.n + 4))
    h, w = frames[0].shape[:2]
    out = a.out or os.path.join(tempfile.gettempdir(), "craft_check", os.path.splitext(os.path.basename(a.video))[0])
    os.makedirs(out, exist_ok=True)
    head, tail = list(range(a.n)), list(range(n - a.n, n))
    contact_sheet([frames[i] for i in head], head, os.path.join(out, "first%d_100pct.jpg" % a.n))
    contact_sheet([frames[i] for i in tail], tail, os.path.join(out, "last%d_100pct.jpg" % a.n))
    # geometry: ORB + RANSAC affine at 960 px wide, as experiments/TEST-022-small-cargo/finals/scan_geometry.py
    s = 960.0 / w
    hs = int(round(h * s))
    g = {}

    def gray(i):
        if i not in g:
            g[i] = cv2.cvtColor(cv2.resize(frames[i], (960, hs), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        return g[i]
    mask = None
    if a.mask:
        mask = np.zeros((hs, 960), np.uint8)
        for box in a.mask:
            x0, y0, x1, y1 = [float(v) for v in box.split(",")]
            mask[int(y0 * hs):int(y1 * hs), int(x0 * 960):int(x1 * 960)] = 255
    orb, bf = cv2.ORB_create(6000), cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def step(i):
        A = affine_step(gray(i), gray(i + 1), mask, orb, bf)
        if A is None:
            return None, None
        sx, sy = np.hypot(A[0, 0], A[1, 0]), np.hypot(A[0, 1], A[1, 1])
        return corner_motion(A, 960, hs) / s, (sx - 1) * 100, (sy - 1) * 100
    mid = [step(i)[0] for i in range(n // 2 - 6, n // 2 + 6)]
    mid = [m for m in mid if m is not None]
    if not mid:
        raise CheckError("too few features to track the mid-shot (try --mask on the static set)")
    ref = np.median(np.array(mid), axis=0)
    print("edges: %s, %d frames %dx%d; sheets in %s" % (os.path.basename(a.video), n, w, h, out))
    print("mid-shot drift %.2f px/frame (worst corner); a jump is a step's departure from it, threshold %.1f px"
          % (float(np.abs(ref).max()), a.max_jump))
    fails, worst = 0, []
    for label, rng in (("first", range(0, a.n)), ("last", range(n - a.n - 1, n - 1))):
        bad = []
        for i in rng:
            r = step(i)
            if r[0] is None:
                bad.append((i, None, 0, 0))
                continue
            jump = float(np.abs(r[0] - ref).max())
            worst.append(jump)
            if jump > a.max_jump:
                bad.append((i, jump, r[1], r[2]))
        hard = [b for b in bad if b[1] is not None]
        fails += bool(hard)
        if hard:
            print("FAIL %-5s %d frames: jumps %s" % (label, a.n, ", ".join(
                "f%d->f%d %.1f px (scale x %+.2f %%, y %+.2f %%)" % (i, i + 1, j, sx, sy) for i, j, sx, sy in hard)))
        else:
            ws = [x for x in worst]
            print("PASS %-5s %d frames: largest jump %.2f px" % (label, a.n, max(ws) if ws else 0.0))
        lost = [b[0] for b in bad if b[1] is None]
        if lost:
            print("     %s: could not track f%s (no features); check those by eye" % (label, ", f".join(str(i) for i in lost)))
        worst = []
    print("Now look at both sheets at 100 %: hands, props and any snap where the take meets its given frame.")
    return finish(fails, 2, "ends")


# ---------------------------------------------------------------- 4. context
ROW = re.compile(r"^(?P<title>.*?)\s+(?P<main>[\d.]+)\s+(?P<subs>[\d.]+)\s+(?P<fresh>[\d.]+)\s+(?P<replies>\d+)\s+(?P<peak>\d+)(?:\s+<- over 250 K)?\s*$")


def cmd_context(a):
    cmd = [sys.executable, "-I", "-X", "utf8", os.path.join(TOOLS, "token_count.py"), a.film]
    if a.budget:
        cmd += ["--budget", str(a.budget)]
    if a.project:
        cmd += ["--project", a.project]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if p.returncode not in (0, 1) or "Traceback" in p.stderr:
        raise CheckError("token_count.py failed: %s" % (p.stderr.strip() or p.stdout.strip()))
    lines = p.stdout.splitlines()
    if not lines or lines[0].startswith("No sessions"):
        raise CheckError(lines[0] if lines else "token_count.py printed nothing")
    rows, total = [], None
    for ln in lines[1:]:
        if ln.startswith("TOTAL"):
            total = ln
            continue
        m = ROW.match(ln)
        if m:
            rows.append((m.group("title").strip(), int(m.group("peak")), float(m.group("main")) + float(m.group("subs"))))
    if not rows:
        raise CheckError("could not read token_count.py output")
    fails = 0
    print("context: peak context per session for %r, limit %d K (hand off mid-stage at about 250 K)" % (a.film, a.limit))
    for title, peak, used in rows:
        ok = peak <= a.limit
        fails += not ok
        print("%s %-58s peak %4d K  %7.1f M processed%s" % ("PASS" if ok else "FAIL", title[:58], peak, used,
                                                          "" if ok else "  <- over %d K" % a.limit))
    if total:
        print(total)
    return finish(fails, len(rows), "sessions")


# ---------------------------------------------------------------- 5. spend
SPEND_HELP = """\
Ledger format (one file per film, e.g. <film>/SPEND.jsonl; one JSON object per line, oldest first):

  {"date": "2026-11-09 10:00", "kind": "cap",   "usd": 45,   "authorised_by": "lock row 16: 'USD 45 per-film cap'"}
  {"date": "2026-11-11 20:03", "kind": "cap",   "usd": 63.5, "authorised_by": "'Yes, USD 4.50'"}
  {"date": "2026-11-11 20:14", "kind": "spend", "usd": 3.96, "job": "B2_move, B10_move", "gate": "fine cut",
   "go_usd": 4.50, "authorised_by": "'Yes, USD 4.50'", "source": "pilot/results_waveC.json round5"}
  {"date": "2026-11-12 09:00", "kind": "quote", "usd": 2.20, "job": "B10 retake", "gate": "fine cut"}

  kind   cap   = the film's cap from this line on (usd = the new cap, not the raise)
         spend = money gone (usd = charged; use the balance difference when known)
         quote = a job quoted and not yet run; counted against the cap until a spend replaces it
                 (delete or mark "done": true when it runs or is dropped)
  go_usd        the amount his typed yes named; a spend or quote above it fails
  authorised_by his words, quoted; a spend without it fails (no paid job without his typed yes)

Fails when: running total + open quotes + --next is over the cap; any spend has no
authorised_by; any spend or quote is over its go_usd; or spend passed the cap at any
point in the history. Reports the number of cap raises (the lesson: a cap is a cap)."""


def read_ledger(path):
    if not os.path.isfile(path):
        raise CheckError("no such ledger: %s" % path)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    try:
        rows = json.loads(text)
        if isinstance(rows, dict):
            rows = rows.get("entries", [])
    except ValueError:
        rows = []
        for k, ln in enumerate(text.splitlines(), 1):
            if ln.strip() and not ln.lstrip().startswith("//"):
                try:
                    rows.append(json.loads(ln))
                except ValueError as e:
                    raise CheckError("%s line %d is not JSON: %s" % (path, k, e))
    for k, r in enumerate(rows, 1):
        if r.get("kind") not in ("cap", "spend", "quote") or not isinstance(r.get("usd"), (int, float)):
            raise CheckError("%s entry %d needs kind cap/spend/quote and a number usd" % (path, k))
    return rows


def cmd_spend(a):
    rows = read_ledger(a.ledger)
    cap, spent, raises, problems = None, 0.0, [], []
    open_quotes = []
    for k, r in enumerate(rows, 1):
        tag = ("%s %s" % (r.get("date", "entry %d" % k), r.get("job", ""))).strip()
        if r["kind"] == "cap":
            if cap is not None and r["usd"] > cap:
                raises.append((cap, r["usd"], r.get("date", ""), r.get("authorised_by", "")))
            cap = float(r["usd"])
            continue
        go = r.get("go_usd")
        if isinstance(go, (int, float)) and r["usd"] > go + 1e-9:
            problems.append("%s: USD %.2f is over his Go of USD %.2f" % (tag, r["usd"], go))
        if r["kind"] == "quote":
            if not r.get("done"):
                open_quotes.append(r)
            continue
        if not str(r.get("authorised_by", "")).strip():
            problems.append("%s: USD %.2f spent with no typed yes recorded" % (tag, r["usd"]))
        spent += r["usd"]
        if cap is not None and spent > cap + 1e-6:
            problems.append("%s: spend reached USD %.2f against a cap of USD %.2f" % (tag, spent, cap))
    if cap is None:
        raise CheckError("the ledger has no cap line")
    pending = sum(q["usd"] for q in open_quotes)
    nxt = a.next or 0.0
    if a.go is not None and nxt > a.go + 1e-9:
        problems.append("next job USD %.2f is over his Go of USD %.2f" % (nxt, a.go))
    after = spent + pending + nxt
    print("spend: %s" % a.ledger)
    print("     spent USD %.2f of cap USD %.2f; open quotes USD %.2f; next job USD %.2f; after it USD %.2f, headroom USD %.2f"
          % (spent, cap, pending, nxt, after, cap - after))
    print("     cap raises: %d%s" % (len(raises), "".join("\n       %.2f -> %.2f %s %s" % (o, n_, d, ("(" + w + ")") if w else "")
                                                     for o, n_, d, w in raises)))
    fails = 0
    if after > cap + 1e-6:
        fails += 1
        print("FAIL cap: USD %.2f would pass the cap of USD %.2f by USD %.2f. Stop and re-plan the rest of the film with him; do not ask for a small raise."
              % (after, cap, after - cap))
    else:
        print("PASS cap: USD %.2f within USD %.2f" % (after, cap))
    for p in problems:
        fails += 1
        print("FAIL %s" % p)
    return finish(fails, 1 + len(problems), "spend checks")


# ---------------------------------------------------------------- 6. hd
def cmd_hd(a):
    cap = open_video(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    n, w, h = 0, None, None
    for f in iter_frames(a.video):        # decoded count, not the container's claim
        if w is None:
            h, w = f.shape[:2]
        n += 1
    expected = a.frames
    if expected is None and a.edl:
        e = load_json(a.edl)
        expected = e.get("total_frames") if isinstance(e, dict) else None
    fails = 0
    ok_size = (w, h) in ((1920, 1080), (1080, 1920))
    fails += not ok_size
    print("hd: %s" % a.video)
    print("%s size %dx%d%s" % ("PASS" if ok_size else "FAIL", w or 0, h or 0, "" if ok_size else "  <- not 1920x1080 or 1080x1920"))
    checks = 1
    if expected is not None:
        checks += 1
        ok_n = n == int(expected)
        fails += not ok_n
        print("%s frames %d (expected %d) at %.3f fps%s" % ("PASS" if ok_n else "FAIL", n, int(expected), fps,
                                                          "" if ok_n else "  <- %+d frames" % (n - int(expected))))
    else:
        print("     frames %d at %.3f fps (no expected count given: use --frames or --edl)" % (n, fps))
    print("     note: a probe proves size and length only; an upscaled file is also 1920x1080. Faces still need the 100 % look.")
    return finish(fails, checks, "checks")


# ---------------------------------------------------------------- 7. sfx
def read_wav_mono(path):
    if not os.path.isfile(path):
        raise CheckError("no such file: %s" % path)
    try:
        w = wave.open(path)
    except (wave.Error, EOFError) as e:
        raise CheckError("not a PCM WAV (%s): %s" % (e, path))
    with w:
        n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    if sw == 2:
        x = np.frombuffer(raw, np.int16).astype(np.float64) / 32768.0
    elif sw == 4:
        x = np.frombuffer(raw, np.int32).astype(np.float64) / 2147483648.0
    elif sw == 3:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 3)
        x = ((b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16)) << 8 >> 8) / 8388608.0
    else:
        raise CheckError("unsupported sample width %d in %s" % (sw, path))
    return x.reshape(-1, ch).mean(axis=1), sr


def onset_near(env, db, c, reach, rise_db=9.0):
    """Nearest attack to sample-ms c within +-reach ms. An attack is a rise of rise_db over the
    previous 15 ms; its time is the first point within 12 dB of the peak that follows (60 ms)."""
    lo, hi = max(1, c - reach), min(len(env) - 61, c + reach)
    if hi <= lo:
        return None
    floor = 0.1 * env[lo:hi + 60].max()   # ignore rises more than 20 dB under the loudest event nearby (pre-roll, hiss)
    best, i = None, lo
    while i < hi:
        if db[i] - db[max(0, i - 15):i].min() >= rise_db:
            pk = i + int(np.argmax(env[i:i + 60]))
            if env[pk] < floor:
                i = pk + 1
                continue
            thr, j = env[pk] * 0.25, pk
            while j > max(0, i - 15) and env[j - 1] >= thr:
                j -= 1
            if best is None or abs(j - c) < abs(best - c):
                best = j
            i = pk + 1                   # one onset per rise
        else:
            i += 1
    return best


def load_cues(path, edl_path):
    """Lab cue sheet ({"cues": [[shot, local_frame, sound, gain, why], ...]} with --edl), or
    a plain list of {"t": seconds} / {"frame": absolute frame} objects, with "fps" at the top."""
    c = load_json(path)
    cues = c.get("cues") if isinstance(c, dict) else c
    if not isinstance(cues, list) or not cues:
        raise CheckError("%s has no cues" % path)
    fps = float(c.get("fps", 24)) if isinstance(c, dict) else 24.0
    out = []
    if isinstance(cues[0], list):
        if not edl_path:
            raise CheckError("a shot-local cue sheet needs --edl to place its cues")
        e, shots = load_edl_shots(edl_path)
        fps = float(e.get("fps", fps))
        t_in = {sid: t0 for sid, t0, _ in shots}
        for q in cues:
            if q[0] not in t_in:
                raise CheckError("cue on shot %s, which is not in %s" % (q[0], edl_path))
            out.append(("%s %s f%s" % (q[0], q[2] if len(q) > 2 else "", q[1]), t_in[q[0]] + float(q[1])))
    else:
        for k, q in enumerate(cues):
            if "frame" in q:
                f = float(q["frame"])
            elif "t" in q:
                f = float(q["t"]) * fps
            else:
                raise CheckError("cue %d needs t or frame" % k)
            out.append((str(q.get("name", "cue %d" % (k + 1))), f))
    return out, fps


def cmd_sfx(a):
    x, sr = read_wav_mono(a.stem)
    cues, fps = load_cues(a.cues, a.edl)
    hop, w = sr // 1000, max(1, int(0.003 * sr))
    env = np.sqrt(np.convolve(x * x, np.ones(w) / w, "same"))[::hop]   # 3 ms RMS on a 1 ms grid
    db = 20 * np.log10(env + 1e-7)
    reach = int(round(a.search / fps * 1000))
    dur = len(x) / sr
    print("sfx: %s, %.3f s (%.1f frames at %g fps); %d cues; tolerance %d frames"
          % (os.path.basename(a.stem), dur, dur * fps, fps, len(cues), a.tolerance))
    fails = 0
    for name, f in cues:
        c = int(round(f / fps * 1000))
        o = onset_near(env, db, c, reach) if c < len(env) else None
        if o is None:
            fails += 1
            print("FAIL %-28s at frame %7.1f: no onset within %d frames" % (name[:28], f, a.search))
            continue
        off = (o - c) / 1000.0 * fps
        ok = abs(off) <= a.tolerance
        fails += not ok
        print("%s %-28s at frame %7.1f: onset %+5.1f frames%s" % ("PASS" if ok else "FAIL", name[:28], f, off,
                                                                 "" if ok else "  <- %s" % ("late" if off > 0 else "early")))
    return finish(fails, len(cues), "cues")


# ---------------------------------------------------------------- command line
def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="craft_check.py",
        description="The Lab's gate checks: each prints PASS/FAIL with the measured number; exit 1 on any fail. "
                    "Details, thresholds and the films that taught them are in the Lab's CRAFT_CHECK.md (not in the kit). "
                    "The proposed spend ledger format for future films: craft_check.py spend --help.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="check", metavar="CHECK")

    p = sub.add_parser("motion", help="per-shot motion scan: median frame difference at 320 px under 0.1 is frozen or near-still",
                       description="Median of the mean grey difference between consecutive frames, per shot, at 320 px wide. "
                                   "Under 0.1 is frozen or near-still (House of Courtesy v4: B2 0.009, B10 0.022; final shots 0.16 and up).")
    p.add_argument("video")
    p.add_argument("--edl", help="Lab EDL JSON (shots with t_in and frames): scan each shot of a cut")
    p.add_argument("--window", help="source frames A-B of a take, as used in the cut")
    p.add_argument("--threshold", type=float, default=0.1)
    p.add_argument("--width", type=int, default=320)
    p.add_argument("--held", type=float, default=0.02, help="a difference under this counts as a repeated frame (reported, not failed)")
    p.set_defaults(fn=cmd_motion)

    p = sub.add_parser("anchors", help="generation job arguments: fail when the first and last frame are the same image",
                       description="Reads a job record (any Lab results/quote JSON) or --first/--last. Fails when both ends name the "
                                   "same URL or file, identical files, pixels within --same-px, or a note says 'first and last'.")
    p.add_argument("record", nargs="?", help="JSON with jobs (image/last_image, first_frame, end_image, plate ...)")
    p.add_argument("--job", help="only this job (its key, e.g. B2_live or round4.jobs.B2_live)")
    p.add_argument("--first", help="first-frame argument (path or URL)")
    p.add_argument("--last", help="last-frame argument (path or URL)")
    p.add_argument("--same-px", type=float, default=1.0, help="mean grey difference at 320 px under which two files are the same picture")
    p.set_defaults(fn=cmd_anchors)

    p = sub.add_parser("edges", help="first and last 12 frames at 100 %% as contact sheets, plus geometry jumps (edge snaps)",
                       description="Writes two contact sheets at 100 %% for the hand-prop and snap check, and measures each "
                                   "frame-to-frame affine step (ORB + RANSAC) in the first and last frames against the mid-shot drift.")
    p.add_argument("video")
    p.add_argument("--out", help="folder for the sheets (default: a temp folder; never beside the take)")
    p.add_argument("--n", type=int, default=12)
    p.add_argument("--max-jump", type=float, default=2.0, help="px at full size; default 2.0 whole-frame, 0.5 with --mask on the static set")
    p.add_argument("--mask", action="append", help="static-set box as x0,y0,x1,y1 fractions; repeatable")
    p.set_defaults(fn=cmd_edges)

    p = sub.add_parser("context", help="peak context per session for a film (tools/token_count.py); fail any over 250 K")
    p.add_argument("film", help="text in the session titles, e.g. 'House of Courtesy'")
    p.add_argument("--limit", type=int, default=250, help="K tokens")
    p.add_argument("--budget", type=float, help="film token budget in M, passed to token_count.py")
    p.add_argument("--project", help="transcript folder (default ~/.claude/projects/F--Design-Project-Daily-Cinematic-Lab)")
    p.set_defaults(fn=cmd_context)

    p = sub.add_parser("spend", help="running total against the cap from the film's spend ledger; fail if the next job passes it",
                       description="Reads the film's spend ledger and reports the running total against the cap.",
                       epilog=SPEND_HELP, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ledger")
    p.add_argument("--next", type=float, help="the job about to run, USD (its live quote)")
    p.add_argument("--go", type=float, help="the amount his typed yes named for that job, USD")
    p.set_defaults(fn=cmd_spend)

    p = sub.add_parser("hd", help="fail unless native 1920x1080 (or 1080x1920) with the expected frame count")
    p.add_argument("video")
    p.add_argument("--frames", type=int, help="expected decoded frame count")
    p.add_argument("--edl", help="Lab EDL JSON: expected count = its total_frames")
    p.set_defaults(fn=cmd_hd)

    p = sub.add_parser("sfx", help="effects-stem onsets against the cue sheet; fail beyond 3 frames",
                       description="Finds each cue's attack in an effects-only WAV stem (3 ms RMS, a 9 dB rise, timed at the first "
                                   "point within 12 dB of the peak) and reports its offset in frames.")
    p.add_argument("stem", help="effects-only WAV of the cut")
    p.add_argument("cues", help="cue sheet JSON (Lab shot-local sheet with --edl, or [{t|frame}])")
    p.add_argument("--edl", help="Lab EDL JSON for a shot-local cue sheet")
    p.add_argument("--tolerance", type=int, default=3, help="frames")
    p.add_argument("--search", type=int, default=12, help="frames either side of each cue to look for its onset")
    p.set_defaults(fn=cmd_sfx)

    a = ap.parse_args(argv)
    if not getattr(a, "fn", None):
        ap.print_help()
        return 2
    try:
        return a.fn(a)
    except CheckError as e:
        print("ERROR %s" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
