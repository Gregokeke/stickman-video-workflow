from pathlib import Path
import subprocess,re,json,wave,hashlib
import numpy as np
P=Path(__file__).parent
source=P/'assets/audio/source-narration.mp3'
rate=48000
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-ac','1','-ar',str(rate),'-f','f32le','-']),dtype='<f4')
result=subprocess.run(['ffmpeg','-hide_banner','-i',str(source),'-af','silencedetect=noise=-42dB:d=0.22','-f','null','-'],capture_output=True,text=True)
events=re.findall(r'silence_(start|end): ([\d.]+)',result.stderr)
cuts=[]; start=None
for kind,t in events:
 t=float(t)
 if kind=='start':start=t
 elif start is not None:
  if t-start>.26:cuts.append([round(start+.07,5),round(t-.07,5)])
  start=None
parts=[];cursor=0
for st,en in cuts:
 parts.append(a[cursor:round(st*rate)]);cursor=round(en*rate)
parts.append(a[cursor:]);edited=np.concatenate(parts)
pcm=(np.clip(edited,-1,1)*32767).astype('<i2')
with wave.open(str(P/'assets/audio/narration.wav'),'wb') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(pcm.tobytes())
report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_duration':len(a)/rate,'tightened_audio_duration':len(pcm)/rate,'removed_seconds':(len(a)-len(pcm))/rate,'cuts':cuts,'sample_rate':rate,'method':'Actual detected silence only; -42 dB, >260ms gaps, 70ms protected at each edge. No time stretching.','join_review':'Pending listening review'}
(P/'audio-edits.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
