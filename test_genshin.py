
from genshin.achievements import Achievement
from genshin.enums.displays import CGType
import json
from typing import Dict, List
from genshin.rewards import Reward, RewardConfig
from genshin.tags import TagConfig
from genshin.enums.attr_type import BodyType, QualityType
from genshin.enums.target import EquipPart
from genshin.enums.item_type import MaterialType
from genshin.genshin import RepoData


repo1_4 = RepoData("./GenshinData", lang="EN", encoding="utf8")
print(repo1_4.materials[104011])