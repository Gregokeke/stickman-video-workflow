#!/usr/bin/env python3
"""Verify current bytes, ZIPs, twelve renders and expanded-reference imports."""
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
  if not p.is_file():errors.append('Missing: '+i['path']);continue
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
 if sorted(i['reference'] for i in pairs)!=list(range(1,m['reference_projects']+1)):errors.append('Expected all numbered project renders')
 for i in pairs:
  if i.get('layout')=='expanded':
   p=R/i['render_path']
   if not p.is_file() or p.stat().st_size!=i['render_size'] or sha(p)!=i['sha256']:errors.append('Expanded render mismatch: '+str(i['reference']))
  else:
   with zipfile.ZipFile(R/i['project']) as z:
    h=hashlib.sha256()
    with z.open(i['render_path']) as f:
     for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
   if h.hexdigest()!=i['sha256'] or sha(R/i['external_render'])!=i['sha256']:errors.append('Render mismatch: '+str(i['reference']))
 audit=json.loads((R/'REFERENCE-IMPORT-AUDIT.json').read_text())
 expanded={i['reference'] for i in pairs if i.get('layout')=='expanded'}
 if {i['reference'] for i in audit['projects']}!=expanded:errors.append('Expanded import audit/reference mismatch')
 imported=0;destinations=set()
 for project in audit['projects']:
  if len(project['files'])!=project['file_count']:errors.append('Import member count mismatch: '+project['name'])
  if sum(i['bytes'] for i in project['files'])!=project['total_original_bytes']:errors.append('Import byte total mismatch: '+project['name'])
  for member in project['files']:
   name=member['repository_path'];p=R/name;imported+=1
   if name in destinations:errors.append('Duplicate import destination: '+name)
   destinations.add(name)
   if not name.startswith(project['directory']+'/'):errors.append('Import path outside project: '+name)
   if not p.is_file() or p.stat().st_size!=member['bytes'] or sha(p)!=member['sha256']:errors.append('Original member mismatch: '+name)
 for i in m['files']:
  if i['bytes']>=100*1024*1024:errors.append('File at or above GitHub size limit: '+i['path'])
 if (R/'04-Workflow-and-Animation/Stickman Animations Workflow.md').exists():errors.append('Duplicate standalone workflow')
 if errors:print('\n'.join(errors),file=sys.stderr);return 1
 print(f"Verified {len(m['files'])} files, {len(archives)} ZIPs, {len(pairs)} project renders and {imported} original expanded members.")
 return 0
if __name__=='__main__':raise SystemExit(main())
