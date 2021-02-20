from genshin.enums.target import EquipPart
from genshin.enums.item_type import MaterialType
from genshin.genshin import RepoData

repo = RepoData("./GenshinData")


for x in repo.bp_mission.match(lambda x: x.schedule is not None and x.schedule.id == 1300):
    print(str(x.exp) + " " + x.desc.localize())
