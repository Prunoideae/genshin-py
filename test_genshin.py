from genshin.enums.target import EquipPart
from genshin.enums.item_type import MaterialType
from genshin.genshin import RepoData

repo = RepoData("./GenshinData", lang="EN", encoding="utf8")

for x in repo.bp_mission.match(lambda x: x.schedule.id == 1300 if x.schedule else False):
    print(x.activity, x.desc.localize())
