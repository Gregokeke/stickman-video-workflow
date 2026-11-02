from pathlib import Path
import json,numpy as np
from PIL import Image
P=Path(__file__).parent;rows=json.load(open(P/'production/dense-layout-samples.json'));W,H=540,960;cache={};errors=[]
for row in rows:
 items=[]
 for a in row['actors']:
  if a['presenter']or a['opacity']<.56:continue
  if a['asset']not in cache:cache[a['asset']]=Image.open(P/f'assets/graphics/{a["asset"]}.png').convert('RGBA')
  im=cache[a['asset']];x,y,w,h=[v/2 for v in a['box']];m=im.getchannel('A').point(lambda v:255 if v>160 else 0).resize((max(1,round(w)),max(1,round(h))));o=Image.new('L',(W,H));o.paste(m,(round(x),round(y)));items.append((a,np.array(o)>160))
 for i,(a,m)in enumerate(items):
  for b,n in items[i+1:]:
   if {a['id'],b['id']}=={'echo-padlock','echo-chamber-friends'}:continue
   ov=int(np.sum(m&n));ratio=ov/max(1,min(np.sum(m),np.sum(n)))
   if ratio>.022:errors.append({'t':row['t'],'a':a['id'],'b':b['id'],'fraction':float(ratio)})
proof={'samples':len(rows),'errors':errors,'intentional_contact_exemption':['echo-chamber-friends','echo-padlock']};(P/'production/transition-overlap-audit.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof,indent=2))
