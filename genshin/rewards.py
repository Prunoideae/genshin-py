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

    def __eq__(self, o: 'Reward') -> bool:
        a = self.items.copy()
        a.sort(key=lambda x: x.__id__)
        b = o.items.copy()
        b.sort(key=lambda x: x.__id__)
        return all(x == y for x, y in zip(a, b))


class RewardConfig(MappedAdapter[Reward]):
    def __init__(self, entries: List[Dict]) -> None:
        super().__init__(entries, additional=[])
