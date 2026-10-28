import {createRequire} from 'module';
import http from 'http';
import fs from 'fs';
import path from 'path';
import {fileURLToPath} from 'url';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const root=path.dirname(fileURLToPath(import.meta.url));
const mime={'.html':'text/html; charset=utf-8','.css':'text/css','.png':'image/png','.ttf':'font/ttf'};
const server=http.createServer((req,res)=>{const p=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));if(!p.startsWith(root+path.sep)){res.writeHead(403).end();return}fs.readFile(p,(e,b)=>{if(e){res.writeHead(404).end();return}res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');res.end(b)})});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
const page=await browser.newPage({viewport:{width:1280,height:1450},deviceScaleFactor:1});
const errors=[];page.on('pageerror',e=>errors.push(String(e)));
await page.goto(`http://127.0.0.1:${server.address().port}/title-exploration.html`);
await page.evaluate(()=>window.ready);
for(const [id,dir,name] of [['a','A','A-Previous'],['b','B','A-Refined']]){
for(const [suffix,opts] of [['1080x1920',{}],['H3-textless-plate',{omitType:true,omitKanji:true}]]){
const data=await page.evaluate(({id,dir,opts})=>{const c=document.getElementById(id);window.drawTitle(c,dir,1.8,opts);return c.toDataURL('image/png').split(',')[1]}, {id,dir,opts});
fs.writeFileSync(path.join(root,'exports',name+'-'+suffix+'.png'),Buffer.from(data,'base64'));
}
}
await page.evaluate(()=>{drawTitle(document.getElementById('a'),'A',1.8);drawTitle(document.getElementById('b'),'B',1.8)});
await page.screenshot({path:path.join(root,'exports','Title-directions-desktop.png'),fullPage:true});
await page.setViewportSize({width:390,height:844});
await page.screenshot({path:path.join(root,'exports','Title-directions-phone.png'),fullPage:true});
const fontCheck=await page.evaluate(()=>({unbounded:document.fonts.check('900 180px Unbounded'),orbitron:document.fonts.check('900 184px Orbitron'),michroma:document.fonts.check('42px Michroma'),japanese:document.fonts.check('700 46px "Zen Kaku Gothic New"','影の弟子サイバー忍者第零話')}));
console.log(JSON.stringify({fontCheck,errors,exports:fs.readdirSync(path.join(root,'exports'))},null,2));
if(errors.length||Object.values(fontCheck).includes(false))process.exitCode=1;
}finally{if(browser)await browser.close();server.close()}
