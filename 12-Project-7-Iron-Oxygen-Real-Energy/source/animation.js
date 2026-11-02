const tl=gsap.timeline({paused:true});window.__timelines={main:tl};
const routes={'lower-left':{x:-240,y:480,scale:.96,duration:.46,ease:'power3.out'},left:{x:-410,y:25,scale:.95,duration:.60,ease:'power3.out'},right:{x:410,y:-15,scale:.96,duration:.62,ease:'power4.out'},rise:{x:20,y:270,scale:.89,duration:.56,ease:'power2.out'},depth:{x:0,y:50,scale:.74,duration:.56,ease:'power3.out'},down:{x:-20,y:-240,scale:1.04,duration:.62,ease:'sine.out'},diagonal:{x:330,y:160,scale:.86,rotation:-5,duration:.62,ease:'power3.out'}};
for(const s of DATA.schedule){
 const outer='#'+s.key,travel=outer+' .travel',pose=outer+' .pose';
 tl.to(outer,{opacity:1,duration:.13,ease:'power2.out'},s.start);
 if(s.route==='presenter'){
  tl.from(travel,{x:s.flip?150:-150,y:35,scale:.98,duration:.28,ease:'power4.out',immediateRender:false},s.start);
  const l=s.x-s.w/2,t=s.y-s.h/2;
  for(const [at,x,y,height]of s.targets.slice(1)){
   const k=height/s.h,px=s.w/2+(s.tip[0]-s.w/2)*k,py=s.h/2+(s.tip[1]-s.h/2)*k;
   tl.to(travel,{x:x-l-px,y:y-t-py,scale:k,duration:.28,ease:'power3.out'},at);
  }
 }else{
  const r={...routes[s.route],duration:s.entry_duration??routes[s.route].duration,immediateRender:false};
  // Related app screens keep a stable phone-sized footprint and settle promptly.
  if(s.asset.startsWith('phone-')&&s.asset!=='phone-scan')Object.assign(r,{x:s.route==='left'?-140:140,y:0,scale:.985,duration:s.entry_duration??.45});
  tl.from(travel,r,s.start);
  for(const m of s.moves)tl.to(pose,{x:m.x,y:m.y,scale:m.scale,rotation:m.rotation,duration:m.d,ease:m.ease||'power2.inOut'},m.t);
 }
 if(s.handoff<DATA.duration-.05){
  // Match reference six: begin transparency during the incoming movement, never after it settles.
  tl.to(outer,{opacity:0,duration:.24,ease:'power2.out'},s.handoff+.025);
  if(s.route!=='presenter'&&!s.moves.some(m=>m.t+m.d>s.handoff-.05)){
   const last=s.moves.at(-1)||{x:0,y:0,scale:1,rotation:0};
   tl.to(pose,{x:last.x+(s.route==='right'?110:-110),y:last.y+25,scale:last.scale*.96,duration:.32,ease:'power2.in'},s.handoff);
  }
 }
}
for(let i=0;i<DATA.captions.length;i++){
 const c=DATA.captions[i],id='#c'+i;
 tl.fromTo(id,{opacity:0,y:13},{opacity:1,y:0,duration:.11,ease:'power2.out',immediateRender:false},c.start);
 tl.to(id,{opacity:0,duration:.065,ease:'none'},c.end-.065);
}
function trace(id,st,en,d=.35){const e=document.querySelector(id),len=e.getTotalLength();tl.fromTo(id,{opacity:0,strokeDasharray:len,strokeDashoffset:len},{opacity:1,strokeDashoffset:0,duration:d,ease:'power2.inOut',immediateRender:false},st);tl.to(id,{opacity:0,duration:.18},en-.18);}
trace('#lung-brain',22.22,23.58,.30);trace('#lung-muscle',22.80,23.58,.28);
trace('#equals-lines',40.08,41.74,.2);trace('#crossing-slash',40.48,41.74,.3);
// Drain exactly four of the five independently outlined cells, right to left.
for(const [j,t]of [[4,42.4],[3,42.72],[2,43.04],[1,43.36]])tl.to('#battery-bar-'+j,{scaleY:0,duration:.18,ease:'power2.in'},t);
// Type the real app name; keep the completed search and actual icon readable through the CTA.
tl.set('#typing-cursor',{x:DATA.typing_widths[0]},92.22);
for(let j=0;j<5;j++){tl.set('#search-letter-'+j,{opacity:1},92.30+j*.14);tl.set('#typing-cursor',{x:DATA.typing_widths[j+1]},92.30+j*.14);}
for(let j=0;j<6;j++)tl.set('#typing-cursor',{opacity:j%2===0?1:0},92.22+j*.16);
tl.set('#typing-cursor',{opacity:0},93.16);
tl.fromTo('#app-icon-window',{opacity:0,scale:.93},{opacity:1,scale:1,duration:.25,ease:'power2.out',immediateRender:false},93.08);
// The scanner line is a child of the actual phone silhouette and follows every transform.
tl.fromTo('#scan .scan-line',{opacity:0,y:0},{opacity:.9,y:270,duration:.7,ease:'sine.inOut',immediateRender:false},62.55);tl.to('#scan .scan-line',{opacity:0,duration:.13},63.25);
// One finite membrane-to-cell uptake, anchored between the two settled illustrations.
// Keep the route invisible: only the nutrient travels from villus wall to cell rim.
const path=document.querySelector('#absorb-route'),len=path.getTotalLength();
tl.set('#nutrient-particle',{opacity:1,x:0,y:0},83.1);
for(let i=1;i<=24;i++){let p=path.getPointAtLength(len*i/24);tl.to('#nutrient-particle',{x:p.x-450,y:p.y-1000,duration:.025,ease:'none'},83.1+(i-1)*.025);}
tl.to('#nutrient-particle',{opacity:0,duration:.12},83.72);
tl.seek(0);
