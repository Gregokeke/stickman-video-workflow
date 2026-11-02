from pathlib import Path
import wave,subprocess
import numpy as np
p=Path(__file__).parent/'assets/sfx';rate=48000;rng=np.random.default_rng(20261024)
def read(n):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p/(n+'.wav')),'-ac','1','-ar',str(rate),'-f','f32le','-']),np.float32)
def save(n,a):
 a=a/(max(np.max(np.abs(a)),1e-6))*0.75;edge=min(300,len(a)//8);a[:edge]*=np.linspace(0,1,edge);a[-edge:]*=np.linspace(1,0,edge)
 with wave.open(str(p/(n+'.wav')),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes((a*32767).astype('<i2').tobytes())
def pad(a,n):return np.pad(a[:n],(0,max(0,n-len(a))))
t=np.arange(round(.6*rate))/rate
click=read('click');impact=read('impact-bass-1');whoosh=read('whoosh-short');glitch=read('glitch-1')
save('stamp',pad(impact,len(t))*.8+pad(click,len(t))*.6)
cash=np.zeros_like(t)
for s,g in [(0,1),(.1,.65),(.22,.48)]:
 i=round(s*rate);a=click[:min(len(click),len(cash)-i)];cash[i:i+len(a)]+=a*g
save('cash',cash)
save('news-hit',pad(read('impact-bass-2'),len(t))+.22*np.sin(2*np.pi*880*t)*np.exp(-t*18))
noise=rng.standard_normal(len(t));smooth=np.convolve(noise,np.ones(8)/8,'same')
phase=2*np.pi*(1500*t-950*t*t)
save('record-scratch',(np.sin(phase)*.45+smooth*.55)*(np.sin(2*np.pi*22*t)*.25+.75)*np.exp(-t*7))
save('deflate',(smooth*.8+np.sin(2*np.pi*(300*t-180*t*t))*.25)*np.exp(-t*6))
save('draw',smooth*(.25+.75*np.sin(np.pi*np.minimum(t/.4,1))**2)*np.exp(-t*6))
alarm=np.sin(2*np.pi*1050*t)*((t<.13)|((t>.22)&(t<.36)))*np.exp(-t*2)
save('alarm',alarm)
save('scan-tone',np.sin(2*np.pi*(650*t+450*t*t))*np.sin(np.pi*np.minimum(t/.52,1))**2*.7)
save('flush',pad(whoosh,len(t))*.45+np.sin(2*np.pi*140*t+np.sin(2*np.pi*19*t)*3)*np.exp(-t*6)*.30+smooth*np.exp(-t*4)*.25)
print('Designed nine short motivated effect variants; deterministic48kHzPCM')
