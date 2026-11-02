function microGroup(sel,st,en){tl.fromTo(sel,{opacity:0,y:14},{opacity:1,y:0,duration:.2,ease:'power2.out',immediateRender:false},st);tl.to(sel,{opacity:0,duration:.23,ease:'power1.out'},en);}
function tracePath(e,st,d){const len=e.getTotalLength();tl.fromTo(e,{strokeDasharray:len,strokeDashoffset:len},{strokeDashoffset:0,duration:d,ease:'power2.inOut',immediateRender:false},st);}
microGroup('#study-count',25.32,27.22);
const adults={value:0};tl.to(adults,{value:25000,duration:.62,ease:'power3.out',onUpdate:()=>document.querySelector('#adult-count').textContent=Math.round(adults.value).toLocaleString('en-US')+'+'},25.32);
microGroup('#heart-half',29.94,31.32);microGroup('#eye-stat',51.66,52.96);microGroup('#kidney-half',72.36,73.74);microGroup('#muscle-stat',130.04,132.52);
microGroup('#atp-battery',115.92,117.86);microGroup('#atp-battery',122.52,124.05);
const bars=[...document.querySelectorAll('.energy-bar')];
for(let i=4;i>=1;i--)tl.to(bars[i],{fill:'#fff',duration:.14,ease:'none'},116.72+(4-i)*.20);
for(let i=1;i<=4;i++)tl.to(bars[i],{fill:'#ff0000',duration:.14,ease:'none'},122.60+(i-1)*.20);
tl.seek(0);
