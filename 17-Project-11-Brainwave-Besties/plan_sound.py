from pathlib import Path
import json
P=Path(__file__).parent;S=json.load(open(P/'storyboard.json'));W=json.load(open(P/'words.json'));C=[];wh=['O01','B20','B06','B31','B36'];pl=['B08','B15','B16','A11','B18']
for i,s in enumerate(S):
 if s['route']=='presenter':C.append([s['start']+.04,'B06',-20,s['id']+' entrance']);continue
 if s['id'] in ['glance-right','mirror-follower','emotion-masks','sentence-bubbles','empathy-comfort']:continue
 person='stickman' in s['description'].lower() and 'no human' not in s['description'].lower()
 C.append([round(s['start']+.04,5),wh[i%5]if person else pl[i%5],-14.5 if person else -17,s['id']+' arrival'])
for i,id,gain,why in [(15,'C14',-20,'Wireless sync'),(27,'C12',-20,'Shared brain-cell joke'),(43,'B02',-21,'Sentence recognition'),(51,'C18',-23,'Unhinged glance'),(58,'C12',-22,'Shared laugh reaction'),(71,'A02',-20,'Cancellation stamp contact'),(84,'B27',-21,'Rhythms align'),(100,'B02',-22,'Leader gesture'),(102,'B02',-22,'Follower matches'),(128,'B27',-21,'Schematic matched spikes'),(139,'B27',-21,'Same-time emphasis'),(151,'B02',-22,'Decision fork'),(157,'C18',-21,'Terrible choices reversal'),(185,'B36',-24,'Echo chamber'),(194,'B19b',-24,'Serious warning'),(202,'B02',-21,'Choose company'),(216,'B27',-20,'Zero ambition'),(220,'C18',-23,'Negated casual interpretation'),(229,'B13',-22,'Download process'),(231,'C20',-21,'Broken wiring metaphor'),(235,'B27',-23,'Network rewrite'),(241,'B19b',-24,'Closing emphasis')]:C.append([W[i]['start'],id,gain,why])
C[0][1]='B15';C[0][2]=-18;C.sort(key=lambda c:c[0]);(P/'sound-plan.json').write_text(json.dumps(C,indent=2));print(len(C),'motivated sound cues')
