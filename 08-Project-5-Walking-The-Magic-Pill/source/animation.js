const tl=gsap.timeline({paused:true,defaults:{ease:'power3.inOut'}});
// Each entrance has a narrative role. The travel layer handles handoffs;
// the nested pose layer carries center/side/return choreography.
const entrance={
 'death-hourglass':['stat',.45],'cane-presenter-left':['right',.65],'happy-pill-pop':['right',.62],'pill-refusal':['left',.68],'legs-exasperated':['close',.58],'pharma-salesman':['left',.7],'extra-pill-stack':['rise',.65],
 'zero-effects':['depth',.48],'eager-buyer':['right',.65],
 'sarcastic-presenter':['left',.62],'confused':['depth',.7],
 'coffee-sip':['close',.6],'couch-slouch':['left',.58],
 'walking-hero':['right',.72],'lab-scientist':['rise',.6],
 'research-participants':['rise',.55],'doorstep-shuffle':['left',.85],
 'doorstep-handoff':['right',.7],'long-distance-walker':['left',.72],
 'horizontal-dread':['close',.7],'cane-presenter':['left',.6],
 'bribe-handoff':['right',.78],'reaper-look-away':['left',.65],
 'offended-professor':['close',.5],'bottom-marinate':['left',.7],
 'top-energetic':['right',.65],'shocked-comparison':['depth',.65],
 'rotting-bed':['left',.75],'mattress-winner':['rise',.7],
 'smoking-reject':['depth',.55],'marching-person':['left',.7],
 'sprint':['right',.55],'average-slow':['left',.7],
 'exhausted-drag':['left',.85],'tying-shoes':['close',.65],
 'doorway-walk':['right',.72],'magic-pill-reveal':['depth',.75],
 'pallbearers-six':['left',.8]
};
function poseMove(a,at,vars,d=.7){tl.to('#'+a.key+' .pose',{...vars,duration:d,ease:'power2.inOut'},at)}
for(const a of DATA.schedule){
 const root='#'+a.key,travel=root+' .travel',pose=root+' .pose';
 let [mode,d]=entrance[a.asset]??[a.role==='support'?'rise':'right',.56];
 let from=mode==='stat'?{x:90}:mode==='left'?{x:-540}:mode==='right'?{x:540}:mode==='rise'?{y:150}:mode==='close'?{scale:1.12,y:25}:{scale:.86,y:65};
 tl.fromTo(root,{opacity:0},{opacity:1,duration:a.asset==='death-hourglass'?.45:.23,ease:a.asset==='death-hourglass'?'power3.out':'sine.out',immediateRender:false},a.start);
 tl.fromTo(travel,from,{x:0,y:0,scale:1,duration:d,ease:mode==='depth'?'power2.out':'power3.out',immediateRender:false},a.start);
 const exit=a.end-.28;
 tl.to(travel,{x:mode==='left'?165:-165,y:-15,duration:.36,ease:'power2.in'},exit-.04);
 tl.to(root,{opacity:0,duration:.28,ease:'sine.in'},exit);tl.set(root,{opacity:0},a.end+.02);
 if(a.asset==='pharma-salesman')poseMove(a,2.65,{x:-145,y:30,scale:.8},.65);
 if(a.asset==='cane-presenter-left'){tl.set(pose,{y:0},a.start);poseMove(a,6.08,{y:95.04},.88)}
 if(a.asset==='confused')poseMove(a,16.42,{x:295,y:345,scale:.38},.72);
 // Stable center -> side -> center. Labels remain large in their own column.
 if(['long-distance-walker','marching-person','average-slow'].includes(a.asset)){
  const start=a.asset==='long-distance-walker'?37.98:a.asset==='marching-person'?90.92:95.95;
  poseMove(a,start,{x:-155,y:35,scale:.83},.65);
  if(a.asset==='long-distance-walker')poseMove(a,40.55,{x:0,y:0,scale:1},.8);
 }
 if(a.asset==='walking-hero'&&a.start>110){
  tl.set(pose,{x:-155,y:40,scale:.82},a.start);
  poseMove(a,112.95,{x:0,y:0,scale:1},.85);
 }
 // One coherent held illustration first; a second concept earns shared space.
 if(a.asset==='bottom-marinate')poseMove(a,61.76,{x:-190,y:20,scale:.63},.8);
 if(a.asset==='rotting-bed')poseMove(a,80.05,{x:-160,y:15,scale:.70},.72);
 if(a.asset==='mattress-winner')poseMove(a,84.43,{x:-140,y:10,scale:.84},.65);
 // Presenter returns to full frame after the literal sink leaves.
 if(a.asset==='sarcastic-presenter'&&a.start>75&&a.start<78)poseMove(a,77.08,{x:215,y:0,scale:1.28},.68);
 // The cane tip tracks the actual reduction, not an arbitrary location.
 if(a.asset==='cane-presenter'&&a.start<60){tl.set(pose,{x:58},a.start);poseMove(a,49.9,{x:0},1.2)}
 if(a.asset==='doorstep-shuffle')poseMove(a,33.45,{x:55},1.05);
 if(a.asset==='offended-professor')poseMove(a,58.65,{scale:1.08,y:-20},.4);
 if(a.asset==='shocked-comparison')poseMove(a,68.85,{scale:1.09,y:-22},.5);
 // The conclusion travels with the depicted action, then holds the punchline.
 if(a.asset==='doorway-walk')poseMove(a,117.2,{x:65},.8);
 if(a.asset==='pallbearers-six')poseMove(a,123.45,{x:32},1.1);
}
for(let i=0;i<DATA.captions.length;i++){
 const g=DATA.captions[i],sel='#c'+i,d=Math.min(.1,(g.end-g.start)/3);
 tl.fromTo(sel,{opacity:0,y:9},{opacity:1,y:0,duration:d,ease:'power2.out',immediateRender:false},g.start);
 tl.to(sel,{opacity:0,duration:.065,ease:'sine.in'},Math.max(g.start+d,g.end-.065));
 tl.set(sel,{opacity:0},g.end);
}
function diagram(sel,start,end){
 tl.fromTo(sel,{opacity:0,y:35},{opacity:1,y:0,duration:.35,ease:'power3.out',immediateRender:false},start);
 tl.to(sel,{opacity:0,duration:.25,ease:'sine.in'},end-.25);tl.set(sel,{opacity:0},end);
}
diagram('#pill-example',4.52,8.95);
tl.fromTo('#pill-example .gauge-fill',{scaleY:.88},{scaleY:.76,duration:.88,ease:'power2.inOut',immediateRender:false},6.08);
tl.fromTo('#pill-example .gauge-level',{y:0},{y:95.04,duration:.88,ease:'power2.inOut',immediateRender:false},6.08);
tl.to('#pill-example .pill-88',{opacity:0,duration:.15},6.65);
tl.fromTo('#pill-example .pill-76',{opacity:0},{opacity:1,duration:.22,immediateRender:false},6.76);
tl.fromTo('#pill-example .pill-difference',{opacity:0,y:18},{opacity:1,y:0,duration:.35,ease:'power3.out',immediateRender:false},6.76);
diagram('#steps',28.08,30.85);
tl.fromTo('.category-bar',{scaleY:0},{scaleY:1,duration:.6,stagger:.07,ease:'power3.out',immediateRender:false},28.2);
tl.fromTo('#steps span',{opacity:0,y:12},{opacity:1,y:0,duration:.24,stagger:.07,immediateRender:false},28.35);
tl.fromTo('.step-pointer',{opacity:0,x:60},{opacity:1,x:0,duration:.42,immediateRender:false},29.1);
diagram('#relative',45.15,52.6);
tl.fromTo('#relative .chart-title',{opacity:0,y:15},{opacity:1,y:0,duration:.35,immediateRender:false},46.15);
tl.fromTo('#relative .base',{scaleX:0},{scaleX:1,duration:.65,ease:'power2.out',immediateRender:false},46.4);
tl.fromTo('#relative .reduced',{scaleX:0},{scaleX:1,duration:.65,ease:'power2.out',immediateRender:false},47.05);
tl.to('#relative .reduced',{scaleX:.88,duration:1.2,ease:'power3.inOut'},49.9);
tl.fromTo('#relative .takeaway',{opacity:0,y:25},{opacity:1,y:0,duration:.42,ease:'power3.out',immediateRender:false},51.1);
tl.fromTo('#relative .qualifier',{opacity:0},{opacity:1,duration:.3,immediateRender:false},45.35);
tl.fromTo('#relative .relative-row:last-child b',{opacity:0},{opacity:1,duration:.3,immediateRender:false},51.1);
for(const [sel,start,end,n,reveal] of [['#ratio3',63.65,67.35,3,65.0],['#ratio2',71.3,75.35,2,73.0]]){
 diagram(sel,start,end);
 tl.fromTo(sel+' .unit',{opacity:0,y:25},{opacity:1,y:0,duration:.32,stagger:.14,ease:'power3.out',immediateRender:false},start+.25);
 tl.fromTo(sel+' .multiplier',{opacity:0,scale:.88},{opacity:1,scale:1,duration:.45,ease:'power3.out',immediateRender:false},reveal);
}
diagram('#progress',102.7,110.55);
tl.fromTo('#progress .progress-fill',{scaleX:.08},{scaleX:.68,duration:2.3,ease:'power2.inOut',immediateRender:false},103.05);
tl.fromTo('#progress .progress-marker',{x:20},{x:455,duration:2.3,ease:'power2.inOut',immediateRender:false},103.05);
tl.fromTo('#progress .takeaway',{opacity:0,y:22},{opacity:1,y:0,duration:.48,ease:'power3.out',immediateRender:false},108.7);
tl.fromTo('#progress .qualifier',{opacity:0},{opacity:1,duration:.3,immediateRender:false},108.95);
tl.fromTo('#hookstat',{opacity:0,x:90},{opacity:1,x:0,duration:.45,ease:'power3.out',immediateRender:false},3.1);
tl.to('#hookstat',{opacity:0,duration:.28},4.58);
window.__timelines=window.__timelines||{};window.__timelines.main=tl;
