from pathlib import Path
from PIL import Image
import numpy as np,json,sys
p=Path(__file__).parent
im=Image.open(p/'references/red-zone-canvas.png').resize((1080,1920),Image.Resampling.NEAREST)
mask=np.asarray(im)[:,:,3]>64
# Ignore single-pixel export specks inside the transparent opening, retain the connected UI.
# All UI pixels are within the frame border or one of its three filled bars.
yy,xx=np.indices(mask.shape);mask &= ((xx<65)|(xx>1020)|(yy<205)|(yy>1600)|((xx>850)&(yy>705)))
exceptions=json.loads((p/'safe-zone-config.json').read_text())['exceptions']
expected=[]
states=json.loads(Path(sys.argv[1] if len(sys.argv)>1 else p/'safe-zone-states.json').read_text());cache={};tot={};events=[];caption_hits=[]
for frame in states['frames']:
 for it in frame['items']:
  k=it['id']
  if k not in cache:
   a=np.asarray(Image.open(p/'assets'/(k+'.png')).convert('RGBA'))[::5,::5,3];y,x=np.where(a>32);cache[k]=(x*5+2.5,y*5+2.5,Image.open(p/'assets'/(k+'.png')).size)
  sx,sy,(nw,nh)=cache[k];w,h=it['iw'],it['ih']
  scale=min(w/nw,h/nh);px=(w-nw*scale)/2;py=(h-nh*scale)/2
  lx=sx*scale+px;ly=sy*scale+py
  ox,oy=it['origin'];a,b,c,d,tx,ty=it['matrix']
  x=it['left']+ox+a*(lx-ox)+c*(ly-oy)+tx;y=it['top']+oy+b*(lx-ox)+d*(ly-oy)+ty
  inframe=(x>=0)&(x<1080)&(y>=0)&(y<1920)
  bad=np.ones(len(x),bool);bad[inframe]=mask[y[inframe].astype(int),x[inframe].astype(int)]
  allowed=np.zeros(len(x),bool)
  for ex in exceptions:
   if ex['asset']==k and ex['start']<=frame['time']<=ex['end']:
    allowed=(x<80)|(y>1600)
  expected_n=int((bad&allowed).sum())
  if expected_n:expected.append({'time':frame['time'],'asset':k,'samples':expected_n})
  bad &= ~allowed
  n=int(bad.sum())
  if n>0:
   ev={'time':frame['time'],'asset':k,'samples':n,'fraction':round(n/len(x),5),'opacity':round(it['opacity'],3)};events.append(ev)
   v=tot.setdefault(k,{'samples_with_overlap':0,'peak_fraction':0,'first':frame['time'],'last':frame['time']});v['samples_with_overlap']+=1;v['peak_fraction']=max(v['peak_fraction'],ev['fraction']);v['last']=frame['time']
 for x,y,w,h in frame['captions']:
  l,r=max(0,int(x)),min(1080,int(x+w)+1);t,b=max(0,int(y)),min(1920,int(y+h)+1)
  if mask[t:b,l:r].any():caption_hits.append(frame['time'])
report={'checked_frames':len(states['frames']),'interval_seconds':.1,'alpha_threshold':32,'visible_opacity_threshold':.1,'foreground_events':events,'assets':tot,'caption_hits':caption_hits,'documented_exceptions':exceptions,'expected_exception_events':expected}
out=Path(sys.argv[2]) if len(sys.argv)>2 else p/'safe-zone-report.json';out.write_text(json.dumps(report,indent=2));print(json.dumps({'frames':len(states['frames']),'assets':tot,'caption_hits':caption_hits,'documented_exceptions':exceptions,'expected_exception_events':expected},indent=2))
