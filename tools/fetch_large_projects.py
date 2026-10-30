#!/usr/bin/env python3
"""Fetch the two whole release-hosted ZIPs and verify their exact SHA-256 values."""
from pathlib import Path
import hashlib,json,os,tempfile,urllib.request
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 manifest=json.loads((R/'PACKAGE-MANIFEST.json').read_text())
 for item in manifest['files']:
  url=item.get('download_url')
  if not url:continue
  p=R/item['path']
  if p.exists():
   if p.stat().st_size==item['bytes'] and sha(p)==item['sha256']:
    print('Already verified:',item['path']);continue
   raise SystemExit('Existing file differs; move it aside before retrying: '+str(p))
  p.parent.mkdir(parents=True,exist_ok=True)
  fd,name=tempfile.mkstemp(prefix=p.name+'.',suffix='.download',dir=p.parent)
  temp=Path(name)
  try:
   h=hashlib.sha256();size=0
   print('Downloading:',item['path'],flush=True)
   with os.fdopen(fd,'wb') as target,urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Stickman-Workspace-Setup'}),timeout=120) as source:
    while block:=source.read(1024*1024):target.write(block);h.update(block);size+=len(block)
   if size!=item['bytes'] or h.hexdigest()!=item['sha256']:raise RuntimeError('Downloaded size/checksum mismatch: '+item['path'])
   temp.replace(p);print('Verified:',item['path'])
  finally:
   if temp.exists():temp.unlink()
 print('Both individual large projects are available.')
if __name__=='__main__':main()
