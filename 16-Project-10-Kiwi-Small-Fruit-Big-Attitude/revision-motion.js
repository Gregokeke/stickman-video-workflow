// Independent finite acting layers; all actions are seekable on the registered master.
const proteinSplit=DATA.schedule.find(s=>s.key==='protein');
for(const [selector,y] of [['.protein-top',-32],['.protein-bottom',32]]){tl.to('#protein '+selector,{x:0,y,rotation:0,duration:.24,ease:'power3.out'},proteinSplit.split_at);}
// Droplet follows the fiber absorption path; its arrival drives the sponge response.
tl.to('#water-drop .pose',{x:-5,y:80,scale:.90,duration:.16,ease:'power1.in'},46.10);
tl.to('#water-drop .pose',{x:-15,y:180,scale:.75,duration:.16,ease:'none'},46.26);
tl.to('#water-drop .pose',{x:-20,y:280,scale:.46,duration:.16,ease:'power2.in'},46.42);
tl.to('#water-drop',{opacity:0,duration:.12},46.60);
