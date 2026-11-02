from PIL import Image
from pathlib import Path
import numpy as np,json
p=Path(__file__).parent;mask=np.asarray(Image.open(p/'references/red-zone-canvas.png').resize((1080,1920),Image.Resampling.NEAREST))[:,:,3]>64
yy,xx=np.indices(mask.shape);mask &= ((xx<65)|(xx>1020)|(yy<205)|(yy>1600)|((xx>850)&(yy>705)))
data=json.loads((p/'review-states.json').read_text());cache={};events=[];labels=[]
for f in data['frames']:
 for it in f['items']:
  k=it['id']
  if k not in cache:
   im=Image.open(p/'assets'/f'{k}.png').convert('RGBA');a=np.asarray(im)[::5,::5,3];y,x=np.where(a>32);cache[k]=(x*5+2.5,y*5+2.5,im.size)
  sx,sy,(nw,nh)=cache[k];l,t,w,h=it['image'];a,b,c,d,tx,ty=it['matrix'];lx=l+sx*w/nw;ly=t+sy*h/nh;x=a*lx+c*ly+tx;y=b*lx+d*ly+ty;inside=(x>=0)&(x<1080)&(y>=0)&(y<1920);bad=np.ones(len(x),bool);bad[inside]=mask[y[inside].astype(int),x[inside].astype(int)]
  if bad.any():events.append(dict(time=f['time'],asset=k,pixels=int(bad.sum()),fraction=float(np.mean(bad))))
 for e in f['labels']:
  x,y,w,h=e['rect'];l,t,r,b=max(0,int(x)),max(0,int(y)),min(1080,int(x+w)+1),min(1920,int(y+h)+1)
  if mask[t:b,l:r].any():labels.append(dict(time=f['time'],id=e['id']))
out=dict(samples=len(data['frames']),exceptions=[],foreground_events=events,label_events=labels,console_errors=data['errors']);(p/'safe-zone-report.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
