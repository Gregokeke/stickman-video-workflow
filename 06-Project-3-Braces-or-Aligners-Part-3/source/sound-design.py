from pathlib import Path
import numpy as np,wave
p=Path(__file__).parent/'assets/sfx';sr=48000;rng=np.random.default_rng(9413)
def save(name,a):
 a=a/max(np.max(np.abs(a)),1e-8)*.8;a[:240]*=np.linspace(0,1,240);a[-1200:]*=np.linspace(1,0,1200)
 with wave.open(str(p/(name+'.wav')),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((a*32767).astype('<i2').tobytes())
t=np.arange(int(.6*sr))/sr;n=rng.normal(0,1,len(t));smooth=np.convolve(n,np.ones(13)/13,mode='same');splash=(n*.18+smooth*.9)*(np.exp(-t*8)*(1-np.exp(-t*70)))
for pos,freq in [(.04,850),(.12,600),(.23,1050)]:
 z=np.maximum(t-pos,0);splash+=.07*np.sin(2*np.pi*(freq*z-400*z*z))*np.exp(-z*24)*(t>=pos)
save('water-splash',splash)
t=np.arange(int(.42*sr))/sr;clink=sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*r) for a,f,r in [(1,2200,15),(.45,3470,23),(.20,5170,32)]);save('ice-clink',clink)
t=np.arange(int(.4*sr))/sr;n=rng.normal(0,1,len(t));soft=np.convolve(n,np.ones(35)/35,mode='same');save('soft-brush',soft*np.sin(np.pi*t/.4)**2)
print('Created deterministic splash, ice clink and soft brush accents')
