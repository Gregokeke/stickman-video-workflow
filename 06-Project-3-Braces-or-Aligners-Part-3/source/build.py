from pathlib import Path
from PIL import Image
import json,html,math,wave,subprocess
import numpy as np
p=Path(__file__).parent
words=json.loads((p/'words.json').read_text())
# Orthodontic term in this phrase, rendered as one word rather than Whisper's split homophone.
words[77]['word']='Aligners.';words[78]['word']=''
T=lambda i:words[i]['start']
nd=json.loads((p/'audio-edits.json').read_text())['duration'];duration=math.ceil((nd+.28)*30)/30
starts=[0,4,6,9,11,15,17,20,22,24,27,29,31,34,36,37,39,42,44,46,48,50,51,54,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,88,90,92,95,97,99,100,102,104,106,108,109,111,113,115,118,120,122,124,126,128,130,132]
caps=[dict(text=' '.join(w['word'] for w in words[a:b] if w['word']),start=T(a),end=T(b) if b<len(words) else duration) for a,b in zip(starts,starts[1:]+[len(words)])]
(p/'captions.json').write_text(json.dumps(caps,indent=2));(p/'script.txt').write_text(' '.join(c['text'] for c in caps))
plan=[('bracehero',0,'Large braced smile hook; wearing braces'),('bracesmouth',4,'Exact metal-bracket/wire close-up'),('adultlife',9,'Preparation for adult life series'),('uncertain',17,'Considering whether braces are right'),('filtercard',27,'braces wialiska TikTok mask identified from supplied reference'),('yearone',37,'One-year commitment'),('yearthree',44,'Sometimes up to three years, not a personal prediction'),('speech',46,'Changes in speech with braces'),('jawpain',51,'Soreness/discomfort gesture'),('soretooth',55,'Tooth discomfort close-up'),('smilehero',57,'Result and confident straight-smile payoff'),('straightmouth',65,'Even straight white teeth close-up'),('guide',73,'Another option, presenter'),('aligner',77,'Empty clear removable aligner shell'),('alignerfit',79,'Matched tray above teeth and fitting arrow'),('alignerwear',88,'Thin clear shell over teeth, close-up'),('daily',92,'Almost invisible in daily life'),('crookedmouth',95,'Severe crowding illustration; limitation phrase'),('consult',102,'Actual clinician/patient consultation'),('dentist',111,'Professional dental care'),('earlycare',117,'Earlier tooth-care action'),('tagphone',126,'Tag friend, readable @FRIEND send UI'),('friendbraces',128,'Friendly crooked-smile friend, relevant closing joke')]
keys=[k for k,_,_ in plan]
# Normalize the actual alpha silhouette in CSS; source PNGs remain untouched.
meta={}
for k in keys:
 im=Image.open(p/'assets'/f'{k}.png').convert('RGBA');box=im.getchannel('A').point(lambda a:255 if a>24 else 0).getbbox();x0,y0,x1,y1=box;bw,bh=x1-x0,y1-y0;f=1000/max(bw,bh);left=(1000-bw*f)/2-x0*f;top=(1000-bh*f)/2-y0*f
 meta[k]=dict(nw=im.width,nh=im.height,bbox=box,ink=[(1000-bw*f)/2,(1000-bh*f)/2,(1000+bw*f)/2,(1000+bh*f)/2],img=[left,top,im.width*f,im.height*f])
(p/'asset-layout.json').write_text(json.dumps(meta,indent=2))
css=(p/'design.css').read_text()+'''
.asset{left:0;top:0;width:1000px;height:1000px;transform-origin:0 0;z-index:3}
.asset img{position:absolute;object-fit:fill;max-width:none;filter:drop-shadow(-13px 18px 12px rgba(0,0,0,.28))}
.annotation{position:absolute;inset:0;width:1000px;height:1000px;overflow:visible;pointer-events:none;z-index:5}
.annotation path{fill:none;stroke:#101010;stroke-width:16;stroke-linecap:round;stroke-linejoin:round}
.annotation .light{stroke:white;stroke-width:11}
.label{position:absolute;font:700 46px Caption,sans-serif;text-align:center;opacity:0;color:#101010;z-index:10;white-space:nowrap}
.part{left:110px;top:500px;font-size:42px;letter-spacing:1px;text-transform:uppercase;color:#de0b13}
.qualifier{left:550px;top:520px;font-size:42px;color:#de0b13}
'''
parts=[f'<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>{css}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920">']
# Local traced overlays travel with the generated objects. Fitting anchor refined after visual review.
paths={'alignerfit':[('fit-arrow','M500 535 L500 715 L472 680 M500 715 L528 680')], 'aligner':[('not-left','M220 220 L780 780'),('not-right','M780 220 L220 780')], 'soretooth':[('pain-left','M860 485 A105 105 0 1 1 650 485 A105 105 0 1 1 860 485')]}
for k,_,desc in plan:
 l,t,w,h=meta[k]['img'];svg=''
 if k in paths:svg='<svg class="annotation" viewBox="0 0 1000 1000">'+''.join(f'<path id="{pid}" d="{d}" opacity="0"/>' for pid,d in paths[k])+'</svg>'
 parts.append(f'<div class="asset" id="{k}" data-layout-allow-overflow><img src="assets/{k}.png" alt="{desc}" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px">{svg}</div>')
accent={'braces','right','adult','three','tiktok','mask','one','year','years','speech','teeth','hurt','result','worth','straight','attractive','another','option','aligners','clear','trays','fit','invisible','daily','severe','crookedness','doctor','consult','earlier','care','tag','friend','urgently','guide'}
for i,c in enumerate(caps):
 txt=' '.join(f'<b>{html.escape(w)}</b>' if w.lower().strip(',.!?') in accent else html.escape(w) for w in c['text'].split());parts.append(f'<div class="caption" id="cap{i}"><span>{txt}</span></div>')
parts.append('<div id="part" class="label part">PART 3</div><div id="upto" class="label qualifier">UP TO</div>')
parts.append(f'<div class="shade"></div><audio id="audio" src="assets/mix.wav" data-start="0" data-duration="{duration}" data-track-index="1"></audio></div>')
js=['window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});window.__timelines.main=tl;'];state={};timeline=[];cue=[]
H=[90,580,740,900];HUP=[100,570,720,760];SUP=[90,1090,480,500];RIGHT=[330,570,510,660];LEFT=[90,600,430,600]
def fit(k,box):
 x,y,w,h=box;il,it,ir,ib=meta[k]['ink'];s=min(w/(ir-il),h/(ib-it));return dict(x=x+(w-(ir-il)*s)/2-il*s,y=y+(h-(ib-it)*s)/2-it*s,scale=s)
def clamp(k,v):
 il,it,ir,ib=meta[k]['ink'];s=v['scale'];v=dict(v);v['x']=max(80-il*s,min(840-ir*s,v['x']));v['y']=max(550-it*s,min(1590-ib*s,v['y']));return v
def tw(k,t,v,start=None):
 if start is None:js.append(f'tl.to("#{k}",{json.dumps(v)},{round(t,4)});')
 else:js.append(f'tl.fromTo("#{k}",{json.dumps(start)},{json.dumps(dict(v,immediateRender=False))},{round(t,4)});')
 timeline.append(dict(asset=k,time=t,duration=v.get('duration',0),properties=list(v)))
def sound(t,name='whoosh',db=-22.5,d=.5):cue.append((max(.1,t),name,d,db))
def enter(k,t,box=H,d=.58,dx=0,dy=140,ease='power3.out',fx=True):
 v=clamp(k,fit(k,box));st=clamp(k,dict(v,x=v['x']+dx,y=v['y']+dy,scale=v['scale']*.86));tw(k,t,dict(v,opacity=1,duration=d,ease=ease),dict(st,opacity=0));state[k]=v
 if fx:sound(t,'whoosh-short' if abs(dy)>abs(dx) else 'whoosh',-22.5,min(.5,d))
def move(k,t,box,d=.58):
 v=clamp(k,fit(k,box));tw(k,t,dict(v,duration=d,ease='power2.inOut'));state[k]=v
def exit(k,t,dx=110,dy=20,d=.53):
 v=clamp(k,dict(state[k],x=state[k]['x']+dx,y=state[k]['y']+dy,scale=state[k]['scale']*.90));tw(k,t,dict(v,duration=d,ease='power2.in'));tw(k,t+.025,dict(opacity=0,duration=.29,ease='power1.out'));state[k]=v

def swap(k,t,old,box=H,dx=-190,dy=0,d=.58):
 enter(k,t,box,d,dx,dy)
 for o in ([old] if isinstance(old,str) else old):exit(o,t,dx=-dx*.65,dy=35)
def fade(k,t,d=.22):tw(k,t,dict(opacity=0,duration=d,ease='power1.out'))
def draw(pid,t,end,d=.6):
 js.append(f'tl.set("#{pid}",{{opacity:1,strokeDasharray:document.querySelector("#{pid}").getTotalLength(),strokeDashoffset:document.querySelector("#{pid}").getTotalLength()}},{t});');tw(pid,t,dict(strokeDashoffset=0,duration=d,ease='sine.inOut'));fade(pid,end,.16);sound(t,'draw',-22,.35)
def label(k,t,end):tw(k,t,dict(opacity=1,y=0,duration=.18,ease='power3.out'),dict(opacity=0,y=15));fade(k,end,.15)
# Large active hook: full braced figure develops into the exact bracket/wire detail.
enter('bracehero',.10,H,d=.52,dx=-170,dy=60)
move('bracehero',T(4),[90,1100,480,490],.52)
enter('bracesmouth',T(4),[120,590,700,450],dx=150,dy=0,d=.52)
swap('adultlife',T(9),['bracehero','bracesmouth'],dx=190)
label('part',T(15),5.95)
swap('uncertain',T(17),'adultlife',dx=-180)
move('uncertain',T(27),[90,1100,480,490],.50)
enter('filtercard',T(27),[100,600,740,420],dx=160,dy=0,d=.50)
swap('bracehero',T(31),['uncertain','filtercard'],dx=-180)
move('bracehero',T(37),[90,1100,480,490],.52)
enter('yearone',T(37),[300,580,540,510],dx=150,dy=0,d=.52);sound(T(37),'click',-21,.16)
enter('yearthree',T(44),[280,600,560,500],dx=120,dy=-70,d=.45);exit('yearone',T(44),dx=-110,dy=45,d=.45)
label('upto',T(42),14.24);sound(T(44),'whoosh-short',-22,.35)
# Consequences receive specific actions, then move cleanly into the positive result.
swap('speech',T(46),['bracehero','yearthree'],dx=-180)
sound(T(50),'click',-23,.14)
swap('jawpain',T(51),'speech',dx=160)
move('jawpain',T(55),[90,1110,480,480],.43)
enter('soretooth',T(55),[300,580,540,510],dx=150,dy=0,d=.43)
draw('pain-left',17.26,17.92,.30);sound(T(55),'deflate',-22,.45)
swap('smilehero',T(57),['jawpain','soretooth'],dx=-170)
sound(T(61),'chime',-21,.40)
swap('straightmouth',T(65),'smilehero',[110,650,710,550],dx=150,d=.48)
enter('smilehero',T(67),[360,570,480,740],dx=140,dy=0,d=.52)
move('straightmouth',T(67),[90,1300,420,240],.52)
sound(T(72),'chime',-22,.36)
# Clear aligners are removable shells, followed by a precise fitting demonstration.
swap('guide',T(73),['straightmouth','smilehero'],dx=-180)
move('guide',T(77),[90,1110,480,480],.50)
enter('aligner',T(77),[200,590,640,480],dx=150,dy=0,d=.50)
swap('alignerfit',T(79),['guide','aligner'],[100,600,740,820],dx=-160,d=.46)
draw('fit-arrow',T(84),27.62,.60);sound(27.12,'click',-22,.17)
swap('alignerwear',T(88),'alignerfit',[110,630,710,750],dx=160,d=.46)
swap('daily',T(92),'alignerwear',dx=-150,d=.46)
# Limitation: the negation belongs to the aligner, not a random person or smile.
swap('crookedmouth',T(95),'daily',[100,600,740,490],dx=150,d=.47)
enter('aligner',T(95),[160,1160,610,400],dx=-150,dy=50,d=.47)
draw('not-left',T(97),33.12,.30);draw('not-right',T(97)+.12,33.12,.30);sound(T(97),'record-scratch',-22,.40)
swap('consult',T(102),['crookedmouth','aligner'],[90,570,740,1010],dx=-170)
sound(T(110),'click',-23,.16)
# Consultation and early care lead to a prominent clean smile; then the precise tag action.
swap('dentist',T(111),'consult',dx=160,d=.48)
swap('earlycare',T(117),'dentist',dx=-150,d=.47);sound(T(117),'soft-brush',-22,.38)
swap('smilehero',T(120),'earlycare',[90,560,740,980],dx=160,d=.50)
sound(T(125),'chime',-21,.40)
swap('tagphone',T(126),'smilehero',[380,570,460,510],dx=-150,d=.48)
enter('friendbraces',T(128),[90,1100,480,490],dx=-140,dy=30,d=.50)
sound(T(128),'click',-21,.16);sound(T(133),'whoosh-short',-23,.36)
for i,c in enumerate(caps):tw(f'cap{i}',c['start'],dict(opacity=1,y=0,duration=.10,ease='power2.out'),dict(opacity=0,y=12));js.append(f'tl.set("#cap{i}",{{opacity:0}},{c["end"]});')
js.append('tl.seek(0);');parts.append('<script>'+'\n'.join(js)+'</script></body></html>');(p/'index.html').write_text('\n'.join(parts))
exec((p/'mixer.py').read_text())
(p/'asset-plan.json').write_text(json.dumps(plan,indent=2));(p/'motion-events.json').write_text(json.dumps(timeline,indent=2))
(p/'storyboard.md').write_text('# Braces or Aligners — context storyboard\n\n23 distinct illustrations on '+str(round(nd,3))+' seconds of gently tightened narration. Duration minimum14, never a cap. Actual actions translated from the supplied cat reference to our established stickman art.\n\n|Time|Asset|Meaning|\n|---|---|---|\n'+'\n'.join(f'|{T(i):.2f}|{k}|{d}|' for k,i,d in plan)+'\n\nRepeated appearances do not inflate the count. Earlier art remains only while relevant; ordinary replacements travel and fade early. Filter exact name verified in8s frame. “Aligners” is the orthodontic term; Whisper split it as a homophone, corrected in caption generation without changing the supplied recording. No independent clinical claims, personalized duration predictions or app advertisement added.\n')
(p/'production-notes.json').write_text(json.dumps(dict(title='Braces or Aligners — Part 3',source_duration=44.930625,tightened_duration=nd,render_duration=duration,minimum_visuals=14,distinct_used_visuals=len(plan),new_visuals=21,reused_visuals=2,caption_groups=len(caps),sound_cues=len(cue),voice='Supplied K. V. Hagen; no new generation',voice_id='t1yzxMpe9zK42bXmI1T2',filter_reference='braces wialiska from source frame8s',audio_method='Only genuine silence >.26s at-42dB,70ms retained on both edges. No word-gap cuts.',art='Flat red/black ImageGen cutouts, alpha-bound silhouette fitting, large readable people, separate faint directional shadows.',guide='references/red-zone-canvas.png; no exceptions; guide absent from clean export.',inspection_note='CLI inspect:0 errors,0 warnings; one connector-orphan info at27.001s. The fit arrow connects two visible regions in the same generated PNG, so no separate DOM endpoints exist. Actual exported geometry visually verified; no real orphan.'),indent=2))
print('Built',duration,'seconds;',len(plan),'illustrations;',len(caps),'captions;',len(cue),'sound cues')
