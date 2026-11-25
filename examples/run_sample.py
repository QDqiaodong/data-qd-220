import json
from pathlib import Path
from isotope_clusters import process
p=Path(__file__).parents[1]/"fixtures"/"input.json"
print(json.dumps(process(json.loads(p.read_text())),indent=2))
