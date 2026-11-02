import {browserPath} from './browser-path.mjs';
import puppeteer from 'puppeteer-core';
import {execFileSync} from 'node:child_process';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import path from 'node:path';
const chrome=browserPath();
const browser=await puppeteer.launch({executablePath:chrome,headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 const page=await browser.newPage();await page.setViewport({width:1080,height:1920,deviceScaleFactor:.5});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('file://'+path.resolve('index.html'),{waitUntil:'load'});
 await mkdir('production/review',{recursive:true});
 const times=[1.1,3.9,6.9,7.9,9.7,11.7,14.4,16.9,18.9,20.3,22.7,24.9,26.6,27.6,29.7,31.9,34.8,36.2,39.2,41.8,44.3,47.9,51.7,53.4,55.8,57.1,58.9,60.6,61.8,63.1,65.9,68.4,71.9,73.7,75.1,76.8,78.6,80.1,81.7,83.1,85.1,87.6,89.2,91.8,94.0,95.1,97.4,99.3,101.1,103.1,105.0,107.8,109.6,112.5,114.8,116.2,117.8,119.3,121.8,123.5,124.6];
 const shots=[];
 for(let i=0;i<times.length;i++){
  await page.evaluate(t=>{window.__timelines.main.seek(t);return true},times[i]);
  const buf=await page.screenshot({type:'png',path:'production/review/'+String(i).padStart(2,'0')+'.png'});shots.push({t:times[i],data:buf.toString('base64')});
 }
 const audit=await page.evaluate(()=>{
  const flags=[],seen=new Set(),conflicts=[];const tl=window.__timelines.main;
  for(let t=0;t<125.1;t+=1/15){
   tl.seek(t);const active=[...document.querySelectorAll('.actor')].filter(e=>+getComputedStyle(e).opacity>.2);
   for(const e of active)seen.add(e.dataset.asset);
   const caps=[...document.querySelectorAll('.caption')].filter(e=>+getComputedStyle(e).opacity>.2);
   if(caps.length>1)flags.push({time:t,type:'multiple captions'});
   for(const e of caps){const b=e.getBoundingClientRect();if(e.scrollHeight>215||b.right>885||b.left<80)flags.push({time:t,type:'caption bounds',id:e.id})}
  }
  const tw=tl.getChildren(false,true,false),props=['x','y','scale','rotation','opacity','strokeDashoffset'];
  for(let i=0;i<tw.length;i++)for(let j=i+1;j<tw.length;j++){
   const a=tw[i],b=tw[j];if(Math.min(a.endTime(),b.endTime())-Math.max(a.startTime(),b.startTime())<.001)continue;
   if(a.targets().some(x=>b.targets().includes(x))){const shared=props.filter(p=>p in a.vars&&p in b.vars);if(shared.length)conflicts.push({at:Math.max(a.startTime(),b.startTime()),properties:shared})}
  }
  return {samples:1877,seen:[...seen],flags,conflicts,tweens:tw.length};
 });
 audit.runtime_errors=errors;await writeFile('production/choreography-audit.json',JSON.stringify(audit,null,2));
 for(let start=0;start<shots.length;start+=12){
  const group=shots.slice(start,start+12);const cp=await browser.newPage();await cp.setViewport({width:1120,height:1560});
  await cp.setContent('<body style="margin:0;background:#ddd;display:grid;grid-template-columns:repeat(4,280px)">'+group.map(s=>'<div style="height:520px;text-align:center;font:24px sans-serif;background:#fff"><img style="width:270px;height:480px" src="data:image/png;base64,'+s.data+'"><div>'+s.t+'s</div></div>').join(''));
  await cp.evaluate(async()=>await Promise.all([...document.images].map(i=>i.decode())));await cp.screenshot({path:'production/review/sheet-'+Math.floor(start/12)+'.png'});await cp.close();
 }
 console.log(JSON.stringify({runtime_errors:errors,used:audit.seen.length,flags:audit.flags.length,conflicts:audit.conflicts.length,tweens:audit.tweens}));
}finally{await browser.close()}
