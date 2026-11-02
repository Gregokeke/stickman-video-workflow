from pathlib import Path
from PIL import Image,ImageFont
import json,html,hashlib,sys
P=Path(__file__).parent;S=json.loads((P/'storyboard.json').read_text());C=json.loads((P/'captions.json').read_text());D=json.loads((P/'audio-edits.json').read_text())['video_duration'];review='--review-incomplete' in sys.argv
parts=[];css=[];schedule=[];missing=[];lanes=[0]*24
for source in S:
 s=dict(source);assert 0<=s['start']<s['handoff']<=s['end']<=D,(s['id'],s['start'],s['handoff'],s['end']);f=P/'assets/graphics'/f'{s["asset"]}.png'
 if not f.exists():
  if review:missing.append(s['asset']);continue
  raise FileNotFoundError(f)
 im=Image.open(f).convert('RGBA');l,t,r,b=im.getchannel('A').point(lambda v:255 if v>110 else 0).getbbox();iw,ih=im.size;x,y,mw,mh=s['layout'];k=min(mw/(r-l),mh/(b-t)) if s['route']!='presenter' else s['targets'][0][3]/(b-t);w=(r-l)*k;h=(b-t)*k
 if s['route']=='presenter':
  tx=(s['tip_source'][0]-l)*k;ty=(s['tip_source'][1]-t)*k
  if s.get('flip'):tx=w-tx
  _,px,py,_=s['targets'][0];x=px-tx+w/2;y=py-ty+h/2;s['tip']=[tx,ty]
 if s.get('anchor_source'):
  ax,ay=s['anchor_source'];px,py=s['anchor_screen'];x=px-(ax-l)*k+w/2;y=py-(ay-t)*k+h/2
 key=s['id'];s.update(key=key,x=x,y=y,w=w,h=h,alpha_bounds=[l,t,r,b],source_size=[iw,ih],image_scale=k);lane=next(i for i,v in enumerate(lanes) if v<=s['start']);lanes[lane]=s['end']
 inner=f'<img class="principal" src="assets/graphics/{s["asset"]}.png" alt="{html.escape(s["phrase"])}">'
 if s['route']=='presenter':inner=f'<div class="flip" style="transform:scaleX({-1 if s.get("flip") else 1})">'+inner+'</div>'
 parts.append(f'<div id="{key}" class="clip actor" data-asset="{s["asset"]}" data-start="{s["start"]}" data-duration="{s["end"]-s["start"]}" data-track-index="{lane+1}" style="z-index:{s["z"]}" data-layout-allow-overflow><div class="travel"><div class="pose">{inner}</div></div></div>')
 css.append(f'#{key} .travel{{left:{x-w/2}px;top:{y-h/2}px;width:{w}px;height:{h}px}}#{key} img.principal{{left:{-l*k}px;top:{-t*k}px;width:{iw*k}px;height:{ih*k}px}}')
 if s.get('anchor_source'):css.append(f'#{key} .pose{{transform-origin:{(s["anchor_source"][0]-l)*k}px {(s["anchor_source"][1]-t)*k}px}}')
 schedule.append(s)
accent={'brain','brains','friend','friend’s','sync','bluetooth','single','cell','neurosynchrony','sentences','glance','dark','cancelled','time','align','brainwaves','mirror','neurons','copy','mimic','feelings','scanners','synchronized','spikes','regions','millisecond','amygdala','emotion','prefrontal','cortex','decision','terrible','empathy','weirdos','nervous','trapped','echo','terrifying','choose','circle','wisely','broke','toxic','zero','ambition','downloading','broken','wiring','rewriting','become'}
for i,c in enumerate(C):
 size=62
 while size>48:
  f=ImageFont.truetype(str(P/'assets/fonts/caption-bold.ttf'),size);lines=['']
  for word in c['text'].upper().split():
   trial=(lines[-1]+' '+word).strip()
   if f.getlength(trial)>790 and lines[-1]:lines.append(word)
   else:lines[-1]=trial
  if len(lines)<=2:break
  size-=2
 text=' '.join('<b>'+html.escape(w)+'</b>' if w.lower().strip(',.!?') in accent else html.escape(w) for w in c['text'].split())
 parts.append(f'<div id="c{i}" class="clip caption" data-start="{c["start"]}" data-duration="{c["end"]-c["start"]}" data-track-index="26" style="font-size:{size}px"><span>{text}</span></div>')
parts.append((P/'micro.html').read_text())
base='''@font-face{font-family:Caption;src:url(assets/fonts/caption-bold.ttf)}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#fff;color:#101010}#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#fff}.scene-content{width:100%;height:100%;display:flex;flex-direction:column;padding:0}.actor{position:absolute;inset:0;opacity:0;pointer-events:none}.travel,.pose,.flip{position:absolute;transform-origin:center}.pose,.flip{inset:0}.actor img{position:absolute;max-width:none;filter:drop-shadow(-13px 18px 12px #0004)}.caption{position:absolute;left:105px;top:220px;width:790px;height:260px;display:flex;align-items:center;justify-content:center;font:italic 700 62px/1.12 Caption,sans-serif;text-transform:uppercase;text-align:center;letter-spacing:-1.5px;z-index:100;opacity:0}.caption span{display:block;max-width:790px}.caption b{font-weight:inherit;color:#de0b13}.edge-shadow{position:absolute;inset:-20px;z-index:80;pointer-events:none;box-shadow:inset 95px 0 120px -40px #0009,inset -95px 0 120px -40px #0009,inset 0 65px 95px -40px #0006,inset 0 -65px 95px -40px #0006}.micro{position:absolute;inset:0;width:1080px;height:1920px;pointer-events:none;z-index:40;opacity:0}.micro path,.micro line{stroke:#101010;stroke-width:8;stroke-linecap:round;stroke-linejoin:round;fill:none}.micro text{font:42px Caption,sans-serif;fill:#101010}.micro .red{stroke:#de0b13}.micro .fill{fill:#de0b13;stroke:#101010;stroke-width:4}.micro .faint{stroke:#bdbdbd;stroke-width:5}.micro .unit{fill:#ff0000;stroke:#101010;stroke-width:6}#supply-fill{transform-origin:440px 710px}'''
base+=(P/'micro.css').read_text()+'\n.protein-half{position:absolute;inset:0;transform-origin:center}.protein-top{clip-path:inset(0 0 50% 0)}.protein-bottom{clip-path:inset(50% 0 0 0)}'
js='const DATA='+json.dumps(dict(schedule=schedule,captions=C,duration=D))+';\n'+(P/'animation.js').read_text()+'\n'+(P/'micro.js').read_text()+'\n'+(P/'revision-motion.js').read_text()
out='<!doctype html><html><head><meta charset="utf-8"><title>Brainwave Besties</title><style>'+base+'\n'+'\n'.join(css)+'</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="'+str(D)+'" data-width="1080" data-height="1920"><div class="scene-content">'+''.join(parts)+'</div><div class="edge-shadow" data-layout-ignore></div><audio id="mix" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="'+str(D)+'" data-track-index="31"></audio></div><script src="assets/vendor/gsap.min.js"></script><script>'+js+'</script></body></html>'
(P/('index-review.html' if review else 'index.html')).write_text(out);(P/'production/final-schedule.json').write_text(json.dumps(schedule,indent=2));(P/'production/missing-assets.json').write_text(json.dumps(missing,indent=2))
used=set(s['asset'] for s in schedule);(P/'asset-inventory.json').write_text(json.dumps([dict(id=a,path=f'assets/graphics/{a}.png',sha256=hashlib.sha256((P/'assets/graphics'/f'{a}.png').read_bytes()).hexdigest()) for a in sorted(used)],indent=2))
print('Built',len(schedule),'appearances;',len(used),'distinct art;',len(C),'captions; missing',missing)
