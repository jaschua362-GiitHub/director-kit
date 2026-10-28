/* Coffee brand — 10s logo sting (v5: 8s of story + 2s logo hold; critic round-1 fixes).
   Narrative: seed → wireframe bean → roast graph (BT / ET / RoR, green → brown, first crack)
   → the three roast lines lift off, braid toward camera in 3D and wrap into the cup's rings
   → latte-art pour draws the yellow leaf-halves → cup becomes the "O" while the wordmark builds and settles.
   render(t) is a pure function of time so frames can be exported deterministically. */
(() => {
  // ?fmt=9x16 → vertical 1080×1920 cut. The world stays in 1920×1080 design space; only the camera + backgrounds change.
  const PORTRAIT = new URLSearchParams(location.search).get('fmt') === '9x16';
  const W = PORTRAIT ? 1080 : 1920, H = PORTRAIT ? 1920 : 1080, DUR = 10, FPS = 60;
  const cv = document.getElementById('c');
  if (PORTRAIT) {
    cv.width = W; cv.height = H;
    const wcss = 'min(100%, calc((100vh - 80px) * 9 / 16))';
    cv.style.aspectRatio = '9 / 16'; cv.style.width = wcss;
    const tr = document.querySelector('.track'); if (tr) tr.style.width = wcss;
  }
  let ctx = cv.getContext('2d');      // `let`: lightLayer() briefly points the drawing helpers at an offscreen layer

  // ---------- palette (from the logo + July menu template; no black) ----------
  const C = {
    brown: '#6C3715', caramel: '#B37544', yellow: '#FEDA00', olive: '#A9A937',
    oliveDeep: '#6E7228', cream: '#FBF6EA', espTop: '#28180E', espBot: '#170E08',
  };
  const LINE = [251, 246, 234];

  // ---------- helpers ----------
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const lerp3 = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
  const seg = (t, a, b) => clamp((t - a) / (b - a));
  const E = {
    inOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    inOutSine: x => -(Math.cos(Math.PI * x) - 1) / 2,
    out: x => 1 - Math.pow(1 - x, 3),
    in: x => x * x * x,
    outQuint: x => 1 - Math.pow(1 - x, 5),
    outExpo: x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x),
    smoother: x => x * x * x * (x * (6 * x - 15) + 10),   // zero velocity + acceleration at both ends
    outBack: (x, s = 1.6) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2),
  };
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const mix = (a, b, t) => a.map((v, i) => Math.round(lerp(v, b[i], t)));
  const rgba = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  const TAU = Math.PI * 2;
  function ramp(stops, p) {
    for (let i = 1; i < stops.length; i++) {
      if (p <= stops[i][0]) {
        const [p0, c0] = stops[i - 1], [p1, c1] = stops[i];
        return mix(hex(c0), hex(c1), clamp((p - p0) / (p1 - p0)));
      }
    }
    return hex(stops[stops.length - 1][1]);
  }
  function rng(seed) { // mulberry32
    return () => {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  const bez = (p, u) => {
    const v = 1 - u;
    return [0, 1].map(k => v * v * v * p[0][k] + 3 * v * v * u * p[1][k] + 3 * v * u * u * p[2][k] + u * u * u * p[3][k]);
  };

  // ---------- grain ----------
  const grains = [];
  { const r = rng(7);
    for (let n = 0; n < 6; n++) {
      const g = document.createElement('canvas'); g.width = g.height = 320;
      const x = g.getContext('2d'), id = x.createImageData(320, 320);
      for (let i = 0; i < id.data.length; i += 4) {
        const v = 128 + (r() + r() + r() - 1.5) * 150;
        id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255;
      }
      x.putImageData(id, 0, 0); grains.push(g);
    }
  }
  function grain(f, alpha) {
    ctx.save();
    ctx.globalAlpha = alpha; ctx.globalCompositeOperation = 'overlay';
    ctx.fillStyle = ctx.createPattern(grains[f % grains.length], 'repeat');
    ctx.translate((f * 37) % 320, (f * 91) % 320);
    ctx.fillRect(-320, -320, W + 640, H + 640);
    ctx.restore();
  }

  function blob(x, y, r, c, a) {
    const g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, rgba(c, a)); g.addColorStop(.45, rgba(c, a * .5));
    g.addColorStop(1, rgba(c, 0));
    ctx.fillStyle = g; ctx.fillRect(x - r, y - r, 2 * r, 2 * r);
  }
  function glowDot(x, y, s, col, a = 1) {
    if (a <= 0) return;
    blob(x, y, 70 * s, col, .45 * a);
    blob(x, y, 22 * s, hex(C.yellow), .85 * a);
    ctx.fillStyle = rgba([255, 252, 238], a);
    ctx.beginPath(); ctx.arc(x, y, 6.5 * s, 0, TAU); ctx.fill();
  }

  // ---------- timeline ----------
  const T = {
    seedIn: [0.0, 1.35], open: [1.22, 1.95], crease: [1.75, 2.35], fill: [2.25, 2.8],
    roast: [2.6, 4.05], graphIn: [2.5, 2.9], graphOut: [3.95, 4.35],
    morph: [4.45, 4.95], wipe: [5.3, 6.0], disc: [5.35, 5.75], handle: [5.45, 5.85],
    streamIn: [5.6, 5.75], bloom: [5.73, 6.17], pull: [6.2, 6.45], streamOut: [6.39, 6.53],
    toLogo: [6.45, 7.15],   // v5: slower + smootherstep (v4 peaked at 2x the speed and popped)
  };
  const roastP = t => E.inOut(seg(t, ...T.roast));
  let crackT = 0; { let a = T.roast[0], b = T.roast[1];
    for (let i = 0; i < 40; i++) { const m = (a + b) / 2; if (roastP(m) < .78) a = m; else b = m; } crackT = a; }
  const ROAST = [[0, '#A7AB6C'], [.3, '#D2BE6C'], [.55, '#C08A4E'], [.78, '#8A4C22'], [1, '#55301A']];
  const wipeR = t => E.inOut(seg(t, ...T.wipe)) * 2300;
  // v5: the wipe edge is feathered by the distance it travels during the shutter (1/120 s), so it smears smoothly
  // instead of stepping into sub-frame bands (critic r5: ~12 hard rings at 5.6 s)
  const wipeFeather = t => clamp(Math.abs(wipeR(t + .002) - wipeR(t - .002)) / .004 * .5 / FPS, 1.5, 40);   // capped: wider read as a blob
  let lc = null, lx = null;
  function lightLayer(t, wipe) {
    const main = ctx, m = main.getTransform();
    if (!lc) { lc = document.createElement('canvas'); lc.width = W; lc.height = H; lx = lc.getContext('2d'); }
    lx.setTransform(1, 0, 0, 1, 0, 0); lx.globalAlpha = 1; lx.globalCompositeOperation = 'source-over'; lx.clearRect(0, 0, W, H);
    ctx = lx;
    if (PORTRAIT) lightBGP(t); else { lx.setTransform(m); lightBG(t); }
    const fw = wipeFeather(t);
    lx.setTransform(m); lx.globalCompositeOperation = 'destination-in';
    const g = lx.createRadialGradient(960, 540, Math.max(0, wipe - fw), 960, 540, wipe + fw);
    g.addColorStop(0, 'rgba(0,0,0,1)'); g.addColorStop(1, 'rgba(0,0,0,0)');
    lx.fillStyle = g; lx.fillRect(960 - wipe - fw - 10, 540 - wipe - fw - 10, 2 * (wipe + fw + 10), 2 * (wipe + fw + 10));
    lx.globalCompositeOperation = 'source-over';
    ctx = main;
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(lc, 0, 0); ctx.restore();
  }

  // ---------- camera: never still ----------
  // zoom keys per scene: in on seed + bean, out to reveal the graph, in on rings + cup, drift out on the logo
  // v5: out to .9 while the lines swing round (their turn stays in frame); the hold keeps a visible ~10% pull-out
  const ZK = [[0, .94], [1.0, 1.04], [1.6, 1.07], [2.5, 1.13], [3.95, 1.0], [4.55, .9], [5.3, 1.09], [6.45, 1.2], [8.0, 1.0]];
  // v5 logo: pull out 1.2 -> 1.0 while the cup lands and the letters build (6.45-7.6), then push in 12% to the last frame,
  // already moving at 8 s and still accelerating at 10 s (never a turnaround inside the hold)
  function zoomAt(t) {
    if (t < 6.45) return hermiteKeys(ZK, t);
    if (t < 7.6) return lerp(1.2, 1.0, E.smoother(seg(t, 6.45, 7.6)));
    const x = seg(t, 7.6, 10), g = x < .15 ? x * x / .3 : x - .075;   // short ease-in, then constant speed to the end
    return 1 + .12 * g / .925;
  }
  function hermiteKeys(ZK, t) {
    const n = ZK.length;
    let i = 0; while (i < n - 2 && t > ZK[i + 1][0]) i++;
    const [t0, z0] = ZK[i], [t1, z1] = ZK[i + 1];
    const tan = j => j <= 0 ? (ZK[1][1] - ZK[0][1]) / (ZK[1][0] - ZK[0][0])
      : j >= n - 1 ? (ZK[n - 1][1] - ZK[n - 2][1]) / (ZK[n - 1][0] - ZK[n - 2][0])
      : (ZK[j + 1][1] - ZK[j - 1][1]) / (ZK[j + 1][0] - ZK[j - 1][0]);
    const h = t1 - t0, u = clamp((t - t0) / h), u2 = u * u, u3 = u2 * u;
    return (2 * u3 - 3 * u2 + 1) * z0 + (u3 - 2 * u2 + u) * h * tan(i) + (-2 * u3 + 3 * u2) * z1 + (u3 - u2) * h * tan(i + 1);
  }
  function camera(t) {
    const dm = PORTRAIT ? 1 - E.inOutSine(seg(t, 6.8, 8.0)) : 1;   // 9:16: pan drift settles for the logo hold (zoom keeps breathing)
    return { z: zoomAt(t), x: 7 * Math.sin(t * .45) * dm, y: 5 * Math.sin(t * .6 + 1) * dm, r: .004 * Math.sin(t * .5) };
  }

  // ---------- wordmark (traced glyphs, source-pixel coords of the square logo) ----------
  const WM = { cx: 645, cy: 623 };
  const wmS = t => lerp(.64, .385, E.out(seg(t, T.toLogo[0], 7.6)));   // builds while it settles smaller; then the camera pushes in through the hold
                                                                       // (final size = .385 x 1.12 = v4's .43: 16:9 ~25% wide)
  const toWM = (x, y, t) => { const s = wmS(t); return [960 + (x - WM.cx) * s, 540 + (y - WM.cy) * s]; };
  const glyphs = (window.GLYPHS || []).map(g => ({ ...g, p: new Path2D(g.d),
    cx: (g.bbox[0] + g.bbox[2]) / 2, cy: (g.bbox[1] + g.bbox[3]) / 2 }));
  const G = id => glyphs.find(g => g.id === id);
  const tags = glyphs.filter(g => g.id === 'tag').sort((a, b) => a.cx - b.cx);
  const O_SRC = { x: 548.5, y: 474.5, r: 112.5 };            // cup "O" inside the wordmark

  // ---------- cup icon geometry (icon space, 1280 artboard: outer ring r 447.5 @ 717,642.5) ----------
  const ICON = { x: 717, y: 642.5, R: 447.5 };
  const HERO_R = 270;
  const leafTop = new Path2D('M665 490 L888 490 A148 144 0 0 1 740 634 L519 634 A146 144 0 0 1 665 490 Z');
  const leafBot = new Path2D('M519 660 L740 660 A148 143 0 0 1 888 803 L665 803 A146 143 0 0 1 519 660 Z');

  function cupState(t) {
    const k = E.smoother(seg(t, ...T.toLogo));
    const [ox, oy] = toWM(O_SRC.x, O_SRC.y, t);
    return { x: lerp(960, ox, k), y: lerp(540, oy, k), R: lerp(HERO_R, O_SRC.r * wmS(t), k) };
  }
  const cupXf = cup => { const s = cup.R / ICON.R; return (x, y) => [cup.x + (x - ICON.x) * s, cup.y + (y - ICON.y) * s]; };
  function withCup(cup, fn) {
    const s = cup.R / ICON.R;
    ctx.save(); ctx.translate(cup.x, cup.y); ctx.scale(s, s); ctx.translate(-ICON.x, -ICON.y);
    fn(s); ctx.restore();
  }

  // ---------- bean ----------
  const BEAN = { rx: 150, ry: 212, tilt: .42 };
  function crackPulse(t) { const d = t - crackT; return d < 0 ? 0 : Math.exp(-Math.pow((d - .06) / .09, 2)); }
  function beanGeom(t) {
    const cup = cupState(t);
    const m = E.inOut(seg(t, ...T.morph));
    const sc = lerp(1, .92, E.inOut(seg(t, 2.6, 3.2))) * (1 + .07 * crackPulse(t));
    const openY = E.outExpo(seg(t, 1.22, 1.7));
    const openX = E.outExpo(seg(t, 1.3, 1.95));
    return {
      x: cup.x, y: cup.y, m,
      rx: lerp(BEAN.rx * sc * openX, cup.R, m), ry: lerp(BEAN.ry * sc * openY, cup.R, m),
      tilt: lerp(BEAN.tilt, 0, m),
      fan: E.outBack(seg(t, 1.4, 2.05), 1.2),
      rot: .7 * t + 6.5 * E.in(seg(t, T.roast[0], T.roast[1] + .3)),
    };
  }

  // ---------- backgrounds (drawn under the camera, with overscan) ----------
  const OS = 200;   // v5: covers the .9 zoom-out at 4.55 s
  function darkBG(t) {
    const g = ctx.createLinearGradient(0, -OS, 0, H + OS);
    g.addColorStop(0, C.espTop); g.addColorStop(1, C.espBot);
    ctx.fillStyle = g; ctx.fillRect(-OS, -OS, W + 2 * OS, H + 2 * OS);
    blob(300 + 90 * Math.sin(t * .5), 900 - 50 * Math.cos(t * .4), 980, hex(C.oliveDeep), .55);
    blob(1650 - 70 * Math.sin(t * .35), 170 + 30 * Math.sin(t * .6), 950, hex(C.caramel), .26);
    blob(1150, 1060, 760, hex(C.brown), .55);
    const p = roastP(t), heat = p * (1 - seg(t, 4.1, 4.7));
    if (heat > 0) blob(960, 540, 620 + 260 * heat, mix(hex(C.olive), hex(C.caramel), p), .5 * heat);
    const v = ctx.createRadialGradient(960, 540, 400, 960, 540, 1300);
    v.addColorStop(0, 'rgba(23,14,8,0)'); v.addColorStop(1, 'rgba(23,14,8,.55)');   // v5: floor = espBot, no near-black corners
    ctx.fillStyle = v; ctx.fillRect(-OS, -OS, W + 2 * OS, H + 2 * OS);
  }
  function lightBG(t) {
    ctx.fillStyle = C.cream; ctx.fillRect(-OS, -OS, W + 2 * OS, H + 2 * OS);
    blob(260 + 70 * Math.sin(t * .45), 920, 950, hex(C.olive), .20);
    blob(1680, 150 + 50 * Math.sin(t * .5), 820, hex(C.yellow), .20);
    blob(1560 - 40 * Math.sin(t * .3), 1000, 760, hex(C.caramel), .15);
    blob(420, 120, 600, hex(C.caramel), .08);
    holdLight(t, 1920, 1080, 1);
  }
  // v5 hold: a warm light sweeps slowly behind the logo (large-area motion; the logo alone is small on flat cream)
  function holdLight(t, w, h, s) {
    const a = seg(t, 6.9, 7.8);
    if (a <= 0) return;
    const u = E.inOutSine(seg(t, 6.9, 10.4));
    blob(lerp(-.05 * w, 1.05 * w, u), h * (.62 - .18 * u), 900 * s, hex(C.yellow), .26 * a);
    blob(lerp(1.0 * w, .1 * w, u), h * (.3 + .2 * u), 700 * s, hex(C.caramel), .12 * a);
  }

  // ---------- scene 1: seed ----------
  const SEED = [[-60, 880], [420, 1080], [620, 250], [960, 540]];
  function seed(t) {
    const u = lerp(PORTRAIT ? .66 : .12, 1, E.out(seg(t, ...T.seedIn)));   // 9:16 frame is narrower: start where the seed is on screen      // v5: already travelling at frame 0, settles into the centre
    if (u <= 0) return;
    const fade = 1 - seg(t, 1.5, 2.3);
    ctx.lineCap = 'round';
    ctx.strokeStyle = rgba(LINE, .32 * fade); ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (let i = 0; i <= 90; i++) { const p = bez(SEED, u * i / 90); i ? ctx.lineTo(...p) : ctx.moveTo(...p); }
    ctx.stroke();
    const mv = 1 - seg(t, 1.2, 1.45);
    for (let k = 0; k < 28 && mv > 0; k++) {
      const a = u - .2 * (1 - k / 28), b = u - .2 * (1 - (k + 1) / 28);
      if (b <= 0) continue;
      const q = k / 28;
      ctx.strokeStyle = rgba(mix(hex(C.olive), hex(C.yellow), q), q * q * .9 * mv);
      ctx.lineWidth = 1.5 + 7 * q;
      ctx.beginPath(); ctx.moveTo(...bez(SEED, Math.max(0, a))); ctx.lineTo(...bez(SEED, b)); ctx.stroke();
    }
    const p = bez(SEED, u);
    const pulse = 1 + .18 * Math.sin(seg(t, 1.35, 1.75) * Math.PI);
    glowDot(p[0], p[1], pulse * (2.7 - 1.7 * E.inOut(seg(t, 0, 1.2))), hex(C.olive), 1 - seg(t, 1.72, 1.88));
    for (const st of [-.18, .2]) {                                // v5 hook: ring pulses leave the seed; the first is already visible on frame 0
      const e = seg(t, st, st + .9);
      if (e <= 0 || e >= 1) continue;
      ctx.strokeStyle = rgba(hex(C.yellow), .55 * (1 - e) * (1 - e)); ctx.lineWidth = 2.2 * LWS;
      ctx.beginPath(); ctx.arc(p[0], p[1], 14 + 190 * E.out(e), 0, TAU); ctx.stroke();
    }
  }
  // v5 hook: hairline target rings sweep in at the centre while the seed travels; the bean opens inside them
  function targetRings(t) {
    const fade = 1 - E.inOut(seg(t, 1.45, 2.1));
    if (fade <= 0) return;
    blob(960, 540, 520, hex(C.olive), .32 * fade);                 // v5 hook: a warm glow anchors the target from frame 0
    [[150, 0, .6], [235, .06, .55], [330, .12, .5]].forEach(([r, st, a], i) => {
      const e = E.out(seg(t, st, st + .6));
      if (e <= 0) return;
      const dir = i % 2 ? -1 : 1, a0 = -Math.PI / 2 - .6 * dir + .25 * t * dir;
      ctx.strokeStyle = rgba(LINE, .5 * a * fade); ctx.lineWidth = 1.6 * LWS;
      ctx.beginPath(); ctx.arc(960, 540, r * (1 + .04 * E.outExpo(seg(t, 1.25, 1.9))), a0, a0 + TAU * e * dir, dir < 0); ctx.stroke();
    });
  }

  // ---------- scene 3: roast graph — three lines (BT, ET, RoR) ----------
  const GX0 = -700, GX1 = 700, GBASE = 365;              // graph frame, relative to screen centre (v5: narrower, leaves room for the turn)
  const LINES = [
    { id: 'ET', label: 'ENV TEMP', col: [224, 168, 112], w: 1.8, sc: 640, ring: 'wipe', phi0: -Math.PI / 2 - .45,
      val: u => .74 - .07 * Math.exp(-u / .1) + .12 * u + .012 * Math.sin(u * 9) },
    { id: 'BT', label: 'BEAN TEMP', col: LINE, w: 2.4, sc: 640, ring: 1, phi0: -Math.PI / 2,
      val: u => .08 + .5 * Math.exp(-u / .05) + .74 * (1 - Math.exp(-u / .45)) },
    { id: 'RoR', label: 'RoR', col: [206, 207, 100], w: 1.8, sc: 600, ring: .6816, phi0: -Math.PI / 2 + .45,
      val: u => .06 + .62 * (1 - Math.exp(-u / .05)) * Math.exp(-u / .5) },
  ];
  const BT = LINES[1];
  const gX = u => lerp(GX0, GX1, u);
  const GV = PORTRAIT ? 2.5 : 1;                           // portrait: stretch the graph vertically about the centre
  const TS = PORTRAIT ? 1.6 : 1, LWS = PORTRAIT ? 1.4 : 1; // portrait: larger type + lines for phone screens
  const gY = (L, u) => (GBASE - L.sc * L.val(u)) * GV;

  const FOC = 1250;
  function proj(P) {
    const z = Math.min(P[2], FOC * .72), k = FOC / (FOC - z);
    return [960 + P[0] * k, 540 + P[1] * k, k, P[2]];
  }
  // Each roast line is a "snake" travelling one continuous path, parameter σ ∈ [0,3]:
  //   [0,1] its own graph curve → [1,2] a twisting 3D swoop toward camera → [2,3] once round its ring.
  // The body is always the last 1 unit of path behind the head, so graph → swoop → circle is one flowing stroke.
  const SNAKE = { t0: 3.98, dur: 1.3, stagger: .07 };
  const headOf = (k, t) => 1 + 2 * E.inOut(seg(t, SNAKE.t0 + k * SNAKE.stagger, SNAKE.t0 + k * SNAKE.stagger + SNAKE.dur));
  const bez3 = (a, b, c, d, u) => { const v = 1 - u;
    return [0, 1, 2].map(i => v * v * v * a[i] + 3 * v * v * u * b[i] + 3 * v * u * u * c[i] + u * u * u * d[i]); };
  function ringOf(L, t) {
    const R = HERO_R;
    return { rho: L.ring === 'wipe' ? Math.max(R * 1.4, wipeR(t) + 14) : R * L.ring, dy: L.id === 'RoR' ? .0212 * R : 0 };
  }
  function pathPt(L, k, sg, t) {
    if (sg <= 1) { const u = clamp(sg); return [gX(u), gY(L, u), 0]; }
    const { rho, dy } = ringOf(L, t);
    const c0 = [rho * Math.cos(L.phi0), rho * Math.sin(L.phi0) + dy, 0];
    if (sg < 2) {
      const w = sg - 1;
      const Td = [Math.sin(L.phi0), -Math.cos(L.phi0)];          // ring travel direction at entry (anticlockwise on screen)
      const P0 = [GX1, gY(L, 1), 0];
      // v5 (tuned offline against the frame edges): every line rises into a wide, nested U inside the frame;
      // v4 folded BT into a hairpin at x~1890 and RoR into a point.
      const far = L.id === 'RoR', DW = 1, D1 = (far ? 400 : 300) * DW, D2 = (far ? 780 : 700) * DW;   // (9:16 wider turns tried: lines left the frame)
      const lift = (far ? 200 : L.id === 'ET' ? 120 : 200) * (PORTRAIT ? 2.1 : 1);   // 9:16 has the height: taller, wider turns
      const dx = gX(1) - gX(.97), dyy = gY(L, 1) - gY(L, .97), dl = Math.hypot(dx, dyy);
      const P1 = [P0[0] + dx / dl * D1, P0[1] + dyy / dl * D1, 0];           // leave along the graph's own tangent (wide turn)
      const P2 = [c0[0] - Td[0] * D2, c0[1] - Td[1] * D2, 0];              // arrive along the ring's own tangent
      const P = bez3(P0, P1, P2, c0, w);
      const bump = Math.pow(Math.sin(Math.PI * w), 2);                         // zero value + zero slope at both ends
      const th = 1.7 * Math.PI * w + k * TAU / 3, r = 40 * bump;               // braid twist (v5: 85 -> 40, it pinched the turn)
      const pull = 1 - .35 * bump;                                              // offsets perspective so the loop stays in frame
      return [P[0] * pull, (P[1] - lift * bump + r * Math.cos(th)) * pull, 400 * bump + r * Math.sin(th)];
    }
    const phi = L.phi0 - TAU * Math.min(1, sg - 2);
    return [rho * Math.cos(phi), rho * Math.sin(phi) + dy, 0];
  }
  function lineAlpha(L, t) {
    let a = seg(t, ...T.graphIn);
    if (L.id === 'BT') a *= 1 - seg(t, 5.4, 5.65);
    if (L.id === 'RoR') a *= 1 - seg(t, 5.5, 5.75);
    if (L.id === 'ET') a *= 1 - seg(t, 5.75, 6.0);
    return a;
  }
  // variable-width stroke as one filled polygon: smooth through any bend, no chunk joins
  function ribbon(pts, i0, i1, wf) {
    const Lp = [], Rp = [];
    for (let i = i0; i <= i1; i++) {
      const p = pts[i], pa = pts[Math.max(i0, i - 1)], pb = pts[Math.min(i1, i + 1)];
      const dx = pb[0] - pa[0], dy = pb[1] - pa[1], d = Math.hypot(dx, dy) || 1;
      const hw = wf(p, i) / 2, nx = -dy / d * hw, ny = dx / d * hw;
      Lp.push(p[0] + nx, p[1] + ny); Rp.push(p[0] - nx, p[1] - ny);
    }
    ctx.beginPath(); ctx.moveTo(Lp[0], Lp[1]);
    for (let i = 2; i < Lp.length; i += 2) ctx.lineTo(Lp[i], Lp[i + 1]);
    for (let i = Rp.length - 2; i >= 0; i -= 2) ctx.lineTo(Rp[i], Rp[i + 1]);
    ctx.closePath(); ctx.fill();
  }
  // TEXT: 'all' = normal frame; 'none' = everything except type (motion-blur sub-frames); 'only' = type alone,
  // drawn sharp over the averaged frame at the frame's own time. Fast-moving labels ghosted under blur (critic r3-r4).
  let TEXT = 'all';
  function lines3D(t, pass) {
    const drawP = roastP(t);
    if (drawP <= 0 || t > 6.05) return;
    const N = 360;
    LINES.forEach((L, k) => {
      const a = lineAlpha(L, t);
      if (a <= 0) return;
      const h = headOf(k, t);
      const s0 = h > 1 ? h - 1 : 0, s1 = h > 1 ? h : drawP;
      const sg = [], pts = [];
      for (let i = 0; i <= N; i++) { const q = lerp(s0, s1, i / N); sg.push(q); pts.push(proj(pathPt(L, k, q, t))); }
      const col = L.id === 'ET' ? mix(L.col, hex(C.caramel), seg(t, 5.3, 5.6)) : L.col;
      const ss = x => { x = clamp(x); return x * x * (3 - 2 * x); };
      const tAmt = h > 1 ? clamp(1.6 * Math.sin(Math.PI * clamp((h - 1) / 2))) : 0;
      // v5 (Jason): while the head is inside its turn the front end thins to nothing, so the turn is only ever
      // seen as a whole U behind the head, never as a J. 0 before/after, smooth (sin^2) in between.
      const hf = Math.pow(Math.sin(Math.PI * clamp((h - 1 - .1) / .9)), 2), headLen = lerp(.28, .75, hf);
      const taper = i => { const f = i / N; return lerp(1, ss(f / .22) * ss((1 - f) / headLen), tAmt); };
      const isFront = i => sg[i] > 1;                     // graph behind the bean; swoop + rings in front (one switch, off-screen)
      // split into contiguous runs on the same side of the bean
      let i0 = 0;
      for (let i = 1; i <= N + 1; i++) {
        if (i <= N && isFront(i) === isFront(i0)) continue;
        const i1 = Math.min(N, i);                            // overlap one point so runs meet seamlessly
        if (TEXT !== 'only' && (pass === 'front') === isFront(i0) && i1 > i0) {
          ctx.fillStyle = rgba(col, a * .1); ribbon(pts, i0, i1, (p, i) => L.w * LWS * p[2] * 4 * taper(i));   // glow
          ctx.fillStyle = rgba(col, a);      ribbon(pts, i0, i1, (p, i) => L.w * LWS * p[2] * taper(i));
          for (const e of [i0, i1]) if ((e === 0 || e === N) && taper(e) > .05) {                      // round tips
            ctx.beginPath(); ctx.arc(pts[e][0], pts[e][1], L.w * LWS * pts[e][2] * taper(e) / 2, 0, TAU); ctx.fill();
          }
        }
        i0 = i;
      }
      // tip marker + label while the graph is drawn
      const hp = pts[N];
      const ta = a * (1 - seg(t, 3.95, 4.2));
      if (pass === 'back' && ta > 0) {
        if (TEXT !== 'only') {
          if (L.id === 'BT') glowDot(hp[0], hp[1], .8, mix(hex(C.yellow), hex(C.caramel), drawP), ta);
          else { ctx.fillStyle = rgba(L.col, ta); ctx.beginPath(); ctx.arc(hp[0], hp[1], 4.5 * TS, 0, TAU); ctx.fill(); }
        }
        ctx.font = `600 ${19 * TS}px Montserrat`; ctx.letterSpacing = `${3 * TS}px`; ctx.textAlign = 'left';
        ctx.fillStyle = rgba(L.col, ta * .9);
        let ly = hp[1] + (L.id === 'RoR' ? 30 : -14) * TS;            // v5: RoR label under its tip ...
        if (L.id === 'RoR') ly = Math.max(ly, 540 + gY(BT, drawP) - 14 * TS + 70 * TS);   // ... and never within 70 px of BEAN TEMP
        if (TEXT !== 'none') ctx.fillText(L.label, hp[0] + 18 * TS, ly);
        ctx.letterSpacing = '0px';
      }
    });
  }
  // axis, ticks, BT area and event labels (flat, fades before the lines lift)
  function graphFrame(t) {
    const a = seg(t, ...T.graphIn) * (1 - seg(t, ...T.graphOut));
    if (a <= 0) return;
    const X0 = 960 + GX0, X1 = 960 + GX1, BASE = 540 + GBASE * GV;
    const base = E.inOut(seg(t, 2.45, 3.05)), geo = TEXT !== 'only';
    ctx.strokeStyle = rgba(LINE, .22 * a); ctx.lineWidth = 1.2;
    if (geo) { ctx.beginPath(); ctx.moveTo(X0, BASE); ctx.lineTo(lerp(X0, X1, base), BASE); ctx.stroke(); }
    for (let x = X0, i = 0; geo && x <= X1; x += 40, i++) {
      if (x > lerp(X0, X1, base)) break;
      const major = i % 5 === 0;
      ctx.strokeStyle = rgba(LINE, (major ? .4 : .2) * a);
      ctx.beginPath(); ctx.moveTo(x, BASE); ctx.lineTo(x, BASE + (major ? 14 : 7)); ctx.stroke();
    }
    const p = roastP(t);
    if (p <= 0) return;
    const P = u => [960 + gX(u), 540 + gY(BT, u)];
    const N = 160;
    ctx.beginPath(); ctx.moveTo(X0, BASE);
    for (let i = 0; i <= N; i++) ctx.lineTo(...P(p * i / N));
    ctx.lineTo(P(p)[0], BASE); ctx.closePath();
    const fg = ctx.createLinearGradient(0, BASE - 605 * GV, 0, BASE);
    fg.addColorStop(0, rgba(hex(C.caramel), .2 * a)); fg.addColorStop(1, rgba(hex(C.caramel), 0));
    ctx.fillStyle = fg; if (geo) ctx.fill();
    ctx.font = `600 ${22 * TS}px Montserrat`; ctx.letterSpacing = `${3.5 * TS}px`; ctx.textAlign = 'center';
    for (const [u, label] of [[0, 'CHARGE'], [.3, 'DRYING'], [.55, 'MAILLARD'], [.78, 'FIRST CRACK'], [1, 'DROP']]) {
      const e = E.out(clamp((p - u) / .05 + (u === 0 ? 1 : 0)));
      if (e <= 0) continue;
      const q = P(u), hot = label === 'FIRST CRACK';
      ctx.strokeStyle = rgba(LINE, .28 * a * e); ctx.lineWidth = 1;
      ctx.setLineDash([3, 5]);
      if (geo) { ctx.beginPath(); ctx.moveTo(q[0], BASE); ctx.lineTo(q[0], lerp(BASE, q[1], e)); ctx.stroke(); }
      ctx.setLineDash([]);
      ctx.fillStyle = hot ? rgba(hex(C.yellow), a * e) : rgba(LINE, .7 * a * e);
      ctx.textAlign = u === 0 ? 'left' : 'center';                  // v5: CHARGE starts at its tick (was clipped in 9:16)
      if (TEXT !== 'none') ctx.fillText(label, q[0] - (u === 0 ? 10 * TS : 0), BASE + 52 * TS + 8 * (1 - e));
      ctx.strokeStyle = rgba(hot ? hex(C.yellow) : LINE, a * e); ctx.lineWidth = 1.6;
      if (geo) { ctx.beginPath(); ctx.arc(q[0], q[1], 5 * e, 0, TAU); ctx.stroke(); }
    }
    ctx.letterSpacing = '0px';
  }

  function heatRings(t, b) {
    for (const st of [2.8, 3.15, 3.5, 3.85]) {
      const e = seg(t, st, st + 1.1);
      if (e <= 0 || e >= 1) continue;
      ctx.save(); ctx.translate(b.x, b.y); ctx.rotate(b.tilt);
      ctx.strokeStyle = rgba(LINE, .3 * (1 - e) * (1 - b.m)); ctx.lineWidth = 1.3;
      ctx.beginPath(); ctx.ellipse(0, 0, b.rx * (1.08 + 1.1 * E.out(e)), b.ry * (1.06 + .75 * E.out(e)), 0, 0, TAU); ctx.stroke();
      ctx.restore();
    }
  }

  function crease(b, u0, u1) {
    const P = [[0, -b.ry * .86], [b.rx * .42, -b.ry * .3], [-b.rx * .42, b.ry * .3], [0, b.ry * .86]];
    ctx.beginPath();
    for (let i = 0; i <= 60; i++) { const q = bez(P, lerp(u0, u1, i / 60)); i ? ctx.lineTo(...q) : ctx.moveTo(...q); }
    return [bez(P, u0), bez(P, u1)];
  }

  function bean(t, b) {
    if (t < 1.2) return;
    const p = roastP(t), fillA = E.out(seg(t, ...T.fill));
    ctx.save(); ctx.translate(b.x, b.y); ctx.rotate(b.tilt);
    if (fillA > 0) {
      const base = mix(ramp(ROAST, p), hex(C.brown), b.m);
      const hi = mix(base, hex(C.cream), .3 * (1 - b.m)), lo = mix(base, [40, 20, 10], .35 * (1 - b.m));
      const g = ctx.createRadialGradient(-b.rx * .35, -b.ry * .4, 0, 0, 0, Math.max(b.rx, b.ry) * 1.05);
      g.addColorStop(0, rgba(hi)); g.addColorStop(.55, rgba(base)); g.addColorStop(1, rgba(lo));
      ctx.globalAlpha = fillA; ctx.fillStyle = g;
      ctx.beginPath(); ctx.ellipse(0, 0, b.rx, b.ry, 0, 0, TAU); ctx.fill();
      ctx.globalAlpha = 1;
    }
    const wa = lerp(.85, .32, fillA) * (1 - b.m);
    if (wa > 0.01) {
      ctx.lineWidth = 1.5;
      const N = 12;
      for (let i = 0; i < N; i++) {
        const phi = b.rot + b.fan * i * Math.PI / N;
        const w = Math.abs(b.rx * Math.sin(phi));
        ctx.strokeStyle = rgba(LINE, wa * (.35 + .65 * Math.abs(Math.sin(phi))));
        ctx.beginPath(); ctx.ellipse(0, 0, Math.max(.5, w), b.ry, 0, 0, TAU); ctx.stroke();
      }
      const la = wa * seg(t, 1.5, 1.9);
      for (const k of [-.5, .5]) {
        ctx.strokeStyle = rgba(LINE, la * .8);
        ctx.beginPath(); ctx.ellipse(0, k * b.ry, b.rx * .866, b.rx * .866 * .22, 0, 0, TAU); ctx.stroke();
      }
      ctx.strokeStyle = rgba(LINE, Math.min(1, wa * 1.15)); ctx.lineWidth = 2;
      ctx.beginPath(); ctx.ellipse(0, 0, b.rx, b.ry, 0, 0, TAU); ctx.stroke();
    }
    const d = .5 * E.inOut(seg(t, ...T.crease));
    const ca = 1 - seg(t, 4.35, 4.65);
    if (d > 0 && ca > 0) {
      ctx.lineCap = 'round';
      ctx.strokeStyle = rgba(hex(C.yellow), ca); ctx.lineWidth = 4;
      const [e0, e1] = crease(b, .5 - d, .5 + d); ctx.stroke();
      const ta = (1 - seg(t, 2.3, 2.6)) * ca;
      glowDot(e0[0], e0[1], .55, hex(C.olive), ta); glowDot(e1[0], e1[1], .55, hex(C.olive), ta);
    }
    ctx.restore();
  }

  function crackBurst(t, b) {
    const e = seg(t, crackT, crackT + .75);
    if (e <= 0 || e >= 1) return;
    const ex = E.outExpo(e), r = rng(3);
    ctx.save(); ctx.translate(b.x, b.y); ctx.rotate(b.tilt); ctx.lineCap = 'round';
    for (let k = 0; k < 18; k++) {
      const a = k * TAU / 18 + .09;
      const ex0 = b.rx * Math.cos(a), ey0 = b.ry * Math.sin(a), L = Math.hypot(ex0, ey0);
      const dx = ex0 / L, dy = ey0 / L;
      const r0 = 26 + 150 * ex, len = 56 * (1 - ex) + 4;
      ctx.strokeStyle = rgba(k % 3 ? LINE : hex(C.yellow), (1 - e) * .9); ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(ex0 + dx * r0, ey0 + dy * r0); ctx.lineTo(ex0 + dx * (r0 + len), ey0 + dy * (r0 + len)); ctx.stroke();
    }
    for (let k = 0; k < 30; k++) {
      const a = r() * TAU, sp = 80 + r() * 320, sz = 3 + r() * 6;
      const x = Math.cos(a) * (b.rx + sp * ex), y = Math.sin(a) * (b.ry + sp * ex) + 60 * e * e;
      ctx.save(); ctx.translate(x, y); ctx.rotate(a + e * (r() * 8 - 4));
      ctx.fillStyle = rgba(r() < .5 ? hex(C.caramel) : [230, 205, 160], (1 - e) * .9);
      ctx.beginPath(); ctx.ellipse(0, 0, sz, sz * .45, 0, 0, TAU); ctx.fill(); ctx.restore();
    }
    ctx.restore();
  }

  // ---------- cup + latte art ----------
  function outerRipples(t, cp) {
    for (const st of [5.4, 5.56, 5.72]) {
      const e = seg(t, st, st + 1.0);
      if (e <= 0 || e >= 1) continue;
      ctx.strokeStyle = rgba(hex(C.brown), .22 * (1 - e)); ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(cp.x, cp.y, cp.R * (1.05 + .9 * E.out(e)), 0, TAU); ctx.stroke();
    }
  }
  function cupHandle(t, cp) {
    const hE = E.outExpo(seg(t, ...T.handle));
    if (hE <= 0) return;
    withCup(cp, () => {
      ctx.strokeStyle = C.brown; ctx.lineWidth = 160; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(420, 637); ctx.lineTo(lerp(420, 165, hE), 637); ctx.stroke();
    });
  }
  function cupInner(t, cp) {
    const dE = E.outBack(seg(t, ...T.disc), 1.4);
    if (dE <= 0) return;
    withCup(cp, s => {
      ctx.fillStyle = C.caramel;
      ctx.beginPath(); ctx.arc(717, 652, 305 * dE, 0, TAU); ctx.fill();
      ctx.save(); ctx.beginPath(); ctx.arc(717, 652, 305 * Math.min(1, dE), 0, TAU); ctx.clip();
      for (const st of [5.35, 5.5, 5.65]) {
        const e = seg(t, st, st + .8);
        if (e <= 0 || e >= 1) continue;
        ctx.strokeStyle = rgba(hex(C.brown), .45 * (1 - e)); ctx.lineWidth = 2.2 / s;
        ctx.beginPath(); ctx.arc(717, 652, 20 + 290 * E.out(e), 0, TAU); ctx.stroke();
      }
      ctx.restore();
      const g = E.outBack(seg(t, ...T.bloom), 1.25);
      if (g > 0) {
        ctx.save();
        ctx.beginPath(); ctx.arc(703, 646, 262 * g, 0, TAU); ctx.clip();
        ctx.fillStyle = C.yellow;
        ctx.fill(leafTop); ctx.fill(leafBot);
        const sx = streamX(t);
        const gapR = t < T.pull[0] ? 740 : Math.min(740, sx);
        if (gapR > 519) ctx.fillRect(519, 632, gapR - 519, 30);
        ctx.restore();
      }
    });
  }
  function streamX(t) {
    const w0 = T.bloom[1] - .07;
    if (t < w0) return 703 + Math.sin(t * 34) * 16 * (1 - seg(t, T.bloom[0], w0));
    if (t < T.pull[0]) return lerp(703, 770, E.inOut(seg(t, w0, T.pull[0])));
    return lerp(770, 470, E.inOut(seg(t, ...T.pull)));
  }
  function stream(t, cp) {
    const head = E.in(seg(t, ...T.streamIn));
    if (head <= 0 || t > T.streamOut[1]) return;
    const X = cupXf(cp);
    const [x, yb] = X(streamX(t), 647);
    const SKY = PORTRAIT ? -1700 : -OS;
    const yTop = lerp(SKY, yb, E.in(seg(t, ...T.streamOut)));
    const yHead = lerp(SKY, yb, head);
    ctx.strokeStyle = C.yellow; ctx.lineCap = 'round';
    ctx.lineWidth = 7 * (1 - .5 * seg(t, ...T.streamOut));
    ctx.beginPath(); ctx.moveTo(x, yTop); ctx.lineTo(x, yHead); ctx.stroke();
    const e = seg(t, T.streamIn[1], T.streamIn[1] + .5);
    if (e > 0 && e < 1) {
      ctx.strokeStyle = rgba(hex(C.yellow), 1 - e); ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.arc(x, yb, 10 + cp.R * .35 * E.out(e), 0, TAU); ctx.stroke();
    }
  }

  // ---------- wordmark ----------
  function wordmark(t) {
    if (t < 6.98 || !glyphs.length) return;
    const s = wmS(t);
    ctx.save();
    ctx.translate(960, 540); ctx.scale(s, s); ctx.translate(-WM.cx, -WM.cy);
    // v5: every letter builds whole (fade + scale from its own centre + a short rise), staggered; v4's partial masks read as shards
    const build = (g, start, col) => {
      const e = seg(t, start, start + .42);
      if (e <= 0) return;
      const s2 = lerp(.82, 1, E.outBack(e, 1.2)), a = E.out(seg(t, start, start + .22));
      ctx.save(); ctx.globalAlpha = a;
      ctx.translate(g.cx, g.cy + 40 * (1 - E.outQuint(e))); ctx.scale(s2, s2); ctx.translate(-g.cx, -g.cy);
      ctx.fillStyle = col; ctx.fill(g.p); ctx.restore();
    };
    build(G('C'), 7.0, C.brown);
    build(G('F1'), 7.06, C.brown);
    build(G('F2'), 7.12, C.brown);
    ['N', 'A', 'T', 'U', 'R', 'E'].forEach((id, i) => build(G(id), 7.14 + i * .05, C.olive));
    const tr = 1 - E.outQuint(seg(t, 7.35, 8.2));
    tags.forEach((g, i) => {
      const e = E.out(seg(t, 7.38 + i * .008, 7.38 + i * .008 + .5));
      if (e <= 0) return;
      ctx.save(); ctx.globalAlpha = e;
      ctx.translate((g.cx - 648) * .35 * tr, (1 - e) * 14);
      ctx.fillStyle = C.brown; ctx.fill(g.p); ctx.restore();
    });
    ctx.restore();
  }

  // ---------- portrait layout: base scale per scene + camera that tracks the roast tip ----------
  // v5: graph scale reached sooner (the bean stayed clipped at 2.0-2.8 s); wide pull over the swoop so its turns stay in frame
  const PS = [[0, 1.15], [2.1, 1.15], [2.65, .9], [4.0, .9], [4.55, .6], [5.1, 1.12], [5.7, 1.12], [10, 1.12]];   // 5.7 key: flat hold (no sinking tail)
  const layoutScale = t => PORTRAIT ? hermiteKeys(PS, t) : 1;
  // final logo: centre on visual weight (COFF row is heavier + sits left) and lift to the optical centre
  const OPT = PORTRAIT ? [5.6, -40] : [0, 0];               // screen px (9:16 only)
  function layoutFocus(t) {
    const k = E.inOutSine(seg(t, 6.7, 7.8)) / (layoutScale(t) * zoomAt(t));
    const [fx, fy] = layoutFocusBase(t);
    return [fx - OPT[0] * k, fy - OPT[1] * k];
  }
  function layoutFocusBase(t) {
    if (!PORTRAIT) return [960, 540];
    const half = W / 2 / (layoutScale(t) * zoomAt(t));
    const tipX = 960 + gX(roastP(t));
    const track = clamp(tipX - .4 * half, 960 + GX0 - 150 + half, 960 + GX1 + 330 - half);  // tip sits ~70% across; edges + tip labels framed (v5: room for larger labels)
    const wIn = E.inOutSine(seg(t, 2.15, 2.85)), wOut = E.inOutSine(seg(t, 3.95, 4.85));
    // cup scene: centre cup + handle as one unit (group spans −1.41R…+R → centre at −0.206R), back to centre for the logo
    const cupShift = -.206 * HERO_R * E.inOutSine(seg(t, 5.35, 5.85)) * (1 - E.inOutSine(seg(t, 6.45, 7.0)));
    const swoop = 330 * Math.pow(Math.sin(Math.PI * seg(t, 4.0, 5.1)), 2);   // v5: frame the U-turns on the right while the lines swing round
    return [lerp(lerp(960, track, wIn), 960, wOut) + cupShift + swoop, 540 + 250 * wIn * (1 - wOut) - .25 * swoop];
  }
  function darkBGP(t, bx, by, s) {
    const g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, C.espTop); g.addColorStop(1, C.espBot);
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    blob(W * .12 + 70 * Math.sin(t * .5), H * .86 - 60 * Math.cos(t * .4), H * .62, hex(C.oliveDeep), .55);
    blob(W * .95 - 60 * Math.sin(t * .35), H * .1 + 40 * Math.sin(t * .6), H * .55, hex(C.caramel), .26);
    blob(W * .75, H * 1.0, H * .45, hex(C.brown), .55);
    const p = roastP(t), heat = p * (1 - seg(t, 4.1, 4.7));
    if (heat > 0) blob(bx, by, (620 + 260 * heat) * s, mix(hex(C.olive), hex(C.caramel), p), .5 * heat);
    const v = ctx.createRadialGradient(W / 2, H / 2, H * .22, W / 2, H / 2, H * .72);
    v.addColorStop(0, 'rgba(23,14,8,0)'); v.addColorStop(1, 'rgba(23,14,8,.55)');
    ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
  }
  function lightBGP(t) {
    ctx.fillStyle = C.cream; ctx.fillRect(0, 0, W, H);
    blob(W * .1 + 60 * Math.sin(t * .45), H * .88, H * .55, hex(C.olive), .20);
    blob(W * .92, H * .1 + 50 * Math.sin(t * .5), H * .5, hex(C.yellow), .20);
    blob(W * .85 - 40 * Math.sin(t * .3), H * .95, H * .45, hex(C.caramel), .15);
    blob(W * .15, H * .08, H * .35, hex(C.caramel), .08);
    holdLight(t, W, H, 1.1);
  }

  // ---------- frame ----------
  let debugImg = null;
  function render(t, f = Math.round(t * FPS), mode = 'all') {
    TEXT = mode;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
    const cam = camera(t), shake = crackPulse(t) * 4;
    ctx.save();
    const sc = cam.z * layoutScale(t), fc = layoutFocus(t);
    ctx.translate(W / 2 + cam.x + shake * Math.sin(t * 90), H / 2 + cam.y + shake * Math.cos(t * 77));
    ctx.rotate(cam.r); ctx.scale(sc, sc); ctx.translate(-fc[0], -fc[1]);
    if (mode === 'only') { graphFrame(t); lines3D(t, 'back'); ctx.restore(); TEXT = 'all'; return; }

    const wipe = wipeR(t);
    if (!PORTRAIT) {
      if (wipe < 2300) darkBG(t);
      if (wipe >= 2300) lightBG(t);
      else if (wipe > 0) lightLayer(t, wipe);
    } else {                                              // portrait: backgrounds laid out in screen space
      const bp = ctx.getTransform().transformPoint(new DOMPoint(960, 540));
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
      if (wipe < 2300) darkBGP(t, bp.x, bp.y, sc);
      ctx.restore();
      if (wipe >= 2300) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); lightBGP(t); ctx.restore(); }
      else if (wipe > 0) lightLayer(t, wipe);
    }

    graphFrame(t);
    lines3D(t, 'back');
    targetRings(t);
    seed(t);
    const b = beanGeom(t);
    heatRings(t, b);
    const cp = cupState(t);
    outerRipples(t, cp);
    cupHandle(t, cp);
    bean(t, b);
    crackBurst(t, b);
    cupInner(t, cp);
    lines3D(t, 'front');
    stream(t, cp);
    wordmark(t);
    if (debugImg) {
      ctx.globalCompositeOperation = 'multiply';
      const [x0, y0] = toWM(0, 0, t), s = wmS(t);
      ctx.drawImage(debugImg, x0, y0, 1280 * s, 1280 * s);
      ctx.globalCompositeOperation = 'source-over';
    }
    ctx.restore();
    grain(f, .025);   // dither only: breaks gradient banding, not visible as grain
    TEXT = 'all';
  }

  // ---------- motion blur: average `sub` sub-frames spread over the shutter ----------
  // shutter = fraction of the frame interval the "film" is exposed (.5 = 180°), centred on the frame time.
  // Still a pure function of the frame index; sub = 1 is the plain frame. Grain uses the frame index, so the
  // dither pattern is identical in every sub-frame and survives the average.
  let acc = null;
  function renderMB(f, sub = 1, shutter = .5) {
    if (sub <= 1) { render(f / FPS, f); return; }
    const n = W * H * 4;
    if (!acc || acc.length !== n) acc = new Float32Array(n); else acc.fill(0);
    for (let k = 0; k < sub; k++) {
      render(clamp((f + shutter * ((k + .5) / sub - .5)) / FPS, 0, DUR), f, 'none');
      const d = ctx.getImageData(0, 0, W, H).data;
      for (let i = 0; i < n; i++) acc[i] += d[i];
    }
    const img = ctx.createImageData(W, H), o = img.data;
    for (let i = 0; i < n; i++) o[i] = acc[i] / sub;   // Uint8Clamped rounds
    ctx.putImageData(img, 0, 0);
    render(f / FPS, f, 'only');                        // type stays sharp: drawn once, over the blurred frame
  }

  // ---------- modes: live player, still (?t=), export (?export[&sub=4&shutter=.5]) ----------
  const q = new URLSearchParams(location.search);
  const bar = document.getElementById('bar');
  async function boot() {
    try { await document.fonts.load('600 15px Montserrat'); } catch (e) {}
    if (q.has('debug')) { debugImg = new Image(); debugImg.src = 'src/logo_src.jpg'; await debugImg.decode(); }
    if (q.has('export')) {
      const total = Math.round(DUR * FPS), status = document.getElementById('status');
      const sub = Math.max(1, Math.round(+q.get('sub') || 1)), shutter = clamp(+(q.get('shutter') ?? .5), 0, 1);
      for (let f = 0; f < total; f++) {
        renderMB(f, sub, shutter);
        const blob = await new Promise(r => cv.toBlob(r, 'image/png'));
        await fetch('/frame?i=' + f, { method: 'POST', body: blob });
        if (status) status.textContent = `exporting ${f + 1}/${total}`;
      }
      await fetch('/done', { method: 'POST' });
      if (status) status.textContent = 'export done';
      window.__done = true;
      return;
    }
    if (q.has('t')) { render(parseFloat(q.get('t'))); return; }
    let t0 = performance.now(), paused = false, tp = 0;
    const tick = now => {
      const t = paused ? tp : ((now - t0) / 1000) % DUR;
      tp = t; render(t);
      if (bar) bar.style.width = (t / DUR * 100) + '%';
      requestAnimationFrame(tick);
    };
    cv.addEventListener('click', () => { paused = !paused; if (!paused) t0 = performance.now() - tp * 1000; });
    addEventListener('keydown', e => {
      if (e.key === ' ') { paused = !paused; if (!paused) t0 = performance.now() - tp * 1000; }
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        paused = true; tp = clamp(tp + (e.key === 'ArrowRight' ? 1 : -1) / FPS, 0, DUR);
      }
      if (e.key === 'r') { paused = false; t0 = performance.now(); }
    });
    requestAnimationFrame(tick);
  }
  window.renderAt = render;
  window.renderMB = renderMB;
  window.FPS = FPS;
  boot();
})();
