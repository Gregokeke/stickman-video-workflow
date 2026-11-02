from pathlib import Path
from PIL import Image,ImageFont
import json,html,sys,hashlib
import numpy as np
p=Path(__file__).parent;D=json.loads((p/'audio-edits.json').read_text())['video_duration'];A={x['id']:x for x in json.loads((p/'asset-plan.json').read_text())};S=json.loads((p/'storyboard.json').read_text());C=json.loads((p/'captions.json').read_text());review='--review-incomplete' in sys.argv
parts=[];css=[];schedule=[];missing=[];lanes=[0]*20
for s0 in S:
 s=dict(s0);f=p/A[s['asset']]['path']
 if not f.exists():
  if review:missing.append(s['asset']);continue
  raise FileNotFoundError(f)
 im=Image.open(f).convert('RGBA');l,t,r,b=im.getchannel('A').point(lambda v:255 if v>110 else 0).getbbox();iw,ih=im.size;x,y,mw,mh=s['layout'];k=min(mw/(r-l),mh/(b-t)) if s['route']!='presenter' else s['targets'][0][3]/(b-t);w=(r-l)*k;h=(b-t)*k
 if s['route']=='presenter':
  tx=(s['tip_source'][0]-l)*k;ty=(s['tip_source'][1]-t)*k
  if s.get('flip'):tx=w-tx
  _,px,py,_=s['targets'][0];x=px-tx+w/2;y=py-ty+h/2;s['tip']=[tx,ty]
 key=s['id'];s.update(key=key,x=x,y=y,w=w,h=h,alpha_bounds=[l,t,r,b]);lane=next(i for i,a in enumerate(lanes) if a<=s['start']);lanes[lane]=s['end']
 inner='<img class="principal" src="'+A[s['asset']]['path']+'" alt="'+html.escape(A[s['asset']]['phrase'])+'">'
 if s['asset']=='thermometer':inner+='<div class="thermo-window"><div class="thermo-fluid"></div></div>'
 if s['asset']=='clock':
  label=html.escape(s['clock_text']);font=143 if len(s['clock_text'])<=7 else 115
  inner+=f'<svg class="clock-label" style="left:{-l*k}px;top:{-t*k}px;width:{iw*k}px;height:{ih*k}px" viewBox="0 0 {iw} {ih}"><defs><clipPath id="{key}-display-clip"><path d="M430 435 L1260 328 Q1300 323 1305 367 L1325 598 Q1328 628 1280 638 L480 740 Q440 743 437 707 Z"/></clipPath></defs><g clip-path="url(#{key}-display-clip)"><text x="875" y="542" text-anchor="middle" dominant-baseline="central" transform="rotate(-7.2 875 542)" font-family="Caption" font-size="{font}" fill="#101010" letter-spacing="-1">{label}</text></g></svg>' 
 if s['asset']=='clock-shell':
  ar=np.array(im);ys,xs=np.where((ar[:,:,:3].min(axis=2)>225)&(ar[:,:,3]>200));cx=(xs.min()+xs.max())/2;cy=(ys.min()+ys.max())/2;rad=min(xs.max()-xs.min(),ys.max()-ys.min())/2;s['clock_origin']=[float(cx),float(cy)]
  inner+=f'<svg class="clock-hands" style="left:{-l*k}px;top:{-t*k}px;width:{iw*k}px;height:{ih*k}px" viewBox="0 0 {iw} {ih}"><g id="clock-hour"><path d="M{cx} {cy} L{cx} {cy-rad*.48}"/></g><g id="clock-minute"><path d="M{cx} {cy} L{cx} {cy-rad*.76}"/></g><circle cx="{cx}" cy="{cy}" r="22"/></svg>' 
 if s['asset']=='survival-switch':
  inner+='<div class="switch-slot"><div class="switch-knob"><span class="switch-off">OFF</span><span class="switch-on">ON</span></div></div>'
 if s['asset']=='dividing-cells':
  image=inner
  inner='<div class="division-half division-left">'+image+'</div><div class="division-half division-right">'+image+'</div>'
 if s['route']=='presenter':inner='<div class="flip" style="transform:scaleX('+('-1' if s.get('flip') else '1')+')">'+inner+'</div>'
 parts.append(f'<div id="{key}" class="clip actor" data-asset="{s["asset"]}" data-start="{s["start"]}" data-duration="{s["end"]-s["start"]}" data-track-index="{lane+1}" style="z-index:{s["z"]}" data-layout-allow-overflow><div class="travel"><div class="handoff"><div class="pose">{inner}</div></div></div></div>')
 css.append(f'#{key} .travel{{left:{x-w/2}px;top:{y-h/2}px;width:{w}px;height:{h}px}}#{key} img.principal{{left:{-l*k}px;top:{-t*k}px;width:{iw*k}px;height:{ih*k}px}}')
 schedule.append(s)
accent={'fast','fasting','autophagy','senescent','self-eating','broken','retired','rent','free','alive','useless','rotting','inflammation','puffy','stiff','80','20s','cannibalizes','junk','amino','fuel','fog','depuffs','joints','garbage','healing','repair','stem','fresh','healthy','tighter','recovery','gut','war','jaw','divine','protein','bioavailable','absorb','100%','muscles','amino','repair','joints','antioxidants','lutein','zeaxanthin','retinas','blue','cataracts','choline','fat','liver','acetylcholine','focus','concentration','memory','cholesterol','HDL','good','plaque','pastry','insulin','stabilized','functional','crashing','coma','stop','bed','fork','weight','less','hijacking','corpse','blood','gut','heart','heat','cool','repair','40%','tanks','energy','cortisol','anxious','ghrelin','leptin','wrecked','exhausted','ravenous','trash','11','unhinged','fridge','raccoon','simple','three','five','insulin','settle','tonight'}
for i,c in enumerate(C):
 size=62
 while size>48:
  f=ImageFont.truetype(str(p/'assets/fonts/caption-bold.ttf'),size);lines=['']
  for word in c['text'].upper().split():
   trial=(lines[-1]+' '+word).strip()
   if f.getlength(trial)>790 and lines[-1]:lines.append(word)
   else:lines[-1]=trial
  if len(lines)<=2:break
  size-=2
 text=' '.join('<b>'+html.escape(w)+'</b>' if w.lower().strip(',.!?') in accent else html.escape(w) for w in c['text'].split())
 parts.append(f'<div id="c{i}" class="clip caption" data-start="{c["start"]}" data-duration="{c["end"]-c["start"]}" data-track-index="25" style="font-size:{size}px"><span>{text}</span></div>')
parts.append((p/'micro-explanations.html').read_text())
base='''@font-face{font-family:Caption;src:url(assets/fonts/caption-bold.ttf)}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#fff;color:#101010}#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#fff}.scene-content{width:100%;height:100%;display:flex;flex-direction:column;padding:0}.actor{position:absolute;inset:0;opacity:0;pointer-events:none}.travel,.pose,.flip,.handoff{position:absolute;transform-origin:center}.pose,.flip,.handoff{inset:0}.actor img{position:absolute;max-width:none;filter:drop-shadow(-13px 18px 12px #0004)}.caption{position:absolute;left:105px;top:220px;width:790px;height:260px;display:flex;align-items:center;justify-content:center;font:italic 700 62px/1.12 Caption,sans-serif;text-transform:uppercase;text-align:center;letter-spacing:-1.5px;z-index:100;opacity:0}.caption span{display:block;max-width:790px}.caption b{font-weight:inherit;color:#de0b13}.edge-shadow{position:absolute;inset:-20px;z-index:80;pointer-events:none;box-shadow:inset 95px 0 120px -40px #0009,inset -95px 0 120px -40px #0009,inset 0 65px 95px -40px #0006,inset 0 -65px 95px -40px #0006}#micro{position:absolute;inset:0;width:1080px;height:1920px;pointer-events:none;z-index:40}.trace{stroke:#101010;stroke-width:8;stroke-linecap:round;stroke-linejoin:round;fill:none;opacity:0}#signal-disrupt{stroke:#de0b13;stroke-width:12}#timing-label{position:absolute;left:400px;top:1050px;width:190px;text-align:center;font:42px/1.05 Caption;opacity:0;z-index:45}.thermo-window{position:absolute;left:42%;top:7%;width:16%;height:68%;overflow:hidden;border-radius:10px;background:#fff}.thermo-fluid{position:absolute;inset:0;background:#de0b13;transform-origin:center bottom}.clock-display{position:absolute;left:25%;top:32%;width:65%;height:36%;display:flex;align-items:center;justify-content:center;gap:7px;background:transparent;border-radius:8px;transform:rotate(-7deg);font:50px/1 Caption;font-variant-numeric:tabular-nums;letter-spacing:-3px}.clock-display span{font-size:19px;letter-spacing:0}.diamond-glints{position:absolute;pointer-events:none;overflow:visible}.diamond-glint{opacity:0;fill:#fff;stroke:#101010;stroke-width:5;transform-box:fill-box;transform-origin:center}.clock-label{position:absolute;pointer-events:none;overflow:hidden}.clock-hands{position:absolute;inset:0;width:100%;height:100%;overflow:visible}.clock-hands path{stroke:#101010;stroke-width:26;stroke-linecap:round}.clock-hands circle{fill:#101010}'''
base+=(p/'micro-explanations.css').read_text()
js='const DATA='+json.dumps(dict(schedule=schedule,captions=C,duration=D,micro=json.loads((p/'micro-times.json').read_text())))+';\n'+(p/'animation.js').read_text()+'\n'+(p/'micro-explanations.js').read_text()
out='<!doctype html><html><head><meta charset="utf-8"><title>Fasting — Self Recycling</title><style>'+base+'\n'+'\n'.join(css)+'</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="'+str(D)+'" data-width="1080" data-height="1920"><div class="scene-content">'+''.join(parts)+'</div><div class="edge-shadow" data-layout-ignore></div><audio id="mix" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="'+str(D)+'" data-track-index="31"></audio></div><script src="assets/vendor/gsap.min.js"></script><script>'+js+'</script></body></html>'
(p/('index-review.html' if review else 'index.html')).write_text(out);(p/'production/final-schedule.json').write_text(json.dumps(schedule,indent=2));(p/'production/missing-assets.json').write_text(json.dumps(missing,indent=2))
(p/'asset-inventory.json').write_text(json.dumps([dict(id=a['id'],path=a['path'],sha256=hashlib.sha256((p/a['path']).read_bytes()).hexdigest(),kind=a['kind']) for a in A.values() if (p/a['path']).exists()],indent=2))
print('Built',len(schedule),'appearances;',len(set(x['asset'] for x in schedule)),'distinct art;',len(C),'captions; missing',missing)
