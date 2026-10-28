import {createRequire} from 'module';
import fs from 'fs';
import path from 'path';
import {fileURLToPath,pathToFileURL} from 'url';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const root=path.dirname(fileURLToPath(import.meta.url));
const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
try{
const page=await browser.newPage({viewport:{width:390,height:844}});
const errors=[],external=[];page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))external.push(r.url())});
await page.goto(pathToFileURL(path.join(root,'title-exploration.html')).href);
await page.evaluate(()=>window.ready);
const fonts=await page.evaluate(()=>({english:document.fonts.check('900 184px Orbitron'),japanese:document.fonts.check('700 46px "Zen Kaku Gothic New"','影の弟子サイバー忍者第零話')}));
const samples=[];
for(const t of [0,.2,.7,1.3,1.8,2.5]){
for(const [id,dir] of [['a','A'],['b','B']]){
await page.evaluate(({id,dir,t})=>drawTitle(document.getElementById(id),dir,t),{id,dir,t});
const buf=await page.locator('#'+id).screenshot();
const sharp=require('sharp');
const stats=await sharp(buf).stats();samples.push({dir,t,meanRGB:stats.channels.slice(0,3).reduce((s,c)=>s+c.mean,0)/3});
if(dir==='B'&&[.2,.7,1.3].includes(t))fs.writeFileSync(path.join(root,'exports',`A-refined-study-${t.toFixed(1)}s.png`),buf);

}
}
await page.locator('#hold').click();
await page.locator('#play').click();
await page.waitForTimeout(2700);
const finalClock=await page.locator('#clock').textContent();
await page.locator('#hold').click();
const holdClock=await page.locator('#clock').textContent();
await page.screenshot({path:path.join(root,'exports','Title-directions-phone-file.png'),fullPage:true});
await page.goto(pathToFileURL(path.join(root,'review-board.html')).href);
const images=await page.locator('img').evaluateAll(imgs=>imgs.map(im=>({src:im.getAttribute('src'),complete:im.complete,width:im.naturalWidth,height:im.naturalHeight})));
const result={file_preview:true,fonts,errors,externalRequests:external,finalClock,holdClock,samples,reviewImages:images};
fs.writeFileSync(path.join(root,'RENDER_CHECK.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify(result,null,2));
if(errors.length||external.length||!fonts.english||!fonts.japanese||finalClock!=='2.50 s'||holdClock!=='1.80 s'||images.some(i=>i.width!==1080||i.height!==1920))process.exitCode=1;
}finally{await browser.close()}
