"""Constrain generated illustration pixels to the supplied red-zone guide's clear area.
Preserve aspect ratios, event timing and easing; no source artwork is edited.
"""
from PIL import Image
from pathlib import Path
import math,json
class SafeLayout:
 def __init__(self,root,keys):
  self.bounds={};self.states={};self.changes=[];self.rect=(80,220,840,1600)
  self.exceptions=json.loads((Path(root)/'safe-zone-config.json').read_text())['exceptions']
  for k in keys:
   im=Image.open(Path(root)/'assets'/(k+'.png')).convert('RGBA');a=im.getchannel('A');box=a.point(lambda v:255 if v>24 else 0).getbbox()
   if k in {'clearportrait','badportrait'}:l,t,w,h,ox,oy=140,490,800,960,400,480;ink=(0,0,800,800)
   else:
    l,t,w,h,ox,oy=110,460 if k in {'scan','analysis','overview','plan'} else 410,860,1090,430,632.2
    f=min(w/im.width,h/im.height);px=(w-im.width*f)/2;py=(h-im.height*f)/2;ink=(px+box[0]*f,py+box[1]*f,px+box[2]*f,py+box[3]*f)
   self.bounds[k]=(l,t,ox,oy,ink)
 def constrain(self,k,values,base):
  state=dict(base);state.update({q:values[q] for q in ['x','y','scale','rotation'] if q in values})
  l,t,ox,oy,(x0,y0,x1,y1)=self.bounds[k];r=math.radians(state['rotation']);c,sn=math.cos(r),math.sin(r)
  pts=[(c*(x-ox)-sn*(y-oy),sn*(x-ox)+c*(y-oy)) for x,y in [(x0,y0),(x0,y1),(x1,y0),(x1,y1)]]
  lo_x,hi_x=min(x for x,y in pts),max(x for x,y in pts);lo_y,hi_y=min(y for x,y in pts),max(y for x,y in pts)
  L,T,R,B=self.rect
  scale=min(state['scale'],(R-L)/(hi_x-lo_x),(B-T)/(hi_y-lo_y));state['scale']=scale
  state['x']=max(L-l-ox-scale*lo_x,min(R-l-ox-scale*hi_x,state['x']))
  state['y']=max(T-t-oy-scale*lo_y,min(B-t-oy-scale*hi_y,state['y']))
  out=dict(values);out.update({q:round(state[q],5) for q in ['x','y','scale','rotation']})
  return out,state
 def adapt(self,k,time,values,start=None):
  if k not in self.bounds or not any(q in values or (start and q in start) for q in ['x','y','scale','rotation']):return values,start
  base=self.states.get(k,dict(x=0,y=0,scale=1,rotation=0))
  if any(e['asset']==k and e['start']<=time<=e['end'] for e in self.exceptions):
   self.states[k]=dict(base,**{q:values[q] for q in ['x','y','scale','rotation'] if q in values});return values,start
  v,state=self.constrain(k,values,base)
  ss=None
  if start is not None:ss,_=self.constrain(k,start,base)
  self.states[k]=state
  requested={q:values[q] for q in ['x','y','scale','rotation'] if q in values};actual={q:v[q] for q in ['x','y','scale','rotation'] if q in v}
  if any(abs(float(requested[q])-actual[q])>.01 for q in requested):self.changes.append(dict(asset=k,time=time,requested=requested,actual=actual))
  return v,ss
 def rect_for(self,k):
  st=self.states[k];l,t,ox,oy,(x0,y0,x1,y1)=self.bounds[k];s=st['scale']
  return (l+ox+s*(x0-ox)+st['x'],t+oy+s*(y0-oy)+st['y'],l+ox+s*(x1-ox)+st['x'],t+oy+s*(y1-oy)+st['y'])
 def connector(self,k):
  if k=='microbe-link':
   a=self.rect_for('gutglow');b=self.rect_for('microbiome');sx,sy=a[2]+12,a[1]+(a[3]-a[1])*.48;ex,ey=b[0]-10,b[1]+(b[3]-b[1])*.50
  else:
   a=self.rect_for('pectin');b=self.rect_for('colon');sx,sy=a[2]+12,a[1]+(a[3]-a[1])*.62;ex,ey=b[0]-12,b[1]+(b[3]-b[1])*.28
  sy+=140;ey+=140;cx=(sx+ex)/2;cy=min(sy,ey)-25
  return f'M{sx:.2f} {sy:.2f} Q{cx:.2f} {cy:.2f} {ex:.2f} {ey:.2f} L{ex-20:.2f} {ey-20:.2f} M{ex:.2f} {ey:.2f} L{ex-29:.2f} {ey+8:.2f}'
