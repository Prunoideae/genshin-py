from __future__ import annotations
from typing import Union
import genshin.items as items
from datetime import datetime


class ItemStack():

    def __init__(self, Id, Count: int) -> None:
        self.__id__ = Id
        self.count = Count

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

    def __eq__(self, o: 'ItemStack') -> bool:
        return self.__id__ == o.__id__ and self.count == o.count


class WeightedItemStack(ItemStack):
    def __init__(self, id, count: int, weight: int) -> None:
        super().__init__(id, count)
        self.weight = weight


def genshin_datetime(s: str) -> Union[datetime, None]:
    try:
        d, t = s.split(' ')
        Y, M, D = d.split('-')
        h, m, s = t.split(':')
        return datetime(Y, M, D, h, m, s)
    except:
        return None
