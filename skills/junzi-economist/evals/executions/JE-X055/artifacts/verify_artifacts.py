import csv, hashlib, json, sys
from pathlib import Path
import numpy as np

root=Path(__file__).resolve().parent
names=['response.md','provenance.json','summary.json','nfxp_starts.json','ccp_starts.json','alternative_search.csv','independent_verification.json','compact_arrays.npz','simulated_panel.csv','run_model.py','independent_verify.py']
checks={n:(root/n).is_file() and (root/n).stat().st_size>0 for n in names}
summary=json.loads((root/'summary.json').read_text(encoding='utf-8'))
verify=json.loads((root/'independent_verification.json').read_text(encoding='utf-8'))
json.loads((root/'provenance.json').read_text(encoding='utf-8'))
with (root/'alternative_search.csv').open(encoding='utf-8-sig') as f: alt_rows=sum(1 for _ in csv.DictReader(f))
with (root/'simulated_panel.csv').open(encoding='utf-8-sig') as f: panel_rows=sum(1 for _ in csv.DictReader(f))
arr=np.load(root/'compact_arrays.npz')
checks.update({'independent_pass':verify['pass'] is True,'alt_row_reconciliation':alt_rows==summary['restricted_alternative_search']['evaluations']==378,'panel_row_reconciliation':panel_rows==summary['sample']['rows']==15750,'singular_value_roundtrip':np.max(np.abs(arr['singular_values']-summary['population_local_rank_evidence']['singular_values']))<1e-14,'response_mentions_local_only':'local evidence only' in (root/'response.md').read_text(encoding='utf-8')})
checks={k:bool(v) for k,v in checks.items()}
hashes={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
result={'pass':all(checks.values()),'checks':checks,'sha256':hashes}
print(json.dumps(result,indent=2))
if not result['pass']: sys.exit(1)
