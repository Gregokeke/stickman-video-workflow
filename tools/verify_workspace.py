#!/usr/bin/env python3
"""Verify all current bytes, ZIP integrity, and seven embedded/outside video pairs."""
from pathlib import Path
import hashlib,json,sys,zipfile
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 errors=[];m=json.loads((R/'PACKAGE-MANIFEST.json').read_text())
 for i in m['files']:
  p=R/i['path']
  if not p.is_file():errors.append('Missing: '+i['path']+'; run python3 tools/fetch_large_projects.py for release downloads');continue
  with p.open('rb') as f:prefix=f.read(100)
  if prefix.startswith(b'version https://git-lfs.github.com/spec/v1'):errors.append('Unexpected pointer; fetch real project bytes: '+i['path']);continue
  if p.stat().st_size!=i['bytes'] or sha(p)!=i['sha256']:errors.append('Size/checksum mismatch: '+i['path'])
 if errors:print('\n'.join(errors),file=sys.stderr);return 1
 archives=[R/i['path'] for i in m['files'] if i['path'].endswith('.zip')]
 for p in archives:
  with zipfile.ZipFile(p) as z:
   bad=z.testzip()
   if bad:errors.append('Corrupt ZIP member: '+str(p)+' / '+bad)
 pairs=json.loads((R/'PROJECT-RENDERS-INDEX.json').read_text())
 if sorted(i['reference'] for i in pairs)!=list(range(1,8)):errors.append('Expected seven project/render pairs')
 for i in pairs:
  with zipfile.ZipFile(R/i['project']) as z:
   h=hashlib.sha256()
   with z.open(i['render_path']) as f:
    for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
  if h.hexdigest()!=i['sha256'] or sha(R/i['external_render'])!=i['sha256']:errors.append('Render mismatch: '+str(i['reference']))
 if (R/'04-Workflow-and-Animation/Stickman Animations Workflow.md').exists():errors.append('Duplicate standalone workflow')
 if errors:print('\n'.join(errors),file=sys.stderr);return 1
 print(f"Verified {len(m['files'])} files, {len(archives)} ZIPs and all seven embedded/outside render pairs.")
 return 0
if __name__=='__main__':raise SystemExit(main())
