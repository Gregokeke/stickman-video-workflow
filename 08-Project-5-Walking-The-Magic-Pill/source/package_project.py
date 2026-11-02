from pathlib import Path
import json,zipfile,hashlib,sys
P=Path(__file__).parent
assets=json.loads((P/'asset-plan.json').read_text());selected={x['path'] for x in assets}
name=sys.argv[1] if len(sys.argv)>1 else 'Walking-The-Magic-Pill-Editable-Project.zip'
out=P.parent/name
excluded={'node_modules','.browser','.hyperframes','.git','.claude','.agents','.codex','renders'}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(P.rglob('*')):
  if not f.is_file():continue
  rel=f.relative_to(P)
  if any(x in rel.parts for x in excluded):continue
  if rel.parts[:2]==('production','review'):continue
  if f.suffix in ['.png','.jpg'] and rel.parts[0]=='production':continue
  if str(rel).startswith('assets/graphics/') and str(rel) not in selected:continue
  if f.name in ['plan.py','repair_export.mjs','render-gauge-revision.mjs','CLAUDE.md','AGENTS.md']:continue
  if f.name.endswith('.log') or f.name=='review-log.txt' or (rel.parts[0]=='production' and 'save' in f.name):continue
  z.write(f,str(Path('Walking-Magic-Pill')/rel))
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for f in selected:assert str(Path('Walking-Magic-Pill')/f) in z.namelist()
 print(json.dumps({'file':str(out),'size':out.stat().st_size,'entries':len(z.namelist()),'illustrations':len(selected),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
