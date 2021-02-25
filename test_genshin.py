from genshin.enums.target import EquipPart
from genshin.enums.item_type import MaterialType
from genshin.genshin import RepoData
import datetime

repo = RepoData("./GenshinData", lang="EN", encoding="utf8")
now = datetime.datetime.now()

for x in repo.avatar_codex:
    print(f"{x.avatar}: {x.time - now}")
