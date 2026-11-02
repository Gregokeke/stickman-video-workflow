const tl=gsap.timeline({paused:true});
window.__timelines={main:tl};
const routes={left:{x:-410,y:35,scale:.94,duration:.72,ease:'power3.out'},right:{x:420,y:-20,scale:.96,duration:.74,ease:'power4.out'},rise:{x:25,y:290,scale:.88,duration:.66,ease:'power2.out'},down:{x:-20,y:-250,scale:1.05,duration:.80,ease:'sine.out'},diagonal:{x:340,y:170,scale:.83,rotation:-7,duration:.78,ease:'power3.out'}};
for(const s of DATA.schedule){
 const outer='#'+s.key,travel=outer+' .travel',pose=outer+' .pose';
 tl.to(outer,{opacity:1,duration:.15,ease:'power2.out'},s.start);
 if(s.route==='presenter'){
  const [first,tx,ty,h]=s.targets[0];
  tl.from(travel,{x:s.flip===false?-180:180,y:45,scale:.97,duration:.28,ease:'power4.out'},s.start);
  const baseL=s.x-s.w/2,baseT=s.y-s.h/2,tip=s.tip;
  for(const [t,x,y,height] of s.targets.slice(1)){
   const k=height/s.h;
   // Scale about center, then translate so the measured flipped cane tip stays on target.
   const tipAfterX=s.w/2+(tip[0]-s.w/2)*k;
   const tipAfterY=s.h/2+(tip[1]-s.h/2)*k;
   tl.to(travel,{x:x-baseL-tipAfterX,y:y-baseT-tipAfterY,scale:k,duration:.28,ease:'power3.out'},t);
  }
 }else if(s.route==='nozzle'){
  tl.fromTo(travel,{x:s.origin[0]-s.x,y:s.origin[1]-s.y,scale:.015},{x:0,y:0,scale:1,duration:.55,ease:'power2.out'},s.start);
 }else{
  tl.from(travel,{...routes[s.route],duration:s.entry_duration??routes[s.route].duration,overwrite:false},s.start);
  for(const m of s.moves)tl.to(pose,{x:m.x,y:m.y,scale:m.scale,rotation:m.rotation,duration:m.d,ease:'power2.inOut'},m.t);
 }
 // User's ordinary replacement handoff: continued travel with an EARLY fade.
 const end=s.end;
 if(end<DATA.duration-.05){
  tl.to(outer,{opacity:0,duration:.29,ease:'power2.out'},Math.max(s.start+.5,end-.29));
  const last=s.moves.at(-1)||{x:0,y:0,scale:1,rotation:0};
  if(s.route!=='presenter'&&!s.moves.some(m=>m.t+m.d>end-.34))tl.to(pose,{x:last.x+(s.route==='right'?100:-100),y:last.y+25,scale:last.scale*.97,duration:.34,ease:'power2.in'},Math.max(end-.34,s.start+.5));
 }
}
for(let i=0;i<DATA.captions.length;i++){
 const c=DATA.captions[i],id='#c'+i;
 tl.fromTo(id,{opacity:0,y:16},{opacity:1,y:0,duration:.13,ease:'power2.out'},c.start);
 tl.to(id,{opacity:0,duration:.075,ease:'none'},Math.max(c.start+.13,c.end-.075));
}
const panels=[['crash',22.59,26.1],['stable',30.27,33.15],['stress-crash',68.54,71],['insulin-low',48.4,50.22],['glycation-links',101.95,103.8]];
for(const [id,st,en] of panels){
 tl.fromTo('#'+id,{opacity:0},{opacity:1,duration:.2,ease:'power2.out'},st);
 if(document.querySelector('#'+id+' .axis'))tl.to('#'+id+' .axis',{strokeDashoffset:0,duration:.55,ease:'power2.out'},st+.15);
 if(document.querySelector('#'+id+' .curve'))tl.to('#'+id+' .curve',{strokeDashoffset:0,duration:id==='stable'?1.1:1.8,ease:'sine.inOut'},st+.55);
 if(document.querySelector('#'+id+' .plot-dot'))tl.to('#'+id+' .plot-dot',{opacity:1,duration:.15},st+2.1);
 if(!id.includes('crash')&&id!=='stable'&&document.querySelector('#'+id+' .trace'))tl.to('#'+id+' .trace',{strokeDashoffset:0,duration:.85,ease:'sine.inOut'},st+.25);
 tl.to('#'+id,{opacity:0,duration:.25},en-.25);
}
tl.fromTo('#low-fill',{scaleX:.85},{scaleX:.28,duration:1.1,ease:'power2.inOut'},48.75);

