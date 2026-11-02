from pathlib import Path
import subprocess,json,hashlib
import numpy as np
P=Path(__file__).parent;E=json.loads((P/'audio-edits.json').read_text());sr=E['sample_rate']
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(P/'assets/audio/original.mp3'),'-f','f32le','-ar',str(sr),'-ac','1','-']),dtype=np.float32)
out=np.concatenate([a[round(l*sr):round(r*sr)] for l,r in E['keep_intervals']])
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(sr),'-ac','1','-i','pipe:0','-c:a','pcm_s24le',str(P/'assets/audio/narration.wav')],input=out.tobytes(),check=True)
assert abs(len(out)/sr-E['duration'])<1/sr
print('Rebuilt protected silence-only edit',len(out)/sr,'seconds')
