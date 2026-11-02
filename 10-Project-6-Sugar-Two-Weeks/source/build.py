from pathlib import Path
import json,html,sys
from PIL import Image,ImageFont
p=Path(__file__).parent;D=json.load(open(p/'audio-edits.json'))['video_duration'];sc=json.load(open(p/'storyboard.json'));caps=json.load(open(p/'captions.json'));A={x['id']:x for x in json.load(open(p/'asset-plan.json'))};review='--review-incomplete' in sys.argv
css=[];parts=[];schedule=[];missing=[];lanes=[0]*16
for i,s in enumerate(sc):
 f=p/A[s['asset']]['path']
 if not f.exists():
  if review:missing.append(s['asset']);continue
  raise SystemExit('Missing art '+s['asset'])
 im=Image.open(f).convert('RGBA');l,t,r,b=im.getchannel('A').point(lambda v:255 if v>110 else 0).getbbox();iw,ih=im.size
 x,y,mw,mh=s['layout'];z=s.get('z',10);key='a'+str(i)
 if s['route']=='presenter':
  # Cane photo geometry comes from the verified last project; flipped to point left.
  _,tx,ty,h=s['targets'][0];mh=h;mw=1000;scale=mh/(b-t);w=(r-l)*scale;h=(b-t)*scale
  tip_src=A[s['asset']].get('cane_tip',[1144,96]);tipx=(tip_src[0]-l)*scale;tipy=(tip_src[1]-t)*scale
  tipx=w-tipx if s.get('flip',True) else tipx
  x=tx-tipx+w/2;y=ty-tipy+h/2
  s=dict(s,tip=[tipx,tipy],presenter_width=w,presenter_height=h)
 else:
  scale=min(mw/(r-l),mh/(b-t));w=(r-l)*scale;h=(b-t)*scale
 lane=next(k for k,v in enumerate(lanes) if v<=s['start']);lanes[lane]=s['end']
 inner=f'<div class="flip" style="transform:scaleX({-1 if s.get('flip',True) else 1})"><img src="{A[s["asset"]]["path"]}" alt="{html.escape(A[s["asset"]]["phrase"])}"></div>' if s['route']=='presenter' else f'<img src="{A[s["asset"]]["path"]}" alt="{html.escape(A[s["asset"]]["phrase"])}">'
 parts.append(f'<div id="{key}" class="clip actor" data-asset="{s["asset"]}" data-start="{s["start"]}" data-duration="{s["end"]-s["start"]:.5f}" data-track-index="{lane+1}" style="z-index:{z}" data-layout-allow-overflow><div class="travel"><div class="pose">{inner}</div></div></div>')
 css.append(f'#{key} .travel{{left:{x-w/2}px;top:{y-h/2}px;width:{w}px;height:{h}px}}#{key} img{{left:{-l*scale}px;top:{-t*scale}px;width:{iw*scale}px;height:{ih*scale}px}}')
 schedule.append(dict(s,key=key,x=x,y=y,w=w,h=h))
for i,c in enumerate(caps):
 size=76
 while size>54:
  font=ImageFont.truetype(str(p/'assets/fonts/caption-bold.ttf'),size);lines=['']
  for word in c['text'].split():
   trial=(lines[-1]+' '+word).strip()
   if font.getlength(trial)>740 and lines[-1]:lines.append(word)
   else:lines[-1]=trial
  if len(lines)<=2:break
  size-=2
 parts.append(f'<div class="clip caption" id="c{i}" data-start="{c["start"]}" data-duration="{c["end"]-c["start"]}" data-track-index="25" style="font-size:{size}px">{html.escape(c["text"])}</div>')
def panel(id,st,en,body):
 parts.append(f'<section class="clip diagram" id="{id}" data-start="{st}" data-duration="{en-st}" data-track-index="27">{body}</section>')
# Schematic lines have no invented clinical measurements or patient values.
for id,st,en,stable in [('crash',22.59,26.1,False),('stable',30.27,33.15,True),('stress-crash',68.54,71.0,False)]:
 curve='M150 1170 C240 1160 260 1185 330 1170 S470 1185 560 1170' if stable else 'M150 1220 C220 1220 230 770 325 790 S410 1390 555 1300'
 if id in ('crash','stable'):
  curve='M110 1170 C270 1155 360 1185 480 1170 S750 1185 965 1170' if stable else 'M110 1220 C250 1220 275 770 430 790 S650 1400 965 1300'
 axis='M100 740 V1410 H965' if id in ('crash','stable') else 'M135 740 V1410 H580'
 panel(id,st,en,f'<svg viewBox="0 0 1080 1920"><path class="axis trace" d="{axis}" pathLength="1"/><path class="curve trace" d="{curve}" pathLength="1"/><text x="140" y="680" class="diagram-title">BLOOD SUGAR</text><text x="140" y="1470" class="note">ILLUSTRATIVE PATTERN</text></svg>')
panel('insulin-low',48.4,50.22,'<div class="micro-label">INSULIN · SCHEMATIC</div><div class="mini-meter"><div id="low-fill"></div></div>')
panel('glycation-links',101.95,103.8,'<svg viewBox="0 0 1080 1920"><path class="trace" d="M485 840 L430 900" pathLength="1"/></svg>')
base='''@font-face{font-family:Caption;src:url(assets/fonts/caption-bold.ttf)}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#fff;color:#101010}#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#fff}.scene-content{width:100%;height:100%;display:flex;flex-direction:column;padding:0}.actor{position:absolute;inset:0;opacity:0;pointer-events:none}.travel,.pose,.flip{position:absolute;transform-origin:center}.pose,.flip{inset:0}.flip{transform:scaleX(-1)}.actor img{position:absolute;max-width:none;filter:drop-shadow(-10px 16px 10px #0003)}.caption{position:absolute;left:115px;top:285px;width:740px;max-height:220px;font:76px/1.1 Caption,sans-serif;text-align:center;letter-spacing:-1px;z-index:100;opacity:0}.edge-shadow{position:absolute;inset:-20px;pointer-events:none;z-index:80;box-shadow:inset 95px 0 120px -40px #0009,inset -95px 0 120px -40px #0009,inset 0 65px 95px -40px #0006,inset 0 -65px 95px -40px #0006}.diagram{position:absolute;inset:0;opacity:0;z-index:35;font-family:Caption}.diagram svg{width:100%;height:100%;overflow:visible}.trace{fill:none;stroke:#101010;stroke-width:8;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}.curve{stroke:#ed0b10;stroke-width:13}.diagram-title{font-size:36px;fill:#101010}.note{font-size:23px;fill:#101010}.plot-dot{fill:#ed0b10;opacity:0}#insulin-low{left:140px;top:1270px;width:430px;height:160px}.micro-label{font-size:27px;margin-bottom:18px}.mini-meter{height:42px;border:6px solid #101010;padding:5px;border-radius:8px}.mini-meter div{height:100%;background:#ed0b10;transform-origin:left}'''
js='const DATA='+json.dumps(dict(schedule=schedule,captions=caps,duration=D))+';\n'+(p/'animation.js').read_text()
(p/('index-review.html' if review else 'index.html')).write_text('<!doctype html><html><head><meta charset="utf-8"><title>Sugar · Two Weeks</title><style>'+base+'\n'+'\n'.join(css)+'</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="'+str(D)+'" data-width="1080" data-height="1920"><div class="scene-content">'+''.join(parts)+'</div><div class="edge-shadow" data-layout-ignore></div><audio id="mix" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="'+str(D)+'" data-track-index="31"></audio></div><script src="assets/vendor/gsap.min.js"></script><script>'+js+'</script></body></html>')
(p/'production/final-schedule.json').write_text(json.dumps(schedule,indent=2));(p/'production/missing-assets.json').write_text(json.dumps(sorted(set(missing)),indent=2));print('Ready appearances',len(schedule),'missing',len(set(missing)))
