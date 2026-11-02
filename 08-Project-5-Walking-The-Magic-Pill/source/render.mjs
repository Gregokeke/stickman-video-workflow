import {browserPath} from './browser-path.mjs';
import puppeteer from 'puppeteer-core';
import {spawn,execFileSync} from 'node:child_process';
import {once} from 'node:events';
import {mkdir,copyFile,writeFile,mkdtemp} from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
const temp=await mkdtemp(path.join(os.tmpdir(),'walking-export-'));
const visual=path.join(temp,'visual.mp4'),final=path.join(temp,'final.mp4');
execFileSync('python3',['build.py'],{stdio:'inherit'});
await mkdir('renders',{recursive:true});
const chrome=browserPath();
const browser=await puppeteer.launch({executablePath:chrome,headless:true,pipe:true,args:['--no-sandbox','--disable-dev-shm-usage']});
let enc;
try{
 const page=await browser.newPage();await page.setViewport({width:1080,height:1920});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('file://'+path.resolve('index.html'),{waitUntil:'load'});
 
 if(errors.length)throw Error(errors.join('; '));
 const duration=125.1,count=Math.round(duration*30);
 enc=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','30','-i','pipe:0','-an','-c:v','libx264','-threads','2','-preset','medium','-crf','16','-vf','scale=out_color_matrix=bt709:out_range=tv','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',visual],{stdio:['pipe','inherit','inherit']});
 const done=once(enc,'close');let pipeError;enc.stdin.on('error',e=>pipeError=e);
 for(let i=0;i<count;i++){
  await page.evaluate(t=>{window.__timelines.main.seek(t);return true},i/30);
  const png=await page.screenshot({type:'png'});if(pipeError)throw pipeError;
  if(!enc.stdin.write(png))await once(enc.stdin,'drain');
  if(i%150===0)console.log('Frames',i,'/',count);
 }
 enc.stdin.end();const [code]=await done;if(code!==0)throw Error('Encoder exit '+code);
 execFileSync('ffmpeg',['-v','error','-y','-i',visual,'-i','assets/audio/mix.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-af','apad','-t',String(duration),'-movflags','+faststart',final],{stdio:'inherit'});
 execFileSync('ffmpeg',['-v','error','-xerror','-i',final,'-f','null','-'],{stdio:'inherit'});
 const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_entries','format=duration,size:stream=codec_name,pix_fmt,width,height,nb_frames,r_frame_rate','-of','json',final],{encoding:'utf8'}));
 if(!probe.streams.some(s=>s.width===1080&&s.height===1920&&+s.nb_frames===count)||!probe.streams.some(s=>s.codec_name==='aac'))throw Error('Invalid output');
 await copyFile(final,'renders/Walking-The-Magic-Pill.mp4');
 await writeFile('production/export-verification.json',JSON.stringify(probe,null,2));console.log('Verified final',probe.format);
}finally{if(enc&&enc.exitCode===null)enc.kill('SIGTERM');await browser.close()}
