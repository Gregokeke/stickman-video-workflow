import puppeteer from 'puppeteer-core';
import {writeFile} from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
const chrome=execFileSync('npx',['--no-install','hyperframes','browser','path'],{encoding:'utf8',env:{...process.env,HYPERFRAMES_NO_TELEMETRY:'1',DO_NOT_TRACK:'1'}}).trim();
const browser=await puppeteer.launch({executablePath:chrome,headless:true,pipe:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
const page=await browser.newPage();await page.goto('file://'+path.resolve('index.html'),{waitUntil:'domcontentloaded'});
const report=await page.evaluate(()=>{
 const visual=new Set(['opacity','x','y','scale','rotation','rotationY','clipPath','strokeDashoffset']);
 const tweens=window.__timelines.main.getChildren(false,true,false).map(t=>({target:t.targets()[0]?.id,start:t.startTime(),end:t.startTime()+t.duration(),props:Object.keys(t.vars).filter(k=>visual.has(k))})).filter(t=>t.target&&t.props.length);
 const conflicts=[];for(let i=0;i<tweens.length;i++)for(let j=i+1;j<tweens.length;j++){const a=tweens[i],b=tweens[j];if(a.target!==b.target||Math.min(a.end,b.end)-Math.max(a.start,b.start)<.001)continue;const props=a.props.filter(p=>b.props.includes(p));if(props.length)conflicts.push({target:a.target,props,a:[a.start,a.end],b:[b.start,b.end]});}
 return {tweenCount:tweens.length,conflicts,tweens};
});await writeFile('choreography-review.json',JSON.stringify(report,null,2));console.log(JSON.stringify({tweenCount:report.tweenCount,conflicts:report.conflicts}));if(report.conflicts.length)process.exitCode=1;
}finally{await browser.close();}
