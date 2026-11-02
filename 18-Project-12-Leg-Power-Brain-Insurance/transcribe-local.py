from pathlib import Path
import json,subprocess
import numpy as np
from faster_whisper import WhisperModel
P=Path(__file__).parent
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(P/'assets/audio/source-narration.mp3'),'-ac','1','-ar','16000','-f','f32le','-']),np.float32)
print('Loading local alignment model',flush=True)
m=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4)
segments,info=m.transcribe(a,word_timestamps=True,beam_size=5,language='en',vad_filter=True)
out=[]
for s in segments:
 row=dict(start=s.start,end=s.end,text=s.text,words=[dict(start=w.start,end=w.end,word=w.word.strip(),probability=w.probability)for w in s.words]);out.append(row);print(s.start,s.end,s.text,flush=True)
(P/'transcript.json').write_text(json.dumps(out,indent=2));(P/'script.txt').write_text(' '.join(s['text'].strip()for s in out))
