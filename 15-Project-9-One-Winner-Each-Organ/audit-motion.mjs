import {ensureBrowser} from './setup_browser.mjs';
import puppeteer from 'puppeteer-core';import path from 'node:path';import fs from 'node:fs';
const b=await puppeteer.launch({executablePath:await ensureBrowser(),headless:'shell',args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--allow-file-access-from-files']});const p=await b.newPage();await p.setViewport({width:1080,height:1920});await p.goto('file://'+path.resolve('index.html'));await p.evaluate(()=>document.fonts.ready);
const report=await p.evaluate(()=>{
 const tl=window.__timelines.main;const schedule=DATA.schedule;const tweens=tl.getChildren(false,true,false).map(t=>({start:t.startTime(),end:t.endTime(),duration:t.duration(),props:Object.keys(t.vars).filter(k=>!['duration','ease','immediateRender','parent','onUpdate'].includes(k)),targets:t.targets().map(e=>e instanceof Element?(e.id?'#'+e.id:'#'+e.closest('.actor')?.id+' .'+[...e.classList].join('.')):'counter')}));
 const collisions=[],outOfFrame=[],missing=[],counts={};
 for(let t=.7;t<DATA.duration;t+=.2){tl.seek(t);const vis=schedule.filter(s=>t>s.start+.7&&t<s.handoff-.01&&+getComputedStyle(document.getElementById(s.key)).opacity>.9&&s.route!=='presenter').map(s=>{const r=document.querySelector('#'+s.key+' .pose').getBoundingClientRect();return {id:s.key,x:r.x,y:r.y,w:r.width,h:r.height};});
  for(const a of vis){if(a.x<-30||a.y<480||a.x+a.w>1050||a.y+a.h>1760)outOfFrame.push({t:+t.toFixed(2),...a});}
  for(let i=0;i<vis.length;i++)for(let j=i+1;j<vis.length;j++){const a=vis[i],b=vis[j];let area=Math.max(0,Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x))*Math.max(0,Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y));const ratio=area/Math.min(a.w*a.h,b.w*b.h);if(ratio>.12&&!collisions.some(c=>c.a===a.id&&c.b===b.id))collisions.push({t:+t.toFixed(2),a:a.id,b:b.id,overlapRatio:ratio});}
 }
 for(const s of schedule)counts[s.route]=(counts[s.route]||0)+1;
 for(const i of document.images)if(!i.complete||!i.naturalWidth)missing.push(i.src);
 return {tweens,routes:counts,collisions,outOfFrame,missing,notes:'Independent travel/pose/handoff wrappers sampled every 0.2sec after settling; presenter cane intentionally intersects scientific target; emergence/overlap handoffs excluded from stable collision checks.'};
});await b.close();fs.writeFileSync('production/animation-map.json',JSON.stringify(report,null,2));console.log(JSON.stringify({tweens:report.tweens.length,routes:report.routes,collisions:report.collisions,outOfFrame:report.outOfFrame.slice(0,8),missing:report.missing},null,2));
