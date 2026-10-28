// Render each poster element of source16.html as its own transparent 1920x1080 PNG (layers/) for the animated end title.
import {createRequire} from 'module';import http from 'http';import fs from 'fs';import path from 'path';import {fileURLToPath} from 'url';
const require=createRequire(import.meta.url);const {chromium}=require('playwright');
const here=path.dirname(fileURLToPath(import.meta.url));const root=path.dirname(here);
const mime={'.html':'text/html; charset=utf-8','.css':'text/css','.png':'image/png','.ttf':'font/ttf'};
const server=http.createServer((req,res)=>{const p=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));if(!p.startsWith(root+path.sep)){res.writeHead(403).end();return}fs.readFile(p,(e,b)=>{if(e){res.writeHead(404).end();return}res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');res.end(b)})});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const out=path.join(here,'layers');fs.mkdirSync(out,{recursive:true});let browser;
try{browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1920,height:1080}});
 for(const L of ['bg','kanji','duo','shade','THE','SHADOW','APPRENTICE','lines','jp','blade','column']){
  await page.goto(`http://127.0.0.1:${server.address().port}/blade-dance-16x9/source16.html?layer=${L}`);await page.evaluate(()=>window.ready);
  const data=await page.evaluate(()=>document.getElementById('art').toDataURL('image/png').split(',')[1]);fs.writeFileSync(path.join(out,L+'.png'),Buffer.from(data,'base64'));}
 console.log('layers ok');}finally{if(browser)await browser.close();server.close()}
