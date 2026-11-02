from pathlib import Path
import json,re,subprocess,wave,hashlib,numpy as np
p=Path(__file__).parent;sr=48000;src=p/'assets/audio/source-narration.mp3'
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-ar',str(sr),'-ac','1','-f','f32le','-']),dtype='<f4').copy()
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-af','silencedetect=noise=-42dB:d=0.22','-f','null','-'],capture_output=True,text=True,check=True)
cuts=[];st=None
for typ,t in re.findall(r'silence_(start|end): ([\d.]+)',r.stderr):
 t=float(t)
 if typ=='start':st=t
 elif st is not None:
  if t-st>.26:cuts.append((st+.07,t-.07))
  st=None
parts=[];cur=0
for st,en in cuts:parts.append(a[cur:round(st*sr)]);cur=round(en*sr)
parts.append(a[cur:]);voice=np.concatenate(parts)
with wave.open(str(p/'assets/audio/narration.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(voice,-1,1)*32767).astype('<i2').tobytes())
def retime(t):return t-sum(max(0,min(t,en)-st) for st,en in cuts if t>st)
w=[dict(x,start=round(retime(x['start']),3),end=round(retime(x['end']),3)) for x in json.load(open(p/'source-words.json'))]
corrections=[]
(p/'words.json').write_text(json.dumps(w,indent=2));(p/'script.txt').write_text(' '.join(x['word'] for x in w));(p/'production/transcript-corrections.json').write_text(json.dumps(corrections,indent=2))
meta={'source_duration':len(a)/sr,'tightened_voiceover_duration':len(voice)/sr,'video_duration':float(np.ceil((len(voice)/sr+.25)*30)/30),'cuts':cuts,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'method':'Single transcription aligned through genuine silence cuts >260ms at -42dB with 70ms protection on each boundary; no new speech or time stretching.'}
(p/'audio-edits.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta));print((p/'script.txt').read_text())
