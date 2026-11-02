(()=>{
 const S=window.FULL,tl=gsap.timeline({paused:true}),A=Object.fromEntries(S.actors.map(a=>[a.id,a])),origins=[],guideProof=[];
 const dirs={left:[-290,0],right:[290,0],high:[0,-190],low:[0,190]};
 for(const a of [...S.actors].sort((x,y)=>x.start-y.start)){
  const el=document.getElementById(a.id),d=a.entry==='emerge'?.56:.44;let from={x:0,y:0,scale:.94,opacity:0};
  if(a.entry==='first'){tl.set(el,{opacity:1,x:0,y:0,scale:1},0);tl.fromTo(el,{scale:.98},{scale:1,duration:.38,ease:'power2.out',immediateRender:false},0)}
  else{
   if(a.parent){
    tl.seek(a.start,false);const parent=document.getElementById(a.parent),r=parent.getBoundingClientRect(),origin=[r.x+r.width*a.anchor[0],r.y+r.height*a.anchor[1]];
    from={x:origin[0]-a.x,y:origin[1]-a.y,scale:.075,opacity:0};origins.push({id:a.id,parent:a.parent,start:a.start,duration:d,origin,anchor:a.anchor,parent_opacity:+getComputedStyle(parent).opacity});
   }else{const q=dirs[a.entry]||dirs.right;from.x=q[0];from.y=q[1]}
   tl.set(el,{zIndex:a.parent?4:12,opacity:0},a.start);delete from.opacity;tl.fromTo(el,from,{x:0,y:0,scale:1,duration:d,ease:a.parent?'power3.inOut':(a.entry==='high'?'expo.out':'power3.out'),immediateRender:false},a.start);tl.fromTo(el,{opacity:0},{opacity:1,duration:a.parent?.26:.25,ease:a.parent?'power2.out':'power2.in',immediateRender:false},a.start+.035);if(a.parent)tl.set(el,{zIndex:22},a.start+.14);
  }
  for(const mv of a.moves)tl.to(el,{x:mv.x-a.x,y:mv.y-a.y,scale:mv.scale,duration:mv.d,ease:'power3.out'},mv.t);
  if(a.end<S.duration){const t=a.end-.28;tl.to(el,{opacity:0,duration:.22,ease:'power2.out'},t);tl.to(el,{x:'+='+(a.x<500?-90:90),y:'+=25',duration:.32,ease:'power2.in'},t)}
 }
 if(A['power-difference']){tl.to('#bar-left-wipe',{attr:{width:330},duration:.42,ease:'power2.out'},75.39);tl.to('#bar-right-wipe',{attr:{width:450},duration:.54,ease:'power2.out'},75.53);tl.to('#power-bar-overlay',{opacity:0,duration:.08},76.10);}
 // Independent, finite explanatory accents. These do not increase art count.
 tl.to('#leg-muscle',{scaleX:1.055,scaleY:.94,duration:.17,ease:'power2.out'},51.61);tl.to('#leg-muscle',{scaleX:1,scaleY:1,duration:.22,ease:'power2.inOut'},51.94);
 tl.to('#resistance-weight',{y:-18,duration:.16,ease:'power2.out'},52.50);tl.to('#resistance-weight',{y:0,duration:.18,ease:'power2.inOut'},52.77);
 for(const[id,t]of [['genetic-helix',71.11],['childhood-photo',71.91],['horoscope-wheel',73.05],['shrinking-brain-contrast',64.85]])tl.to('#'+id+' .negation',{strokeDashoffset:0,duration:.30,ease:'none'},t);
 const path=document.getElementById('axon-signal'),len=path.getTotalLength();tl.set(path,{strokeDasharray:len,strokeDashoffset:len,opacity:0},0);tl.to(path,{strokeDashoffset:0,opacity:.9,duration:.58,ease:'none'},62.0);tl.to(path,{opacity:0,duration:.15},62.62);
 tl.set('.network-node',{opacity:0},0);document.querySelectorAll('.network-node').forEach((el,i)=>{tl.to(el,{opacity:.85,duration:.10},63.75+i*.15);tl.to(el,{opacity:0,duration:.15},63.89+i*.15)});
 tl.to('#neural-network',{scale:1.035,y:-15,duration:.34,ease:'power2.out'},64.03);
 for(const[id,t]of [['leg-reveal',10.38],['alarmed-host',66.25],['raw-leg-power',74.80],['leg-day-finale',111.45]]){if(!A[id])continue;tl.to('#'+id,{scale:1.035,duration:.22,ease:'power2.out'},t);tl.to('#'+id,{scale:1,duration:.18,ease:'power2.inOut'},t+.28)}
 for(let i=0;i<S.captions.length;i++){const c=S.captions[i];if(!i)tl.set('#'+c.id,{opacity:1,y:0},0);else tl.fromTo('#'+c.id,{opacity:0,y:14},{opacity:1,y:0,duration:.115,ease:'power2.out',immediateRender:false},c.start);tl.set('#'+c.id,{opacity:0},c.end)}
 // Measure each moving target from the actual composed artwork at every frame.
 // Then bake cane registration into the same deterministic paused timeline.
 const keys=[];const E=gsap.parseEase('power3.out'),clamp=x=>Math.max(0,Math.min(1,x));
 const point=q=>{const r=document.getElementById(q.id).getBoundingClientRect();return[r.x+r.width*q.point[0],r.y+r.height*q.point[1]]};
 for(const g of S.guides){let prev=null;const tip=[g.flip?g.native[0]-g.tip[0]:g.tip[0],g.tip[1]];
  for(let f=Math.floor(g.start*30);f<=Math.ceil(g.end*30);f++){
   const t=f/30;tl.seek(t,false);let j=0;for(let k=0;k<g.targets.length;k++)if(t>=g.targets[k].t)j=k;
   const q=g.targets[j];let p=point(q),scale=q.scale;
   if(j&&t<q.t+.23){const old=g.targets[j-1],b=point(old),v=E(clamp((t-q.t)/.23));p=[b[0]+(p[0]-b[0])*v,b[1]+(p[1]-b[1])*v];scale=old.scale+(q.scale-old.scale)*v}
   const enter=110*(1-E(clamp((t-g.start)/.35))),exit=100*E(clamp((t-(g.end-.23))/.23));
   const state={x:p[0]-tip[0]*scale-(g.flip?exit:-exit),y:p[1]-tip[1]*scale+enter+exit,scale};keys.push({id:g.id,t,state});
   if(t>=q.t+.25&&t>g.start+.4&&t<g.end-.25)guideProof.push({guide:g.id,t,target:q.id,point:p,expected_tip:p});
  }
 }
 tl.seek(0,false);
 for(const g of S.guides){const kk=keys.filter(k=>k.id===g.id);if(kk.length){tl.set('#'+g.id,kk[0].state,kk[0].t);for(let i=1;i<kk.length;i++)tl.to('#'+g.id,{...kk[i].state,duration:kk[i].t-kk[i-1].t,ease:'none'},kk[i-1].t)}tl.to('#'+g.id,{opacity:1,duration:.25,ease:'power2.out'},g.start);tl.to('#'+g.id,{opacity:0,duration:.20,ease:'power2.out'},g.end-.23)}
 tl.pause(0);window.ORIGINS=origins;window.GUIDE_PROOF=guideProof;window.__timelines=window.__timelines||{};window.__timelines['main']=tl;
})();
