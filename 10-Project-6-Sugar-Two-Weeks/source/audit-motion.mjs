import puppeteer from 'puppeteer-core';import {browserPath} from './browser-path.mjs';import path from 'node:path';import {writeFile} from 'node:fs/promises';
const b=await puppeteer.launch({executablePath:browserPath(),headless:true,args:['--no-sandbox']});
try{const p=await b.newPage();await p.setViewport({width:1080,height:1920});await p.goto('file://'+path.resolve('index.html'));const result=await p.evaluate(()=>{
 const map=[],conflicts=[],seen=new Map();
 for(const t of window.__timelines.main.getChildren(true,true,false)){
  if(t.duration()===0)continue;
  const props=Object.keys(t.vars).filter(k=>['opacity','x','y','scale','rotation','strokeDashoffset'].includes(k));
  const start=t.startTime(),end=start+t.duration();
  for(const el of t.targets()){
   let id=el.id||el.closest('[id]')?.id+' '+(el.className?.baseVal??el.className??el.tagName);
   map.push({target:id,start,end,props});
   if(!seen.has(el))seen.set(el,[]);
   for(const old of seen.get(el))if(Math.min(old.end,end)-Math.max(old.start,start)>.001){const common=props.filter(k=>old.props.includes(k));if(common.length)conflicts.push({target:id,common,first:old,second:{start,end}})}
   seen.get(el).push({start,end,props});
  }
 }
 return {tweens:map.length,conflicts,map};
});await writeFile('production/choreography-audit.json',JSON.stringify(result,null,2));console.log('Timed animation targets:',result.tweens,'Conflicts:',result.conflicts.length);if(result.conflicts.length)throw Error('Animation property conflict');}finally{await b.close()}
