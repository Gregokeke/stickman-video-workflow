from pathlib import Path
import numpy as np,subprocess,json,wave
P=Path(__file__).parent;SR=48000;D=125.1
def decode(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ar',str(SR),'-ac','2','-f','f32le','-']),dtype='<f4').reshape(-1,2).copy()
voice=decode(P/'assets/audio/narration.wav');mix=np.zeros((round(D*SR),2),np.float32);fx=np.zeros_like(mix)
voice*=min(1.35,.78/max(float(np.max(abs(voice))),.001));mix[:len(voice)]=voice
# Selected major spatial handoffs; all intervening illustration changes are quiet.
whooshes=[(0.12,'pitch enters'),(4.54,'hypothetical pill comparison'),(7.16,'happy pill-taking illustration'),(10.26,'eager purchase'),(12.72,'reveal turn'),(18.28,'coffee fantasy'),(21.9,'walking reveal'),(25.92,'research setup'),(30.72,'door shuffle'),(35.44,'delivery interaction'),(37.58,'high-step contrast'),(42.42,'existential reaction'),(45.16,'relative explanation'),(52.44,'grim reaper metaphor'),(57.96,'offended reaction'),(67.32,'perspective reaction'),(78.06,'bed punchline'),(82.36,'mattress winner'),(86.08,'explicit smoking rejection'),(90.72,'marching contrast'),(94.48,'average steps'),(100.2,'reluctant start'),(114.32,'prepare to walk'),(118.46,'magic pill callback'),(122.46,'pallbearer punchline')]
cues=[]
for i,(t,why) in enumerate(whooshes):cues.append(dict(time=t,file='whoosh-short.wav' if i%3 else 'whoosh.wav',peak_db=-19 if i%3 else -18,trim=.55,reason=why))
for t,why in [(3.18,'hypothetical 12 percent'),(22.25,'walking title reveal'),(51.2,'relative decrease resolved'),(65.18,'threefold resolved'),(73.1,'twofold resolved'),(84.25,'mattress joke'),(109.12,'over 50 percent resolved'),(123.02,'six pallbearers')]:cues.append(dict(time=t,file='impact-bass-1.wav' if t<80 else 'impact-bass-2.wav',peak_db=-17,trim=.65,reason=why))
for t,why,file in [(54.85,'bribe exchange','cash.wav'),(97.0,'daily step watch revealed','click.wav')]:cues.append(dict(time=t,file=file,peak_db=-22,trim=.3,reason=why))
for c in cues:
 a=decode(P/'assets/sfx'/c['file'])[:round(c['trim']*SR)]
 peak=max(float(np.max(abs(a))),.001);a*=10**(c['peak_db']/20)/peak
 fade=min(round(.055*SR),len(a)//4);a[-fade:]*=np.linspace(1,0,fade)[:,None];a[:180]*=np.linspace(0,1,180)[:,None]
 st=round(c['time']*SR);n=min(len(a),len(fx)-st);fx[st:st+n]+=a[:n]
mix+=fx
peak=float(np.max(abs(mix)));mix*=min(1,.95/peak)
for name,a in [('effects.wav',fx),('mix.wav',mix)]:
 with wave.open(str(P/'assets/audio'/name),'wb') as f:
  f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
(P/'sound-cues.json').write_text(json.dumps(sorted(cues,key=lambda c:c['time']),indent=2));print(len(cues),'motivated cues, peak',float(np.max(abs(mix))))
