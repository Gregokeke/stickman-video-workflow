from pathlib import Path
import json,zipfile,re,hashlib,shutil
P=Path(__file__).parent;ROOT=P.parent;NAME='Kiwi-Small-Fruit-Big-Attitude'
video=P/'renders'/f'{NAME}.mp4';assert video.is_file()
h=json.load(open(P/'production/hyperframes-check.json'));assert h['ok'] and not h['browserSkipped']
v=json.load(open(P/'production/export-verification.json'));assert v['full_decode_passed'] and v['frame_count']==3438
au=json.load(open(P/'production/audio-export-verification.json'));assert au['passed']
S=json.load(open(P/'storyboard.json'));used={x['asset']for x in S};assert len(used)>=75
for x in S:assert 0<=x['start']<x['handoff']<=x['end']<=114.6
text=(P/'index.html').read_text();refs=set(re.findall(r'(?:src=["\']|url\()([^"\'\)]+)',text))
for r in refs:assert not r.startswith(('http:','https:')) and (P/r).is_file(),r
base=['index.html','DESIGN.md','README.md','SFX-CREDITS.md','requirements.txt','package.json','package-lock.json','build.py','animation.js','revision-motion.js','micro.html','micro.css','micro.js','prepare_audio.py','transcribe.py','mix_audio.py','sound-plan.json','build-sound-plan.py','render.mjs','browser-path.mjs','review.mjs','audit-safe.mjs','audit-revision.mjs','verify_audio.py','package_project.py','script.txt','words.json','source-words.json','transcript.json','captions.json','audio-edits.json','storyboard.json','storyboard.md','sound-cues.json','asset-sources.json','asset-plan.json','asset-inventory.json']
files={P/n for n in base};files|={P/'assets/graphics'/f'{a}.png' for a in used}
for folder in ['assets/fonts','assets/vendor','assets/sfx','references']:
 files|={f for f in(P/folder).rglob('*')if f.is_file()}
for n in ['source-narration.mp3','narration.wav','effects.wav','mix.wav']:files.add(P/'assets/audio'/n)
for n in ['export-verification.json','final-media.json','hyperframes-check.json','audio-mastering.json','audio-export-verification.json','production-notes.json','SCIENTIFIC-NOTES.md','REFERENCE-STUDY.md','final-schedule.json','safe-area-main.json','FINAL-VERIFICATION.json','generation-prompts.md','review-final.json','review-polish.json','continuity-review.json','check-summary.json','REVISION-24-FIXES.md','revision-verification.json']:
 files.add(P/'production'/n)
files.add(video)
for f in files:assert f.is_file(),f
manifest=[dict(path=str(f.relative_to(P)),size=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest())for f in sorted(files)]
f=P/'production/PACKAGE-MANIFEST.json';f.write_text(json.dumps(manifest,indent=2));files.add(f)
out=ROOT/f'{NAME}-Project.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for f in sorted(files):z.write(f,Path(NAME)/f.relative_to(P))
with zipfile.ZipFile(out)as z:
 assert z.testzip()is None
 assert hashlib.sha256(z.read(f'{NAME}/renders/{NAME}.mp4')).digest()==hashlib.sha256(video.read_bytes()).digest()
 for r in refs:assert f'{NAME}/{r}'in z.namelist(),r
shutil.copy2(video,ROOT/f'{NAME}.mp4');print(json.dumps(dict(files=len(files),distinct_used_illustrations=len(used),verified_media_dependencies=len(refs),zip_bytes=out.stat().st_size,video_bytes=video.stat().st_size,matching_embedded_render=True),indent=2))
