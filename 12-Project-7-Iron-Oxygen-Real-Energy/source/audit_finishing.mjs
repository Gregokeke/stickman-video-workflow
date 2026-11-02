import puppeteer from 'puppeteer-core';import chromium from '@sparticuz/chromium';import {browserPath}from'./browser-path.mjs';import path from'node:path';import{writeFile}from'node:fs/promises';
const b=await puppeteer.launch({executablePath:browserPath(),headless:'shell',args:chromium.args});try{
 const p=await b.newPage();await p.setViewport({width:1080,height:1920});await p.goto('file://'+path.resolve('index.html'),{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);
 const checks=[];for(const [t,n]of [[42.2,5],[42.65,4],[42.95,3],[43.27,2],[43.65,1]]){
  const got=await p.evaluate(t=>{window.__timelines.main.seek(t);return [...document.querySelectorAll('.bar-fill')].filter(e=>+gsap.getProperty(e,'scaleY')>.5).length},t);if(got!==n)throw Error(`Battery ${t}: ${got} vs ${n}`);checks.push({time:t,filled_bars:got});
 }
 const search=await p.evaluate(()=>{window.__timelines.main.seek(93.5);return {typed:[...document.querySelectorAll('.search-text span')].filter(e=>+gsap.getProperty(e,'opacity')>.9).map(e=>e.textContent).join(''),icon:document.querySelector('#actual-app-icon').getAttribute('src'),iconVisible:+gsap.getProperty('#app-icon-window','opacity'),cursorHidden:+gsap.getProperty('#typing-cursor','opacity')===0,missing:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),slashOffset:gsap.getProperty('#crossing-slash','strokeDashoffset')}});
 if(search.typed!=='Remea'||search.iconVisible!==1||search.missing.length||!search.cursorHidden)throw Error(JSON.stringify(search));
 await writeFile('production/finishing-audit.json',JSON.stringify({battery:checks,search,passed:true},null,2));console.log('Finishing audit passed',JSON.stringify({battery:checks,search}));
}catch(e){console.error(e);process.exitCode=1}finally{await b.close()}
