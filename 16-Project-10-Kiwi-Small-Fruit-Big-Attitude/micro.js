function explain(id,st,en){tl.fromTo(id,{opacity:0,y:8},{opacity:1,y:0,duration:.12,ease:'power2.out',immediateRender:false},st);tl.to(id,{opacity:0,duration:.16},en-.16)}
// All paths begin hidden, even before their own draw cue. Never flash complete strokes.
function draw(id,st,d=.4){const e=document.querySelector(id),l=e.getTotalLength();tl.set(id,{opacity:0,strokeDasharray:l,strokeDashoffset:l},0);tl.set(id,{opacity:1},st);tl.to(id,{strokeDashoffset:0,duration:d,ease:'power2.inOut'},st);return l}
explain('#versus',10.066,15.05);draw('#vs-slash',10.12,.34);tl.to('#vs-content',{y:-210,duration:.32,ease:'power3.inOut'},12.744);
explain('#heartbeat',17.03,18.166);draw('#pulse-line',17.08,.62);tl.to('#pulse-line',{opacity:.45,duration:.09,repeat:3,yoyo:true},17.73);
explain('#dna-build',19.006,20.362);draw('#dna-path',19.006,.60);
explain('#vitamin-e-gauge',25.645,28.705);tl.set('#e-fill',{scaleX:1,svgOrigin:'145 656'},0);tl.to('#e-fill',{scaleX:0,duration:.55,ease:'power2.inOut'},26.205);tl.to('#e-zero',{opacity:1,duration:.12},26.755);
explain('#vitamin-e-negation',27.765,28.705);draw('#e-slash',27.765,.27);
explain('#seed-route',37.174,39.434);draw('#seed-oil-route',37.174,.65);
explain('#fiber-grams',43.843,45.223);for(let i=0;i<4;i++){tl.set('#gram'+i,{scaleY:0,svgOrigin:`${200+i*155} 690`},0);tl.to('#gram'+i,{scaleY:1,duration:.28,ease:'power2.out'},43.843+i*.12)}
explain('#water-holding',46.10,46.94);const waterLength=draw('#water-route',46.10,.43);tl.to('#water-route',{strokeDashoffset:-waterLength,duration:.30,ease:'power2.in'},46.53);
explain('#gut-sweep',47.30,48.676);draw('#gut-route',47.30,.92);
const gutPath=document.querySelector('#gut-route'),gutLength=gutPath.getTotalLength();const gp=gutPath.getPointAtLength(0);tl.set('#bolus',{x:gp.x,y:gp.y},0);
for(let i=1;i<=24;i++){const p=gutPath.getPointAtLength(gutLength*i/24);tl.to('#bolus',{x:p.x,y:p.y,duration:.92/24,ease:'none'},47.30+(i-1)*.92/24)}
tl.set('#sweep-dirt',{opacity:0},0);tl.to('#sweep-dirt',{opacity:1,duration:.05},48.20);for(let i=0;i<9;i++)tl.to('#dirt'+i,{x:(i%3-1)*48,y:70+i*6,scale:.25,opacity:0,duration:.28,ease:'power2.out'},48.24+i*.012);
explain('#fiber-population',49.416,54.016);for(let i=0;i<20;i++)tl.from('#person'+i,{opacity:0,scale:.5,transformOrigin:'center',duration:.2,immediateRender:false},49.416+i*.035);
explain('#trial-chart',62.967,66.267);tl.set('#trial-after',{scaleY:0,svgOrigin:'645 920'},0);tl.to('#trial-after',{scaleY:1,duration:.7,ease:'power2.inOut'},63.267);
explain('#toilet-clock',66.927,68.287);tl.fromTo('#toilet-minute',{rotation:0,svgOrigin:'750 750'},{rotation:240,duration:.9,ease:'power2.inOut',immediateRender:false},66.927);
explain('#sleep-gauge',75.817,77.677);tl.set('#sleep-fill',{scaleX:.25,svgOrigin:'150 645'},0);tl.to('#sleep-fill',{scaleX:.90,duration:1.1,ease:'power2.inOut'},75.817);
explain('#melatonin-route',80.697,83.475);draw('#melatonin-link',80.697,.35);draw('#melatonin-arrow',81.047,.2);
explain('#carb-fuel',92.18,92.843);draw('#fuel-route',92.18,.36);draw('#fuel-arrowhead',92.54,.1);
explain('#fiber-steady',92.843,94.303);draw('#steady-axis',92.843,.25);draw('#steady-line',93.02,.65);
explain('#cleavage',98.97,100.171);draw('#peptide-arrow',98.99,.42);draw('#peptide-arrowhead',99.41,.08);
