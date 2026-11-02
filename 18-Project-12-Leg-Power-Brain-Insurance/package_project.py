from pathlib import Path
import json,hashlib,zipfile
P=Path(__file__).resolve().parent
O=P.parents[2]/'Leg-Power-Brain-Insurance-Project.zip'
video=P/'renders/Leg-Power-Brain-Insurance.mp4'
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
A=json.loads((P/'production/all-generated-art.json').read_text());assert len(A)==76
for a in A:assert h(P/a['path'])==a['sha256']
V=json.loads((P/'production/final-audio-verification.json').read_text());assert V['full_video_complete']
E=json.loads((P/'production/export-verification.json').read_text());assert E['full_decode_passed'] and E['frame_count']==3390
B=json.loads((P/'full-storyboard-built.json').read_text());assert B['duration']==113 and len({a['asset']for a in B['actors']})==76
for file in ['full-video-plan.json']:
 p=P/file;x=json.loads(p.read_text());x['full_video_complete']=True;p.write_text(json.dumps(x,indent=2)+'\n')
status=dict(full_video_complete=True,duration_seconds=113,original_illustrations=76,appearances=77,caption_phrases=79,voiceover_words=332,video_sha256=h(video),video_bytes=video.stat().st_size)
(P/'production/full-status.json').write_text(json.dumps(status,indent=2)+'\n')
exclude={'node_modules','.browser','.hyperframes','review-full','review-focus','__pycache__'}
exclude_files={'CHECKPOINT-STATUS.md','pending-generation-prompts.json','package_full_checkpoint.py','render_progress.mjs','verify_progress.py','progress-mix.wav','premaster.wav','resume-state.json','narration-and-progress-verification.json','hyperframes-lint.json','hyperframes-layout.json','hyperframes-lint-progress.json','hyperframes-layout-progress.json'}
files=[]
for p in sorted(P.rglob('*')):
 rel=p.relative_to(P)
 if not p.is_file()or any(k in exclude or k.startswith('.')for k in rel.parts)or p.name in exclude_files:continue
 if rel.parts[0]=='renders'and p!=video:continue
 if rel.parts[0]=='production'and p.suffix.lower()in {'.jpg','.png'}:continue
 files.append(p)
with zipfile.ZipFile(O,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in files:z.write(p,P.name+'/'+str(p.relative_to(P)))
with zipfile.ZipFile(O)as z:
 assert not z.testzip()
 assert hashlib.sha256(z.read(P.name+'/renders/'+video.name)).hexdigest()==h(video)
 assert len([n for n in z.namelist()if '/assets/graphics/'in n and n.endswith('.png')])==76
print(json.dumps(dict(zip=str(O),bytes=O.stat().st_size,files=len(files),matching_embedded_video=True,sha256=h(O)),indent=2))
