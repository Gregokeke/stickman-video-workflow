import fs from 'node:fs';import path from 'node:path';import os from 'node:os';import zlib from 'node:zlib';import {execFileSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
export async function ensureBrowser(){
 if(process.env.CHROME_PATH&&fs.existsSync(process.env.CHROME_PATH))return process.env.CHROME_PATH;
 const d=path.join(os.tmpdir(),'fasting-self-recycling-browser'),out=path.join(d,'chromium');fs.mkdirSync(d,{recursive:true});
 const root=path.dirname(fileURLToPath(import.meta.url));const bin=path.join(root,'node_modules/@sparticuz/chromium/bin');
 if(!fs.existsSync(out)||fs.statSync(out).size<150000000){
  const a=zlib.brotliDecompressSync(fs.readFileSync(path.join(bin,'chromium.br'))),fd=fs.openSync(out,'w');
  for(let i=0;i<a.length;i+=1048576){const b=a.subarray(i,Math.min(i+1048576,a.length));let k=0;while(k<b.length)k+=fs.writeSync(fd,b,k,b.length-k,i+k);}fs.closeSync(fd);fs.chmodSync(out,0o755);
  for(const n of ['swiftshader','fonts']){const a=zlib.brotliDecompressSync(fs.readFileSync(path.join(bin,n+'.tar.br'))),t=path.join(d,n+'.tar');fs.writeFileSync(t,a);execFileSync('tar',['--no-same-owner','-xf',t,'-C',d]);}
 }return out;
}
if(process.argv[1]===fileURLToPath(import.meta.url))console.log(await ensureBrowser());
