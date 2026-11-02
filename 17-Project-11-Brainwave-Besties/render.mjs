import {browserPath} from './browser-path.mjs';
import puppeteer from 'puppeteer-core';import chromium from '@sparticuz/chromium';import path from 'node:path';import os from 'node:os';import {spawn,execFileSync} from 'node:child_process';import {once} from 'node:events';import {mkdtemp,mkdir,copyFile,writeFile} from 'node:fs/promises';
const tmp=await mkdtemp(path.join(os.tmpdir(),'zinc-render-'));await mkdir('renders',{recursive:true});
const D=86.23333333333333,FPS=30,N=Math.round(D*FPS),workers=2,errors=[],segments=[];
const browsers=[];
try{
 await Promise.all(Array.from({length:workers},async(_,w)=>{
  const first=Math.floor(w*N/workers),last=Math.floor((w+1)*N/workers),out=path.join(tmp,`part-${w}.mp4`);segments[w]=out;
  const b=await puppeteer.launch({executablePath:browserPath(),headless:'shell',args:chromium.args});browsers.push(b);const p=await b.newPage();await p.setViewport({width:1080,height:1920});p.on('pageerror',e=>errors.push(e.message));
  await p.goto('file://'+path.resolve('index.html'),{waitUntil:'load'});await p.evaluate(async()=>{await document.fonts.ready;return true});
  const missing=await p.evaluate(()=>[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src));if(missing.length)throw Error(JSON.stringify(missing));
  const enc=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-vcodec','mjpeg','-framerate',String(FPS),'-i','pipe:0','-an','-c:v','libx264','-threads','1','-preset','fast','-crf','16','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',out],{stdio:['pipe','inherit','inherit']});const done=once(enc,'close');let pe;enc.stdin.on('error',e=>pe=e);
  for(let i=first;i<last;i++){
   await p.evaluate(t=>{window.__timelines.main.seek(t);return true},i/FPS);const frame=await p.screenshot({type:'jpeg',quality:97,captureBeyondViewport:false});if(pe)throw pe;if(!enc.stdin.write(frame))await once(enc.stdin,'drain');
   if((i-first)%150===0)console.log(`Segment ${w+1}: ${i-first}/${last-first}`);
  }
  enc.stdin.end();const[code]=await done;if(code!==0)throw Error('Encoder '+code);await p.close();await b.close();
 }));
 if(errors.length)throw Error(errors.join('; '));
 const audioDuration=Number(execFileSync('ffprobe',['-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1','assets/audio/mix.wav'],{encoding:'utf8'}));if(Math.abs(audioDuration-D)>1/48000)throw Error('Audio master duration mismatch: '+audioDuration);
 const list=path.join(tmp,'concat.txt');await writeFile(list,segments.map(f=>`file '${f}'`).join('\n'));
 const visual=path.join(tmp,'visual.mp4'),final=path.join(tmp,'final.mp4');
 execFileSync('ffmpeg',['-v','error','-y','-f','concat','-safe','0','-i',list,'-c','copy',visual],{stdio:'inherit'});
 execFileSync('ffmpeg',['-v','error','-y','-i',visual,'-i','assets/audio/mix.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-af','apad','-t',String(D),'-movflags','+faststart',final],{stdio:'inherit'});
 execFileSync('ffmpeg',['-v','error','-xerror','-i',final,'-f','null','-'],{stdio:'inherit'});
 const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_entries','format=duration,size:stream=codec_name,pix_fmt,width,height,nb_frames,r_frame_rate','-of','json',final],{encoding:'utf8'}));
 if(!probe.streams.some(s=>s.codec_name==='h264'&&s.width===1080&&s.height===1920&&+s.nb_frames===N)||!probe.streams.some(s=>s.codec_name==='aac'))throw Error('Unexpected output');
 await copyFile(final,'renders/Brainwave-Besties.mp4');await writeFile('production/export-verification.json',JSON.stringify({revision:'brainwave-besties-original',probe,full_decode_passed:true,frame_count:N,missingImages:[],pageErrors:errors},null,2));console.log('Render verified',probe.format);
}finally{await Promise.allSettled(browsers.map(b=>b.close()))}
