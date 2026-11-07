"""Count Claude Code tokens per session for a film, at any gate.

Usage (from your project root):
    python -I tools/token_count.py "Hold the Note"
    python -I tools/token_count.py "Hold the Note" --budget 150
    python -I tools/token_count.py "Hold the Note" --project-dir "C:\\path\\to\\project"

Matches sessions whose saved title contains the text (case-insensitive), from
~/.claude/projects/<project folder>/<session>/custom-title.json. Claude Code names the
project folder after the project path with every non-alphanumeric character replaced by
"-" (for example "F:\\Films\\My Lab" becomes "F--Films-My-Lab"); the script derives that
from the current directory, or from --project-dir. Subagent transcripts
(<session>/subagents/*.jsonl) are included. Each assistant message is counted once by
message id. Session titles must contain the film name for the match to work.

Processed = input + cache writes + cache reads + output: what each reply reads,
which is what drains the allowance. Fresh = input + cache writes + output.
Read-only: it never writes anything.

Prints one line per session, then the film total. Paste the total line into
each gate message: "Tokens: this phase X M, film so far Y M (budget Z M)".
Sessions whose peak context passed 250 K are flagged; that is the point at which
the Lab hands off to a fresh session.
"""
import argparse
import glob
import json
import os
import re
import sys


def project_folder(project_dir):
    name = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(project_dir))
    return os.path.join(os.path.expanduser("~"), ".claude", "projects", name)


def count(paths):
    seen, proc, fresh, replies, peak = set(), 0, 0, 0, 0
    for p in paths:
        try:
            fh = open(p, encoding="utf-8")
        except OSError:
            continue
        with fh:
            for line in fh:
                try:
                    o = json.loads(line)
                except ValueError:
                    continue
                if o.get("type") != "assistant":
                    continue
                m = o.get("message") or {}
                mid, u = m.get("id"), m.get("usage")
                if not mid or not u or mid in seen:
                    continue
                seen.add(mid)
                i = u.get("input_tokens", 0)
                cw = u.get("cache_creation_input_tokens", 0)
                cr = u.get("cache_read_input_tokens", 0)
                out = u.get("output_tokens", 0)
                proc += i + cw + cr + out
                fresh += i + cw + out
                replies += 1
                peak = max(peak, i + cw + cr)
    return proc, fresh, replies, peak


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("match", help="text in the session titles, e.g. the film name")
    ap.add_argument("--budget", type=float, help="film budget in M tokens")
    ap.add_argument("--project-dir", default=os.getcwd(),
                    help="the project folder Claude Code was opened in (default: current directory)")
    a = ap.parse_args()
    project = project_folder(a.project_dir)
    if not os.path.isdir(project):
        print("No Claude Code project folder at %s" % project)
        return 1

    rows = []
    for tf in glob.glob(os.path.join(project, "*", "custom-title.json")):
        try:
            title = json.load(open(tf, encoding="utf-8")).get("customTitle", "")
        except (OSError, ValueError):
            continue
        if a.match.lower() not in title.lower():
            continue
        sid = os.path.basename(os.path.dirname(tf))
        main_t = os.path.join(project, sid + ".jsonl")
        subs = glob.glob(os.path.join(project, sid, "subagents", "*.jsonl"))
        mp, mf, mr, mpk = count([main_t])
        sp, sf, sr, _ = count(subs)
        mtime = os.path.getmtime(main_t) if os.path.exists(main_t) else 0
        rows.append((mtime, title, mp, sp, mf + sf, mr, sr, mpk))

    if not rows:
        print("No sessions with a title containing %r." % a.match)
        return 1
    rows.sort()
    out = sys.stdout
    out.write("%-58s %9s %9s %8s %7s %9s\n" % ("session", "main M", "subs M", "fresh M", "replies", "peak ctx K"))
    total = 0
    for _, title, mp, sp, fr, mr, sr, pk in rows:
        total += mp + sp
        flag = "  <- over 250 K" if pk > 250_000 else ""
        out.write("%-58s %9.1f %9.1f %8.1f %7d %9.0f%s\n" % (
            title[:58], mp / 1e6, sp / 1e6, fr / 1e6, mr + sr, pk / 1e3, flag))
    line = "TOTAL %s: %.1f M processed over %d sessions" % (a.match, total / 1e6, len(rows))
    if a.budget:
        line += " (budget %.0f M, %.1fx)" % (a.budget, total / 1e6 / a.budget)
    out.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
