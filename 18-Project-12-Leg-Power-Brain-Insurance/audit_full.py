from pathlib import Path
import json,numpy as np
from PIL import Image
P=Path(__file__).parent;data=json.loads((P/'production/full-layout-samples.json').read_text());inv=json.loads((P/'full-asset-inventory.json').read_text());W,H=360,640;factor=3
u=np.array(Image.open(P/'references/red-zone-canvas.png').convert('RGBA').resize((W,H)));ui=(u[:,:,0]>155)&(u[:,:,1]<190)&(u[:,:,2]<190)&(u[:,:,3]>100);cache={};coll=[];unsafe=[];intent=[];pointer=[]
faces={'01-diagonal.png':(201,249,421,468),'02-upward.png':(758,322,985,538),'03-straight-head-tilt.png':(608,326,827,539)}
def mask(asset,box,flip=False,region=None):
 if asset not in cache:cache[asset]=Image.open(P/inv[asset]['path']).convert('RGBA')
 im=cache[asset];m=im.getchannel('A').point(lambda x:255 if x>170 else 0)
 if region:
  r=Image.new('L',im.size);r.paste(255,region);m=Image.fromarray(np.minimum(np.array(m),np.array(r)))
 if flip:m=m.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 x,y,w,h=[v/factor for v in box];m=m.resize((max(1,round(w)),max(1,round(h))));c=Image.new('L',(W,H));c.paste(m,(round(x),round(y)));return np.array(c)>170
for row in data['frames']:
 t=row['t'];ms=[]
 for a in row['actors']:
  if a['opacity']<.55:continue
  m=mask(a['asset'],a['box']);ratio=float((m&ui).sum()/max(1,m.sum()))
  if ratio>.025:unsafe.append(dict(t=t,id=a['id'],ui_fraction=ratio))
  ms.append((a,m))
 for i,(a,m)in enumerate(ms):
  for b,n in ms[i+1:]:
   ratio=float((m&n).sum()/max(1,min(m.sum(),n.sum())))
   if ratio>.018:
    linked=next((e for e in data['origins']if {e['id'],e['parent']}=={a['id'],b['id']} and e['start']<=t<e['start']+e['duration']+.06),None)
    finding=dict(t=t,a=a['id'],b=b['id'],fraction=ratio);(intent if linked else coll).append(finding)
 for g in row['guides']:
  if g['opacity']<.55:continue
  face=mask(g['pose'],g['box'],g['flip'],faces[g['pose']]);r=float((face&ui).sum()/max(1,face.sum()))
  if r>.02:unsafe.append(dict(t=t,id=g['id']+'-face',ui_fraction=r))
  for a,m in ms:
   r=float((face&m).sum()/max(1,min(face.sum(),m.sum())))
   if r>.018:coll.append(dict(t=t,a=g['id']+'-face',b=a['id'],fraction=r))
  q=next((q for q in data['guideProof']if q['guide']==g['id'] and abs(q['t']-t)<.0001),None)
  if q:pointer.append(float(np.linalg.norm(np.array(q['expected_tip'])-g['tip'])))
out=dict(samples=len(data['frames']),unintended_collisions=coll,ui_conflicts=unsafe,intentional_extraction_overlaps=intent,source_opacity_at_emergence=[e for e in data['origins']if e['parent_opacity']<.1],pointer_max_error_px=max(pointer,default=None),missing_images=list({p for r in data['frames']for p in r['missing']}),page_errors=data['errors'],caption_overlaps=[r['t']for r in data['frames']if len(r['captions'])>1],caption_overflow=[dict(t=r['t'],**c)for r in data['frames']for c in r['captions']if c['height']>260],ui_guide='references/red-zone-canvas.png',intentional_crops='Only large instructor lower bodies; normal illustrations remain complete')
(P/'production/full-layout-audit.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items()if k!='intentional_extraction_overlaps'},indent=2))
