from faster_whisper import WhisperModel
import json
import numpy as np,subprocess
from pathlib import Path
P=Path(__file__).parent
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4)
segments,info=model.transcribe(np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(P/'assets/audio/source-narration.mp3'),'-ar','16000','-ac','1','-f','f32le','-']),dtype=np.float32),beam_size=5,word_timestamps=True,language='en',vad_filter=False)
a=[]
for s in segments:
 d={'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in s.words]}
 a.append(d);print(s.start,s.end,s.text,flush=True)
(P/'transcript.json').write_text(json.dumps(a,indent=2))
