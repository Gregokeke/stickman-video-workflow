from pathlib import Path
import json,subprocess,re,math,shutil,wave
import numpy as np
P=Path(__file__).parent
for q in ['assets/audio','assets/graphics','assets/fonts','assets/vendor','assets/sfx','references','production','renders']: (P/q).mkdir(parents=True,exist_ok=True)
src=P/'assets/audio/source-narration.mp3'
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-f','f32le','-ac','1','-ar','48000','-']),dtype=np.float32)
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-af','silencedetect=noise=-36dB:d=0.18','-f','null','-'],capture_output=True,text=True).stderr
starts=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',r)];ends=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',r)]
if len(ends)<len(starts):ends.append(len(a)/48000)
cuts=[(s+.06,e-.06) for s,e in zip(starts,ends) if e-s>.20]
source_words=[w for seg in json.loads((P/'transcript.json').read_text()) for w in seg['words']]
cuts=[(s,e) for s,e in cuts if not any(min(e,w['end'])-max(s,w['start'])>.015 for w in source_words)]
parts=[];pos=0
for s,e in cuts:parts.append(a[round(pos*48000):round(s*48000)]);pos=e
parts.append(a[round(pos*48000):]);out=np.concatenate(parts)
# No added artificial pause in final revision.
pause_at=100.0;pause_duration=0;cut=round(pause_at*48000)
out=np.concatenate([out[:cut],np.zeros(round(pause_duration*48000),dtype=np.float32),out[cut:]])
with wave.open(str(P/'assets/audio/narration.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes((out*32767).astype('<i2').tobytes())
def time(t):
 q=t-sum(max(0,min(t,e)-s) for s,e in cuts if t>s)
 return q+(pause_duration if q>=pause_at else 0)
source=[w for s in json.loads((P/'transcript.json').read_text()) for w in s['words']]
words=[dict(start=round(time(w['start']),3),end=round(time(w['end']),3),word=w['word'].strip()) for w in source]
T=len(out)/48000;D=max(114.6,math.ceil((T+1.0)*30)/30)
(P/'audio-edits.json').write_text(json.dumps(dict(original_duration=len(a)/48000,duration=T,video_duration=D,removed=cuts,revision_insertions=[dict(at=pause_at,duration=pause_duration)]),indent=2));(P/'source-words.json').write_text(json.dumps(source,indent=2));(P/'words.json').write_text(json.dumps(words,indent=2));(P/'script.txt').write_text(' '.join(w['word'] for w in words))
print('Tightened',len(a)/48000,'to',T,'video',D,'minimum',22+max(0,math.ceil((T-70)/3)))
for s in json.loads((P/'transcript.json').read_text()):print(round(time(s['start']),2),round(time(s['end']),2),s['text'])
