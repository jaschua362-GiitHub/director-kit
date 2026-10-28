// Local preview + frame-export server (no dependencies).  node server.js [port]
//   POST /frame?i=<number>  → frames/f_0000.png   (export frames, consumed by scripts/render.py)
//   POST /frame?i=<name>    → stills/<name>.png   (review stills + contact sheets from tools.js)
const http = require('http'), fs = require('fs'), path = require('path');
const root = __dirname, port = +process.argv[2] || 8765;
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.json': 'application/json', '.mp4': 'video/mp4', '.wav': 'audio/wav', '.svg': 'image/svg+xml' };
http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  if (req.method === 'POST' && u.pathname === '/frame') {
    const i = String(u.searchParams.get('i'));
    const numeric = /^\d+$/.test(i);
    const dir = path.join(root, numeric ? 'frames' : 'stills');
    fs.mkdirSync(dir, { recursive: true });
    const file = path.join(dir, numeric ? `f_${i.padStart(4, '0')}.png` : `${i.replace(/[^\w.-]/g, '_')}.png`);
    const ch = [];
    req.on('data', c => ch.push(c));
    req.on('end', () => { fs.writeFileSync(file, Buffer.concat(ch)); res.end(file); });
    return;
  }
  if (req.method === 'POST' && u.pathname === '/done') { console.log('EXPORT DONE'); res.end('ok'); return; }
  const p = path.join(root, decodeURIComponent(u.pathname === '/' ? '/index.html' : u.pathname));
  if (!p.startsWith(root)) { res.writeHead(403); res.end(); return; }
  fs.readFile(p, (e, d) => {
    if (e) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    res.end(d);
  });
}).listen(port, () => console.log(`http://localhost:${port}`));
