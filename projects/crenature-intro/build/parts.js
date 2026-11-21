// Render each logo part of the approved SVG as a white-on-transparent mask at 2x layout (3840x2160).
// Layout: content centre (vb 336.5,107.5) -> (1920,1050) at 2x; scale S2 vb-units -> px.
const { chromium } = require('playwright'); const fs = require('fs');
const S2 = Number(process.argv[2] || 4.428);
(async () => {
  const W = 3840, H = 2160;
  let svg = fs.readFileSync('source/identity/approved-white-lockup.svg', 'utf8');
  const vw = W / S2, vh = H / S2, vx = 336.5 - 1920 / S2, vy = 107.5 - 1050 / S2;
  svg = svg.replace('viewBox="0 0 673 231"', `viewBox="${vx} ${vy} ${vw} ${vh}" width="${W}" height="${H}" id="root"`);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.setContent(`<style>html,body{margin:0;background:transparent}</style>${svg}`);
  const parts = await p.evaluate(() => {
    const root = document.getElementById('root');
    const dragon = [...root.querySelector('svg').querySelectorAll(':scope > path')];
    const letters = [...root.querySelectorAll('g[data-letter]')];
    dragon.forEach((e, i) => e.setAttribute('data-part', ['body', 'horns', 'eye'][i]));
    letters.forEach((e, i) => e.setAttribute('data-part', 'L' + i + '_' + e.getAttribute('data-letter')));
    return [...dragon, ...letters].map(e => e.getAttribute('data-part'));
  });
  for (const name of parts) {
    await p.evaluate((name) => {
      document.querySelectorAll('[data-part]').forEach(e => {
        const on = e.getAttribute('data-part') === name;
        e.style.visibility = on ? 'visible' : 'hidden';
        if (on && !e.closest('mask')) e.style.fill = '#ffffff';
      });
      // keep letter-internal mask fills intact (black/white)
      document.querySelectorAll('mask *').forEach(e => { e.style.visibility = 'visible'; e.style.fill = ''; });
    }, name);
    await p.screenshot({ path: `parts/${name}.png`, omitBackground: true });
  }
  fs.writeFileSync('parts/layout.json', JSON.stringify({ S2, W, H, vx, vy, parts }, null, 1));
  await b.close(); console.log(parts.join(' '));
})();
