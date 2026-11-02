import {ensureBrowser} from './setup_browser.mjs';
import puppeteer from 'puppeteer-core';import chromium from '@sparticuz/chromium';import {browserPath} from './browser-path.mjs';import fs from 'node:fs';import path from 'node:path';
const b=await puppeteer.launch({executablePath:await ensureBrowser(),headless:'shell',args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--allow-file-access-from-files']});
const p=await b.newPage();await p.setViewport({width:1080,height:1920});const errors=[];p.on('pageerror',e=>errors.push(e.message));
const incomplete=process.argv.includes('--incomplete');await p.goto('file://'+path.resolve(incomplete?'index-review.html':'index.html'),{waitUntil:'load'});await p.evaluate(async()=>{await document.fonts.ready;return true});
const d=JSON.parse(fs.readFileSync('audio-edits.json')),s=JSON.parse(fs.readFileSync('storyboard.json'));
const times=[.7,1.9,4.6,5.6,7.3,9.7,11.7,13.25,14.35,15.9,17.6,19.3,21.8,23.8,25.95,27.3,29.3,30.4,32.9,34.6,35.5,36.9,38.3,39.8,40.65,42,44.6,46.8,48.4,49.5,50.9,52.7,54.7,55.9,58.4,60.7,61.7,63.8,65.7,66.9,67.95,69,70.4,71.6,72.6,74.2,76.6,78.7,79.6,80.5,81.85];
fs.mkdirSync('production/review',{recursive:true});
const audits=[];
for(const t of times){await p.evaluate(t=>{window.__timelines.main.seek(t);return true},t);await p.screenshot({path:'production/review/'+t+'.jpg',type:'jpeg',quality:85});audits.push(await p.evaluate(t=>({time:t,visible:[...document.querySelectorAll('.actor')].filter(e=>+getComputedStyle(e).opacity>.8).map(e=>e.id),captions:[...document.querySelectorAll('.caption')].filter(e=>+getComputedStyle(e).opacity>.8).map(e=>e.textContent),missing:[...document.images].filter(e=>!e.complete||!e.naturalWidth).map(e=>e.src)}),t));}
fs.writeFileSync('production/review-audit.json',JSON.stringify({errors,audits},null,2));await b.close();console.log('Reviewed',times.length,'frames; errors',errors);
