from pathlib import Path
import json,html,hashlib,math,argparse
from PIL import Image
import numpy as np
P=Path(__file__).parent;S=json.loads((P/'full-storyboard.json').read_text());parser=argparse.ArgumentParser();parser.add_argument('--until',type=float);args=parser.parse_args();D=args.until or S['duration'];inventory={};markup=[]
if args.until:
 S['duration']=D;S['actors']=[dict(a,end=min(a['end'],D))for a in S['actors']if a['cue']<D];S['guides']=[dict(g,end=min(g['end'],D))for g in S['guides']if g['start']<D]
for asset in dict.fromkeys(a['asset']for a in S['actors']):
 p=P/'assets/graphics'/f'{asset}.png'
 if not p.exists():raise SystemExit('Artwork still pending: '+asset)
 im=Image.open(p).convert('RGBA');b=im.getchannel('A').point(lambda v:255 if v>=12 else 0).getbbox();assert b
 inventory[asset]={'path':f'assets/graphics/{asset}.png','native':list(im.size),'alpha_bounds':list(b),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'original':True}
for i,a in enumerate(S['actors']):
 v=inventory[a['asset']];l,t,r,b=v['alpha_bounds'];f=min(a['max_width']/(r-l),a['max_height']/(b-t));a.update(width=(r-l)*f,height=(b-t)*f,factor=f,native=v['native'],alpha_bounds=v['alpha_bounds'])
 # Find an actual foreground source pixel near each requested extraction anchor.
 # This prevents a detail from emerging from a white hole between limbs.
 if a['parent']:
  parent=next(x for x in S['actors']if x['id']==a['parent']);pv=inventory[parent['asset']];pl,pt,pr,pb=pv['alpha_bounds'];px=pl+a['anchor'][0]*(pr-pl);py=pt+a['anchor'][1]*(pb-pt);im=Image.open(P/pv['path']).convert('RGBA');arr=np.array(im);ys,xs=np.where(arr[:,:,3]>180);dist=(xs-px)**2+(ys-py)**2;j=int(np.argmin(dist));a['anchor']=[(float(xs[j])-pl)/(pr-pl),(float(ys[j])-pt)/(pb-pt)]
 img=f'<img src="{v["path"]}" alt="{a["asset"]}" style="width:{v["native"][0]*f}px;height:{v["native"][1]*f}px;left:{-l*f}px;top:{-t*f}px">'
 overlay=''
 if a['id'] in ['genetic-helix','childhood-photo','horoscope-wheel','shrinking-brain-contrast']:
  overlay='<svg class="actor-overlay" viewBox="0 0 100 100" preserveAspectRatio="none"><path class="negation" d="M14 13 L87 87" pathLength="1" fill="none" stroke="#de0b13" stroke-width="4.4" stroke-linecap="round"/></svg>'
 if a['id']=='power-difference':
  overlay+=f'<svg id="power-bar-overlay" class="native-overlay" viewBox="0 0 1536 1024" style="width:{1536*f}px;height:{1024*f}px;left:{-l*f}px;top:{-t*f}px"><defs><clipPath id="bar-left-region"><path d="M375 225 L680 245 L655 347 L364 323 Z"/></clipPath><clipPath id="bar-right-region"><path d="M804 243 L1205 278 L1183 398 L778 354 Z"/></clipPath><clipPath id="bar-left-reveal"><rect id="bar-left-wipe" x="360" y="210" width="0" height="160"/></clipPath><clipPath id="bar-right-reveal"><rect id="bar-right-wipe" x="775" y="230" width="0" height="190"/></clipPath></defs><path d="M375 225 L680 245 L655 347 L364 323 Z" fill="#f6f7f8"/><path d="M804 243 L1205 278 L1183 398 L778 354 Z" fill="#f6f7f8"/><g clip-path="url(#bar-left-region)"><g clip-path="url(#bar-left-reveal)"><image href="assets/graphics/power-difference.png" width="1536" height="1024"/></g></g><g clip-path="url(#bar-right-region)"><g clip-path="url(#bar-right-reveal)"><image href="assets/graphics/power-difference.png" width="1536" height="1024"/></g></g></svg>'
 if a['id']=='neuron':
  overlay+=f'<svg class="native-overlay" viewBox="0 0 1774 887" style="width:{1774*f}px;height:{887*f}px;left:{-l*f}px;top:{-t*f}px"><path id="axon-signal" d="M480 462 C670 476 1100 475 1435 480" fill="none" stroke="white" stroke-width="23" stroke-linecap="round"/></svg>'
 if a['id']=='neural-network':
  overlay+=f'<svg class="native-overlay" viewBox="0 0 1536 1024" style="width:{1536*f}px;height:{1024*f}px;left:{-l*f}px;top:{-t*f}px"><circle class="network-node" cx="315" cy="555" r="38" fill="white"/><circle class="network-node" cx="830" cy="375" r="38" fill="white"/><circle class="network-node" cx="1340" cy="565" r="38" fill="white"/></svg>'
 markup.append(f'<div id="{a["id"]}" class="actor clip" data-start="{a["start"]}" data-duration="{a["end"]-a["start"]}" data-track-index="{i+1}" style="left:{a["x"]-a["width"]/2}px;top:{a["y"]-a["height"]/2}px;width:{a["width"]}px;height:{a["height"]}px">{img}{overlay}</div>')
for j,g in enumerate(S['guides']):
 im=Image.open(P/'references'/g['pose']).convert('RGBA');g['native']=list(im.size);g['alpha_bounds']=list(im.getchannel('A').getbbox())
 inventory[g['pose']]={'path':'references/'+g['pose'],'native':g['native'],'alpha_bounds':g['alpha_bounds'],'original':False,'tip':g['tip']}
 markup.append(f'<div id="{g["id"]}" class="instructor clip" data-start="{g["start"]}" data-duration="{g["end"]-g["start"]}" data-track-index="{130+j}" data-layout-allow-overflow="true"><img src="references/{g["pose"]}" width="{g["native"][0]}" height="{g["native"][1]}" style="transform:scaleX({-1 if g["flip"] else 1})" alt="Approved instructor"></div>')
W=json.loads((P/'words.json').read_text());groups=[(0,5),(6,11),(12,16),(17,22),(23,28),(29,32),(33,36),(37,40),(41,43),(44,46),(47,50),(51,54),(55,57),(58,61),(62,66),(67,70),(71,76),(77,82),(83,87),(88,93),(94,96),(97,101),(102,104),(105,107),(108,110),(111,115),(116,118),(119,122),(123,126),(127,131),(132,135),(136,139),(140,142),(143,143),(144,147),(148,150),(151,153),(154,158),(159,160),(161,163),(164,165),(166,169),(170,175),(176,178),(179,183),(184,186),(187,191),(192,197),(198,200),(201,204),(205,206),(207,209),(210,214),(215,217),(218,223),(224,227),(228,233),(234,238),(239,245),(246,249),(250,253),(254,258),(259,264),(265,268),(269,272),(273,277),(278,280),(281,285),(286,287),(288,291),(292,294),(295,298),(299,304),(305,308),(309,314),(315,318),(319,322),(323,327),(328,331)]
assert [i for a,b in groups for i in range(a,b+1)]==list(range(len(W)))
emph=set('aging biceps chest toothpicks legs lower look feel perform younger dust study twins strength brain rots wild power sharper cognitive MRI gray matter neurons forgetting stronger healthier why muscles contract resistance chemical messengers myokines protein BDNF miracle grow cells neural pathways shrinking craziest identical genetics childhood horoscope raw older mental taxes walking dying 70 80 walkers paranoia stairs misstep shattered hip afterlife squats thrusts lunges shorts biological insurance nervous firing intact working blankly stop skipping day'.lower().split())
caps=[]
for k,(a,b)in enumerate(groups):
 start=0 if not k else W[a]['start'];end=min(D,W[groups[k+1][0]]['start'])if k+1<len(groups)else D
 if start>=D:continue
 words=[]
 for w in W[a:b+1]:
  txt=w['word'];norm=txt.lower().strip('.,?!;:');val=html.escape(txt);val='<span>'+val+'</span>'if norm in emph else val
  if txt.startswith('-') and words:words[-1]+=val
  else:words.append(val)
 content=' '.join(words);text=' '.join(w['word']for w in W[a:b+1]);caps.append(dict(id=f'cap-{k}',start=start,end=end,text=text,first_word=a,last_word=b))
 markup.append(f'<div id="cap-{k}" class="caption clip" data-start="{start}" data-duration="{end-start}" data-track-index="150"><div class="caption-copy">{content}</div></div>')
css='''@font-face{font-family:Caption;src:url(assets/fonts/caption-bold.ttf)}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#fff}#main{position:relative;width:1080px;height:1920px;overflow:hidden;background:#fff}.stage{position:relative;width:100%;height:100%;padding:0}.actor{position:absolute;opacity:0;transform-origin:50% 50%;will-change:transform,opacity}.actor img{position:absolute;max-width:none;filter:drop-shadow(-12px 18px 12px #0004)}.actor-overlay{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none}.native-overlay{position:absolute;overflow:visible;pointer-events:none}.negation{stroke-dasharray:1;stroke-dashoffset:1}.caption{position:absolute;left:105px;top:220px;width:790px;height:260px;display:flex;align-items:center;justify-content:center;text-align:center;font:italic 700 62px/1.10 Caption,sans-serif;color:#101010;text-transform:uppercase;opacity:0;z-index:100}.caption-copy{width:100%}.caption span{color:#de0b13}.instructor{position:absolute;left:0;top:0;opacity:0;transform-origin:0 0;z-index:35;will-change:transform,opacity}.instructor img{filter:drop-shadow(-13px 18px 12px #0004)}.edge-shadow{position:absolute;inset:-20px;z-index:80;pointer-events:none;box-shadow:inset 95px 0 120px -40px #0009,inset -95px 0 120px -40px #0009,inset 0 65px 95px -40px #0006,inset 0 -65px 95px -40px #0006}#aging-host,#cap-0{opacity:1}'''
S['captions']=caps
(P/'full-schedule.js').write_text('window.FULL='+json.dumps(S)+';')
code=(P/'full-animation.js').read_text()
audio='progress-mix.wav'if args.until else'mix.wav'
out=f'<!doctype html><html><head><meta charset="utf-8"><title>Leg Power — Brain Insurance</title><style>{css}</style></head><body><div id="main" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920"><div class="stage">'+''.join(markup)+f'<div class="edge-shadow" data-layout-ignore="true"></div></div><audio id="master-audio" class="clip" src="assets/audio/{audio}" data-start="0" data-duration="{D}" data-track-index="160" data-volume="1"></audio></div><script src="assets/vendor/gsap.min.js"></script><script src="full-schedule.js"></script><script>'+code+'</script></body></html>'
(P/'index.html').write_text(out);(P/'full-captions.json').write_text(json.dumps(caps,indent=2));(P/'full-asset-inventory.json').write_text(json.dumps(inventory,indent=2));(P/'full-storyboard-built.json').write_text(json.dumps(S,indent=2));print('Built',D,'seconds,',len({a['asset']for a in S['actors']}),'originals,',len(S['actors']),'appearances,',len(caps),'caption phrases')
