const tl=gsap.timeline({paused:true});window.__timelines={main:tl};
// Separate entrance, connected posing and handoff layers keep each motion continuous.
const routes={state:{x:0,y:0,scale:1,duration:.24,ease:'sine.out'},
 left:{x:-350,y:25,scale:.94,duration:.58,ease:'power3.out'},
 right:{x:350,y:20,scale:.95,duration:.58,ease:'power3.out'},
 rise:{x:0,y:230,scale:.94,duration:.58,ease:'power3.out'},
 depth:{x:-35,y:65,scale:.70,duration:.62,ease:'power3.out'},
 diagonal:{x:280,y:155,scale:.88,rotation:-5,duration:.62,ease:'power3.out'},
 down:{x:0,y:-180,scale:1.02,duration:.55,ease:'power2.out'},
 arcLeft:{x:-340,y:125,scale:.9,rotation:3,duration:.64,ease:'power3.out'},
 arcRight:{x:340,y:105,scale:.91,rotation:-3,duration:.64,ease:'power3.out'},
 reveal:{x:-55,y:125,scale:.77,duration:.64,ease:'power2.out'},
 peek:{x:-90,y:560,scale:.98,duration:.55,ease:'power3.out'}
};
const exits={right:{x:185,y:35,scale:.94},left:{x:-185,y:35,scale:.94},up:{x:0,y:-125,scale:.98},sink:{x:-65,y:360,scale:.98},recede:{x:45,y:55,scale:.84}};
for(const s of DATA.schedule){
 const out='#'+s.key,tr=out+' .travel',pose=out+' .pose',handoff=out+' .handoff';
 tl.to(out,{opacity:1,duration:s.route==='peek'?.08:.14,ease:'power1.out'},s.start);
 if(s.route==='presenter'){
  tl.set(out+' .flip',{scaleX:s.flip?-1:1,scaleY:1,rotation:0},s.start);
  tl.from(tr,{x:s.flip?150:-150,y:30,scale:.98,duration:.32,ease:'power3.out',immediateRender:false},s.start);
  const l=s.x-s.w/2,t=s.y-s.h/2;
  for(const[at,x,y,height,d=.28,ease='power3.out',flip=s.flip]of s.targets.slice(1)){
   const k=height/s.h,tx=flip===s.flip?s.tip[0]:s.w-s.tip[0],px=s.w/2+(tx-s.w/2)*k,py=s.h/2+(s.tip[1]-s.h/2)*k;
   tl.to(tr,{x:x-l-px,y:y-t-py,scale:k,duration:d,ease},at);
   if(flip!==s.flip)tl.to(out+' .flip',{scaleX:flip?-1:1,duration:d,ease},at);
  }
 }else{
  if(s.route==='emerge'){
   const source=DATA.schedule.find(q=>q.key===s.emerge_from);
   const prior=source?.moves.filter(m=>m.t+m.d<=s.start+.01).at(-1)||{x:0,y:0};
   tl.from(tr,{x:source?source.x+prior.x-s.x:0,y:source?source.y+prior.y-s.y:100,scale:.20,rotation:3,duration:.62,ease:'power3.inOut',immediateRender:false},s.start);
  }else tl.from(tr,{...routes[s.route],duration:s.entry_duration??routes[s.route].duration,immediateRender:false},s.start);
  for(const m of s.moves)tl.to(pose,{x:m.x,y:m.y,scale:m.scale,rotation:m.rotation,duration:m.d,ease:m.ease||'power3.inOut'},m.t);
 }
 if(s.handoff<DATA.duration-.05){
  // A matched outward travel and early overlap fade are the scene transition.
  tl.to(handoff,{...(exits[s.exit]||exits.recede),duration:.44,ease:'power2.inOut'},s.handoff);
  tl.to(out,{opacity:0,duration:.275,ease:'power1.out'},s.handoff+.025);
 }
}
for(let i=0;i<DATA.captions.length;i++){const c=DATA.captions[i];tl.fromTo('#c'+i,{opacity:0,y:11},{opacity:1,y:0,duration:.11,ease:'power2.out',immediateRender:false},c.start);tl.to('#c'+i,{opacity:0,duration:.06,ease:'none'},c.end-.06);}

