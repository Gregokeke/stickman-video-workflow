from pathlib import Path
import json,html,math,wave,subprocess
import numpy as np
from runpy import run_path
p=Path(__file__).parent
words=json.loads((p/'words.json').read_text())
words[10]['word']='10-step';words[11]['word']=''
T=lambda i:words[i]['start']
narration_duration=json.loads((p/'audio-edits.json').read_text())['duration']
duration=math.ceil((narration_duration+.28)*30)/30
starts=[0,3,5,8,10,14,18,22,25,29,33,37,39,43,46,49,52,55,58,61,63,66,69,72,75,79,82,86,88,91,93,96,100,102,106,109,111,114,119,123,127,131,135,138,142,145,149,152,155,160,163,166,169,171,176]
caps=[]
for a,b in zip(starts,starts[1:]+[len(words)]):caps.append(dict(text=' '.join(w['word'] for w in words[a:b] if w['word']),start=T(a),end=T(b) if b<len(words) else duration))
(p/'captions.json').write_text(json.dumps(caps,indent=2));(p/'script.txt').write_text(' '.join(c['text'] for c in caps))
plan=[('clearportrait',0,'Attractive natural skin; matched fictional adult portrait'),('calendar7',5,'One-week hook'),('tensteps',8,'Expensive ten-step skincare receipt'),('scam',17,'Officially a scam, stamp punctuation'),('badportrait',18,'Prominent acne/puffiness/dark undereye portrait, same woman'),('filter',31,'Social-media beauty filter'),('acnefocus',37,'Battling acne'),('bloathead',41,'Bloated face'),('outsidepimple',43,'Outside-only skincare approach explicitly negated'),('insidegut',49,'Symbolic internal gut problem'),('gutglow',55,'Real glowing skin starts within'),('microbiome',61,'Magnified gut-microbe community, newly generated'),('cloggedgut',67,'Clogged intestinal passage'),('weakbacteria',69,'Exhausted weak gut bacteria'),('faceprice',72,'Face pays the price in breakouts, visual price-tag gag'),('guide',79,'Ultimate fix, later returns for simple solution'),('apple',84,'One of three explicitly named ingredients'),('ginger',84,'Ingredient trio, later shown alone before bloating illustration'),('acerola',84,'Recognizable acerola in trio and individual close-up'),('pectin',87,'Apple pectin fibers'),('colon',89,'Clean-out colon context'),('eatingbloat',97,'Bloating after eating'),('vitaminc',104,'Vitamin C'),('enzymeboost',107,'Boosted lock-and-key enzyme activity; no alarm clock'),('rawroots',111,'Raw ginger chewing, a rejected behavior'),('stoproots',112,'Stop gesture makes negation clear'),('scan',123,'Clean branded scan phone; one Remea label'),('analysis',131,'Matching analyzing screen, no repeated branding'),('overview',135,'Exact issues: acne, puffiness, under-eyes'),('plan',142,'Custom tailored-juice routine, matching phone'),('recipe',147,'Juice with the three named ingredients'),('drinking',149,'Actively drinking the juice'),('period',151,'Generic routine calendar, no invented duration'),('paintproblem',155,'Painting over the problem'),('gutcare',163,'Gut-care payoff'),('share',171,'Send to a friend'),('friend',175,'Friend receives the message'),('reset',180,'A total reset')]
(p/'asset-plan.json').write_text(json.dumps(plan,indent=2))
# 38 distinct used visuals; count is a floor, never a cap. Repeated returns do not inflate it.
cue=[]
silent={'calendar7','scam','badportrait','microbiome','weakbacteria','apple','ginger','acerola','vitaminc','stoproots','analysis','recipe','period','reset'}
for k,i,desc in plan:
    if k in silent:continue
    name='click' if k in {'plan','overview'} else ('whoosh' if len(cue)%2==0 else 'whoosh-short')
    cue.append((max(.12,T(i)),name,.16 if name=='click' else .50,-22.5))
cue += [(T(5),'click',.16,-22),(T(17),'stamp',.30,-20.5),(10.56,'whoosh-short',.42,-24),(11.6,'glitch-1',.20,-22),(12.3,'whoosh-short',.4,-24),
 (T(45),'draw',.30,-23),(T(49),'impact-bass-1',.34,-23),(T(61),'cinematic',.68,-23),(23.68,'whoosh-short',.42,-24),(T(69),'deflate',.50,-23),
 (T(74),'cash',.36,-23),(T(84),'chime',.45,-22),(T(87),'click',.16,-23),(33.05,'draw',.32,-23),(T(93),'whoosh',.5,-22),
 (T(101),'whoosh-short',.45,-23),(T(104),'chime',.42,-22),(T(107),'impact-bass-2',.35,-24),(T(112),'record-scratch',.45,-21),
 (T(119),'chime',.40,-23),(T(128),'scan-tone',.58,-23),(T(131),'click',.16,-22),(47.82,'scan-tone',.40,-25),(T(149),'click',.16,-24),
 (54.48,'click',.13,-24),(54.8,'click',.13,-25),(T(160),'click',.16,-22),(T(169),'chime',.45,-22),(T(180),'chime',.45,-22)]
exec((p/'mixer.py').read_text())
css=(p/'design.css').read_text()+'''
.asset img{filter:drop-shadow(-13px 18px 12px rgba(0,0,0,.30))}
.asset.photo{width:800px;height:960px;left:140px;top:490px;transform-origin:50% 50%}
.asset.photo img{width:100%;height:auto;aspect-ratio:1;object-fit:cover;border-radius:24px;border:5px solid #151515;filter:drop-shadow(-10px 16px 12px rgba(0,0,0,.22))}
.asset#scan,.asset#analysis,.asset#overview,.asset#plan{top:460px}
.phone-overlay{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
.phone-overlay path{fill:none;stroke:#de0b13;stroke-width:9;stroke-linecap:round}
.phone-overlay #outside-slash{stroke:#101010;stroke-width:13.33}
.phone-overlay #analysisfill{stroke-width:26}
.draw{z-index:8}.draw path{stroke-width:12;stroke-linejoin:round}.draw .red{stroke:#de0b13}
b{white-space:nowrap}
'''
parts=[f'<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>{css}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920">']
for k,i,desc in plan:
    cls=' photo' if k in {'badportrait','clearportrait'} else ''
    overlay='<svg class="phone-overlay" viewBox="0 0 860 1090"><path id="scanbeam" d="M285 650 L575 650" opacity="0"/></svg>' if k=='scan' else ''
    if k=='outsidepimple':overlay='<svg class="phone-overlay" viewBox="0 0 860 1090"><path id="outside-slash" d="M274 674 L708 252" opacity="0"/></svg>'
    if k=='analysis':overlay='<svg class="phone-overlay" viewBox="0 0 860 1090"><path id="analysisfill" d="M264 768 L596 768" opacity="0"/></svg>'
    parts.append(f'<div class="asset{cls}" id="{k}" data-layout-allow-overflow><img src="assets/{k}.png" alt="{k}">{overlay}</div>')
accent={'glowing','skin','week','expensive','10-step','skincare','scam','tiktok','filter','acne','bloated','face','rotting','gut','microbiome','clogged','weak','bacteria','price','breakouts','ultimate','glow','trinity','apple','pectin','colon','ginger','toxic','bloating','acerola','vitamin','c','boost','digestive','enzymes','blindly','raw','roots','simple','app','scan','ai','instantly','exact','issues','custom','remedy','plan','tailored','juices','drink','period','painting','problem','heal','glass','friend','reset'}
for i,c in enumerate(caps):
    txt=' '.join(f'<b>{html.escape(w)}</b>' if w.lower().strip(',.!?') in accent else html.escape(w) for w in c['text'].split());parts.append(f'<div class="caption" id="cap{i}"><span>{txt}</span></div>')
parts.append('<svg class="draw" viewBox="0 0 1080 1920"><g transform="translate(0,-140)"><path id="microbe-link" d="M405 1110 Q485 1070 568 1120 L544 1098 M568 1120 L537 1129" opacity="0"/><path id="pectinflow" d="M450 1160 Q545 1060 668 1090 L644 1068 M668 1090 L635 1098" opacity="0"/></g></svg>')
parts.append(f'<div class="shade"></div><audio id="audio" src="assets/mix.wav" data-start="0" data-duration="{duration}" data-track-index="1"></audio></div>')
SafeLayout=run_path(str(p/'safe-layout.py'))['SafeLayout'];safe_layout=SafeLayout(p,[k for k,i,desc in plan])
js=['window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});window.__timelines.main=tl;']
def tw(k,t,v,start=None):
    v,start=safe_layout.adapt(k,t,v,start)
    if start is None:js.append(f'tl.to("#{k}",{json.dumps(v)},{t});')
    else:js.append(f'tl.fromTo("#{k}",{json.dumps(start)},{json.dumps(dict(v,immediateRender=False))},{t});')
def enter(k,t,x=0,y=0,s=1,dx=0,dy=180,d=.62,ease='power3.out',r=0):
    tw(k,t,dict(opacity=1,x=x,y=y,scale=s,rotation=0,duration=d,ease=ease),dict(opacity=0,x=x+dx,y=y+dy,scale=s*.90,rotation=r))
def move(k,t,d=.62,**v):tw(k,t,dict(v,duration=d,ease='power2.inOut'))
def fade(k,t,d=.30):tw(k,t,dict(opacity=0,duration=d,ease='power1.out'))
def depart(k,t,x=None,y=None,s=None,d=.60):
    v={}
    if x is not None:v['x']=x
    if y is not None:v['y']=y
    if s is not None:v['scale']=s
    if v:move(k,t,d=d,**v)
    fade(k,t+.04,min(.30,d-.10))
safe_paths={}
def draw(k,t,end,d=.38,reset_y=None):
    if k in {'microbe-link','pectinflow'}:safe_paths[k]=safe_layout.connector(k)
    y='' if reset_y is None else f',y:{reset_y}'
    js.append(f'tl.set("#{k}",{{opacity:1,strokeDasharray:document.querySelector("#{k}").getTotalLength(),strokeDashoffset:document.querySelector("#{k}").getTotalLength(){y}}},{t});')
    tw(k,t,dict(strokeDashoffset=0,duration=d,ease='sine.inOut'));fade(k,end,.18)
# Original connected hook: hero becomes support, rather than disappearing for a preset.
enter('clearportrait',.10,s=.85,dx=-350,dy=25,d=.58)
move('clearportrait',1.30,x=-170,y=-20,scale=.68,d=.62)
enter('calendar7',T(5),x=180,y=20,s=.30,dx=300,dy=0,d=.58)
enter('tensteps',T(8),s=.96,dx=380,dy=15,d=.66)
depart('clearportrait',T(8),x=-430,y=-30,s=.50);depart('calendar7',T(8),x=470,y=60,s=.25)
move('tensteps',6.0,x=-170,y=720,scale=.94,d=.70)
enter('scam',T(17),x=-70,y=-120,s=.84,dy=-140,d=.30,ease='power4.out',r=-10)
# Portrait comparison, filter interruption, and retained clear portrait returning to center.
enter('badportrait',T(18),s=.80,dx=95,dy=150,d=.56)
depart('tensteps',T(18),x=-220,y=820,s=.94);depart('scam',T(18),x=490,y=170,s=.32)
move('badportrait',T(22)-.18,x=-270,y=-20,scale=.44,d=.60)
enter('clearportrait',T(22),x=110,y=-20,s=.44,dx=350,dy=0,d=.60)
depart('badportrait',10.56,x=-470,y=-50,s=.37)
move('clearportrait',10.56,x=0,y=-15,scale=.82,d=.58)
move('clearportrait',11.38,x=110,y=-20,scale=.44,d=.52)
enter('filter',T(31),x=-250,y=0,s=.49,dx=-320,dy=20,d=.55)
depart('filter',12.30,x=-475,y=30,s=.34,d=.45)
move('clearportrait',12.30,x=0,y=-15,scale=.82,d=.55)
enter('acnefocus',T(37),s=.88,dx=320,dy=20,d=.62);depart('clearportrait',T(37),x=-470,y=-20,s=.5)
move('acnefocus',T(41)-.22,x=-255,y=-10,scale=.50,d=.60)
enter('bloathead',T(41),x=255,y=-10,s=.51,dx=280,dy=0,d=.58)
enter('outsidepimple',T(43),s=.90,dx=-330,dy=0,d=.62)
depart('acnefocus',T(43),x=-490,y=20,s=.32);depart('bloathead',T(43),x=480,y=30,s=.32)
draw('outside-slash',T(45),17.84,.34)
enter('insidegut',T(49),s=.97,dx=-70,dy=300,d=.66);depart('outsidepimple',T(49),x=460,y=-15,s=.55)
move('insidegut',T(54),y=-30,scale=1.05,d=.55)
enter('gutglow',T(55),s=.93,dx=-330,dy=15,d=.62);depart('insidegut',T(55),x=440,y=45,s=.57)
# Meaningful depth: the magnified microbiome grows from the gut and settles beside it.
move('gutglow',22.22,x=-280,y=-10,scale=.50,d=.64)
tw('microbiome',22.22,dict(opacity=.85,x=130,y=45,scale=.38,duration=.40,ease='power3.out'),dict(opacity=0,x=-175,y=95,scale=.12))
tw('microbiome',22.62,dict(opacity=1,x=180,y=-10,scale=.47,duration=.34,ease='sine.out'))
draw('microbe-link',23.0,23.50,.30)
depart('gutglow',23.68,x=-470,y=30,s=.35)
move('microbiome',23.68,x=0,y=-25,scale=.88,d=.56)
enter('cloggedgut',T(67),s=.92,dx=350,dy=0,d=.40);depart('microbiome',T(67),x=-470,y=-15,s=.48)
move('cloggedgut',24.90,x=-250,y=-10,scale=.54,d=.52)
enter('weakbacteria',T(69),x=170,y=20,s=.49,dx=270,dy=70,d=.60)
enter('faceprice',T(72),s=.91,dx=-320,dy=35,d=.60)
depart('cloggedgut',T(72),x=-490,y=35,s=.32);depart('weakbacteria',T(72),x=470,y=65,s=.32)
move('faceprice',T(78),y=-25,scale=.98,d=.42)
enter('guide',T(79),s=.92,dx=330,dy=0,d=.62);depart('faceprice',T(79),x=-470,y=20,s=.54)
# One intentional ingredient trio, followed by isolated, exact ingredient-function beats.
enter('apple',T(84),x=-310,y=-10,s=.35,dx=-260,dy=0,d=.50)
enter('ginger',T(84)+.08,x=-95,y=60,s=.35,dy=160,d=.54)
enter('acerola',T(84)+.16,x=150,y=-10,s=.35,dx=260,dy=0,d=.50)
depart('guide',T(84),x=-450,y=70,s=.4)
move('apple',T(86),x=-130,y=-20,scale=.60,d=.42);fade('ginger',T(86)+.04,.25);fade('acerola',T(86)+.04,.25)
enter('pectin',T(87),s=.82,dx=190,dy=45,d=.34);fade('apple',T(87)-.02,.22)
move('pectin',32.20,x=-270,y=0,scale=.43,d=.48)
enter('colon',T(89),x=270,s=.43,dx=280,dy=0,d=.48)
draw('pectinflow',33.05,33.72,.30)
enter('ginger',T(93),s=.88,dx=-390,dy=20,d=.60)
depart('pectin',T(93),x=-490,y=30,s=.3);depart('colon',T(93),x=490,y=25,s=.3)
move('ginger',34.70,x=-280,y=-25,scale=.43,d=.55)
enter('eatingbloat',T(97),x=150,y=0,s=.59,dx=200,dy=140,d=.50)
move('eatingbloat',T(99),y=-20,scale=.62,d=.38)
enter('acerola',T(101),s=.90,dy=210,d=.60)
depart('ginger',T(101),x=-470,y=35,s=.34);depart('eatingbloat',T(101),x=470,y=45,s=.38)
move('acerola',37.35,x=-245,y=-20,scale=.50,d=.52)
enter('vitaminc',T(104),x=255,s=.48,dx=280,dy=0,d=.52)
enter('enzymeboost',T(107),s=.93,dx=-70,dy=260,d=.62)
depart('acerola',T(107),x=-470,y=40,s=.32);depart('vitaminc',T(107),x=470,y=55,s=.30)
# Funny rejected action is paired with an explicit stop gesture from its first phrase.
enter('rawroots',T(111),x=-230,s=.61,dx=-220,dy=100,d=.55);depart('enzymeboost',T(111),x=430,y=80,s=.5)
enter('stoproots',T(112),x=270,s=.50,dx=300,dy=0,d=.40,ease='expo.out')
move('rawroots',T(115),x=-210,y=-20,scale=.67,d=.50)
enter('guide',T(119),s=.92,dx=-340,dy=0,d=.62)
depart('rawroots',T(119),x=-470,y=35,s=.38);depart('stoproots',T(119),x=480,y=30,s=.31)
# Guide retains its pointing role beside the phone, then yields as the scan becomes hero.
move('guide',T(123),x=-245,y=240,scale=.62,d=.62)
enter('scan',T(123),x=150,s=.78,dx=320,dy=30,d=.62)
move('scan',T(128),x=0,y=0,scale=.90,d=.55);depart('guide',T(128),x=-470,y=25,s=.30)
draw('scanbeam',T(128),47.0,.18,0);tw('scanbeam',T(128)+.18,dict(y=-220,duration=.65,ease='sine.inOut'))
enter('analysis',T(131),s=.90,dx=280,dy=0,d=.60);depart('scan',T(131),x=-420,y=0,s=.53)
draw('analysisfill',47.82,49.00,.80)
enter('overview',T(135),s=.90,dy=190,d=.58);depart('analysis',T(135),x=-420,y=15,s=.52)
enter('plan',T(142),s=.90,dx=-320,dy=10,d=.60);depart('overview',T(142),x=420,y=25,s=.52)
move('plan',52.50,x=-270,y=-35,scale=.52,d=.64)
enter('recipe',T(147),x=150,y=0,s=.50,dx=280,dy=35,d=.58)
enter('drinking',T(149),s=.91,dx=-320,dy=0,d=.50)
depart('plan',T(149),x=-460,y=20,s=.34);depart('recipe',T(149),x=470,y=35,s=.32)
move('drinking',54.02,x=-245,y=-10,scale=.59,d=.55)
enter('period',54.0,x=260,y=15,s=.49,dy=170,d=.40)
move('period',54.48,rotation=-5,d=.24);move('period',54.80,rotation=0,d=.24)
enter('paintproblem',T(155),s=.92,dx=-350,dy=0,d=.58)
depart('drinking',T(155),x=-480,y=20,s=.34);depart('period',T(155),x=480,y=45,s=.30)
enter('scan',T(160),s=.88,dx=320,dy=0,d=.55);depart('paintproblem',T(160),x=-450,y=25,s=.53)
draw('scanbeam',57.82,58.24,.12,0);tw('scanbeam',57.94,dict(y=-180,duration=.22,ease='sine.inOut'))
enter('gutcare',T(163),s=.88,dx=-140,dy=180,d=.50);depart('scan',T(163),x=430,y=-30,s=.52)
enter('clearportrait',T(168),s=.88,dx=-320,dy=0,d=.58);depart('gutcare',T(168),x=420,y=40,s=.48)
move('clearportrait',T(171),x=110,y=-220,scale=.48,d=.58)
enter('share',T(171),x=-180,y=260,s=.75,dx=-300,dy=0,d=.55)
depart('clearportrait',T(175),x=470,y=-60,s=.30)
enter('friend',T(175),s=.87,dx=280,dy=20,d=.55);depart('share',T(175),x=-470,y=30,s=.35)
move('friend',62.85,x=-130,y=365,scale=.82,d=.55)
enter('reset',T(180),x=0,y=-200,s=.83,dy=-130,d=.55)
for i,c in enumerate(caps):
    tw(f'cap{i}',c['start'],dict(opacity=1,y=0,duration=.11,ease='power2.out'),dict(opacity=0,y=14));js.append(f'tl.set("#cap{i}",{{opacity:0}},{c["end"]});')
js.append('tl.seek(0);');parts.append('<script>'+'\n'.join(js)+'</script></body></html>');page='\n'.join(parts)
import re
for key,path in safe_paths.items():page=re.sub(r'(id="'+key+r'" d=")[^"]+',lambda m:m.group(1)+path,page)
(p/'index.html').write_text(page)
(p/'storyboard.md').write_text('# Gut to Glass — Context and Motion\n\nMinimum22; '+str(len(plan))+' distinct meaningful visuals. Original narration67.631s; gently tightened'+str(round(narration_duration,3))+'s; final'+str(round(duration,3))+'s. No word-gap trimming. See OG-MOTION-STUDY.md for source choreography and its application. The precise recording wording is retained, including the recognizer-confirmed phrase “acne in a bloated face.”\n\n|Audio cue time|Asset|Exact role|\n|---|---|---|\n'+'\n'.join(f'|{max(.1,T(i)):.2f}|{k}|{desc}|' for k,i,desc in plan)+'\n\nActual movements, small anticipatory staggers and recurring appearances are explicitly timed in build.py. A return/reposition is not counted as a new visual. Portraits are conceptual fictional art. No scores, diagnoses, doses or invented plan duration added. User-authorized red-zone exception: lower, moderately oversized bottom-left ten-step routine at6.0–8.65s, separated below the enlarged centred SCAM stamp.\n')
(p/'production-notes.json').write_text(json.dumps(dict(original_audio_duration=67.631021,tightened_audio_duration=narration_duration,render_duration=duration,minimum_visual_count=22,planned_distinct_visual_count=len(plan),used_distinct_visual_count=len(plan),caption_groups=len(caps),sound_cues=len(cue),voice_id='t1yzxMpe9zK42bXmI1T2',voice='Supplied K. V. Hagen; no new take',audio='Genuine-silence-only cuts at-42dB with70ms retained at both edges; no estimated word-gap cuts.',motion='Original project lateral glides, center-to-side support, hero returns, travelling early fades, focused pushes and meaningful depth emergence.',placements='Illustrationsy410, portraitsy490, phonesy460; fixed captions. Readable staggered character hierarchy: larger reset upper hero, supporting friend pair lower left; guide and sharing scenes enlarged. Tensteps lowered/reduced with clear gap below centered stamp.',phone_branding='Scan has one Remea label; analysis, results and plan have no repeated brand.',red_zone_review='Mandatory supplied references/red-zone-canvas.png overlay and alpha-aware whole-timeline check. Important ink constrained to conservative clear area; captions and audio unchanged. One user-authorized exception: lower tensteps at6.0–8.65s may extend left/bottom, with a visible gap below the centred SCAM stamp.',line_behavior='Actual stroke lengths, progressive trace, annotations clear before their subjects travel; scanbeam is a child of phone and travels with it.'),indent=2))
(p/'safe-layout-adjustments.json').write_text(json.dumps(safe_layout.changes,indent=2))
print('Built',round(duration,3),'seconds;',len(plan),'distinct visuals;',len(caps),'captions;',len(cue),'sound cues')
