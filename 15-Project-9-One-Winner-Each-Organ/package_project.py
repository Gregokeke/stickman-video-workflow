from pathlib import Path
import json,zipfile,hashlib,shutil,sys
P=Path(__file__).parent;OUT=P.parent;checkpoint='--checkpoint' in sys.argv
A=json.loads((P/'asset-plan.json').read_text());S=json.loads((P/'storyboard.json').read_text());C=json.loads((P/'sound-cues.json').read_text());E=json.loads((P/'audio-edits.json').read_text());used={s['asset'] for s in S};graphics={a['path'] for a in A if a['id'] in used};sfx={c['path'] for c in C}
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert len({sha(P/f) for f in graphics})>=80
assert all(c['tail_preserved'] for c in C)
video=P/'renders/One-Winner-Each-Organ.mp4'
if not checkpoint:
 probe=json.loads((P/'production/export-verification.json').read_text());assert probe['full_decode_passed'] and probe['frame_count']==round(E['video_duration']*30) and probe['distinctIllustrations']>=80
 checks={n:json.loads((P/('production/'+n+'.json')).read_text()) for n in ['runtime-validation','layout-inspection','lint','pointer-audit','animation-map']}
 assert all(checks[n]['ok'] for n in ['runtime-validation','layout-inspection','lint']) and checks['pointer-audit']['passed']
 assert not checks['animation-map']['collisions'] and not checks['animation-map']['outOfFrame'] and not checks['animation-map']['missing']
 report=dict(video_sha256=sha(video),original_audio_seconds=E['original_duration'],snapped_audio_seconds=E['duration'],video_seconds=E['video_duration'],distinct_principal_art=len(graphics),illustration_appearances=len(S),caption_phrases=len(json.loads((P/'captions.json').read_text())),sound_cues=len(C),unique_sounds=len({x['source'] for x in C}),all_effect_tails_preserved=True,full_decode_passed=True,frame_count=probe['frame_count'],runtime_validation=True,layout_issues=checks['layout-inspection']['issueCount'],settled_collisions=0,pointer_max_error_px=checks['pointer-audit']['max_error_px'])
 (P/'production/quality-report.json').write_text(json.dumps(report,indent=2))
(P/'asset-inventory.json').write_text(json.dumps([dict(a,sha256=sha(P/a['path'])) for a in A if a['id'] in used],indent=2))
(P/'storyboard.md').write_text('# One Winner for Each Organ\n\n| Start | Handoff | Illustration | Route |\n|---:|---:|---|---|\n'+'\n'.join(f'| {s["start"]:.2f} | {s["handoff"]:.2f} | {s["asset"]} | {s["route"]} |' for s in sorted(S,key=lambda a:a['start'])))
skip={'PACKAGE-MANIFEST.json','expand80.py','make_story.py','make_captions.py','prepare_audio.py','transcribe_once.py','index-review.html','decoded.wav','premaster.wav','voice-normalized.wav'}
files=[]
for f in sorted(P.rglob('*')):
 if not f.is_file():continue
 r=f.relative_to(P);st=r.as_posix()
 if any(x.startswith('.') or x=='node_modules' for x in r.parts) or r.name in skip or r.suffix=='.jpg':continue
 if st.startswith('production/review/'):continue
 if st.startswith('assets/graphics/') and st not in graphics:continue
 if st.startswith('assets/sfx/') and st not in sfx and r.name!='Manifest.json':continue
 if checkpoint and st.startswith('renders/'):continue
 files.append(f)
manifest=[dict(path=str(f.relative_to(P)),bytes=f.stat().st_size,sha256=sha(f)) for f in files]
(P/'production/PACKAGE-MANIFEST.json').write_text(json.dumps(manifest,indent=2));files+=[P/'production/PACKAGE-MANIFEST.json']
out=OUT/'One-Winner-Each-Organ-Project.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in files:z.write(f,'One-Winner-Each-Organ/'+f.relative_to(P).as_posix())
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 if not checkpoint:assert hashlib.sha256(z.read('One-Winner-Each-Organ/renders/One-Winner-Each-Organ.mp4')).hexdigest()==sha(video)
 print('Verified project',len(z.namelist()),'files',out.stat().st_size,'bytes')
if not checkpoint:shutil.copyfile(video,OUT/'One-Winner-Each-Organ.mp4');print('Matching MP4',sha(video))
