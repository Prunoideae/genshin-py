from __future__ import annotations
from typing import Union
import genshin.items as items


class ItemStack():

    def __init__(self, id, count: int) -> None:
        self.__id__ = id
        self.count = count

    @classmethod
    def set_instance(cls, entry):
        if "__config__" not in cls.__dict__:
            cls.__config__ = []
        cls.__config__.append(entry)

    @property
    def item(self) -> Union[items.MaterialEntry, items.ArtifactEntry, items.WeaponEntry]:
        for config in self.__class__.__config__:
            if self.__id__ in config.mappings:
                return config[self.__id__]
        return None

    def __repr__(self) -> str:
        return f"<{self.item.name.localize()} {self.count}>"


class WeightedItemStack(ItemStack):
    def __init__(self, id, count: int, weight: int) -> None:
        super().__init__(id, count)
        self.weight = weight
