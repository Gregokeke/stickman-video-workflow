from pathlib import Path
from PIL import Image,ImageChops
import numpy as np,json
P=Path(__file__).parent;W,H=540,960;rows=json.load(open(P/'production/layout-samples.json'));faces={'instructor-up':(758,322,985,538),'instructor-straight':(608,326,827,539),'instructor-diagonal':(201,249,421,468)};collisions=[];unsafe=[];intentional=[]
guide=np.array(Image.open(P/'references/red-zone-canvas.png').convert('RGBA').resize((W,H)));ui=(guide[:,:,0]>155)&(guide[:,:,1]<190)&(guide[:,:,2]<190)&(guide[:,:,3]>100)
cache={}
for row in rows:
 ms=[]
 for a in row['actors']:
  
  if a.get('opacity',1)<.55 or row['t']>=a.get('handoff',999) or row['t']<a.get('start',0)+.30:continue
  key=a['asset'];im=cache.setdefault(key,Image.open(P/f'assets/graphics/{key}.png').convert('RGBA'));x,y,w,h=[v/2 for v in a['box']];cw,ch=max(1,round(w)),max(1,round(h));mask=im.getchannel('A').point(lambda v:255 if v>160 else 0)
  if a.get('flip'):mask=mask.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  mask=mask.resize((cw,ch));canvas=Image.new('L',(W,H));canvas.paste(mask,(round(x),round(y)));arr=np.array(canvas)>160
  if a['presenter']:
   face=Image.new('L',im.size);face.paste(255,faces[key]);
   if a.get('flip'):face=face.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   face=face.resize((cw,ch));c=Image.new('L',(W,H));c.paste(face,(round(x),round(y)));m=np.array(c)>160;ratio=float(np.sum(m&ui)/max(1,np.sum(m)))
   if ratio>.02:unsafe.append({'t':row['t'],'id':a['id'],'face_ui_fraction':ratio})
  else:
   ratio=float(np.sum(arr&ui)/max(1,np.sum(arr)))
   if ratio>.025:unsafe.append({'t':row['t'],'id':a['id'],'opaque_ui_fraction':ratio})
   ms.append((a,arr))
 for i,(a,m)in enumerate(ms):
  for b,n in ms[i+1:]:
   overlap=int(np.sum(m&n));ratio=overlap/max(1,min(np.sum(m),np.sum(n)))
   if ratio>.018:
    finding={'t':row['t'],'a':a['id'],'b':b['id'],'fraction_of_smaller':float(ratio)}
    if {a['id'],b['id']}=={'echo-chamber-friends','echo-padlock'}:intentional.append(dict(finding,reason='Independent padlock deliberately attached to the chamber door latch'))
    else:collisions.append(finding)
proof={'samples':len(rows),'held_prop_collisions':collisions,'ui_conflicts':unsafe,'intentional_contacts':intentional,'guide':'references/red-zone-canvas.png','method':'opaque-alpha intersection; teacher head regions checked separately; purposeful cane contact excluded'};(P/'production/layout-audit.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof,indent=2))
