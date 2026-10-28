"""Scaffold a new motion-sting project from the skill template.

    python new_project.py --dest "<PROJECTS>/<Brand>/Motion/<project-name>" [--launch <workspace>/.claude/launch.json]

Creates:  index.html  sting.js (reference engine to adapt)  tools.js  server.js  glyphs.js (placeholder)
          src/  stills/  audio/sfxlib.py  audio/cues.py (copy of the worked example)  BRIEF.md
and adds a preview entry "<project-name>" to the Claude launch.json so preview_start can open it.
Name the folder for the idea, not the duration (durations change: "logo-sting-8s" ended up 10 s).
"""
import argparse, json, os, shutil, socket

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--dest', required=True)
ap.add_argument('--launch', default=r'<workspace>/.claude/launch.json')
a = ap.parse_args()
dest = os.path.abspath(a.dest)
if os.path.exists(dest) and os.listdir(dest):
    raise SystemExit(f'{dest} exists and is not empty - pick a new folder.')
os.makedirs(dest, exist_ok=True)
for f in ('index.html', 'sting.js', 'tools.js', 'server.js'):
    shutil.copy2(os.path.join(SKILL, 'template', f), dest)
open(os.path.join(dest, 'glyphs.js'), 'w').write('window.GLYPHS=[];  // run scripts/trace_logo.py to fill\n')
for d in ('src', 'stills', 'audio'):
    os.makedirs(os.path.join(dest, d), exist_ok=True)
shutil.copy2(os.path.join(SKILL, 'audio', 'sfxlib.py'), os.path.join(dest, 'audio'))
shutil.copy2(os.path.join(SKILL, 'audio', 'cues_example.py'), os.path.join(dest, 'audio', 'cues.py'))
open(os.path.join(dest, 'BRIEF.md'), 'w', encoding='utf-8').write(
    '# Brief\n\n- Brand / logo source:\n- Reference (link) and what we borrow from it:\n- Story beats (symbols):\n'
    '- Formats: 16:9 1920x1080 + 9:16 1080x1920\n- Duration: story + 2 s logo hold\n- Sound: yes\n- Palette source file:\n'
    '\n# Timeline (mirror of T in sting.js)\n\n| t | beat | sound cue |\n|---|---|---|\n')

name = os.path.basename(dest.rstrip('\\/')).replace(' ', '-').lower()
if os.path.exists(a.launch):
    cfg = json.load(open(a.launch, encoding='utf-8'))
    used = {c.get('port') for c in cfg.get('configurations', [])}
    port = next(p for p in range(8770, 8900) if p not in used)
    cfg['configurations'] = [c for c in cfg['configurations'] if c.get('name') != name] + [
        {'name': name, 'runtimeExecutable': 'node', 'runtimeArgs': [os.path.join(dest, 'server.js').replace('\\', '/'), str(port)], 'port': port}]
    json.dump(cfg, open(a.launch, 'w', encoding='utf-8'), indent=2)
    print(f'launch.json: added "{name}" on port {port}')
print(f'project ready: {dest}')
