from pathlib import Path
import json, html, wave, subprocess, shutil
import numpy as np

p = Path(__file__).parent
words = json.loads((p/'words.json').read_text())
# Join the recognizer's split compound without changing any recorded wording.
for i,w in enumerate(words[:-1]):
    if w['word']=='check' and words[i+1]['word']=='-ins':
        w['word']='check-ins'; w['end']=words[i+1]['end']; words[i+1]['word']=''
words=[w for w in words if w['word']]
duration=round(json.loads((p/'audio-edits.json').read_text())['duration']+0.20,3)
phrases=["When a man feels unappreciated,","he doesn't always","pack a bag and leave.","Instead,","he just puts his soul","on mute.","He stops repeating himself,","not because he magically","ran out of things to say,","but because he realized","talking to a brick wall","is a terrible use of oxygen.","He stops asking for effort,","not because he doesn't want it,","but because begging someone","for the bare minimum","is a humiliation ritual","he's finally too exhausted","to perform.","And here's the darkest part.","When he goes quiet,","you'll probably think","everything is fine.","You'll mistake his silence for peace","and think, nice,","we haven't argued in weeks,","spoiler, he isn't at peace.","He's just quietly hosting","a funeral for his feelings","in his head.","You don't lose him","all at once","in some big dramatic breakup.","You drain him,","moment by moment.","Until one day,","you look over and realize","the man who once","gave you his all","is now only giving you","what's left of","his emotional scraps.","He stops showing up","the way he used to,","the little favors vanish,","the check-ins dry up,","and he withdraws quietly","while the emotional space","between you","turns into a canyon.","His body might still","be sitting on your couch,","but make no mistake,","the version of him","that actually loved you","is already dead."]
groups=[]; idx=0
for phrase in phrases:
    n=len(phrase.split()); group=words[idx:idx+n]; idx+=n
    assert ' '.join(w['word'] for w in group).lower()==phrase.lower(),(phrase,group)
    groups.append(group)
assert idx==len(words),(idx,len(words))
caps=[dict(text=' '.join(w['word'] for w in g),start=g[0]['start'],end=g[-1]['end']) for g in groups]
for i,c in enumerate(caps): c['end']=caps[i+1]['start'] if i+1<len(caps) else duration
(p/'captions.json').write_text(json.dumps(caps,indent=2))
(p/'script.txt').write_text(' '.join(w['word'] for w in words))

# Every handoff belongs to the spoken argument, rather than a transition preset.
beats=[
 (0,'When a man feels unappreciated','unappreciated','He offers affection; she looks away.','short arrival'),
 (2.65,"doesn't always pack a bag and leave",'suitcase','Couple reduces and shifts left; suitcase rises at right, a deliberate slash negates leaving.','bag landing'),
 (4.36,'Instead he just puts his soul on mute','muted','Closed mouth and chest; mute icon receives focus.','mute click'),
 (6.84,'He stops repeating himself','unsaid','New closed-mouth portrait and multiple unspoken speech bubbles; he has words but withholds them.','three diminishing ticks'),
 (9.0,'not because he magically ran out of things to say','unsaid','Close in on the available words and firmly closed mouth.','none'),
 (11.96,'talking to a brick wall','wall','Man gestures to solid wall; bubbles stop at its edge.','solid dull knock'),
 (15.76,'He stops asking for effort','effort','He strains to move affection toward an idle partner: one-sided effort.','controlled glide'),
 (18.98,'begging someone for the bare minimum','begging','Move closer toward his open hand; one small heart crumb.','small click'),
 (21.28,'humiliation ritual','begging','Hold the uncomfortable posture at closer scale.','low thud'),
 (23.6,'too exhausted to perform','exhausted','His head sinks into folded arms on a table; begging illustration recedes.','low falling movement'),
 (25.14,"here's the darkest part",'exhausted','Shift to one side; prepare the misleading calm.','bass punctuation'),
 (26.48,"you'll probably think everything is fine",'falsepeace','Shared sofa: she smiles while he looks empty.','soft arrival'),
 (29.14,"mistake his silence for peace",'apparentpeace','She relaxes as though everything is settled: her mistaken interpretation of his silence.','soft glide'),
 (31.98,"nice we haven't argued in weeks",'calendar','Generated calendar appears beside relaxed woman; pages shift.','calendar ticks'),
 (34.06,"spoiler he isn't at peace",'muted','Calendar and false calm recede; his closed posture returns.','abrupt short impact'),
 (35.94,'quietly hosting a funeral for his feelings','funeral','Memorial heart box and bowed figure emerge; not graphic.','soft low impact'),
 (39.44,"don't lose him all at once",'breakup','The dramatic-breakup alternative is shown beneath explicit negating narration and captions.','quiet crack'),
 (42.84,'You drain him moment by moment','drained','Heart hourglass; progressive time emphasis with three anchored ticks.','three descending impacts'),
 (46.92,'the man who once gave you his all','all','Large intact offered heart and warm expression.','soft chime'),
 (49.38,"only giving you what's left of his emotional scraps",'scraps','Intact offering slides aside; hand with heart fragments takes focus.','crack and settling'),
 (52.58,'He stops showing up the way he used to','favors','Helpful grocery-carrying pose; progressively moves aside.','bag landing'),
 (54.56,'little favors vanish','favors','Helpful figure fades while phone enters, an explicit loss of effort.','short receding swish'),
 (56.06,'the check-ins dry up','checkins','A new man holding a phone turns his attention away; messages diminish.','notification ticks stop'),
 (57.48,'he withdraws quietly','withdrawal','New full-body acting: he turns away as she reaches for him.','quiet brush'),
 (59.1,'space between you turns into a canyon','canyon','Opposite cliff edges; emphasize the empty gap.','wide low whoosh'),
 (62.12,'body might still be sitting on your couch','couch','Physical presence on empty sofa with hollow heart.','soft landing'),
 (65.5,'the version of him that actually loved you is already dead','couch','The loving earlier figure appears behind him briefly then drains away; couch remains.','low final impact')
]
(p/'storyboard.json').write_text(json.dumps(beats,indent=2))
(p/'storyboard.md').write_text('# When He Goes Quiet\n\n| Time | Exact narration cue | Visual | Action | Sound |\n| --- | --- | --- | --- | --- |\n'+'\n'.join(f'| {t:.2f} | {phrase} | {asset} | {action} | {sound} |' for t,phrase,asset,action,sound in beats))

cue=[(.08,'whoosh-short',.48,-23),(2.72,'whoosh-short',.45,-23),(3.15,'impact-bass-1',.38,-23),(5.98,'click',.18,-20),
 (7.10,'click',.13,-25),(7.52,'click',.13,-28),(8.0,'click',.13,-31),(11.96,'whoosh',.55,-23),(13.22,'impact-bass-2',.42,-22),
 (15.80,'whoosh-short',.5,-23),(20.12,'click',.2,-23),(21.28,'impact-bass-1',.4,-24),(23.6,'whoosh-cinematic',.65,-26),
 (25.54,'impact-bass-2',.5,-23),(26.48,'whoosh-short',.5,-23),(30.10,'click',.15,-23),(32.0,'click',.14,-24),(32.74,'click',.14,-25),(33.4,'click',.14,-26),
 (34.06,'impact-bass-1',.5,-21),(35.94,'whoosh-cinematic',.75,-23),(37.32,'impact-bass-2',.6,-24),(40.68,'glitch-1',.24,-24),
 (42.86,'whoosh',.55,-23),(43.12,'impact-bass-1',.35,-24),(43.88,'impact-bass-1',.32,-26),(44.32,'impact-bass-1',.32,-28),
 (47.98,'chime',.55,-28),(49.38,'whoosh-short',.5,-23),(51.6,'glitch-1',.27,-24),(52.64,'whoosh-short',.5,-24),(55.16,'whoosh-short',.4,-24),
 (56.12,'click',.2,-21),(56.82,'click',.15,-28),(57.48,'whoosh-cinematic',.6,-28),(59.34,'whoosh',.65,-23),(61.42,'impact-bass-2',.6,-25),
 (62.18,'whoosh-short',.5,-24),(65.5,'whoosh-cinematic',.8,-26),(67.74,'impact-bass-2',.7,-24)]
def audio(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ac','1','-ar','48000','-f','f32le','-']),np.float32).copy()
narr=audio(p/'assets/narration.wav'); n=np.zeros(round(duration*48000),np.float32)
narr*=10**(-19/20)/max(np.sqrt(np.mean(narr*narr)),1e-7)
n[:len(narr)]=narr
fx=np.zeros_like(n)
for t,name,limit,db in cue:
    a=audio(p/'assets/sfx'/f'{name}.mp3')[:round(limit*48000)]
    a*=10**(db/20)/max(np.sqrt(np.mean(a*a)),1e-7)
    a*=min(1,.28/max(np.max(np.abs(a)),1e-7))
    edge=min(1500,len(a)//4);a[:150]*=np.linspace(0,1,150);a[-edge:]*=np.linspace(1,0,edge)
    start=round(t*48000);end=min(len(fx),start+len(a));fx[start:end]+=a[:end-start]
mix=n+fx; mix*=min(1,.96/max(np.max(np.abs(mix)),1e-7))
for name,a in [('mix.wav',mix),('effects.wav',fx)]:
    with wave.open(str(p/'assets'/name),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(48000);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
(p/'sound-cues.json').write_text(json.dumps(cue,indent=2))

style='''@font-face{font-family:Caption;src:url('assets/caption-bold.ttf')}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#fff}#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#fff;color:#101010;font-family:Caption,Arial,sans-serif}.shade{position:absolute;inset:-20px;z-index:20;pointer-events:none;box-shadow:inset 95px 0 120px -40px #0009,inset -95px 0 120px -40px #0009,inset 0 65px 95px -40px #0006,inset 0 -65px 95px -40px #0006}.asset{position:absolute;left:110px;top:550px;width:860px;height:1090px;opacity:0;transform-origin:50% 58%;will-change:transform,opacity}.asset img{width:100%;height:100%;object-fit:contain;display:block}.caption{position:absolute;left:115px;top:220px;width:850px;height:260px;z-index:25;display:flex;align-items:center;justify-content:center;text-align:center;font-size:62px;font-weight:700;font-style:italic;text-transform:uppercase;line-height:1.12;letter-spacing:-1.8px;opacity:0}.caption span{max-width:850px;display:block;transform:scaleX(.90)}b{color:#de0b13}.minor{position:absolute;opacity:0;z-index:9}.bubble{border:8px solid #101010;border-radius:35px;background:#fff;width:175px;height:88px;display:flex;align-items:center;justify-content:center;gap:13px}.bubble i{width:15px;height:15px;border-radius:50%;background:#e20c15}.bubble:after{content:'';position:absolute;bottom:-20px;left:28px;width:24px;height:28px;background:white;border-left:7px solid #111;transform:skewY(-37deg)}.week{width:140px;height:150px;background:white;border:8px solid #111;border-radius:13px;top:1300px;left:720px;display:flex;align-items:center;justify-content:center;font-size:62px;color:#e20c15;box-shadow:0 8px 0 #111}.week:before{content:'';position:absolute;top:0;left:0;right:0;height:24px;background:#e20c15}.draw{position:absolute;inset:0;z-index:10;pointer-events:none}.draw path{fill:none;stroke:#111;stroke-width:12;stroke-linecap:round}.draw .red{stroke:#de0b13}'''
parts=[f'<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>{style}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920">']
keys=['unappreciated','muted','wall','begging','falsepeace','funeral','drained','all','scraps','favors','canyon','couch','phone','suitcase','unsaid','effort','exhausted','apparentpeace','calendar','breakup','checkins','withdrawal']
for key in keys: parts.append(f'<div class="asset" id="{key}"><img src="assets/{key}.png" alt="{key}"></div>')
parts.append('<div class="asset" id="soul" style="z-index:0"><img src="assets/former-self.png" alt="former loving self"></div>')
for i,(x,y) in enumerate([(700,660),(735,825),(690,990)]):
    parts.append(f'<div id="bubble{i}" class="minor bubble" style="left:{x}px;top:{y}px"><i></i><i></i><i></i></div>')
for i in range(3):parts.append(f'<div id="week{i}" class="minor week">{i+1}</div>')
parts.append('<svg class="draw" width="1080" height="1920"><path id="noleave" d="M730 1430 L930 1200"/><path id="divide" d="M540 765 L540 1450"/><path id="tick0" d="M750 950 L790 950"/><path id="tick1" d="M750 1030 L790 1030"/><path id="tick2" d="M750 1110 L790 1110"/></svg>')
accent={'unappreciated','mute','soul','wall','oxygen','effort','begging','minimum','humiliation','exhausted','darkest','quiet','fine','silence','peace','spoiler','funeral','feelings','breakup','drain','moment','all','scraps','vanish','check-ins','withdraws','canyon','couch','loved','dead'}
for i,c in enumerate(caps):
    txt=' '.join(f'<b>{html.escape(w)}</b>' if w.lower().strip(',.!?') in accent else html.escape(w) for w in c['text'].split())
    parts.append(f'<div id="cap{i}" class="caption"><span>{txt}</span></div>')
parts.append(f'<div class="shade"></div><audio id="audio" src="assets/mix.wav" data-start="0" data-duration="{duration}" data-track-index="1"></audio></div>')
js=['window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});window.__timelines.main=tl;']
def tw(key,t,v,start=None):
    if start is None:js.append(f'tl.to("#{key}",{json.dumps(v)},{t});')
    else:js.append(f'tl.fromTo("#{key}",{json.dumps(start)},{json.dumps(dict(v,immediateRender=False))},{t});')
def enter(k,t,x=0,y=0,s=1,dx=0,dy=170,d=.62,r=0):
    tw(k,t,dict(opacity=1,x=x,y=y,scale=s,rotation=r,duration=d,ease='power3.out'),dict(opacity=0,x=x+dx,y=y+dy,scale=s*.92,rotation=r))
def move(k,t,d=.65,**v):tw(k,t,dict(v,duration=d,ease='power2.inOut'))
def fade(k,t,d=.34,**v):tw(k,t,dict(v,opacity=0,duration=d,ease='power1.out'))
def trace(k,t,length=300,d=.36):tw(k,t,dict(opacity=1,strokeDashoffset=0,duration=d,ease='power2.out'),dict(opacity=1,strokeDasharray=length,strokeDashoffset=length))
# All held positions are explicit, no perpetual drift or bounce.
enter('unappreciated',.04,s=1.04,dy=140,d=.55)
move('unappreciated',2.55,x=-230,y=-25,scale=.72)
enter('suitcase',2.72,x=280,y=130,s=.43,dy=240,d=.55)
trace('noleave',3.24,280)
fade('unappreciated',4.38,x=-470);fade('suitcase',4.40,y=260);fade('noleave',4.38)
enter('muted',4.36,s=.98,dy=170,d=.64)
move('muted',6.65,x=-320,y=80,scale=.55)
enter('unsaid',6.84,x=40,s=1.0,dx=260,dy=30)
fade('muted',6.88)
move('unsaid',9.05,x=0,scale=1.10,d=.72)
move('unsaid',11.7,x=-320,y=65,scale=.58)
enter('wall',11.96,s=1.04,dx=320,dy=0)
fade('unsaid',12.00)
move('wall',13.22,scale=1.10,x=-30,d=.45)
fade('wall',15.80,x=300)
enter('effort',15.76,s=1.02,dy=230)
move('effort',18.70,x=-330,y=100,scale=.57)
enter('begging',18.98,x=0,s=1.04,dx=240,dy=50)
fade('effort',19.02)
move('begging',21.28,x=-25,scale=1.10,y=-40,d=.7)
move('begging',23.45,x=330,scale=.56,y=160)
enter('exhausted',23.6,x=-45,s=1.0,dx=-240,dy=0)
fade('begging',23.64)
move('exhausted',25.22,x=-290,y=30,scale=.65)
enter('falsepeace',26.48,s=1.02,dx=270,dy=35)
fade('exhausted',26.52)
move('falsepeace',28.95,x=-310,y=65,scale=.58)
enter('apparentpeace',29.14,x=45,s=.98,dx=230,dy=40)
fade('falsepeace',29.18)
move('apparentpeace',31.75,x=-180,y=-50,scale=.75)
enter('calendar',31.98,x=270,y=155,s=.47,dy=150,d=.52)
move('calendar',32.98,y=120,rotation=-6,d=.4)
move('calendar',33.40,y=130,rotation=4,d=.4)
fade('calendar',34.10,x=380)
move('apparentpeace',33.90,x=330,y=100,scale=.52)
enter('muted',34.06,x=-20,s=.98,dx=-250,dy=0,d=.5)
fade('apparentpeace',34.10)
move('muted',35.75,x=330,y=100,scale=.54)
enter('funeral',35.94,s=1.03,dx=-220,dy=100,d=.72)
fade('muted',35.98)
move('funeral',37.32,y=-20,scale=1.10,d=.65)
fade('funeral',39.48,x=-320)
enter('breakup',39.44,x=0,y=-5,s=.97,dx=260,dy=80)
move('breakup',41.14,x=-80,scale=1.07,y=-40,d=.7)
move('breakup',42.64,x=-340,y=60,scale=.52)
enter('drained',42.84,x=35,s=1.0,dy=240)
fade('breakup',42.88)
for i in range(3):trace(f'tick{i}',43.12+i*.60,50,.2)
for i in range(3):fade(f'tick{i}',44.8)
move('drained',44.96,scale=1.10,y=-30,d=.65)
fade('drained',46.96,x=-360)
enter('all',46.92,s=1.03,dx=260,dy=60)
move('all',49.16,x=-320,y=50,scale=.58)
enter('scraps',49.38,x=100,y=10,s=.96,dy=260)
fade('all',49.42)
move('scraps',51.2,x=0,y=-15,scale=1.12)
fade('scraps',52.62,x=350)
enter('favors',52.58,s=1.02,dx=-260,dy=50)
move('favors',54.56,x=-280,y=70,scale=.62)
enter('phone',55.16,x=200,y=10,s=.70,dy=210)
fade('favors',55.20)
move('phone',55.90,x=-300,y=70,scale=.40,d=.55)
enter('checkins',56.06,x=60,s=.96,dx=220,dy=50,d=.55)
for i in range(3):
    enter(f'bubble{i}',55.6+i*.15,x=-265,y=170-i*95,s=.65,dy=20,d=.3)
    fade(f'bubble{i}',56.35+i*.16,d=.23)
fade('phone',56.10)
fade('checkins',57.52,x=380)
enter('withdrawal',57.48,x=-40,s=1.0,dx=-220,dy=0)
move('withdrawal',58.3,x=-160,scale=.90,d=.65)
enter('canyon',59.1,x=0,y=15,s=1.07,dy=230,d=.75)
fade('withdrawal',59.14,x=-480)
move('canyon',60.62,y=-30,scale=1.13,d=.75)
fade('canyon',62.16,y=-160)
enter('couch',62.12,s=1.04,dy=180,d=.70)
# The loving version retreats while his physical body remains seated.
enter('soul',65.5,x=-100,y=-95,s=.74,dy=120,d=.55)
tw('soul',66.12,dict(opacity=.22,y=-270,x=-100,scale=.72,duration=.8,ease='power2.inOut'))
fade('soul',66.93,d=.75,y=-450,scale=.66)
move('couch',65.52,y=80,scale=.94,d=.70)
move('couch',67.6,y=25,scale=1.0,d=.7)
for k in ['noleave','divide','tick0','tick1','tick2']:js.append(f'tl.set("#{k}",{{opacity:0}},0);')
for i,c in enumerate(caps):
    tw(f'cap{i}',c['start'],dict(opacity=1,y=0,duration=.12,ease='power2.out'),dict(opacity=0,y=15))
    js.append(f'tl.set("#cap{i}",{{opacity:0}},{c["end"]});')
js.append('tl.seek(0);')
parts.append('<script>'+'\n'.join(js)+'</script></body></html>')
(p/'index.html').write_text('\n'.join(parts))
print('Built',duration,'seconds,',len(caps),'caption groups,',len(beats),'visual beats,',len(cue),'purposeful audio cues')
