from pathlib import Path
import json,html,sys,hashlib
from PIL import Image,ImageFont
P=Path(__file__).parent;D=94.8;A={a['id']:a for a in json.loads((P/'asset-plan.json').read_text())};S=json.loads((P/'storyboard.json').read_text());W=json.loads((P/'words.json').read_text());review='--review-incomplete' in sys.argv
for w in W:
 if w['word']=='Ramiya':w['word']='Remea'
 if w['word']=='bioharmony':w['word']='BioHarmony'
 if w['word']=='energize,':w['word']='energized,'
for i in range(len(W)-1):
 if W[i]['word']=='under' and W[i+1]['word']=='-supplied':W[i]['word']='undersupplied';W[i]['end']=W[i+1]['end'];W[i+1]['word']=''
W=[w for w in W if w['word']];(P/'words.json').write_text(json.dumps(W,indent=2));(P/'script.txt').write_text(' '.join(w['word'] for w in W))
phrases=["If you're always tired,","it's entirely your fault.","You aren't lazy, though.","Your body is just wildly","undersupplied because of","what you call a diet.","Low iron alone leaves you","feeling weak, brain fogged,","and pretty much useless","as a human being,","mostly because your body","needs iron to build hemoglobin.","The protein inside","your red blood cells","that carries oxygen","from your lungs","to your brain and muscles","so your cells can","actually produce energy.","Without enough iron,","you are basically suffocating","at a cellular level,","which is why you spend","all day feeling half dead.","Yet most people just chug","a third iced coffee","on an empty stomach","and think, nice,","problem solved.","News Flash","Caffeine isn't oxygen.","Caffeine doesn't give your cells","a single drop of real energy.","It just blocks adenosine.","The brain chemical responsible","for telling you that you're exhausted,","while forcing your adrenal glands","to pump out stress hormones","so you can fake being alive","for another two hours.","Instead of chemically gaslighting","your nervous system","into an early grave,","use this app","to actually track your nutrition.","All you have to do","is scan your meals every day,","and over time,","BioHarmony exposes your","chaotic sugar patterns,","massive nutrient gaps,","and the exact vitamins and minerals","your body keeps quietly begging for","while you neglect it.","Then, Remea steps in","to help plan meals","that actually make you","nutritionally sufficient,","and even recommends","organic juice blends","packed with fast absorbing nutrients","your cells desperately need.","Stick with it,","and you can finally graduate","from a slow, malfunctioning zombie","to energized, clear,","and actually functional.","Search Remea in the app store,","and try it yourself."]
C=[];idx=0
for text in phrases:
 n=len(text.split());g=W[idx:idx+n];idx+=n
 assert ' '.join(w['word'] for w in g).lower()==text.lower(),(text,g)
 C.append(dict(text=text,start=g[0]['start'],end=g[-1]['end']))
assert idx==len(W),(idx,len(W))
for i,c in enumerate(C):c['end']=C[i+1]['start'] if i+1<len(C) else D
(P/'captions.json').write_text(json.dumps(C,indent=2))
css=[];parts=[];schedule=[];missing=[];lanes=[0]*20
for i,s in enumerate(S):
 f=P/A[s['asset']]['path']
 if not f.exists():
  if review:missing.append(s['asset']);continue
  raise SystemExit('Missing art '+s['asset'])
 im=Image.open(f).convert('RGBA');bb=im.getchannel('A').point(lambda v:255 if v>110 else 0).getbbox();l,t,r,b=bb;iw,ih=im.size;x,y,mw,mh=s['layout'];s=dict(s)
 k=min(mw/(r-l),mh/(b-t)) if s['route']!='presenter' else s['targets'][0][3]/(b-t)
 w=(r-l)*k;h=(b-t)*k
 if s['route']=='presenter':
  tipx=(s['tip_source'][0]-l)*k;tipy=(s['tip_source'][1]-t)*k
  if s.get('flip'):tipx=w-tipx
  _,tx,ty,_=s['targets'][0];x=tx-tipx+w/2;y=ty-tipy+h/2;s.update(tip=[tipx,tipy])
 lane=next(j for j,v in enumerate(lanes) if v<=s['start']);lanes[lane]=s['end']
 key=s['id'];s.update(key=key,x=x,y=y,w=w,h=h,alpha_bounds=bb)
 inner='<img class="principal" src="'+A[s['asset']]['path']+'" alt="'+html.escape(A[s['asset']]['phrase'])+'">'
 if s['asset']=='battery':
  bars=''.join(f'<div class="cell-slot" style="left:{183+219*j}px"><div class="bar-fill" id="battery-bar-{j}"></div></div>' for j in range(5))
  inner+=f'<div class="source-ui" style="left:{-l*k}px;top:{-t*k}px;transform:scale({k});width:{iw}px;height:{ih}px">{bars}</div>'
 if s['asset']=='phone-search':
  icon_path='assets/graphics/remea-actual-app-icon.png';ic=Image.open(P/icon_path);il,it,ir,ib=ic.getchannel('A').point(lambda v:255 if v>110 else 0).getbbox();ik=360/max(ir-il,ib-it)
  letters=''.join(f'<span id="search-letter-{j}">{letter}</span>' for j,letter in enumerate('Remea'))
  inner+=f'<div class="source-ui" style="left:{-l*k}px;top:{-t*k}px;transform:scale({k});width:{iw}px;height:{ih}px"><div class="app-clear"></div><div id="app-icon-window"><img id="actual-app-icon" src="{icon_path}" alt="Actual Remea app icon" style="left:{(360-(ir-il)*ik)/2-il*ik}px;top:{(360-(ib-it)*ik)/2-it*ik}px;width:{ic.width*ik}px;height:{ic.height*ik}px"></div><div class="search-text">{letters}<i id="typing-cursor"></i></div></div>'
 if s.get('torso_only'):css.append('#'+key+' img.principal{clip-path:inset(0 0 44% 0)}')
 if s['asset']=='phone-scan':inner+='<div class="scan-window"><div class="scan-line"></div></div>'
 if s['route']=='presenter':inner='<div class="flip" style="transform:scaleX('+('-1' if s.get('flip') else '1')+')">'+inner+'</div>'
 parts.append(f'<div id="{key}" class="clip actor" data-asset="{s["asset"]}" data-start="{s["start"]}" data-duration="{min(D,s["end"]+.31)-s["start"]}" data-track-index="{lane+1}" style="z-index:{s["z"]}" data-layout-allow-overflow><div class="travel"><div class="pose">{inner}</div></div></div>')
 css.append(f'#{key} .travel{{left:{x-w/2}px;top:{y-h/2}px;width:{w}px;height:{h}px}}#{key} img.principal{{left:{-l*k}px;top:{-t*k}px;width:{iw*k}px;height:{ih*k}px}}')
 
 if s['asset']=='caffeine' and s['start']>44:css.append('#'+key+' img{clip-path:inset(0 0 26% 0)}')
 schedule.append(s)
emphasis={'tired','fault','lazy','iron','hemoglobin','oxygen','energy','caffeine','adenosine','stress','nutrition','bioharmony','vitamins','minerals','remea','energized','clear','functional'}
for i,c in enumerate(C):
 size=76;fontpath=P/'assets/fonts/caption-bold.ttf'
 while size>56:
  font=ImageFont.truetype(str(fontpath),size);lines=['']
  for word in c['text'].split():
   trial=(lines[-1]+' '+word).strip()
   if font.getlength(trial)>740 and lines[-1]:lines.append(word)
   else:lines[-1]=trial
  if len(lines)<=2:break
  size-=2
 text=' '.join('<b>'+html.escape(w)+'</b>' if w.lower().strip(',.!?') in emphasis else html.escape(w) for w in c['text'].split())
 parts.append(f'<div id="c{i}" class="clip caption" data-start="{c["start"]}" data-duration="{c["end"]-c["start"]}" data-track-index="25" style="font-size:{size}px">{text}</div>')
# Exact editable explanatory overlays; no invented patient values or diagnostic readings.
parts.append('<svg id="micro" width="1080" height="1920" data-layout-ignore><path id="lung-brain" class="path" d="M420 920 C475 860 490 840 530 840"/><path id="lung-muscle" class="path" d="M410 1070 C460 1170 460 1250 510 1280"/><g transform="rotate(17 545 900)"><path id="equals-lines" class="path comparison" d="M495 880 H595 M495 920 H595"/><path id="crossing-slash" class="path comparison" d="M505 946 L585 854"/></g><path id="absorb-route" class="path" d="M450 1000 C540 1100 520 1180 420 1260"/><circle id="nutrient-particle" cx="450" cy="1000" r="10"/></svg>')
base="""@font-face{font-family:Caption;src:url(assets/fonts/caption-bold.ttf)}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#fff;color:#101010}#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:#fff}.scene-content{width:100%;height:100%;display:flex;flex-direction:column;padding:0}.actor{position:absolute;inset:0;opacity:0;pointer-events:none}.travel,.pose,.flip{position:absolute;transform-origin:center}.pose,.flip{inset:0}.actor img{position:absolute;max-width:none;filter:drop-shadow(-10px 16px 10px #0003)}.caption{position:absolute;left:115px;top:285px;width:740px;max-height:240px;font:76px/1.1 Caption,sans-serif;text-align:center;letter-spacing:-1px;z-index:100;opacity:0}.caption b{font-weight:inherit;color:#de0b13}.edge-shadow{position:absolute;inset:-20px;pointer-events:none;z-index:80;box-shadow:inset 95px 0 120px -40px #0009,inset -95px 0 120px -40px #0009,inset 0 65px 95px -40px #0006,inset 0 -65px 95px -40px #0006}#micro{position:absolute;inset:0;pointer-events:none;z-index:42}.path{fill:none;stroke:#101010;stroke-width:8;stroke-linecap:round;opacity:0}#oxygen-particle,#nutrient-particle{fill:#ed0b10;stroke:#101010;stroke-width:4;opacity:0}#scan-sweep{position:absolute;left:480px;top:880px;width:255px;height:7px;background:#ed0b10;box-shadow:0 0 14px #ed0b1070;opacity:0;z-index:45}.scan-window{position:absolute;left:16%;top:19%;width:68%;height:43%;overflow:hidden}.scan-line{position:absolute;left:0;top:0;width:100%;height:5px;background:#ed0b10;opacity:0}.source-ui{position:absolute;transform-origin:0 0;pointer-events:none}.cell-slot{position:absolute;top:335px;width:195px;height:340px;background:#fff;border:12px solid #101010;border-radius:25px;overflow:hidden}.bar-fill{position:absolute;inset:0;background:#ed0b10;transform-origin:center bottom;border-radius:10px}.comparison{stroke-width:11}.app-clear{position:absolute;left:307px;top:678px;width:405px;height:390px;background:white;border-radius:30px}#app-icon-window{position:absolute;left:332px;top:700px;width:360px;height:360px;border-radius:35px;overflow:hidden;opacity:0}#search #actual-app-icon{position:absolute;filter:none}.search-text{position:absolute;left:284px;top:516px;height:80px;white-space:nowrap;font:68px/1 Caption,sans-serif;color:#101010;letter-spacing:0}.search-text span{opacity:0}#typing-cursor{position:absolute;left:0;top:0;display:block;width:5px;height:64px;background:#101010;opacity:0}"""
payload=dict(schedule=schedule,captions=C,duration=D,typing_widths=[ImageFont.truetype(str(P/'assets/fonts/caption-bold.ttf'),68).getlength('Remea'[:i])+5 for i in range(6)])
out='<!doctype html><html><head><meta charset="utf-8"><title>Iron, Oxygen and Real Energy</title><style>'+base+'\n'+'\n'.join(css)+'</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="'+str(D)+'" data-width="1080" data-height="1920"><div class="scene-content">'+''.join(parts)+'</div><div class="edge-shadow" data-layout-ignore></div><audio id="mix" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="'+str(D)+'" data-track-index="31"></audio></div><script src="assets/vendor/gsap.min.js"></script><script>const DATA='+json.dumps(payload)+';\n'+(P/'animation.js').read_text()+'</script></body></html>'
(P/('index-review.html' if review else 'index.html')).write_text(out);(P/'production/final-schedule.json').write_text(json.dumps(schedule,indent=2));(P/'production/missing-assets.json').write_text(json.dumps(sorted(set(missing)),indent=2))
inventory=[]
for a in A.values():
 f=P/a['path']
 if f.exists():inventory.append(dict(id=a['id'],path=a['path'],sha256=hashlib.file_digest(f.open('rb'),'sha256').hexdigest(),kind=a['kind']))
(P/'asset-inventory.json').write_text(json.dumps(inventory,indent=2))
print('Built',len(schedule),'appearances;',len(set(s['asset'] for s in schedule)),'used distinct assets;',len(C),'exact caption groups; missing',missing)
