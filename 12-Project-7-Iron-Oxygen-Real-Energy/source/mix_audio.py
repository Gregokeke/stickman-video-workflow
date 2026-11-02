from pathlib import Path
import json,subprocess,shutil
import numpy as np
import soundfile as sf
P=Path(__file__).parent;pack=P.parents[1]/'workspace/Stickman-Animations-Complete-Workspace/11-Sound-Effects/Sound-Effects-Pack-v2-Extracted/Sound-Effects-Pack'
local=P/'assets/sfx';local.mkdir(exist_ok=True)
manifest=json.loads(((pack/'Manifest.json') if pack.exists() else local/'Manifest.json').read_text());clips={x['id']:x for x in manifest['clips']}
C=[(0.1, 'O01', -7, 'hook glide'), (2.08, 'B20', -8, 'exact Glow Trinity blame character'), (3.84, 'C04', -10, 'not lazy reversal'), (5.1, 'B31', -8, 'undersupplied character'), (7.94, 'B15', -9, 'diet reveal'), (9.96, 'B19b', -14, 'iron identity'), (11.32, 'A05b', -9, 'weak character'), (12.38, 'B06', -10, 'fog character'), (13.84, 'B20', -8, 'useless punchline'), (15.96, 'O01', -8, 'iron explanation'), (17.46, 'B18', -9, 'hemoglobin handoff'), (19.42, 'B31', -8, 'red blood cell'), (20.72, 'A11', -9, 'oxygen reveal'), (21.3, 'B21', -9, 'lung origin'), (22.2, 'B08', -10, 'brain destination'), (22.76, 'B27', -12, 'muscle destination'), (23.58, 'B36', -8, 'cell zoom'), (24.02, 'B09', -10, 'mitochondrion detail'), (24.82, 'C02', -16, 'ATP energy'), (25.36, 'C18', -9, 'deficient blood contrast'), (27.48, 'B20', -8, 'starved cell'), (30.36, 'B31', -8, 'half dead acting'), (32.98, 'O01', -7, 'coffee chapter'), (34.4, 'B16', -9, 'third coffee'), (35.6, 'B08', -10, 'empty stomach'), (36.38, 'C14', -12, 'false solution joke'), (38.96, 'C04', -9, 'news flash'), (40.35, 'C20', -12, 'not oxygen'), (41.74, 'B31', -8, 'cell and depleted battery'), (43.05, 'B27', -13, 'battery strike'), (44.46, 'B21', -9, 'receptor explanation'), (44.96, 'C02', -16, 'adenosine'), (45.5, 'B02', -12, 'caffeine docks'), (46.2, 'C10', -13, 'adenosine rejected'), (47.38, 'B06', -10, 'exhaustion'), (48.94, 'B36', -8, 'stress response'), (49.62, 'B15', -9, 'adrenal glands'), (50.96, 'B19b', -14, 'stress hormone identities'), (52.18, 'B20', -8, 'fake smile'), (53.36, 'B27', -10, 'two hours'), (55.36, 'C18', -9, 'nervous system reveal'), (57.6, 'C21', -14, 'grave punchline'), (58.74, 'O01', -7, 'app chapter'), (62.08, 'B31', -8, 'meal scanner'), (63.12, 'B02', -12, 'daily scan logged'), (64.58, 'B18', -9, 'patterns screen'), (67.44, 'C04', -10, 'gaps contrast'), (68.15, 'B06', -11, 'assessment'), (69.4, 'B19b', -14, 'vitamins and minerals'), (71.2, 'B06', -10, 'body begging'), (72.54, 'B20', -9, 'neglect'), (74.66, 'O01', -7, 'planner'), (76.34, 'B15', -10, 'balanced meal'), (78.9, 'B31', -8, 'juice options'), (80.24, 'B06', -10, 'blend detail'), (81.9, 'B18', -9, 'absorption'), (82.64, 'C02', -16, 'cell uptake'), (84.12, 'B06', -9, 'body relief'), (86.2, 'C04', -10, 'zombie contrast'), (88.82, 'B31', -7, 'energized reveal'), (89.66, 'C14', -12, 'clear thinking'), (90.44, 'B02', -12, 'functional'), (91.82, 'O01', -8, 'search app'), (93.75, 'C14', -15, 'final invitation')]
C=[(40.48 if t==40.35 else t,i,p,r) for t,i,p,r in C if t not in [43.05,93.75]]
C += [(39.97,'B20',-10,'crossed-arms refusal torso arrives'),(42.4,'B02',-18,'battery drains five to four'),(42.72,'B02',-18,'battery drains four to three'),(43.04,'B02',-18,'battery drains three to two'),(43.36,'B27',-15,'battery drains two to one'),(92.30,'B02',-23,'search typing begins'),(92.58,'B02',-24,'search typing continues'),(92.86,'B02',-23,'search word completed'),(93.08,'C14',-15,'actual Remea icon result settles')]
C.sort(key=lambda c:c[0])
D=94.8;sr=48000;N=round(D*sr);fx=np.zeros((N,2),np.float32);out=[]
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
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(P/'assets/audio/premaster.wav'),'-af','loudnorm=I=-16:TP=-1.8:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);j=json.loads(r.stderr[r.stderr.rfind('{'):])
af='loudnorm=I=-16:TP=-1.8:LRA=9:measured_I='+j['input_i']+':measured_TP='+j['input_tp']+':measured_LRA='+j['input_lra']+':measured_thresh='+j['input_thresh']+':offset='+j['target_offset']+':linear=true:print_format=json'
r=subprocess.run(['ffmpeg','-hide_banner','-y','-i',str(P/'assets/audio/premaster.wav'),'-af',af,'-ar',str(sr),'-c:a','pcm_s24le',str(P/'assets/audio/mix.wav')],capture_output=True,text=True,check=True)
(P/'sound-cues.json').write_text(json.dumps(out,indent=2));(P/'production/audio-mastering.json').write_text(json.dumps(dict(input=j,output=r.stderr[r.stderr.rfind('{'):],cues=len(out),unique_sources=len(set(c['source'] for c in out)),all_tails_preserved=all(c['tail_preserved'] for c in out)),indent=2))
(local/'Manifest.json').write_text(json.dumps({'clips':[clips[id] for id in dict.fromkeys(c['source'] for c in out)],'provenance':'User supplied 72-effect pack v2; preserve original source rights'},indent=2))
print(len(out),'cues;',len(set(c['source'] for c in out)),'source sounds;',sum(c['tail_preserved'] for c in out),'full tails',flush=True)
