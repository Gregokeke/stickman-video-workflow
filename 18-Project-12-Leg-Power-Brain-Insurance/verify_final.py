from pathlib import Path
import json,subprocess
import numpy as np,soundfile as sf
P=Path(__file__).parent;sr=48000
T=json.loads((P/'source-words.json').read_text());W=json.loads((P/'words.json').read_text());cuts=json.loads((P/'audio-edits.json').read_text())['removed']
conflicts=[(a,b,w['word'])for a,b in cuts for w in T if a<w['end']+.025 and b>w['start']-.025];assert not conflicts
source=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(P/'assets/audio/source-narration.mp3'),'-ac','1','-ar',str(sr),'-f','f32le','-']),np.float32)
pieces=[];last=0
for a,b in cuts:pieces.append(source[last:round(a*sr)]);last=round(b*sr)
pieces.append(source[last:]);expected=np.concatenate(pieces);actual,_=sf.read(P/'assets/audio/narration.wav',dtype='float32');error=float(abs(expected-actual).max());assert error<1.3e-7
assert len(T)==len(W)==332;assert W[-1]['word']=='day.';assert W[-1]['end']+.025<len(actual)/sr
master,_=sf.read(P/'assets/audio/mix.wav',dtype='float32',always_2d=True);assert len(master)==113*sr
video=P/'renders/Leg-Power-Brain-Insurance.mp4';decoded=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-ac','2','-ar',str(sr),'-f','f32le','-']),np.float32).reshape(-1,2);assert len(decoded)>=len(master);decoded=decoded[:len(master)]
corr=[]
for k in range(113):
 a=decoded[k*sr:(k+1)*sr].ravel();b=master[k*sr:(k+1)*sr].ravel()
 if float(np.mean(b*b))>1e-6:corr.append(float(np.corrcoef(a,b)[0,1]))
assert min(corr)>.99
C=json.loads((P/'full-captions.json').read_text());assert ' '.join(c['text']for c in C)==' '.join(w['word']for w in W)
E=json.loads((P/'production/export-verification.json').read_text());assert E['full_decode_passed'] and E['frame_count']==3390
out=dict(full_narration_word_count=332,quiet_cut_word_guard_conflicts=conflicts,narration_reconstruction_max_error=error,full_narration_duration=len(actual)/sr,last_full_word=W[-1],full_master_duration=len(master)/sr,full_captions_match_all_words=True,caption_phrases=len(C),encoded_audio_correlation_min=min(corr),active_audio_windows=len(corr),full_video_complete=True)
(P/'production/final-audio-verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
