from pathlib import Path
import json
P=Path(__file__).parent;S=json.loads((P/'full-storyboard.json').read_text());cues=[];last=-10
for i,a in enumerate(sorted(S['actors'],key=lambda x:x['cue'])):
 t=a['cue']+.09
 if t-last<.44:continue
 if a['parent']:id=['B15','B16','A11','B08'][i%4];level=-17.5;why='Detail emerges from '+a['parent']
 elif a['max_height']>=700:id=['B20','B31','O01'][i%3];level=-18.5;why='Character or scene arrival: '+a['id']
 else:id=['B02','B27','B18'][i%3];level=-19;why='Supporting prop resolves: '+a['id']
 cues.append([t,id,level,why]);last=t
for g in S['guides']:cues.append([g['start']+.13,'B06',-20,'Instruction guide arrives'])
cues.extend([[51.64,'B02',-18,'Finite muscle contraction'],[62.04,'B02',-22,'Axon signal begins'],[63.84,'C14',-22,'Neural pathway resolves'],[73.02,'C18',-23,'Horoscope excuse rejected'],[93.04,'C20',-18,'Hip-fracture diagram emphasis'],[112.00,'C14',-20,'Leg-day closing resolution']])
cues=sorted(cues);(P/'sound-plan.json').write_text(json.dumps(cues,indent=2));print(len(cues),'motivated sound cues')
