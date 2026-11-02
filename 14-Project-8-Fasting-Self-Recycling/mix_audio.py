from pathlib import Path
import json,subprocess,shutil
import numpy as np
import soundfile as sf
P=Path(__file__).parent;pack=P.parents[1]/'workspace/Stickman-Animations-Complete-Workspace/11-Sound-Effects/Sound-Effects-Pack-v2/Sound-Effects-Pack'
local=P/'assets/sfx';local.mkdir(exist_ok=True)
manifest=json.loads(((pack/'Manifest.json') if pack.exists() else local/'Manifest.json').read_text());clips={x['id']:x for x in manifest['clips']}
C=[(0.03, 'O01', -8, 'fasting hook arrival'), (1.26, 'B06', -12, 'question enters beside retained actor'), (3.74, 'C18', -13, 'stop-giving reversal'), (4.4, 'B31', -10, 'body energy cutaway'), (4.84, 'B15', -15, 'food-energy source'), (6.66, 'B20', -10, 'stopped-eating pose'), (7.8, 'B36', -10, 'internal recycling body reveal'), (9.16, 'B08', -18, 'attention shifts inside body'), (10.84, 'B06', -12, 'Yep knowing delivery'), (12.86, 'B18', -13, 'glucose identity'), (13.58, 'B19b', -16, 'insulin identity'), (13.88, 'B27', -19, 'two illustrative fills drop'), (15.02, 'B31', -10, 'survival switch arrives'), (15.28, 'B02', -17, 'switch clicks on'), (16.78, 'O01', -10, 'autophagy membrane emerges'), (18.7, 'B15', -13, 'self-recycling detail'), (20.36, 'B20', -11, 'hunting detective'), (21.0, 'B18', -14, 'senescent cell found'), (22.74, 'B16', -14, 'damaged-cell state'), (23.12, 'C10', -15, 'retired-cell comic beat'), (25.66, 'B27', -15, 'rent-free doorway lands'), (26.28, 'B06', -13, 'idle worker'), (28.68, 'B18', -15, 'still-alive identity'), (29.68, 'C18', -15, 'useless reaction'), (31.7, 'B21', -11, 'rotting cell'), (32.66, 'C09', -17, 'inflammatory leak'), (33.74, 'B06', -13, 'Basically setup'), (35.1, 'B31', -10, 'unemployed roommate'), (36.18, 'B20', -11, 'doorframe refusal'), (38.8, 'B15', -13, 'puffy waking face'), (40.22, 'B27', -16, 'stiff knee'), (40.82, 'C04', -15, 'eighty-in-twenties joke'), (43.98, 'B18', -13, 'inflammation recalled'), (45.72, 'O01', -10, 'cell cleanup detail'), (47.7, 'C09', -17, 'junk fragments emerge'), (48.74, 'B15', -14, 'amino acids emerge'), (50.14, 'B18', -16, 'protein'), (50.6, 'B27', -18, 'building blocks'), (51.78, 'B36', -11, 'burning for fuel'), (53.12, 'B06', -12, 'brain fog actor'), (54.36, 'C14', -16, 'fog clears and same face refreshes'), (54.9, 'B15', -14, 'depuffed face'), (57.0, 'B18', -14, 'joint close-up'), (57.52, 'B06', -13, 'joint relief'), (59.66, 'B31', -11, 'body cleanup returns'), (61.2, 'B15', -15, 'cellular waste'), (62.14, 'B20', -12, 'healing switch'), (62.58, 'B02', -17, 'healing switch on'), (64.88, 'O01', -10, 'stem cell hero'), (66.26, 'B18', -15, 'worn-out cell'), (67.3, 'C09', -16, 'new cells emerge'), (67.78, 'B08', -18, 'daughter cells separate'), (68.42, 'C14', -15, 'fresh healthy cell'), (69.72, 'B06', -12, 'tighter skin actor'), (70.72, 'B31', -11, 'recovery jog'), (72.06, 'B18', -14, 'gut irritation metaphor'), (72.52, 'B06', -17, 'gut calms on negation'), (75.4, 'B15', -12, 'wonder narrator'), (78.0, 'B27', -16, 'jaw-lock joke'), (79.06, 'B02', -18, 'a few hours clock'), (81.04, 'C14', -17, 'divine closing glint')]
D=json.loads((P/'audio-edits.json').read_text())['video_duration'];sr=48000;N=round(D*sr);fx=np.zeros((N,2),np.float32);out=[]
for t,id,peak,reason in C:
 c=clips[id];src=pack/c['wav'] if pack.exists() else local/Path(c['wav']).name;dst=local/src.name
 if src.resolve()!=dst.resolve():shutil.copy2(src,dst)
 a,fs=sf.read(src,dtype='float32',always_2d=True);assert fs==sr
 a*=10**(peak/20)/max(float(abs(a).max()),1e-9)
 start=max(0,t-c.get('attack_offset_ms',0)/1000);i=round(start*sr);n=min(len(a),N-i);fx[i:i+n]+=a[:n]
 out.append(dict(time=t,start=start,source=id,path='assets/sfx/'+src.name,target_peak_dbfs=peak,reason=reason,duration=len(a)/sr,tail_preserved=n==len(a)))
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'assets/audio/narration.wav'),'-af','loudnorm=I=-16:TP=-3:LRA=9','-ar',str(sr),str(P/'assets/audio/voice-normalized.wav')],check=True)
v,_=sf.read(P/'assets/audio/voice-normalized.wav',dtype='float32',always_2d=True)
if v.shape[1]==1:v=np.repeat(v,2,axis=1)
v=v[:N];v=np.pad(v,((0,max(0,N-len(v))),(0,0)));duck=np.ones(N,np.float32)
for c in out:
 if c['target_peak_dbfs']>-13:
  st=max(0,round((c['time']-.025)*sr));en=min(N,round((c['time']+.2)*sr));attack=min(1200,en-st);release=min(6500,N-en);level=10**(-1.5/20)
  duck[st:st+attack]=np.minimum(duck[st:st+attack],np.linspace(1,level,attack));duck[st+attack:en]=np.minimum(duck[st+attack:en],level);duck[en:en+release]=np.minimum(duck[en:en+release],np.linspace(level,1,release))
sf.write(P/'assets/audio/effects.wav',fx,sr,subtype='PCM_24');sf.write(P/'assets/audio/premaster.wav',v*duck[:,None]+fx,sr,subtype='FLOAT')
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(P/'assets/audio/premaster.wav'),'-af','loudnorm=I=-16:TP=-2.0:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);j=json.loads(r.stderr[r.stderr.rfind('{'):])
af='loudnorm=I=-16:TP=-2.0:LRA=9:measured_I='+j['input_i']+':measured_TP='+j['input_tp']+':measured_LRA='+j['input_lra']+':measured_thresh='+j['input_thresh']+':offset='+j['target_offset']+':linear=true:print_format=json'
r=subprocess.run(['ffmpeg','-hide_banner','-y','-i',str(P/'assets/audio/premaster.wav'),'-af',af,'-ar',str(sr),'-c:a','pcm_s24le',str(P/'assets/audio/mix.wav')],capture_output=True,text=True,check=True)
(P/'sound-cues.json').write_text(json.dumps(out,indent=2));(P/'production/audio-mastering.json').write_text(json.dumps(dict(input=j,output=r.stderr[r.stderr.rfind('{'):],cues=len(out),unique_sources=len(set(c['source'] for c in out)),all_tails_preserved=all(c['tail_preserved'] for c in out)),indent=2))
(local/'Manifest.json').write_text(json.dumps({'clips':[clips[id] for id in dict.fromkeys(c['source'] for c in out)],'provenance':'User supplied 72-effect pack v2; preserve original source rights'},indent=2))
print(len(out),'cues;',len(set(c['source'] for c in out)),'source sounds;',sum(c['tail_preserved'] for c in out),'full tails',flush=True)
