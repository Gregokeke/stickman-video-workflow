from pathlib import Path
import json,subprocess,re,math
import numpy as np,soundfile as sf
P=Path(__file__).parent;sr=48000
src=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(P/'assets/audio/source-narration.mp3'),'-ac','1','-ar',str(sr),'-f','f32le','-']),np.float32)
T=json.load(open(P/'transcript.json'));W=[w for s in T for w in s['words']];(P/'source-words.json').write_text(json.dumps(W,indent=2))
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(P/'assets/audio/source-narration.mp3'),'-af','silencedetect=noise=-40dB:d=0.23','-f','null','-'],capture_output=True,text=True,check=True);(P/'silence-detection.txt').write_text(r.stderr)
starts=[float(x)for x in re.findall(r'silence_start: ([0-9.]+)',r.stderr)];ends=[float(x)for x in re.findall(r'silence_end: ([0-9.]+)',r.stderr)];cuts=[]
for a,b in zip(starts,ends):
 a+=.07;b-=.07
 if b-a<.08 or a<.15 or b>W[-1]['end']:continue
 safe=[(a,b)]
 for w in W:
  lo,hi=w['start']-.025,w['end']+.025;nextsafe=[]
  for x,y in safe:
   if hi<=x or lo>=y:nextsafe.append((x,y))
   else:
    if lo>x:nextsafe.append((x,min(y,lo)))
    if hi<y:nextsafe.append((max(x,hi),y))
  safe=nextsafe
 for x,y in safe:
  if y-x>=.08:cuts.append([round(x*sr)/sr,round(y*sr)/sr])
chunks=[];last=0
for a,b in cuts:chunks.append(src[last:round(a*sr)]);last=round(b*sr)
chunks.append(src[last:]);out=np.concatenate(chunks);sf.write(P/'assets/audio/narration.wav',out,sr,subtype='PCM_24')
def warp(t):return t-sum(max(0,min(t,b)-a)for a,b in cuts if t>a)
for w in W:w['start']=round(warp(w['start']),5);w['end']=round(warp(w['end']),5)
(P/'words.json').write_text(json.dumps(W,indent=2));D=math.ceil((len(out)/sr+.5)*30)/30;(P/'audio-edits.json').write_text(json.dumps({'original_duration':len(src)/sr,'duration':len(out)/sr,'video_duration':D,'removed':cuts,'method':'Only genuine detected silence;70ms boundary tails and25ms word guards; no speed change'},indent=2));print('Audio',len(src)/sr,'->',len(out)/sr,'video',D,'cuts',len(cuts),'words',len(W))
for i,w in enumerate(W):print(i,f"{w['start']:.3f}",w['word'])
