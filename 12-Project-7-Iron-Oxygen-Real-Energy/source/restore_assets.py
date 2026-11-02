#!/usr/bin/env python3
"""Restore original working PNGs and byte-identical WAV tracks from bundled lossless FLAC files."""
from pathlib import Path
import base64,hashlib,json,os,shutil,subprocess,tempfile
ROOT=Path(__file__).resolve().parent

def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as source:
  for block in iter(lambda:source.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def main():
 if not shutil.which('ffmpeg'):raise SystemExit('Install FFmpeg (already required by this project), then run python restore_audio.py again.')
 manifest=json.loads((ROOT/'LOSSLESS-COMPRESSION.json').read_text())
 for item in manifest['audio']:
  dest=ROOT/item['original_path'];encoded=ROOT/item['flac_path']
  if dest.exists():
   if sha(dest)==item['original_sha256']:
    print('Already restored:',item['original_path']);continue
   raise SystemExit('Existing WAV differs; preserve your edit and do not overwrite it: '+str(dest))
  if sha(encoded)!=item['flac_sha256']:raise SystemExit('Compressed audio checksum mismatch: '+str(encoded))
  dest.parent.mkdir(parents=True,exist_ok=True)
  fd,name=tempfile.mkstemp(prefix=dest.name+'.',suffix='.restore',dir=dest.parent);temp=Path(name)
  try:
   process=subprocess.Popen(['ffmpeg','-v','error','-i',str(encoded),'-map','0:a:0','-f',item['pcm_format'],'-c:a','pcm_'+item['pcm_format'],'-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   count=0
   with os.fdopen(fd,'wb') as out:
    out.write(base64.b64decode(item['wav_prefix_base64']))
    for block in iter(lambda:process.stdout.read(1024*1024),b''):out.write(block);count+=len(block)
    out.write(base64.b64decode(item['wav_suffix_base64']))
   error=process.stderr.read().decode(errors='replace');code=process.wait()
   if code or count!=item['pcm_bytes']:raise RuntimeError('Audio decoding failed: '+error)
   if sha(temp)!=item['original_sha256']:raise RuntimeError('Restored WAV checksum mismatch: '+item['original_path'])
   temp.replace(dest);print('Restored exactly:',item['original_path'])
  finally:
   if temp.exists():temp.unlink()
 for item in manifest.get('images',[]):
  from PIL import Image
  dest=ROOT/item['original_path'];encoded=ROOT/item['encoded_path']
  def pixels(path):
   with Image.open(path) as image:return list(image.size),hashlib.sha256(image.convert('RGBA').tobytes()).hexdigest()
  if dest.exists():
   if pixels(dest)==(item['size'],item['rgba_sha256']):
    print('Already restored:',item['original_path']);continue
   raise SystemExit('Existing PNG differs; preserve your edit and do not overwrite it: '+str(dest))
  if sha(encoded)!=item['encoded_sha256']:raise SystemExit('Compressed image checksum mismatch: '+str(encoded))
  dest.parent.mkdir(parents=True,exist_ok=True)
  fd,name=tempfile.mkstemp(prefix=dest.name+'.',suffix='.restore',dir=dest.parent);os.close(fd);temp=Path(name)
  try:
   with Image.open(encoded) as image:image.convert(item['mode']).save(temp,format='PNG',compress_level=1)
   if pixels(temp)!=(item['size'],item['rgba_sha256']):raise RuntimeError('Restored PNG pixels differ: '+item['original_path'])
   temp.replace(dest);print('Restored pixels exactly:',item['original_path'])
  finally:
   if temp.exists():temp.unlink()
 print('Original working assets restored: byte-identical WAVs and pixel-identical PNGs. Follow the normal project README.')

if __name__=='__main__':main()
