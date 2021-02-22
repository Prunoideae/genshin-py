import json
from typing import Dict, List

excel = "./GenshinData/Excel/AvatarSkillDepotExcelConfigData.json"
j: List[Dict] = json.load(open(excel))

keys = set()
for i in j:
    for k, v in i.items():
        keys.add((k, type(v).__name__))

print("\n".join([" ".join(x) for x in keys]))
