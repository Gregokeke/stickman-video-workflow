from pathlib import Path
import json,numpy as np
from PIL import Image
p=Path(__file__).parent;factor=4;W,H=270,480
im=Image.open(p/'references/red-zone-canvas.png').convert('RGBA').resize((W,H));guide=np.array(im)[:,:,3]>180
cache={};issues=[];essentials=[]
for s in json.load(open(p/'production/safe-area-transforms.json')):
 if s['path'] not in cache:cache[s['path']]=Image.open(p/s['path']).convert('RGBA')
 im=cache[s['path']];a,b,c,d,e,f=s['matrix'];sw,sh=s['size'];sx=sw/im.width;sy=sh/im.height
 M=np.array([[a*sx,c*sy,e],[b*sx,d*sy,f],[0,0,1.]])/factor;M[2]=[0,0,1];inv=np.linalg.inv(M);coef=tuple(inv[:2].ravel());alpha=im.getchannel('A').point(lambda v:255 if v>110 else 0);mask=np.array(alpha.transform((W,H),Image.Transform.AFFINE,coef,resample=Image.Resampling.NEAREST))>127
 total=int(mask.sum());over=int((mask&guide).sum());ratio=over/max(1,total)
 if s['asset']=='cane-presenter':
  for label,rect in [('face',(192,235,435,477)),('grip',(620,400,745,550))]:
   roi=Image.new('L',im.size);roi.paste(alpha.crop(rect),rect);m=np.array(roi.transform((W,H),Image.Transform.AFFINE,coef,resample=Image.Resampling.NEAREST))>127;n=int((m&guide).sum())
   if n>3:essentials.append(dict(time=s['time'],asset=s['asset'],part=label,overlap_pixels=n))
 elif over>6 and ratio>.004:issues.append(dict(time=s['time'],asset=s['asset'],overlap_fraction=round(ratio,4),pixels=over))
report=dict(samples=len(json.load(open(p/'production/safe-area-transforms.json'))),guide='references/red-zone-canvas.png',ordinary_foreground_issues=issues,presenter_essential_issues=essentials,method='Source alpha >110 transformed from real DOM matrices; exact supplied guide alpha >180, quarter-resolution. Presenter face/grip checked separately; deliberate lower-leg crops recorded in layout decisions.')
(p/'production/safe-area-audit.json').write_text(json.dumps(report,indent=2));print('Ordinary foreground issues',len(issues),'Presenter essential issues',len(essentials));print(json.dumps(issues[:8]+essentials[:8],indent=2))
