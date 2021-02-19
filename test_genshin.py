from genshin.enums.target import EquipPart
from genshin.enums.item_type import MaterialType
from genshin.genshin import RepoData

repo = RepoData("./GenshinData", lang="ZHS")


for x in repo.rewards.entries:
    print(x.id)
    print(x.items)
