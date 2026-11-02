from pathlib import Path
import json,subprocess,shutil
import numpy as np
def write_audio(path,a,rate,subtype=None):
 subprocess.run(["ffmpeg","-y","-v","error","-f","f32le","-ar",str(rate),"-ac","2","-i","-","-c:a","pcm_f32le" if subtype=="FLOAT" else "pcm_s24le",str(path)],input=a.astype("<f4").tobytes(),check=True)
p=Path(__file__).parent;pack=Path(__file__).parent.parent/'sfxpack/Sound-Effects-Pack'
pack=pack if pack.exists() else p/'assets/sfx'
manifest=json.loads((pack/'Manifest.json').read_text());clips={x['id']:x for x in manifest['clips']}
# Intended audible attack, manifest ID, peak level before mastering, exact action.
C=[(.08,'B31',-10,'hook lateral arrival'),(.68,'B15',-13,'danger warning settles'),(2.38,'C04',-13,'rejected obvious liar reversal'),(4.52,'O01',-10,'friendly truthful exchange arrives'),(5.55,'B19b',-17,'truth check reveal'),(6.48,'C18',-15,'truth twists'),(7.34,'B06',-19,'conversation returns to focus'),(8.26,'B20',-11,'argument alternative enters'),(10.30,'B16',-13,'agreement settles'),(12.08,'B27',-17,'one deliberate nod'),(13.84,'A05b',-12,'mirrored pose reveal'),(15.24,'B08',-14,'seen reaction'),(16.70,'B35',-14,'understanding reaction'),(17.58,'C14',-17,'validation'),(19.32,'C10',-12,'shield drops'),(20.15,'B06',-18,'sneaking hand approaches'),(20.86,'C02',-18,'idea planted'),(21.45,'B20',-11,'subtle sassy reaction'),(22.90,'C04',-15,'idea appears self-originated'),(23.94,'B06',-20,'return to confident hero'),(24.72,'O01',-11,'force alternative enters'),(25.02,'C20',-17,'force negation stroke'),(26.64,'B31',-11,'gentle guide arrives'),(27.62,'B06',-18,'whisper suggestion'),(28.55,'C08',-14,'mind metaphor reveal'),(30.10,'C10',-13,'steering wheel turns'),(30.98,'B15',-13,'choice pose arrival'),(32.70,'B20',-11,'knowing face reveal'),(34.36,'C04',-12,'you did not reversal'),(36.62,'B27',-18,'negated persuasion'),(38.24,'B02',-15,'conditions chess placement'),(39.42,'B08',-14,'self-convinced stance'),(40.80,'B19b',-16,'realization'),(42.72,'A05b',-11,'already fulfilled request'),(45.18,'O01',-12,'willing agreement emergence'),(45.70,'C14',-18,'final willing handshake')]
def decode(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ar','48000','-ac','2','-f','f32le','-']),np.float32).reshape(-1,2).copy()
# Normalize voice first; no speech generation and no change of pace.
subprocess.run(['ffmpeg','-y','-v','error','-i',str(p/'assets/narration.wav'),'-af','loudnorm=I=-16.5:TP=-2.5:LRA=11','-ar','48000',str(p/'assets/narration-level.wav')],check=True)
voice=decode(p/'assets/narration-level.wav');N=round(46.74*48000);n=np.zeros((N,2),np.float32);n[:min(N,len(voice))]=voice[:N]
fx=np.zeros_like(n);out=[];(p/'assets/sfx').mkdir(exist_ok=True)
for attack,id,db,action in C:
 c=clips[id];src=pack/c['wav'];src=src if src.exists() else pack/Path(c['wav']).name;dst=p/'assets/sfx'/src.name
 if src.resolve()!=dst.resolve():shutil.copy2(src,dst)
 a=decode(src);a*=10**(db/20)/max(float(np.max(np.abs(a))),1e-9)
 onset=max(0,attack-c.get('attack_offset_ms',0)/1000);i=round(onset*48000);j=min(N,i+len(a));fx[i:j]+=a[:j-i]
 out.append(dict(id=id,file='assets/sfx/'+dst.name,action=action,attack_time=attack,onset=onset,attack_offset_ms=c.get('attack_offset_ms',0),peak_dbfs=db,duration=len(a)/48000,tail_preserved=j-i==len(a)))
write_audio(p/'assets/effects.wav',fx,48000,subtype='PCM_24');write_audio(p/'assets/premaster.wav',n+fx,48000,subtype='FLOAT')
subprocess.run(['ffmpeg','-y','-v','error','-i',str(p/'assets/premaster.wav'),'-af','loudnorm=I=-16:TP=-2:LRA=11','-ar','48000','-c:a','pcm_s24le',str(p/'assets/mix.wav')],check=True)
(p/'sound-cues.json').write_text(json.dumps(out,indent=2))
(p/'assets/sfx/Manifest.json').write_text(json.dumps({'clips':[clips[id] for id in dict.fromkeys(x[1] for x in C)],'source_pack':'Sound-Effects-Pack-v2, 72 user-supplied segmented clips'},indent=2))
(p/'SFX-CREDITS.md').write_text('# Sound effects\n\nUsed original WAV effects from the user-supplied Sound-Effects-Pack-v2, drawn from the three supplied compilations plus original project whoosh. Descriptive names do not imply new licensing. Full provenance for used files is in assets/sfx/Manifest.json. No generated or substituted effects; no music. Cue attacks, peak gains and uses are recorded in sound-cues.json. Source attacks/decay tails are retained.\n')
print(len(C),'motivated cues;',len(set(x[1] for x in C)),'distinct sound files;',sum(x['tail_preserved'] for x in out),'full tails')
