import json
from pathlib import Path
p=Path(__file__).parent;S=json.load(open(p/'storyboard.json'));C=[]
# Deliberately select substantial entrances, not every secondary prop.
whooshes=['O01','B20','B31','B36','B06']; pops=['B15','B18','B16','B08','A11'];exclude={'boxer-bottom','e-question','oxidation-negated','p-fiber','p-trial','p-sleep','p-protein','p-dna','p-membrane','heart-calm','water-drop','medal','moon','calendar','meal-light','sassy-appearance'}
for i,s in enumerate(S):
 if s['id']in exclude or s['route']=='presenter':continue
 heavy=s['layout'][3]>650;id=whooshes[i%len(whooshes)] if heavy else pops[i%len(pops)];peak=-9 if heavy else -13
 if s['id']in ['protein','peptides','fiber-mesh','seed-oil','brain']:peak=-15
 C.append([round(s['start']+.11,3),id,peak,'arrival: '+s['phrase']])
# Action effects: matchup punch, opposing judgments, chart/flow milestones, protein cleavage.
C += [[10.19,'A02',-12,'kiwi matchup challenge'],[13.39,'B27',-17,'VS slash draws'],[14.88,'C18',-13,'referee unfair reaction'],[17.56,'B02',-18,'steady heart condition'],[19.17,'B27',-17,'DNA construction link'],[22.45,'B08',-17,'clot closes cut'],[26.35,'B02',-18,'vitamin E absence slash'],[29.55,'B19b',-18,'antioxidant shield'],[32.05,'C20',-18,'oxidative damage negated'],[37.34,'C09',-17,'seed oil trace'],[39.55,'B04',-17,'kiwi crunch'],[44.0,'B27',-18,'fiber units fill'],[46.0,'C09',-17,'water held by fiber'],[47.25,'B06',-18,'bowel flow'],[49.53,'B13',-18,'below-fiber-goal units'],[58.95,'B02',-17,'RCT assignment'],[59.80,'B19b',-18,'gold standard study'],[63.55,'B27',-18,'trial outcome bar grows'],[65.65,'C14',-17,'abdominal comfort'],[67.08,'B27',-17,'forty-minute clock advances'],[68.48,'C12',-17,'praying despair'],[69.37,'B19b',-18,'shrine punchline'],[76.03,'B08',-17,'sleep quality gauge'],[80.86,'C01',-22,'pineal synthesis mechanism'],[84.20,'B06',-16,'sleeping release'],[86.64,'B02',-18,'3AM rejected alternative'],[92.11,'B08',-18,'carb to muscle fuel'],[93.23,'B27',-18,'steady fiber line'],[99.61,'C20',-14,'protein bond cleavage'],[103.64,'C18',-14,'wet brick negation'],[104.91,'B27',-16,'cheap coins'],[110.86,'B19b',-16,'overrate them conclusion']]
C.sort();(p/'sound-plan.json').write_text(json.dumps(C,indent=2));print(len(C),'motivated cues')
