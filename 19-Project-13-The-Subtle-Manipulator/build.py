from pathlib import Path
import json,html
from PIL import Image
p=Path(__file__).parent
R=json.loads((p/'storyboard.json').read_text()); M=json.loads((p/'moves.json').read_text());W=json.loads((p/'words.json').read_text())
duration=46.74
phrases=["The most dangerous manipulator","is not the one","that lies to your face.","It's the one that tells you","the truth,","just slightly twisted.","Real manipulators don't argue.","They agree with you.","Slowly, they nod.","When you speak,","they mirror your energy.","They make you feel seen,","understood,","validated.","And the moment your guard drops,","they plant an idea.","And they do it so subtly,","you think it came from you.","They don't control you with force.","They merely guide you","with suggestion.","They don't change your mind.","They steer it.","You think you made the choice.","That's the entire point.","You didn't.","The greatest manipulators","never convince you of anything.","They make the conditions","where you convince yourself.","And by the time you realize,","you've already done","exactly what they wanted,","willingly."]
idx=0;caps=[]
for text in phrases:
 n=len(text.split());g=W[idx:idx+n];idx+=n
 assert ' '.join(w['word'] for w in g).lower()==text.lower(),(text,g)
 caps.append(dict(text=text,start=g[0]['start'],end=g[-1]['end']))
assert idx==len(W)
for i,c in enumerate(caps):c['end']=caps[i+1]['start'] if i+1<len(caps) else duration
(p/'captions.json').write_text(json.dumps(caps,indent=2));(p/'script.txt').write_text(' '.join(w['word'] for w in W))
style="""@font-face{font-family:Caption;src:url('assets/caption-bold.ttf')}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#fff}#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#fff;color:#101010;font-family:Caption,Arial,sans-serif}.shade{position:absolute;inset:-20px;z-index:20;pointer-events:none;box-shadow:inset 95px 0 120px -40px #0009,inset -95px 0 120px -40px #0009,inset 0 65px 95px -40px #0006,inset 0 -65px 95px -40px #0006}.asset{position:absolute;opacity:0;transform-origin:50% 50%;will-change:transform,opacity}.asset img{display:block;position:absolute;max-width:none;filter:drop-shadow(-13px 18px 12px rgba(0,0,0,.28))}.caption{position:absolute;left:115px;top:220px;width:850px;height:260px;z-index:25;display:flex;align-items:center;justify-content:center;text-align:center;font-size:62px;font-weight:700;font-style:italic;text-transform:uppercase;line-height:1.12;letter-spacing:-1.8px;opacity:0}.caption span{display:block;max-width:850px;transform:scaleX(.90)}b{color:#de0b13}.negation{position:absolute;inset:0;width:100%;height:100%;z-index:12;pointer-events:none}.negation path{stroke:#101010;stroke-width:19;stroke-linecap:round;fill:none;stroke-dasharray:1000;stroke-dashoffset:1000}"""
parts=[f'<!doctype html><html><head><meta charset="utf-8"><title>The Subtle Manipulator</title><script src="assets/gsap.min.js"></script><style>{style}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920">']
geom={}
for b in R:
 f=p/'assets'/f'{b["id"]}.png'
 if not f.exists():raise FileNotFoundError(f)
 im=Image.open(f).convert('RGBA');bb=im.getchannel('A').point(lambda x:255 if x>24 else 0).getbbox();x0,y0,x1,y1=bb
 k=min(b['w']/(x1-x0),b['h']/(y1-y0));iw=im.width*k;ih=im.height*k;ix=(b['w']-(x1-x0)*k)/2-x0*k;iy=(b['h']-(y1-y0)*k)/2-y0*k
 geom[b['id']]=dict(bounds=bb,source=[im.width,im.height],fit=k,visible_width=(x1-x0)*k,visible_height=(y1-y0)*k)
 parts.append(f'<div class="asset" id="{b["id"]}" style="left:{b["cx"]-b["w"]/2}px;top:{b["cy"]-b["h"]/2}px;width:{b["w"]}px;height:{b["h"]}px;z-index:{b["layer"]}" data-layout-allow-overflow><img src="assets/{b["id"]}.png" style="left:{ix:.3f}px;top:{iy:.3f}px;width:{iw:.3f}px;height:{ih:.3f}px" alt="{html.escape(b["phrase"])}">')
 if b['id'] in ['fist']:
  # The negation is attached to its actual generated object and traces a precise diagonal.
  parts.append(f'<svg class="negation" viewBox="0 0 {b["w"]} {b["h"]}"><path id="slash-{b["id"]}" d="M{b["w"]*.18} {b["h"]*.82} L{b["w"]*.82} {b["h"]*.18}"/></svg>')
 parts.append('</div>')
accent={'dangerous','manipulator','lies','truth','twisted','manipulators','argue','agree','nod','mirror','seen','understood','validated','guard','drops','plant','idea','subtly','you.','force','guide','suggestion','change','steer','choice','point','didn\'t','greatest','convince','conditions','yourself','realize','exactly','wanted','willingly'}
for i,c in enumerate(caps):
 txt=' '.join(f'<b>{html.escape(w)}</b>' if w.lower().strip(',.!?') in accent else html.escape(w) for w in c['text'].split())
 parts.append(f'<div class="caption" id="cap{i}"><span>{txt}</span></div>')
parts.append(f'<div class="shade" data-layout-ignore></div><audio id="audio" src="assets/mix.wav" data-start="0" data-duration="{duration}" data-track-index="1"></audio></div>')
J=['window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});window.__timelines.main=tl;']
def tw(id,t,v):J.append(f'tl.to("#{id}",{json.dumps(v)},{t});')
for b in R:
 d=.48 if b['end']-b['start']>1.25 else .38
 routes={'left':(-300,25,.91),'right':(300,35,.91),'rise':(0,200,.93),'depth':(0,35,.67),'behind':(-65,125,.66)}
 dx,dy,s=routes[b['route']];dest=dict(opacity=1,x=0,y=0,scale=1,rotation=0,duration=d,ease='power3.out',immediateRender=False)
 if b['id']=='unguarded':dest.update(x=-55,y=-30,scale=.86)
 if b['id']=='sneaky':dest.update(x=-65,y=90,scale=.84)
 origin=dict(opacity=0,x=dest['x']+dx,y=dest['y']+dy,scale=dest['scale']*s,rotation=0)
 J.append(f'tl.fromTo("#{b["id"]}",{json.dumps(origin)},{json.dumps(dest)},{b["start"]});')
 if b['end']<duration:
  end=b['end'];exitd=.40;fade=.26
  # Each exit is the travelling overlap transition to the incoming layer.
  dx2=-190 if b['route'] in ['right','depth'] else 190
  tw(b['id'],end,dict(x=0,y=340,scale=.64,duration=.36,ease='power2.inOut')) if b['id']=='shield' else tw(b['id'],end,dict(x=f'+={dx2}',y='+=45',scale='*=0.84',duration=exitd,ease='power2.inOut'))
  tw(b['id'],end+.025,dict(opacity=0,duration=fade,ease='power1.out'))
for t,id,d,v in M:
 if t==18.32 and id=='unguarded':continue
 tw(id,t,dict(v,duration=d,ease='power2.inOut' if d>=.35 else 'sine.inOut'))
for id,t in [('fist',24.92)]:
 tw('slash-'+id,t,dict(strokeDashoffset=0,duration=.28,ease='power2.out'))
# The same guiding gesture returns to steer the still-visible thinking subject.
J.append('tl.fromTo("#guide",{opacity:0,x:-310,y:280,scale:.50},{opacity:1,x:-170,y:280,scale:.58,duration:.42,ease:"power3.out",immediateRender:false},30.02);')
tw('guide',30.92,dict(opacity=0,x=-340,y=220,duration=.30,ease='power1.out'))
for i,c in enumerate(caps):
 J.append(f'tl.fromTo("#cap{i}",{{opacity:0,y:15}},{{opacity:1,y:0,duration:.11,ease:"power2.out",immediateRender:false}},{c["start"]});')
 J.append(f'tl.set("#cap{i}",{{opacity:0}},{c["end"]});')
J.append('tl.seek(0);');parts.append('<script>'+'\n'.join(J)+'</script></body></html>')
(p/'index.html').write_text('\n'.join(parts));(p/'asset-geometry.json').write_text(json.dumps(geom,indent=2))
(p/'production-notes.json').write_text(json.dumps(dict(tightened_audio_duration=46.0663125,minimum_visual_count=35,planned_distinct_visual_count=35,used_distinct_visual_count=len(R),source_duration=52.27102083333333,output_duration=duration,style='Quiet-People-Loyal-Friends-1',motion_reference='Project 2 When He Goes Quiet Clean Fades',no_presenter=True,no_micro_explainers=True,return_to_center_sequences=['schemer','conversation','self-idea','choice-thought','mastermind','fulfilled']),indent=2))
print('Built',duration,'seconds,',len(R),'distinct visuals,',len(caps),'exact caption phrases')
