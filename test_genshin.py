from genshin.enums.target import EquipPart
from genshin.enums.item_type import MaterialType
from genshin.genshin import RepoData

repo = RepoData("./GenshinData", lang="EN", encoding="utf8")

print([x.items for x in repo.skill[10415].upgrade_group])
