from pathlib import Path
import json,zipfile,hashlib,shutil
P=Path(__file__).parent;OUT=P.parent
A=json.loads((P/'asset-plan.json').read_text());S=json.loads((P/'storyboard.json').read_text());C=json.loads((P/'sound-cues.json').read_text());E=json.loads((P/'audio-edits.json').read_text())
used={s['asset'] for s in S};graphics={a['path'] for a in A if a['id'] in used};sfx={c['path'] for c in C}
assert len({hashlib.sha256((P/f).read_bytes()).hexdigest() for f in graphics})>=60
assert all(c['tail_preserved'] for c in C)
probe=json.loads((P/'production/export-verification.json').read_text());assert probe['full_decode_passed'] and probe['frame_count']==round(E['video_duration']*30)
checks={n:json.loads((P/('production/'+n+'.json')).read_text()) for n in ['runtime-validation','layout-inspection','lint','pointer-audit']}
assert all(checks[n]['ok'] for n in ['runtime-validation','layout-inspection','lint']) and checks['pointer-audit']['passed']
video=P/'renders/Fasting-Self-Recycling.mp4';h=hashlib.sha256(video.read_bytes()).hexdigest()
report=dict(video_sha256=h,original_audio_seconds=E['original_duration'],snapped_audio_seconds=E['duration'],video_seconds=E['video_duration'],distinct_principal_art=len(graphics),illustration_appearances=len(S),caption_phrases=len(json.loads((P/'captions.json').read_text())),sound_cues=len(C),unique_sounds=len({x['source'] for x in C}),all_effect_tails_preserved=True,full_decode_passed=True,frame_count=probe['frame_count'],runtime_validation=True,layout_issues=checks['layout-inspection']['issueCount'],lint_errors=checks['lint']['errorCount'],lint_warnings=checks['lint']['warningCount'],pointer_max_error_px=checks['pointer-audit']['max_error_px'])
(P/'production/quality-report.json').write_text(json.dumps(report,indent=2))
(P/'asset-inventory.json').write_text(json.dumps([dict(a,sha256=hashlib.sha256((P/a['path']).read_bytes()).hexdigest()) for a in A if a['id'] in used],indent=2))
(P/'storyboard.md').write_text('# Fasting — Self Recycling\n\n| Start | Handoff | Illustration | Route |\n|---:|---:|---|---|\n'+'\n'.join(f'| {s["start"]:.2f} | {s["handoff"]:.2f} | {s["asset"]} | {s["route"]} |' for s in S))
skip={'PACKAGE-MANIFEST.json','make_plan.py','configure_composition.py','prepare_audio.py','transcribe_once.py','index-review.html','premaster.wav','voice-normalized.wav'}
files=[]
for f in sorted(P.rglob('*')):
 if not f.is_file():continue
 r=f.relative_to(P);st=r.as_posix()
 if any(x.startswith('.') or x=='node_modules' for x in r.parts) or r.name in skip or r.suffix=='.jpg':continue
 if st.startswith('production/review/'):continue
 if st.startswith('assets/graphics/') and st not in graphics:continue
 if st.startswith('assets/sfx/') and st not in sfx and r.name!='Manifest.json':continue
 files.append(f)
manifest=[dict(path=str(f.relative_to(P)),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in files]
(P/'production/PACKAGE-MANIFEST.json').write_text(json.dumps(manifest,indent=2));files=[f for f in files if f.name!='PACKAGE-MANIFEST.json']+[P/'production/PACKAGE-MANIFEST.json']
out=OUT/'Fasting-Self-Recycling-Project.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in files:z.write(f,'Fasting-Self-Recycling/'+f.relative_to(P).as_posix())
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 assert hashlib.sha256(z.read('Fasting-Self-Recycling/renders/Fasting-Self-Recycling.mp4')).hexdigest()==h
 print('Verified project',len(z.namelist()),'files',out.stat().st_size,'bytes')
shutil.copyfile(video,OUT/'Fasting-Self-Recycling.mp4');print('Matching MP4',h)
