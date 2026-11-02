function microGroup(sel,st,en){tl.fromTo(sel,{opacity:0},{opacity:1,duration:.18,ease:'power2.out',immediateRender:false},st);tl.to(sel,{opacity:0,duration:.23,ease:'power1.out'},en);}
function tracePath(e,st,d){const len=e.getTotalLength();tl.fromTo(e,{strokeDasharray:len,strokeDashoffset:len},{strokeDashoffset:0,duration:d,ease:'power2.inOut',immediateRender:false},st);}
microGroup('#metabolic-levels',12.86+.30,15.02);
tl.fromTo('.level-fill',{attr:{y:1090,height:220}},{attr:{y:1255,height:55},duration:.45,ease:'power2.inOut',immediateRender:false},13.88);
for(const [id,at] of [['survival',15.28],['healing-switch',62.58]]){
 if(!document.querySelector('#'+id))continue;
 tl.fromTo('#'+id+' .switch-knob',{y:-24,rotationX:-24,backgroundColor:'#fff'},{y:24,rotationX:24,backgroundColor:'#ff0000',duration:.38,ease:'power3.inOut',immediateRender:false},at);
 tl.to('#'+id+' .switch-off',{opacity:0,duration:.1},at+.10);tl.to('#'+id+' .switch-on',{opacity:1,duration:.12},at+.22);
}

if(document.querySelector('#divide')){tl.to('#divide .division-left',{x:-28,duration:.42,ease:'power2.inOut'},67.78);tl.to('#divide .division-right',{x:28,duration:.42,ease:'power2.inOut'},67.78);}
microGroup('#repair-fibers',71.36,71.9);for(const e of document.querySelectorAll('#repair-fibers path'))tracePath(e,71.38,.32);
tl.seek(0);
