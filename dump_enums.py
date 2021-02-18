import json
from glob import glob
path = "./GenshinData/Excel/*.json"

r = set()
for path in glob(path):
    j = json.load(open(path))
    k = "DragType"
    for i in j:
        if k in i:
            r.add(i[k])
for i in r:
    print(i + "=\"" + i + "\"")
