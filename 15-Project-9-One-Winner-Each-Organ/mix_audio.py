from pathlib import Path
import json,subprocess,shutil
import numpy as np
import soundfile as sf
P=Path(__file__).parent
local=P/'assets/sfx';local.mkdir(exist_ok=True)
manifest=json.loads((local/'Manifest.json').read_text());clips={x['id']:x for x in manifest['clips']}
C=[]
S=json.loads((P/'storyboard.json').read_text())
accent={'host','overload','winner','heart','inflamed','rupture','omega','next-eyes','screen','eye-protected','kidneys','crystals','magnesium','skeleton','d3','k2','liver','nac','glutathione','hospital','muscle','lift','creatine','old-lift','dose'}
routes={'left':'B06','right':'B18','depth':'B31','rise':'B15','diagonal':'B20','arcLeft':'B20','arcRight':'B36','emerge':'B15','peek':'B06','state':'B08'}
for i,a in enumerate(sorted(S,key=lambda a:a['start'])):
 if a['route']=='presenter':continue
 C.append((a['start'], 'O01' if a['id'] in {'host','heart','next-eyes','kidneys','skeleton','liver','muscle'} else routes.get(a['route'],'B06'), -11 if a['id'] in accent else -17, a['id']+' phrase-matched arrival'))
C += [(25.32,'B08',-19,'study number reveal'),(29.94,'C14',-17,'half risk result'),(51.66,'C14',-17,'vision study result'),(72.36,'C14',-17,'kidney study result'),(116.72,'B27',-19,'ATP energy drains'),(122.6,'C14',-17,'ATP replenishment'),(130.04,'C14',-17,'training result')]
C.sort(key=lambda c:c[0])
D=json.loads((P/'audio-edits.json').read_text())['video_duration'];sr=48000;N=round(D*sr);fx=np.zeros((N,2),np.float32);out=[]
for t,id,peak,reason in C:
 c=clips[id];src=local/Path(c['wav']).name;dst=local/src.name
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
