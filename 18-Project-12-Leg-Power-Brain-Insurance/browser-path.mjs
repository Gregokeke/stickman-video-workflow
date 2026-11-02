import fs from 'node:fs';import os from 'node:os';import path from 'node:path';
export function browserPath(){
 if(process.env.CHROME_PATH&&fs.existsSync(process.env.CHROME_PATH))return process.env.CHROME_PATH;
 if(fs.existsSync(path.resolve('.browser/chromium')))return path.resolve('.browser/chromium');
 const local=path.resolve('.browser/chrome-headless-shell-linux64/chrome-headless-shell');if(fs.existsSync(local))return local;
 const base=path.join(os.homedir(),'.cache/hyperframes/chrome/chrome-headless-shell');
 if(fs.existsSync(base))for(const version of fs.readdirSync(base)){const p=path.join(base,version,'chrome-headless-shell-linux64/chrome-headless-shell');if(fs.existsSync(p))return p}
 for(const p of ['/usr/bin/chromium','/usr/bin/google-chrome'])if(fs.existsSync(p))return p;
 throw Error('Set CHROME_PATH to an installed Chromium executable.');
}
