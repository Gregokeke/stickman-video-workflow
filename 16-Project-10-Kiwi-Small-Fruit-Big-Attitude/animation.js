const tl=gsap.timeline({paused:true});window.__timelines={main:tl};
const routes={left:{x:-340,y:25,scale:.92,duration:.5,ease:'power3.out'},right:{x:340,y:20,scale:.93,duration:.52,ease:'power4.out'},rise:{x:0,y:230,scale:.91,duration:.55,ease:'power2.out'},behind:{x:-65,y:140,scale:.67,duration:.5,ease:'power3.out'},depth:{x:0,y:35,scale:.70,duration:.5,ease:'expo.out'},diagonal:{x:310,y:165,scale:.85,rotation:-4,duration:.56,ease:'power3.out'},down:{x:0,y:-220,scale:1.035,duration:.55,ease:'sine.out'}};
for(const s of DATA.schedule){
 const out='#'+s.key,tr=out+' .travel',pose=out+' .pose';
 tl.to(out,{opacity:1,duration:.13,ease:'power2.out'},s.start);
 if(s.route==='presenter'){
  tl.from(tr,{x:s.entry_x??(s.flip?150:-150),y:s.entry_y??35,scale:s.entry_scale??.98,duration:s.entry_duration??.28,ease:'power4.out',immediateRender:false},s.start);
  const l=s.x-s.w/2,t=s.y-s.h/2;
  for(const[at,x,y,height,d=.28,ease='power3.out']of s.targets.slice(1)){const k=height/s.h,px=s.w/2+(s.tip[0]-s.w/2)*k,py=s.h/2+(s.tip[1]-s.h/2)*k;tl.to(tr,{x:x-l-px,y:y-t-py,scale:k,duration:d,ease},at);}
 }else{
  tl.from(tr,{...routes[s.route],duration:s.entry_duration??routes[s.route].duration,immediateRender:false},s.start);
  for(const m of s.moves)tl.to(pose,{x:m.x,y:m.y,scale:m.scale,rotation:m.rotation,duration:m.d,ease:m.ease||'power2.inOut'},m.t);
 }
 if(s.handoff<DATA.duration-.05){
  tl.to(out,{opacity:0,duration:s.exit_duration??.26,ease:'power2.out'},s.handoff+.025);
  if(!s.exit_via_travel&&s.route!=='presenter'&&!s.moves.some(m=>m.t+m.d>s.handoff-.05)){const m=s.moves.at(-1)||{x:0,y:0,scale:1};tl.to(pose,{x:m.x+(s.route==='right'?-145:145),y:m.y+35,scale:m.scale*.88,duration:.4,ease:'power2.inOut'},s.handoff);}
 }
}
for(let i=0;i<DATA.captions.length;i++){const c=DATA.captions[i];tl.fromTo('#c'+i,{opacity:0,y:15},{opacity:1,y:0,duration:.11,ease:'power2.out',immediateRender:false},c.start);tl.set('#c'+i,{opacity:0},c.end);}
tl.seek(0);
