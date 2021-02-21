from genshin.enums.target import EquipPart
from genshin.enums.item_type import MaterialType
from genshin.genshin import RepoData

repo = RepoData("./GenshinData", lang="EN", encoding="utf8")

print(repo.trialsets.match_first(lambda x: x.trials[0].avatar_data.avatar.name == "Hu Tao").trials)
