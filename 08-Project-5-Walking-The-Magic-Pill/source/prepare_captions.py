from pathlib import Path
import json,re
P=Path(__file__).parent
raw=json.loads((P/'words.json').read_text());words=[]
for w in raw:
 t=w['word']
 if words and (t.startswith(',') and t[1:].replace(',','').isdigit() or t in ['%','-fold','-smokers']):
  words[-1]['word']+=t;words[-1]['end']=w['end']
 else:words.append(dict(w))
for w in words:
 if w['word']=='track':w['word']='tracked'
 if w['word']=='big':w['word']='Big'
 if w['word']=='pharma':w['word']='Pharma'
groups=[];current=[]
for i,w in enumerate(words):
 current.append(w)
 nxt=words[i+1] if i+1<len(words) else None
 if len(current)>=5 or re.search(r'[.!?,]$',w['word']) or nxt is None or nxt['start']-w['end']>.16:
  groups.append(dict(text=' '.join(x['word'] for x in current),start=current[0]['start'],end=current[-1]['end']));current=[]
for i,g in enumerate(groups):g['end']=min(groups[i+1]['start'] if i+1<len(groups) else 124.81575,g['end']+.07)
(P/'captions.json').write_text(json.dumps(groups,indent=2));(P/'words.json').write_text(json.dumps(words,indent=2));(P/'script.txt').write_text(' '.join(w['word'] for w in words))
scenes=json.loads((P/'storyboard.json').read_text())
for s in scenes:
 s['exact_phrase']=' '.join(w['word'] for w in words if w['start']<s['end'] and w['end']>s['start'])
 s['last_relevant_time']=s['end']
(P/'storyboard.json').write_text(json.dumps(scenes,indent=2))
lines=['# Phrase-level storyboard','', '| Time | Exact recorded phrase | Illustration | Role | Handoff |','|---|---|---|---|---|']
for s in scenes:lines.append(f"| {s['start']:.2f}–{s['end']:.2f} | {s['exact_phrase']} | {s['asset']} | {s['role']} | {s['handoff']} |")
(P/'storyboard.md').write_text('\n'.join(lines)+'\n');print(len(groups),'caption groups')
