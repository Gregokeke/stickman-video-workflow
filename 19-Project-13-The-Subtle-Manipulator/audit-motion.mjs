import puppeteer from 'puppeteer-core';
import {writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
const browser = await puppeteer.launch({executablePath:process.env.CHROME_PATH || '/root/.cache/hyperframes/chrome/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell',headless:true,args:['--no-sandbox','--allow-file-access-from-files']});
const page=await browser.newPage();
await page.goto('file://'+resolve('index.html'));
const report=await page.evaluate(()=>{
 const tl=window.__timelines.main;
 const tweens=tl.getChildren(false,true,false).map(t=>({start:t.startTime(),end:t.endTime(),targets:t.targets().map(e=>e.id),vars:Object.fromEntries(Object.entries(t.vars).filter(([k])=>['x','y','scale','opacity','rotation','duration','ease'].includes(k)))}));
 const conflicts=[];
 for(let i=0;i<tweens.length;i++)for(let j=i+1;j<tweens.length;j++){
  const a=tweens[i],b=tweens[j];
  if(Math.min(a.end,b.end)-Math.max(a.start,b.start)<.001)continue;
  for(const id of a.targets.filter(id=>b.targets.includes(id)))for(const k of ['x','y','scale','opacity','rotation'])if(k in a.vars&&k in b.vars)conflicts.push({id,k,a:a.start,b:b.start});
 }
 return {tweens,conflicts,notes:'Still holds are intentional. Ordinary illustration handoffs use the Project 2 early opacity fade. No presenter or micro explanatory animation.'};
});
writeFileSync('motion-audit.json',JSON.stringify(report,null,2));
console.log(JSON.stringify({tweens:report.tweens.length,conflicts:report.conflicts}));
await browser.close();
if(report.conflicts.length)process.exitCode=1;
