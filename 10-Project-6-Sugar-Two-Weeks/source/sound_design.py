from pathlib import Path
import json,subprocess,numpy as np,soundfile as sf,shutil
p=Path(__file__).parent;pack=p;clips={x['id']:x for x in json.load(open(p/'references/sfx-pack-manifest.json'))['clips']};sr=48000;D=json.load(open(p/'audio-edits.json'))['video_duration'];N=round(D*sr);fx=np.zeros((N,2),np.float32);(p/'assets/sfx').mkdir(exist_ok=True)
# Onsets are actual movement, visible contact, plot milestone or verbal joke timings.
raw=[(44.57,'B27',-10,'twenty-minute time cue'),(.12,'O01',-7,'hook arrival'),(.72,'B20',-8,'independent sugar bowl entrance'),(1.78,'B27',-10,'two-week calendar'),(3.86,'C12',-12,'theatrical torture reaction'),(5.04,'B31',-8,'sugar ghoul reveal'),(5.45,'B15',-8,'candy jar settlement'),(7.84,'B20',-7,'presenter arrival'),(9.26,'C14',-12,'confident result tease'),(10.94,'A05b',-8,'craving reach'),(11.90,'C19',-11,'candy just out of reach'),(13.34,'B06',-8,'satisfied state'),(14.90,'B27',-10,'two-hour time cue'),(15.65,'B15',-9,'held plate acting state'),(18.07,'O01',-7,'sugar spoon arrival'),(19.21,'B19b',-14,'insulin identity reveal'),(20.99,'A11',-8,'glucose identity'),(21.51,'B31',-8,'bloodstream reveal'),(22.59,'B21',-9,'chart frame entrance'),(24.53,'C18',-8,'blood sugar crash punchline'),(25.99,'B36',-8,'brain takes focus'),(27.55,'C12',-12,'starvation exaggeration'),(28.71,'C04',-9,'just ate reversal'),(30.27,'C20',-8,'cut sugar'),(31.81,'C14',-12,'stable pattern resolves'),(33.03,'B09',-9,'gut context'),(34.59,'B18',-8,'bacteria detail emerges'),(36.99,'B20',-8,'nervous system handoff'),(38.43,'C09',-12,'begging bacterium joke'),(39.21,'B15',-8,'junk-food lure'),(40.48,'B31',-7,'energy chapter entrance'),(43.19,'C14',-11,'steady charge reveal'),(44.23,'C19',-10,'sugar high rise'),(46.55,'C18',-8,'sloth reversal'),(48.12,'B06',-9,'mechanism resets'),(50.10,'B20',-8,'fat cell emerges'),(50.74,'C01',-17,'unlock mechanism metaphor'),(51.64,'A05b',-8,'reserve tank reveal'),(53.85,'B21',-9,'mitochondrion handoff'),(54.45,'C02',-16,'steady energy takeaway'),(56.48,'B31',-7,'weight chapter entrance'),(58.02,'B15',-9,'scale settles'),(59.90,'C04',-10,'fat reserve reduction'),(61.46,'C21',-14,'old reserve trunk lands'),(63.6,'B03',-19,'dread tonal space'),(64.8,'C15',-15,'anxiety stutter'),(66.22,'B06',-8,'relief movement'),(67.8,'C14',-12,'upward mood resolve'),(68.54,'B21',-10,'crash explanation'),(71.60,'B19b',-15,'cortisol identity reveal'),(73.78,'B06',-10,'existential slump'),(77.08,'B15',-10,'diet plate entrance'),(79.21,'B20',-7,'brain tissue reveal'),(80.79,'B18',-9,'tissue detail'),(82.59,'B31',-8,'clear-thinking handoff'),(84.23,'B27',-12,'focused reading contact'),(86.61,'C04',-10,'blank-screen reversal'),(87.81,'B10',-12,'screen detail'),(88.47,'B27',-9,'40-minute timer'),(89.91,'B36',-8,'skin chapter'),(92.75,'C02',-16,'cheek glint'),(94.71,'C12',-13,'pretend corpse reaction'),(97.03,'B20',-8,'glycation schematic entrance'),(99.41,'B18',-9,'glucose binding detail'),(100.11,'B27',-10,'first molecular link contact'),(101.49,'B31',-9,'collagen identity'),(104.11,'C20',-13,'cross-link restriction'),(107.0,'B36',-8,'whole-body chapter'),(110.07,'B06',-9,'joint explanation'),(113.36,'B20',-8,'immune cell reveal'),(115.05,'B27',-12,'signaling contact'),(116.48,'B19b',-15,'cytokine identity'),(118.12,'B31',-8,'knee reaction'),(120.22,'B15',-8,'bubble-wrap pop'),(120.48,'B17',-10,'second bubble pop'),(120.79,'C08',-9,'last bubble pop'),(121.4,'B06',-8,'standing movement')]
cues=[]
for t,id,target,reason in raw:
 c=clips[id];src=pack/c['wav'];out=p/'assets/sfx'/src.name
 if not out.exists():shutil.copy2(src,out)
 a,fs=sf.read(src,dtype='float32',always_2d=True);assert fs==sr
 pk=float(abs(a).max());gain=10**(target/20)/max(pk,1e-9);a=a*gain
 onset=c.get('attack_offset_ms',0)/1000;start=max(0,t-onset);j=round(start*sr);length=min(len(a),N-j);fx[j:j+length]+=a[:length]
 cues.append(dict(time=t,start=round(start,6),source=id,path='assets/sfx/'+out.name,target_peak_dbfs=target,reason=reason,duration=len(a)/sr))
# Finite sidechain envelope: speech remains intelligible during the strong air movements.
voice,fs=sf.read(p/'assets/audio/narration.wav',dtype='float32',always_2d=True);voice=np.repeat(voice,2,axis=1) if voice.shape[1]==1 else voice;v=np.zeros((N,2),np.float32);v[:len(voice)]=voice
# Normalize speech alone to a clear platform mix before FX are added.
sf.write(p/'assets/audio/voice-raw.wav',v,sr,subtype='PCM_24')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'assets/audio/voice-raw.wav'),'-af','loudnorm=I=-16:TP=-2.5:LRA=9','-ar',str(sr),str(p/'assets/audio/voice-normalized.wav')],check=True)
v,fs=sf.read(p/'assets/audio/voice-normalized.wav',dtype='float32',always_2d=True);v=v[:N]
if len(v)<N:v=np.pad(v,((0,N-len(v)),(0,0)))
duck=np.ones(N,np.float32)
for c in cues:
 if c['target_peak_dbfs']<=-10:continue
 st=max(0,round((c['time']-.04)*sr));en=min(N,round((c['time']+.24)*sr));attack=min(1920,en-st);release=min(5760,max(0,N-en));level=10**(-1.5/20)
 duck[st:st+attack]=np.minimum(duck[st:st+attack],np.linspace(1,level,attack))
 duck[st+attack:en]=np.minimum(duck[st+attack:en],level)
 duck[en:en+release]=np.minimum(duck[en:en+release],np.linspace(level,1,release))
v*=duck[:,None];sf.write(p/'assets/audio/effects.wav',fx,sr,subtype='PCM_24');sf.write(p/'assets/audio/mix-premaster.wav',v+fx,sr,subtype='FLOAT')
# Two-pass loudness mastering, with oversampled true-peak control.
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(p/'assets/audio/mix-premaster.wav'),'-af','loudnorm=I=-16:TP=-1.8:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);j=r.stderr[r.stderr.rfind('{'):];stats=json.loads(j)
af='loudnorm=I=-16:TP=-1.8:LRA=9:measured_I='+stats['input_i']+':measured_TP='+stats['input_tp']+':measured_LRA='+stats['input_lra']+':measured_thresh='+stats['input_thresh']+':offset='+stats['target_offset']+':linear=true:print_format=json'
r=subprocess.run(['ffmpeg','-hide_banner','-y','-i',str(p/'assets/audio/mix-premaster.wav'),'-af',af,'-ar',str(sr),'-c:a','pcm_s24le',str(p/'assets/audio/mix.wav')],capture_output=True,text=True,check=True)
(p/'sound-cues.json').write_text(json.dumps(cues,indent=2));(p/'production/audio-mastering.json').write_text(json.dumps(dict(input=stats,output=r.stderr[r.stderr.rfind('{'):],cues=len(cues),unique_sounds=len(set(c['source'] for c in cues))),indent=2))
(p/'SFX-CREDITS.md').write_text('Sound effects are drawn from the user-supplied three compilation pack v2 and the original approved project whoosh. Descriptive aliases are not publisher titles. Source provenance and segment times are retained in the supplied pack manifest. No claim of CC0 or new licensing is made. Each cue records the pack ID, source file, meaningful event and attack-aligned time. No new sound effects or narration were generated.\n')
print('Finished',len(cues),'motivated cues,',len(set(c['source'] for c in cues)),'distinct sounds.')
