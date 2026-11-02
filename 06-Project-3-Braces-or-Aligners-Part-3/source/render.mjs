// Frame-exact capture of the registered HyperFrames GSAP composition.
// No video textures, shaders or nested subcompositions are used in this project.
import puppeteer from 'puppeteer-core';
import {spawn,execFileSync} from 'node:child_process';import {once} from 'node:events';
import {readFile,mkdir,rename,unlink} from 'node:fs/promises';import path from 'node:path';
const env={...process.env,HYPERFRAMES_NO_TELEMETRY:'1',DO_NOT_TRACK:'1'};
execFileSync('python3',['build.py'],{stdio:'inherit',env});await mkdir('renders',{recursive:true});
const chrome=execFileSync('npx',['--no-install','hyperframes','browser','path'],{encoding:'utf8',env}).trim();
const browser=await puppeteer.launch({executablePath:chrome,headless:true,pipe:true,args:['--no-sandbox','--disable-dev-shm-usage']});
let enc;
try {
 const page=await browser.newPage();await page.setViewport({width:1080,height:1920});await page.goto('file://'+path.resolve('index.html'),{waitUntil:'networkidle0'});
 await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));return true;});
 const duration=await page.evaluate(()=>+document.querySelector('#root').dataset.duration);const count=Math.round(duration*30);
 enc=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','30','-i','pipe:0','-an','-c:v','libx264','-threads','2','-preset','medium','-crf','15','-vf','scale=out_color_matrix=bt709:out_range=tv','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart','renders/visual-working.mp4'],{stdio:['pipe','inherit','inherit']});const done=once(enc,'close');let pipeError;enc.stdin.on('error',e=>{pipeError=e;});
 for(let i=0;i<count;i++){
  await page.evaluate(t=>{window.__timelines.main.seek(t);return true;},i/30);
  const png=await page.screenshot({type:'png'});if(pipeError)throw pipeError;
  if(!enc.stdin.write(png))await once(enc.stdin,'drain');
  if(i%120===0)console.log(`Captured ${i}/${count}`);
 }
 enc.stdin.end();const [code]=await done;if(code!==0)throw Error('Video encoder exit '+code);
 execFileSync('ffmpeg',['-v','error','-y','-i','renders/visual-working.mp4','-i','assets/mix.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-af','apad','-t',String(duration),'-movflags','+faststart','renders/final-working.mp4'],{stdio:'inherit'});
 execFileSync('ffmpeg',['-v','error','-i','renders/final-working.mp4','-f','null','-'],{stdio:'inherit'});
 const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_entries','format=duration:stream=codec_name,width,height,nb_frames','-of','json','renders/final-working.mp4'],{encoding:'utf8'}));
 if(!probe.streams.some(s=>s.width===1080&&s.height===1920&&+s.nb_frames===count)||!probe.streams.some(s=>s.codec_name==='aac'))throw Error('Invalid final output');
 await rename('renders/final-working.mp4','renders/Braces-or-Aligners-Part-3.mp4');console.log('Final verified:',JSON.stringify(probe));
}finally{if(enc&&enc.exitCode===null)enc.kill('SIGTERM');await browser.close();}
