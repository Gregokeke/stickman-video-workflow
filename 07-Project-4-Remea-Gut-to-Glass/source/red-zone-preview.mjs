import puppeteer from 'puppeteer-core';
import {mkdir} from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
const chrome=execFileSync('npx',['hyperframes','browser','path'],{encoding:'utf8',env:{...process.env,HYPERFRAMES_NO_TELEMETRY:'1',DO_NOT_TRACK:'1'}}).trim();
const b=await puppeteer.launch({executablePath:chrome,headless:true,pipe:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{const page=await b.newPage();await page.setViewport({width:1080,height:1920});await page.goto('file://'+path.resolve('index.html'),{waitUntil:'networkidle0'});await page.evaluate(async()=>{const img=new Image();img.src='references/red-zone-canvas.png';img.id='review-guide';img.style='position:fixed;inset:0;width:1080px;height:1920px;z-index:2147483647;pointer-events:none;opacity:.42';await img.decode();document.body.appendChild(img);return true;});await mkdir('red-zone-preview',{recursive:true});
const times=[.8,2.3,5.1,6.8,7.7,9.8,11.2,12.15,15.4,17.2,23.35,24.15,25.85,27.8,31.2,33.3,35.9,38.3,42.2,45.7,48.6,53.35,54.85,61.7,63.8];
for(let i=0;i<times.length;i++){await page.evaluate(t=>{window.__timelines.main.seek(t);return true;},times[i]);await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));await page.screenshot({path:`red-zone-preview/${String(i).padStart(2,'0')}-${times[i]}.png`});}console.log('Reviewed',times.length,'selected frames with the actual guide overlay');
}finally{await b.close();}
