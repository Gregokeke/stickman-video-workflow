from pathlib import Path
import json,hashlib,zipfile,re
P=Path(__file__).parent;out=P.parent/'Brainwave-Besties-Project.zip';video=P/'renders/Brainwave-Besties.mp4';assert video.is_file()
ev=json.load(open(P/'production/export-verification.json'));av=json.load(open(P/'production/audio-export-verification.json'));assert ev['full_decode_passed']and av['passed']and ev['frame_count']==2587
inv=json.load(open(P/'asset-inventory.json'));new=[a for a in inv if not a['id'].startswith('instructor-')];assert len(new)==60 and len(inv)==63
for a in inv:assert hashlib.sha256((P/a['path']).read_bytes()).hexdigest()==a['sha256']
assert len({a['sha256']for a in new})==60
h=hashlib.sha256(video.read_bytes()).hexdigest();(P/'production/status.json').write_text(json.dumps({'stage':'Complete','final_video_rendered':True,'used_original_illustrations':60,'reused_instructor_poses':3,'duration':86.23333333333333,'frame_count':2587,'video_sha256':h},indent=2))
files=[]
for f in P.rglob('*'):
 if not f.is_file():continue
 r=f.relative_to(P)
 if any(x in ['node_modules','.browser','.hyperframes','__pycache__']or x.startswith(('review','encoded-review'))for x in r.parts)or f.name in ['premaster.wav','mix-building.wav','index-review.html','plan_visuals.py','finish_plan.py']or f.suffix=='.pyc':continue
 files.append(f)
known={str(f.relative_to(P))for f in files}
for s in re.findall(r'src=["\']([^"\']+)',(P/'index.html').read_text()):
 if s.startswith('assets/'):assert s in known,s
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for f in sorted(files):z.write(f,Path('Brainwave-Besties')/f.relative_to(P))
with zipfile.ZipFile(out)as z:
 assert z.testzip()is None
 assert hashlib.sha256(z.read('Brainwave-Besties/renders/Brainwave-Besties.mp4')).hexdigest()==h
print(json.dumps({'files':len(files),'zip_bytes':out.stat().st_size,'matching_video_sha256':h,'used_original_illustrations':60}))
