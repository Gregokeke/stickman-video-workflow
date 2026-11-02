from pathlib import Path
import json,html,math
from PIL import Image,ImageFont
P=Path(__file__).parent
scenes=json.loads((P/'storyboard.json').read_text());captions=json.loads((P/'captions.json').read_text());micro=json.loads((P/'micro-plan.json').read_text())
assetfiles={a['id']:a['path'] for a in json.loads((P/'asset-plan.json').read_text())}
duration=125.1;missing=[];dimensions={}
for s in scenes:
 f=P/assetfiles[s['asset']]
 if not f.exists():missing.append(s['asset']);continue
 if s['asset'] in dimensions:continue
 im=Image.open(f).convert('RGBA');alpha=im.getchannel('A');bbox=alpha.point(lambda a:255 if a>100 else 0).getbbox()
 dimensions[s['asset']]={'size':im.size,'bounds':bbox}
if missing:raise SystemExit('Cannot build finished composition: missing '+', '.join(sorted(set(missing))))
(P/'production/alpha-bounds.json').write_text(json.dumps(dimensions,indent=2))
def layout(s):
 id=s['asset'];st=s['start'];role=s['role'];x,y,mw,mh=(470,1050,760,970) if role=='hero' else (735,1350,270,350)
 if id in ['couch-slouch','horizontal-dread','rotting-bed','mattress','mattress-winner','pallbearers-six','doorstep-handoff']:x,y,mw,mh=465,1070,810,760
 if id=='pharma-salesman':x,y,mw,mh=450,1050,760,1080
 if id=='pharma-building':x,y,mw,mh=710,680,240,220
 if id=='pill-hand':x,y,mw,mh=725,1370,260,320
 if id=='death-hourglass':x,y,mw,mh=340,1090,440,680
 if id=='risk-shield':x,y,mw,mh=715,1270,230,300
 if id=='extra-pill-stack':x,y,mw,mh=460,1110,680,620
 if id=='pill-bottle':x,y,mw,mh=(475,1090,620,850) if st<10 else (685,1200,290,430)
 if id=='side-effects-checklist':x,y,mw,mh=720,1320,230,330
 if id=='wallet':x,y,mw,mh=720,1330,260,310
 if id=='wallet':x,y,mw,mh=470,1080,700,900
 if id=='sarcastic-presenter' and st<20:x,y,mw,mh=450,1050,720,960
 if id=='confused':x,y,mw,mh=340,1110,510,760
 if id in ['coffee-mug','coffee-sip']:x,y,mw,mh=470,1080,730,840
 if id in ['legs-close','legs-exasperated']:x,y,mw,mh=470,1100,750,900
 if id=='lab-scientist':x,y,mw,mh=350,1110,520,890
 if id=='clipboard-study':x,y,mw,mh=710,1270,245,320
 if id=='calendar':x,y,mw,mh=710,830,230,250
 if id=='step-counter':x,y,mw,mh=720,1240,260,330
 if id=='research-participants':x,y,mw,mh=465,1350,750,540
 if id=='doorstep-shuffle':x,y,mw,mh=350,1090,540,930
 if id in ['cardio','slipper-feet']:x,y,mw,mh=710,1280,260,330
 if id in ['door-handle','phone-order','delivery-bag','takeout-meal']:x,y,mw,mh=710,1250,260,340
 if id=='watch16000':x,y,mw,mh=730,1260,255,335
 if id=='empty-chair':x,y,mw,mh=720,1330,250,320
 if id=='nowhere-to-sit':x,y,mw,mh=360,1040,540,880
 if id=='dread-portrait':x,y,mw,mh=410,1080,620,770
 if id=='brain':x,y,mw,mh=735,1270,230,270
 if id=='cane-presenter':x,y,mw,mh=(429,1092,640,620) if st<60 else (317,1023,640,620)
 if id=='extra-step-foot':x,y,mw,mh=720,1390,230,250
 if id=='closed-coffin':x,y,mw,mh=720,1380,240,230
 if id in ['bribe-coins','reaper-coin-hand']:x,y,mw,mh=710,1320,260,260
 if id=='least-active-chair':x,y,mw,mh=295,1310,350,460
 if id=='top-walker-check':x,y,mw,mh=700,1300,310,530
 if id=='cigarette':x,y,mw,mh=700,1320,220,300
 if id=='smoker':x,y,mw,mh=300,1300,340,540
 if id in ['non-smoker','breathing-person']:x,y,mw,mh=700,1300,310,540
 if id=='sink':x,y,mw,mh=650,1260,390,410
 if id=='sarcastic-presenter' and 75<st<80:x,y,mw,mh=260,1100,440,760
 if id in ['cigarette-pack','pack-hand']:x,y,mw,mh=720,1330,250,320
 if id=='lungs':x,y,mw,mh=720,1280,270,330
 if id=='crime-scene-tape':x,y,mw,mh=490,1480,700,180
 if id=='pedometer5000':x,y,mw,mh=715,1270,265,360
 if id in ['apathy','functional-walker']:x,y,mw,mh=(300,1320,350,520) if id=='apathy' else (695,1290,300,570)
 if id=='first-step':x,y,mw,mh=710,1350,260,280
 if id=='capsule':x,y,mw,mh=720,1330,240,300
 if id=='own-two-feet':x,y,mw,mh=500,1450,450,220
 if id=='own-two-feet':x,y,mw,mh=480,1530,350,160
 if id=='pallbearers-six':x,y,mw,mh=440,1070,770,760
 if id=='cigarette-pack':x,y,mw,mh=450,1080,600,760
 if id=='first-step':x,y,mw,mh=440,1070,740,930
 if 'layout' in s:x,y,mw,mh=s['layout']
 return x,y,mw,mh

parts=[];css=[];schedule=[];tracks=[0]*12
for i,s in enumerate(scenes):
 id=s['asset'];st=s['start'];en=s['end'];x,y,mw,mh=layout(s)
 d=dimensions[id];l,t,r,b=d['bounds'];iw,ih=d['size'];
 if id=='confused':l,t,r,b=207,119,990,1039
 scale=min(mw/(r-l),mh/(b-t));w=(r-l)*scale;h=(b-t)*scale
 key=f'a{i}';lane=next((k for k,v in enumerate(tracks) if v<=st),0);tracks[lane]=en+.1
 parts.append(f'<div id="{key}" class="clip actor" data-asset="{id}" data-start="{st}" data-duration="{en-st+.08:.4f}" data-track-index="{lane+1}" data-layout-allow-overflow><div class="travel"><div class="pose"><img src="{assetfiles[id]}" alt="{html.escape(s["exact_phrase"])}"></div></div></div>')
 css.append(f'#{key} .travel{{left:{x-w/2:.2f}px;top:{y-h/2:.2f}px;width:{w:.2f}px;height:{h:.2f}px}}#{key} img{{width:{iw*scale:.2f}px;height:{ih*scale:.2f}px;left:{-l*scale:.2f}px;top:{-t*scale:.2f}px}}')
 schedule.append(dict(key=key,asset=id,start=st,end=en,role=s['role'],x=x,y=y,w=w,h=h))
for i,g in enumerate(captions):
 size=76
 while size>54:
  font=ImageFont.truetype(str(P/'assets/fonts/caption-bold.ttf'),size);lines=['']
  for word in g['text'].split():
   trial=(lines[-1]+' '+word).strip()
   if font.getlength(trial)>740 and lines[-1]:lines.append(word)
   else:lines[-1]=trial
  if len(lines)<=2:break
  size-=2
 parts.append(f'<div id="c{i}" class="clip caption" style="font-size:{size}px" data-start="{g["start"]}" data-duration="{g["end"]-g["start"]:.4f}" data-track-index="20">{html.escape(g["text"])}</div>')
def label(txt,cls=''):return f'<div class="diagram-label {cls}">{txt}</div>'
parts.append('<section id="pill-example" class="clip diagram" data-start="4.52" data-duration="4.43" data-track-index="22"><div class="gauge-title">RISK INDEX</div><div class="gauge-max">100</div><div class="gauge-track"><div class="gauge-inner"><div class="gauge-fill"></div></div></div><div class="gauge-level"><b class="pill-88">88</b><b class="pill-76">76</b></div><div class="pill-difference">−12%<small>of baseline</small></div><div class="gauge-note">hypothetical example</div></section>')
parts.append('<section id="steps" class="clip diagram" data-start="28.08" data-duration="2.77" data-track-index="21"><div class="chart-title">DAILY STEPS</div><div class="step-columns">'+''.join(f'<div class="category"><div class="category-bar"></div><span>{v}</span></div>' for v in ['3K','5K','8K','12K','16K'])+'</div><div class="step-pointer">START HERE</div></section>')
parts.append('<section id="relative" class="clip diagram" data-start="45.15" data-duration="7.45" data-track-index="21"><div class="chart-title">+1,000 STEPS</div><div class="relative-bars"><div class="relative-row"><span>BEFORE</span><div class="bar-track"><div class="bar-fill base"></div></div><b>100</b></div><div class="relative-row"><span>AFTER</span><div class="bar-track"><div class="bar-fill reduced"></div></div><b>88</b></div></div><div class="takeaway">−12%</div><div class="qualifier">relative risk · illustrative comparison</div></section>')
for key,st,en,n,left,right in [('ratio3',63.65,67.35,3,'LEAST ACTIVE','MOST ACTIVE'),('ratio2',71.3,75.35,2,'SMOKING','NON-SMOKING')]:
 units=''.join(f'<div class="unit slot{i}"></div>' for i in range(n))
 rightunits=''.join(f'<div class="unit {"empty" if i else "filled"} slot{i}"></div>' for i in range(n))
 parts.append(f'<section id="{key}" class="clip diagram ratio" data-start="{st}" data-duration="{en-st}" data-track-index="21"><div class="chart-title">RELATIVE RISK</div><div class="ratio-columns"><div class="ratio-group"><div class="units">{units}</div><span>{left}</span></div><div class="multiplier">{n}×</div><div class="ratio-group"><div class="units">{rightunits}</div><span>{right}</span></div></div></section>')
parts.append('<section id="progress" class="clip diagram" data-start="102.7" data-duration="7.85" data-track-index="21"><div class="chart-title">MORE EVERYDAY MOVEMENT</div><div class="progress-track"><div class="progress-fill"></div><div class="progress-marker"></div></div><div class="progress-labels"><span>LESS ACTIVE</span><span>MORE ACTIVE</span></div><div class="takeaway">OVER 50%</div><div class="qualifier">lower relative risk · no step threshold implied</div></section>')
parts.append('<div id="hookstat" class="callout">−12%</div><div id="bottleslash" class="annotation"><svg viewBox="0 0 300 300"><path d="M35 265 L265 35"/></svg></div>')
base='''@font-face{font-family:Caption;src:url(assets/fonts/caption-bold.ttf)}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#fff;color:#101010}#root{width:1080px;height:1920px;position:relative;overflow:hidden;background:#fff}.scene-content{width:100%;height:100%;padding:0;display:flex;flex-direction:column}.edge-shadow{position:absolute;inset:-20px;pointer-events:none;z-index:80;box-shadow:inset 95px 0 120px -40px #0009,inset -95px 0 120px -40px #0009,inset 0 65px 95px -40px #0006,inset 0 -65px 95px -40px #0006}.actor{position:absolute;inset:0;opacity:0;pointer-events:none}.travel,.pose{position:absolute;transform-origin:center center}.pose{inset:0}.actor img{position:absolute;max-width:none;filter:drop-shadow(-10px 15px 10px #0003)}.caption{position:absolute;left:115px;top:300px;width:740px;max-height:205px;text-align:center;font:76px/1.1 Caption,sans-serif;letter-spacing:-1px;opacity:0;z-index:100}.diagram{position:absolute;left:140px;top:560px;width:700px;height:500px;font-family:Caption,sans-serif;opacity:0;z-index:35}.chart-title{text-align:center;font-size:38px;letter-spacing:1px}.step-columns{display:flex;align-items:flex-end;justify-content:space-between;height:300px;gap:22px;border-bottom:7px solid #101010;margin-top:30px;padding:0 15px}.category{display:flex;flex-direction:column;align-items:center;gap:12px;font-size:32px}.category-bar{width:88px;height:220px;background:#d9d9d9;transform-origin:bottom}.category:first-child .category-bar,.category:last-child .category-bar{background:#ed0b10}.step-pointer{font-size:28px;color:#de0b13;margin-top:22px}.relative-bars{margin-top:45px;display:flex;flex-direction:column;gap:40px}.relative-row{display:grid;grid-template-columns:135px 1fr 55px;align-items:center;gap:15px;font-size:28px}.bar-track{height:64px;background:#dedede;border-radius:7px;overflow:hidden}.bar-fill{height:100%;background:#101010;transform-origin:left}.bar-fill.reduced{background:#ed0b10}.takeaway{font-size:106px;color:#de0b13;text-align:center;margin-top:30px;line-height:1}.qualifier{font:24px/1.3 Caption,sans-serif;text-align:center;margin-top:15px}.ratio-columns{display:flex;justify-content:space-between;align-items:center;gap:20px;margin-top:35px}.ratio-group{width:245px;text-align:center;font-size:28px}.units{height:285px;display:flex;flex-direction:column-reverse;align-items:center;justify-content:flex-start;gap:12px;margin-bottom:22px}.unit{width:140px;height:80px;border:5px solid #101010;background:#ed0b10;border-radius:6px}.unit.empty{background:#fff;border:5px dashed #b5b5b5}.multiplier{font-size:95px;color:#de0b13}.progress-track{margin-top:80px;height:65px;border:5px solid #101010;border-radius:10px;position:relative}.progress-fill{background:#ed0b10;width:100%;height:100%;transform-origin:left}.progress-marker{position:absolute;width:16px;height:95px;background:#101010;top:-20px;left:0}.progress-labels{display:flex;justify-content:space-between;font-size:27px;margin-top:28px}.callout{position:absolute;left:580px;top:920px;font:110px/1 Caption;color:#de0b13;opacity:0}.annotation{position:absolute;left:555px;top:970px;width:260px;height:330px;z-index:45;opacity:0}.annotation path{fill:none;stroke:#101010;stroke-width:14;stroke-linecap:round;stroke-dasharray:330;stroke-dashoffset:330}'''
base+=' .takeaway,.qualifier,.multiplier,.unit,#relative .chart-title,#relative .relative-row:last-child b{opacity:0}.category-bar{transform:scaleY(0)}.bar-fill{transform:scaleX(0)}#relative .takeaway{position:absolute;top:500px;left:430px;width:270px;margin:0}#relative .qualifier,#progress .qualifier{position:absolute;top:-45px;width:700px;margin:0}#progress .takeaway{position:absolute;top:390px;left:350px;width:350px;font-size:80px;margin:0}#progress .progress-labels{position:absolute;top:65px;width:700px;margin:0}'
base+='#steps span,.step-pointer{opacity:0}.progress-fill{transform:scaleX(.08)}.progress-marker{transform:translateX(20px)}'
base+=' .actor[data-asset="confused"] img{clip-path:polygon(16.9348% 7.5075%,84.6740% 7.5075%,84.6740% 66.0661%,61.8120% 66.0661%,61.8967% 66.3664%,61.9814% 66.6667%,61.9814% 66.9670%,62.0660% 67.2673%,62.0660% 67.5676%,62.1507% 67.8679%,62.2354% 68.1682%,62.2354% 68.4685%,62.3201% 68.7688%,62.4047% 69.0691%,62.4047% 69.3694%,62.4894% 69.6697%,62.5741% 69.9700%,62.5741% 70.2703%,62.6588% 70.5706%,62.7434% 70.8709%,62.7434% 71.1712%,62.8281% 71.4715%,63.3362% 71.7718%,63.8442% 72.0721%,64.2676% 72.3724%,64.6063% 72.6727%,64.9450% 72.9730%,65.1990% 73.2733%,65.4530% 73.5736%,65.6224% 73.8739%,65.7070% 74.1742%,65.7917% 74.4745%,65.8764% 74.7748%,65.8764% 75.0751%,65.8764% 75.3754%,65.7917% 75.6757%,65.7070% 75.9760%,65.5377% 76.2763%,65.2837% 76.5766%,64.9450% 76.8769%,64.5216% 77.1772%,63.8442% 77.4775%,62.6588% 77.7778%,61.2193% 77.9279%,37.3412% 77.9279%,36.6638% 77.7778%,35.8171% 77.4775%,35.3091% 77.1772%,34.9704% 76.8769%,34.7163% 76.5766%,34.4623% 76.2763%,34.3776% 75.9760%,34.2930% 75.6757%,34.2083% 75.3754%,34.2083% 75.0751%,34.2930% 74.7748%,34.3776% 74.4745%,34.4623% 74.1742%,34.5470% 73.8739%,34.8010% 73.5736%,34.9704% 73.2733%,35.3091% 72.9730%,35.5631% 72.6727%,35.9865% 72.3724%,36.4098% 72.0721%,36.9179% 71.7718%,37.4259% 71.4715%,37.4259% 71.1712%,37.5106% 70.8709%,37.5953% 70.5706%,37.6799% 70.2703%,37.6799% 69.9700%,37.7646% 69.6697%,37.7646% 69.3694%,37.8493% 69.0691%,37.8493% 68.7688%,37.9340% 68.4685%,38.0186% 68.1682%,38.0186% 67.8679%,38.1033% 67.5676%,38.1033% 67.2673%,38.1880% 66.9670%,38.2727% 66.6667%,38.2727% 66.3664%,38.3573% 66.0661%,16.9348% 66.0661%)}'
base+='#pill-example{left:0;top:0;width:1080px;height:1920px;z-index:35}.gauge-title{position:absolute;left:140px;top:570px;width:260px;font-size:36px;text-align:center}.gauge-max{position:absolute;left:185px;top:630px;width:170px;text-align:center;font-size:52px}.gauge-track{position:absolute;left:185px;top:700px;width:170px;height:820px;background:#101010;border-radius:18px;padding:14px}.gauge-inner{position:relative;width:142px;height:792px;overflow:hidden;border-radius:7px;background:#101010}.gauge-fill{position:absolute;left:0;bottom:0;width:100%;height:100%;background:#ed0b10;transform-origin:bottom;transform:scaleY(.88)}.gauge-level{position:absolute;left:80px;top:782px;width:95px;height:65px;font-size:49px;text-align:right}.gauge-level b{position:absolute;right:0;top:0}.pill-76,.pill-difference{opacity:0}.pill-difference{position:absolute;left:390px;top:1050px;width:200px;font-size:66px;color:#de0b13}.pill-difference small{display:block;font-size:24px;color:#101010;margin-top:10px}.gauge-note{position:absolute;left:125px;top:1550px;width:290px;text-align:center;font-size:24px}.actor[data-asset="cane-presenter-left"] .pose{transform:scaleX(-1)}' 
payload=dict(schedule=schedule,captions=captions,duration=duration)
script='const DATA='+json.dumps(payload)+';\n'+(P/'animation.js').read_text()
out='<!doctype html><html><head><meta charset="utf-8"><title>Walking — The Magic Pill</title><style>'+base+'\n'+'\n'.join(css)+'</style></head><body><div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="125.1"><div class="scene-content">'+''.join(parts)+'</div><div class="edge-shadow" data-layout-ignore></div><audio id="voice-mix" src="assets/audio/mix.wav" data-start="0" data-duration="125.1" data-track-index="30"></audio></div><script src="assets/vendor/gsap.min.js"></script><script>'+script+'</script></body></html>'
(P/'index.html').write_text(out);(P/'production/final-schedule.json').write_text(json.dumps(schedule,indent=2));print('Built',len({assetfiles[k] for k in dimensions}),'distinct illustrations;',len(schedule),'appearances; duration',duration)
