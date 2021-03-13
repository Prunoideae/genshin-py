from typing import Dict, List
from genshin.adapter import Adapter, JsonAdapter, MappedAdapter
from genshin.items import MaterialConfig, ArtifactConfig
from genshin.items import ItemStack


class Reward(JsonAdapter):
    id = Adapter("RewardId", int)
    items = Adapter("RewardItemList", List[ItemStack], lambda x: [y for y in x if y])

    def __init__(self, entry: Dict) -> None:
        super().__init__(entry)
        self.items = [ItemStack(x["ItemId"], x["ItemCount"]) for x in self.items]


class RewardConfig(MappedAdapter[Reward]):
    def __init__(self, entries: List[Dict]) -> None:
        super().__init__(entries, additional=[])
