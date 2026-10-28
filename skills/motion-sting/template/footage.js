// Footage layer: real clips drawn frame-exactly in a deterministic canvas engine.
//   await FOOT.init()                       loads footage/manifest.json (from scripts/extract_clips.py)
//   await FOOT.prepare([{id, t}, ...])      decodes exactly those frames before a render (export / stills)
//   FOOT.draw(ctx, id, t, x, y, w, h, opt)  cover-fits the frame at clip-time t into the box (sync, from cache)
// Clip time t is in seconds from the clip's first extracted frame; it is clamped (holds the first/last frame).
// opt: {fx, fy} focus 0..1 for the cover crop (default .5/.5), {r} corner radius, {alpha}.
// Never use a <video> element for export: its seeking is asynchronous and approximate.
(() => {
  let man = {}, cache = new Map(), order = [];
  const MAX = 240;                                         // decoded frames kept (enough for 8 sub-frames x several clips)
  const idx = (id, t) => { const m = man[id]; return Math.max(1, Math.min(m.n, Math.floor(t * m.fps) + 1)); };
  const key = (id, i) => id + '/' + i;
  async function load(id, i) {
    const k = key(id, i);
    if (cache.has(k)) return cache.get(k);
    const img = new Image();
    img.src = `footage/${id}/f_${String(i).padStart(5, '0')}.jpg`;
    await img.decode();
    cache.set(k, img); order.push(k);
    while (order.length > MAX) cache.delete(order.shift());
    return img;
  }
  window.FOOT = {
    get manifest() { return man; },
    async init() {
      try { man = await (await fetch('footage/manifest.json', { cache: 'no-store' })).json(); } catch (e) { man = {}; }
      return man;
    },
    has: id => !!man[id],
    async prepare(list) { await Promise.all(list.filter(q => man[q.id]).map(q => load(q.id, idx(q.id, q.t)))); },
    draw(ctx, id, t, x, y, w, h, opt = {}) {
      if (!man[id]) return false;
      const img = cache.get(key(id, idx(id, t)));
      if (!img) return false;                                // not prepared (live preview): caller keeps the last frame
      const m = man[id], s = Math.max(w / m.w, h / m.h), sw = w / s, sh = h / s;
      const sx = (m.w - sw) * (opt.fx ?? .5), sy = (m.h - sh) * (opt.fy ?? .5);
      ctx.save();
      if (opt.alpha != null) ctx.globalAlpha *= opt.alpha;
      if (opt.r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, opt.r); ctx.clip(); }
      ctx.drawImage(img, sx, sy, sw, sh, x, y, w, h);
      ctx.restore();
      return true;
    },
  };
})();
