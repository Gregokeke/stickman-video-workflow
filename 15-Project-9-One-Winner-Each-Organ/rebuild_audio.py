from pathlib import Path
import subprocess,json,sys
import numpy as np
import soundfile as sf
P=Path(__file__).parent;E=json.loads((P/'audio-edits.json').read_text());sr=E['sample_rate']
# Preserve the original preparation's 16-bit decoded samples before the cut edit.
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(P/'assets/audio/original.mp3'),'-f','s16le','-ar',str(sr),'-ac','1','-']),dtype='<i2').astype(np.float64)/32768
out=np.concatenate([a[round(l*sr):round(r*sr)] for l,r in E['keep_intervals']])
dst=Path(sys.argv[1]) if len(sys.argv)>1 else P/'assets/audio/narration.wav';sf.write(dst,out,sr,subtype='PCM_24')
assert abs(len(out)/sr-E['duration'])<1/sr
print('Rebuilt protected silence-only edit',len(out)/sr,'seconds')
