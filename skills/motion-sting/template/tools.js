// Review tools — run from the browser pane's javascript tool on  http://localhost:PORT/?t=0  (or ?fmt=9x16&t=0).
// Everything lands in <project>/stills/<name>.png; read it back with the Read tool.
//   await TOOLS.sheet([1.2, 2.5, 3.5, 4.8, 6.1, 9.99], 'beats')   contact sheet of key beats (+ centre cross)
//   await TOOLS.still(3.5, 'crack')                               one full-resolution frame
//   await TOOLS.still(3.5, 'crack_mb', {sub: 8})                  same frame with export motion blur (judge smear)
//   TOOLS.measure(9.99)                                           final-logo centring: bbox margins + visual-weight offset
(() => {
  const cv = () => document.getElementById('c');
  const post = async (canvas, name) => {
    const b = await new Promise(r => canvas.toBlob(r, 'image/png'));
    const r = await fetch('/frame?i=' + encodeURIComponent(name), { method: 'POST', body: b });
    return r.text();
  };
  window.TOOLS = {
    async still(t, name, opts = {}) {
      await document.fonts.ready;
      if (window.beforeRender) await window.beforeRender(t);   // e.g. decode footage frames
      if (opts.sub > 1 && window.renderMB) renderMB(Math.round(t * FPS), opts.sub, opts.shutter ?? .5); else renderAt(t);
      return post(cv(), name || `still_${String(t).replace('.', '_')}`);
    },
    async sheet(times, name = 'sheet', opts = {}) {
      await document.fonts.ready;
      const c = cv(), portrait = c.height > c.width;
      const cols = Math.min(times.length, opts.cols || (portrait ? 8 : 4)), cw = opts.cellW || (portrait ? 270 : 480);
      const ch = Math.round(cw * c.height / c.width), rows = Math.ceil(times.length / cols);
      const sh = document.createElement('canvas'); sh.width = cols * cw; sh.height = rows * ch;
      const x = sh.getContext('2d');
      for (const [i, t] of times.entries()) {
        if (window.beforeRender) await window.beforeRender(t);
        renderAt(t);
        const ox = (i % cols) * cw, oy = Math.floor(i / cols) * ch;
        x.drawImage(c, ox, oy, cw, ch);
        if (opts.cross) {
          x.strokeStyle = 'rgba(255,0,255,.45)'; x.beginPath();
          x.moveTo(ox + cw / 2, oy); x.lineTo(ox + cw / 2, oy + ch); x.moveTo(ox, oy + ch / 2); x.lineTo(ox + cw, oy + ch / 2); x.stroke();
        }
        x.fillStyle = '#f0f'; x.font = '20px sans-serif'; x.fillText(t.toFixed(2), ox + 6, oy + 22);
      }
      return post(sh, name);
    },
    // ink = pixels that are dark (sum < 560) or saturated-yellow; tune isInk for other palettes
    measure(t, isInk = (r, g, b) => r + g + b < 560 || (b < 120 && r > 150)) {
      renderAt(t);
      const c = cv(), W = c.width, H = c.height, d = c.getContext('2d').getImageData(0, 0, W, H).data;
      let x0 = W, x1 = 0, y0 = H, y1 = 0, sx = 0, sy = 0, n = 0;
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
        const i = (y * W + x) * 4;
        if (isInk(d[i], d[i + 1], d[i + 2])) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); sx += x; sy += y; n++; }
      }
      return { W, H, margins: { left: x0, right: W - 1 - x1, top: y0, bottom: H - 1 - y1 },
        bboxOffset: [(x0 + x1) / 2 - W / 2, (y0 + y1) / 2 - H / 2].map(v => +v.toFixed(1)),
        weightOffset: [sx / n - W / 2, sy / n - H / 2].map(v => +v.toFixed(1)) };
    },
  };
})();
