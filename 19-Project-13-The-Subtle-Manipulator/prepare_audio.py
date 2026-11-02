import subprocess,re,json
from pathlib import Path
import numpy as np
import wave
p=Path(__file__).parent
src=p/'assets/source-narration.mp3'
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-f','f32le','-ac','1','-ar','48000','-']),dtype=np.float32)
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-af','silencedetect=noise=-42dB:d=0.26','-f','null','-'],capture_output=True,text=True).stderr
starts=[float(v) for v in re.findall(r'silence_start: ([\d.]+)',r)];ends=[float(v) for v in re.findall(r'silence_end: ([\d.]+)',r)]
if len(ends)<len(starts):ends.append(len(a)/48000)
remove=[]
for s,e in zip(starts,ends):
 if e-s>.26:remove.append((s+.070,e-.070))
segments=[];pos=0
for s,e in remove:
 segments.append(a[round(pos*48000):round(s*48000)]);pos=e
segments.append(a[round(pos*48000):])
out=np.concatenate(segments);w=wave.open(str(p/'assets/narration.wav'),'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes());w.close()
(p/'audio-edits.json').write_text(json.dumps({'original_duration':len(a)/48000,'duration':len(out)/48000,'removed':remove},indent=2))
print('audio',len(a)/48000,'->',len(out)/48000,flush=True)
from faster_whisper import WhisperModel
m=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=4)
segs,info=m.transcribe(np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p/'assets/narration.wav'),'-ar','16000','-ac','1','-f','f32le','-']),dtype=np.float32),word_timestamps=True,beam_size=5)
o=[]
for s in segs:
 print(s.start,s.end,s.text,flush=True)
 o.extend({'start':w.start,'end':w.end,'word':w.word.strip()} for w in s.words)
(p/'words.json').write_text(json.dumps(o,indent=2))
