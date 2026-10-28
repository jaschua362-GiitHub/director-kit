"""Build RUN_MANUALLY.md (Route A sheet) from a pack's JOBS.json.
Usage: python tools/make_manual_sheet.py "bible/pack-a"   (run from the series root)
"""
import json, os, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pack = os.path.join(root, sys.argv[1])
jobs = json.load(open(os.path.join(pack, "JOBS.json"), encoding="utf-8"))
name = os.path.basename(pack.rstrip("/\\"))

out = [f"# Route A sheet: {name}", "",
       "For each job: **new ChatGPT chat → attach the listed images → paste the prompt below → generate → save under the exact name into this pack's `returns/` folder.**",
       "Jobs marked ✅ already have a saved image. Skip them.", ""]
for j in jobs:
    done = os.path.exists(os.path.join(pack, j["out"]))
    prompt = open(os.path.join(pack, j["prompt"]), encoding="utf-8").read().strip()
    out += [f"## {'✅ ' if done else ''}{j['id']}", "",
            f"- **Attach (in this order):** " + ", ".join(f"`{os.path.basename(r)}` (in `{os.path.dirname(r)}`)" for r in j.get("refs", [])) if j.get("refs") else "- **Attach:** nothing",
            f"- **Aspect:** {j['aspect']}",
            (f"- **Run after:** {j['after']}" if j.get("after") else ""),
            f"- **Save as:** `{j['out']}`", "", "```", prompt, "```", ""]
open(os.path.join(pack, "RUN_MANUALLY.md"), "w", encoding="utf-8").write("\n".join(out))
print(f"wrote {name}/RUN_MANUALLY.md with {len(jobs)} jobs")
