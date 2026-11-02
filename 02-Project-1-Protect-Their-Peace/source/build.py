from pathlib import Path
import json,html,shutil,subprocess,wave
import numpy as np
p=Path(__file__).parent
words=json.loads((p/'words.json').read_text());duration=36.70
# Repair token splitting for readable captions without altering the spoken wording.
for i,w in enumerate(words):
 if w['word']=='band' and i+1<len(words) and words[i+1]['word']=='-aid':
  w['word']='band-aid';w['end']=words[i+1]['end'];words[i+1]['word']=''
words=[w for w in words if w['word']]
# Deliberately phrased captions; every spoken word retained.
groups=["It's wildly selfish","to spot a loving,","cheerful, genuine person","and think, nice,","a peaceful life to ruin","with my trauma.","You saw their light,","and instead of protecting it,","you went full emotional vampire","and drained it.","You dumped your chaos","into their calm,","and had the nerve","to call it connection.","Spoiler, that's not love.","That's using someone","as a human band-aid","for wounds you're too lazy","to heal.","The darkest part,","they were perfectly fine","before you spawned.","So if you're not ready,","leave people alone.","Go heal what's broken","before you hand your damage","to someone else,","because the piece of them","you kill might stay dead forever."]
cap=[];idx=0
for g in groups:
 n=len(g.split());chunk=words[idx:idx+n];idx+=n
 if not chunk: continue
 cap.append({'text':' '.join(w['word'] for w in chunk),'start':chunk[0]['start'],'end':chunk[-1]['end']})
assert idx==len(words),(idx,len(words))
for i,c in enumerate(cap):c['end']=cap[i+1]['start'] if i+1<len(cap) else duration
(p/'captions.json').write_text(json.dumps(cap,indent=2))
# Sample library effects; locally mixed once, no new provider generations.
sfx=p/'assets/sfx'
cue=[(.08,'whoosh-short',.7,-24),(4.75,'whoosh',.65,-22),(5.62,'impact-bass-1',.7,-23),(8.52,'chime',1.0,-28),(11.18,'whoosh-cinematic',.8,-22),(13.22,'impact-bass-2',.6,-21),(14.12,'glitch-1',.55,-25),(17.9,'click',.2,-20),(18.86,'impact-bass-1',.75,-20),(20.5,'whoosh-short',.5,-23),(24.67,'chime',.8,-28),(27.25,'impact-bass-2',.5,-23),(29.02,'click',.25,-19),(30.14,'whoosh-short',.6,-24),(33.63,'impact-bass-1',.8,-24),(35.64,'whoosh',.55,-26)]
def read_audio(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ac','1','-ar','48000','-f','f32le','-']),dtype=np.float32).copy()
narr=read_audio(p/'assets/narration.wav');mix=np.zeros(round(duration*48000),dtype=np.float32);nrms=np.sqrt(np.mean(narr*narr));narr=narr*(10**(-20/20)/max(nrms,1e-7));mix[:len(narr)]+=narr
fx=np.zeros_like(mix)
for t,name,limit,db in cue:
 a=read_audio(sfx/(name+'.mp3'))[:int(limit*48000)];rms=np.sqrt(np.mean(a*a));a*=10**(db/20)/max(rms,1e-7)
 fade=min(1800,len(a)//3);a[:250]*=np.linspace(0,1,250);a[-fade:]*=np.linspace(1,0,fade)
 start=round(t*48000);end=min(start+len(a),len(fx));fx[start:end]+=a[:end-start]
mix+=fx;peak=np.max(np.abs(mix));mix*=min(1,.94/max(peak,.001))
def savewave(name,a):
 with wave.open(str(p/'assets'/name),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(48000);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
savewave('mix.wav',mix);savewave('effects.wav',fx);(p/'sound-cues.json').write_text(json.dumps(cue,indent=2));shutil.copy(sfx/'CREDITS.md',p/'SFX-CREDITS.md')
style='''@font-face{font-family:Caption;src:url('assets/caption-bold.ttf') format('truetype');font-weight:700}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#fff}#root{position:relative;width:1080px;height:1920px;background:#fff;overflow:hidden;font-family:Caption,Arial,sans-serif;color:#111}.shade{position:absolute;inset:-20px;z-index:9;pointer-events:none;box-shadow:inset 95px 0 120px -40px #0009,inset -95px 0 120px -40px #0009,inset 0 65px 95px -40px #0006,inset 0 -65px 95px -40px #0006}.asset{position:absolute;left:140px;top:560px;width:800px;height:1080px;opacity:0;transform-origin:50% 70%}.asset img{width:100%;height:100%;object-fit:contain;display:block}.caption{position:absolute;left:115px;top:235px;width:850px;height:240px;z-index:12;display:flex;align-items:center;justify-content:center;opacity:0;text-align:center;line-height:1.12;font-size:61px;font-weight:700;font-style:italic;text-transform:uppercase;letter-spacing:-2px}.caption span{display:inline-block;max-width:850px;transform:scaleX(.88)}.caption b{color:#e10a10}.label{position:absolute;z-index:8;opacity:0;font-weight:700;font-size:49px;line-height:1.05;letter-spacing:-2px}.label strong{color:#ed0b10}.connection{left:600px;top:1020px;width:340px;transform:rotate(-5deg)}.notlove{left:180px;top:940px;width:720px;text-align:center;font-size:110px;letter-spacing:-5px}.darkest{left:120px;top:1480px;font-size:48px}.forever{left:180px;top:1490px;width:720px;text-align:center;font-size:79px}.accent{position:absolute;inset:0;z-index:7;pointer-events:none}.accent path{fill:none;stroke:#111;stroke-width:10;stroke-linecap:round}.accent circle{fill:none;stroke:#ef1212;stroke-width:10}'''
parts=[f'<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>{style}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920">']
for key in ['loving','schemer','vampire','chaos','bandage','boundary','healing','damaged']:
 parts.append(f'<div class="asset" id="{key}"><img src="assets/{key}.png"></div>')
parts += ['<div id="connection" class="label connection">CALLED IT<br><strong>CONNECTION?</strong></div>','<div id="notlove" class="label notlove">NOT <strong>LOVE.</strong></div>','<div id="darkest" class="label darkest">PERFECTLY <strong>FINE.</strong></div>','<div id="forever" class="label forever"><strong>FOREVER.</strong></div>','<svg class="accent" width="1080" height="1920"><path id="strike" d="M180 1050 Q530 1000 900 1040"/><path id="link" d="M670 1170 Q845 1210 845 1145"/></svg>']
keyset={'selfish','trauma','light','vampire','drained','chaos','calm','connection','love','band-aid','wounds','darkest','fine','spawned','alone','heal','broken','damage','dead','forever'}
for i,c in enumerate(cap):
 txt=' '.join(('<b>'+html.escape(w)+'</b>') if w.lower().strip(',.!?') in keyset else html.escape(w) for w in c['text'].split())
 parts.append(f'<div id="cap{i}" class="caption"><span>{txt}</span></div>')
parts.append('<div class="shade"></div><audio id="mix" src="assets/mix.wav" data-start="0" data-duration="36.7" data-track-index="1"></audio></div>')
js=['window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});window.__timelines.main=tl;']
def tween(sel,vars,t,frm=None):
 if frm is None:js.append(f'tl.to({json.dumps(sel)},{json.dumps(vars)},{t});')
 else:js.append(f'tl.fromTo({json.dumps(sel)},{json.dumps(frm)},{json.dumps(dict(vars,immediateRender=False))},{t});')
def into(k,t,x=0,y=0,s=1,dx=0,dy=200,r=0,d=.65):tween('#'+k,{'opacity':1,'x':x,'y':y,'scale':s,'rotation':r,'duration':d,'ease':'power3.out'},t,{'opacity':0,'x':x+dx,'y':y+dy,'scale':s*.88,'rotation':r})
def move(k,t,**v):tween('#'+k,dict(v,duration=.65,ease='power2.inOut'),t)
def fade(k,t,x=None):
 v={'opacity':0,'duration':.35,'ease':'power1.out'}
 if x is not None:v['x']=x
 tween('#'+k,v,t)
# Opening smile develops into a two-character thought.
into('loving',.03,s=.94,dy=140,d=.58)
move('loving',1.8,s=1) if False else None
move('loving',4.5,x=-290,y=120,scale=.59)
into('schemer',4.65,x=150,y=0,s=.95,dx=420,dy=0)
move('schemer',6.7,x=70,scale=1.04)
fade('schemer',8.3,x=410);move('loving',8.35,x=0,y=0,scale=1)
# Light -> vampire. The old warm figure recedes as the metaphor arrives.
move('loving',11.05,x=330,y=50,scale=.53)
into('vampire',11.1,s=1.07,dy=350,dx=-90)
fade('loving',11.5);move('vampire',13.1,x=-65,scale=1.13)
# Chaos and a false connection label.
fade('vampire',14.0,x=-460);into('chaos',14.04,s=1.04,dx=350,dy=50)
move('chaos',16.55,x=-240,y=70,scale=.81)
into('connection',17.25,dx=130,dy=0,d=.4)
# Typography punctuates the statement while illustration remains secondary.
move('chaos',18.65,x=-310,y=150,scale=.52);fade('connection',18.65)
into('notlove',18.87,dy=90,d=.35)
tween('#strike',{'strokeDashoffset':0,'duration':.3,'ease':'power2.out'},19.64,{'strokeDasharray':730,'strokeDashoffset':730,'opacity':1})
fade('chaos',20.35);fade('notlove',20.35);fade('strike',20.35)
into('bandage',20.38,s=1.1,dy=250)
move('bandage',22.5,scale=1.23,y=-55)
fade('bandage',24.53,x=370)
# Return to intact person before the unwanted arrival.
into('loving',24.6,s=.95,dx=-360,dy=0)
into('darkest',25.5,dy=25,d=.35)
move('loving',26.65,x=-230,scale=.77)
into('schemer',26.83,x=300,y=180,s=.57,dy=420,d=.45)
fade('darkest',27.4);fade('loving',27.65,x=-470);fade('schemer',27.6,x=500)
into('boundary',27.48,s=1.05,dy=300)
move('boundary',29.0,scale=1.16,y=-35)
# Healing and consequences are related instead of abrupt independent cards.
move('boundary',30.05,x=400,scale=.55,y=100);into('healing',30.12,x=-80,s=1,dx=-420,dy=0)
fade('boundary',30.52)
move('healing',31.55,x=-300,y=90,scale=.67);into('damaged',31.77,x=270,y=180,s=.62,dy=360)
fade('healing',33.5,x=-510);move('damaged',33.62,x=0,y=0,scale=1.09)
into('forever',35.58,dy=45,d=.35)
# Captions use precise transcript timing, brief glides, firm holds, and hard exits.
for i,c in enumerate(cap):
 t=c['start'];end=c['end'];tween('#cap'+str(i),{'opacity':1,'y':0,'duration':.12,'ease':'power2.out'},t,{'opacity':0,'y':18})
 js.append(f'tl.set("#cap{i}",{{opacity:0}},{end});')
js.append('tl.set("#link",{opacity:0},0);tl.set("#strike",{opacity:0},0);tl.seek(0);')
parts.append('<script>'+'\n'.join(js)+'</script></body></html>')
(p/'index.html').write_text('\n'.join(parts))
(p/'script.txt').write_text(' '.join(w['word'] for w in words))
(p/'package.json').write_text(json.dumps({'name':'emotional-vampire','private':True,'scripts':{'render':'hyperframes render --fps 30 --quality high'},'devDependencies':{'hyperframes':'0.8.181'}},indent=2))
print('built',len(cap),'caption groups;',duration,'seconds;',len(cue),'sound cues')
