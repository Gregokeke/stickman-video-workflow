"""Regenerate the original effect track locally. Requires numpy; no voice service."""
from pathlib import Path
import numpy as np
import wave
sr=48000
y=np.zeros(sr*22)
events=[(.25,730,.06),(1.25,250,.10),(2.85,310,.07),(3.6,1450,.045),(3.74,1650,.04),(4.71,430,.12),(5.21,550,.12),(8.35,320,.09),(9.35,410,.09),(10.35,510,.1),(11.7,850,.07),(15.0,260,.10),(15.6,620,.06),(16.0,740,.06),(16.4,880,.06),(18.2,410,.08),(18.4,520,.08),(18.6,640,.08),(19.55,180,.11),(19.73,250,.08),(19.85,330,.06),(20.2,1040,.08),(20.35,1310,.06)]
for t,f,a in events:
 s=np.arange(int(.45*sr))/sr
 v=a*(np.sin(2*np.pi*(f*s-100*s*s))+.22*np.sin(2*np.pi*f*2*s))*np.exp(-s*17)*(1-np.exp(-s*800))
 i=int(t*sr)
 y[i:i+len(v)]+=v
for t in [6.85,13.8]:
 s=np.arange(int(.9*sr))/sr
 v=.026*(np.sin(2*np.pi*(180*s+950*s*s))+np.sin(2*np.pi*(313*s+750*s*s)))*np.sin(np.pi*s/.9)**2
 i=int(t*sr)
 y[i:i+len(v)]+=v
with wave.open(str(Path(__file__).parent/'motion-sfx.wav'),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
 w.writeframes((y*32767).astype('<i2').tobytes())
