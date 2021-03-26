from genshin.rewards import RewardConfig
from typing import Dict, List
from genshin.textmap import LocalizeAdapter, Localizable
from genshin.adapter import Adapter, IdAdapter, JsonAdapter, MappedAdapter
from genshin.items import MaterialConfig, ArtifactConfig
from genshin.items import ItemStack


class Achievement(LocalizeAdapter):
    id = Adapter("Id", int)
    times = Adapter("Progress", int)

    title = Adapter("TitleTextMapHash", Localizable)
    desc = Adapter("DescTextMapHash", Localizable)

    reward = IdAdapter("FinishReward", RewardConfig)

    def __repr__(self) -> str:
        return f"<{self.id} {self.title.localize()}>"


class AchievementConfig(MappedAdapter[Achievement]):
    pass
