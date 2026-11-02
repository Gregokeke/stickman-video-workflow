from pathlib import Path
import subprocess,json,numpy as np
P=Path(__file__).parent;video=P/'renders/Kiwi-Small-Fruit-Big-Attitude.mp4'
def decode(f):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-vn','-ac','1','-ar','16000','-f','f32le','-']),np.float32)
a=decode(video);b=decode(P/'assets/audio/mix.wav');v=decode(P/'assets/audio/narration.wav');rows=[]
assert abs(len(b)/16000-114.6)<.001
assert len(a)>=len(b)
for t in range(113):
 start=t*16000;stop=min((t+1)*16000,len(v));n=stop-start
 if n<=0:continue
 x=a[start:stop];y=b[start:stop];voice=v[start:stop];energy=float(np.sqrt(np.mean(voice*voice)));rms=float(np.sqrt(np.mean(x*x)));corr=float(np.corrcoef(x,y)[0,1])
 if energy>.003:assert rms>.003 and corr>.985,(t,energy,rms,corr)
 rows.append(dict(second=t,original_voice_rms=energy,decoded_rms=rms,encoded_master_correlation=corr))
W=json.load(open(P/'words.json'));assert W[-1]['word']=='egg.' and W[-1]['end']<len(v)/16000
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-af','loudnorm=I=-16:TP=-2:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);j=json.loads(r.stderr[r.stderr.rfind('{'):]);assert -17<float(j['input_i'])<-15 and float(j['input_tp'])<-1.8,j
proof=dict(passed=True,decoded_duration=len(a)/16000,master_duration=len(b)/16000,narration_duration=len(v)/16000,final_word=W[-1],active_windows_checked=len(rows),minimum_master_correlation=min(x['encoded_master_correlation']for x in rows if x['original_voice_rms']>.003),ending_windows=rows[-10:],integrated_lufs=float(j['input_i']),true_peak_db=float(j['input_tp']),loudness_range=float(j['input_lra']),no_missing_ending=True)
(P/'production/audio-export-verification.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof,indent=2))
