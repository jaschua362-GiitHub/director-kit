"""Hold the Note posters: text-free plate from the film's own subtitle-free picture + the approved title-v08 art set by hand
(SVG paths from approved/DCL-20261102-NOTE/title-v08, no image-model lettering).
Variant A = the ribbon bridge (shot 8, frame 288). Variant B = the young flautist (shot 9, frame 500, eyes open), Jason's request 6 Nov."""
import pathlib, re, subprocess
LAB = pathlib.Path(__file__).resolve().parents[3]
EXP = LAB / "experiments/TEST-020-hold-the-note"
W = pathlib.Path(__file__).parent / "poster_work"
FF = str(LAB / "experiments/TEST-001/tools/python-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TV = LAB / "approved/DCL-20261102-NOTE/title-v08"
FORMATS = {  # w, h, picture, svg, title viewBox crop
    "H": (1920, 1080, "PICTURE_H.mkv", "landscape.svg", "520 395 880 300"),
    "V": (1080, 1920, "PICTURE_V.mkv", "portrait.svg", "290 590 500 790")}
VARIANTS = {  # frame; per format: title width px, css position of the title box, gradient css
    "A": dict(frame=288, H=dict(tw=820, pos="left:50%;margin-left:-410px;bottom:78px",
                                grad="linear-gradient(to top,rgba(6,12,16,.80) 0%,rgba(6,12,16,.55) 32%,rgba(6,12,16,0) 55%)"),
              V=dict(tw=380, pos="left:50%;margin-left:-190px;bottom:120px",
                     grad="linear-gradient(to top,rgba(6,12,16,.80) 0%,rgba(6,12,16,.55) 40%,rgba(6,12,16,0) 62%)")),
    "B": dict(frame=500, frame_V=466, H=dict(tw=640, pos="right:90px;top:50%;margin-top:-170px",
                                grad="linear-gradient(to left,rgba(6,12,16,.78) 0%,rgba(6,12,16,.50) 40%,rgba(6,12,16,0) 70%)"),
              V=dict(tw=380, pos="left:50%;margin-left:-190px;bottom:110px",
                     grad="linear-gradient(to top,rgba(6,12,16,.82) 0%,rgba(6,12,16,.55) 38%,rgba(6,12,16,0) 62%)")),
}


def title_svg(name, vb):
    s = (TV / name).read_text(encoding="utf-8")
    s = re.sub(r"<defs>.*?</defs>", "", s, flags=re.S)
    s = re.sub(r'<rect width="100%" height="100%"[^>]*/>', "", s)
    return re.sub(r'width="\d+" height="\d+" viewBox="[^"]*"', f'viewBox="{vb}"', s, count=1)


for v, var in VARIANTS.items():
    for k, (w, h, pic, svg, vb) in FORMATS.items():
        cfg = var[k]
        plate = W / f"plate_{v}_{k}.png"
        subprocess.run([FF, "-v", "error", "-y", "-i", str(EXP / "production/p5c_build" / pic), "-vf",
                        "select=eq(n\\," + str(var.get("frame_" + k, var["frame"])) + "),format=rgb24", "-fps_mode", "passthrough", "-frames:v", "1", str(plate)], check=True)
        vbw, vbh = map(float, vb.split()[2:])
        th = cfg["tw"] * vbh / vbw
        html = (f"<!doctype html><meta charset=utf-8><style>html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;background:#000}}"
                f".p{{position:absolute;inset:0;background:url(plate_{v}_{k}.png) center/cover}}.g{{position:absolute;inset:0;background:{cfg['grad']}}}"
                f".t{{position:absolute;{cfg['pos']};width:{cfg['tw']}px;height:{th:.0f}px;filter:drop-shadow(0 2px 10px rgba(0,0,0,.55))}}"
                f".t svg{{width:100%;height:100%}}</style><div class=p></div><div class=g></div><div class=t>{title_svg(svg, vb)}</div>")
        (W / f"poster_{v}_{k}.html").write_text(html, encoding="utf-8")
        out = W / f"poster_{v}_{k}.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}", "--force-device-scale-factor=1",
                        f"--screenshot={out}", (W / f"poster_{v}_{k}.html").as_uri()], check=True, capture_output=True, timeout=120)
        print(v, k, out.stat().st_size)
