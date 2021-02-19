from typing import Dict, List
from genshin.enums.attr_type import ArtiAttrType
from .adapter import Adapter, JsonAdapter, MappedAdapter


class MainDepot(JsonAdapter):
    id: Adapter("Id", int)
    depot_id: Adapter("PropDepotId", int)
    prop_type: Adapter("PropType", ArtiAttrType)
    affix: Adapter("AffixName")
    weight: Adapter("Weight", int)

    def __repr__(self) -> str:
        return f"<{self.prop_type.name} {self.weight}>"


class AppendDepot(JsonAdapter):
    id: Adapter("Id", int)
    depot_id: Adapter("DepotId", int)
    group_id: Adapter("GroupId", int)
    prop_type: Adapter("PropType", ArtiAttrType)
    prop_value: Adapter("PropValue", float)
    weight: Adapter("Weight", int)
    upgrade_weight: Adapter("UpgradeWeight", int)

    def __repr__(self) -> str:
        return f"<{self.prop_type.name} {self.weight} {self.prop_value:.2f}>"


class MainDepots(MappedAdapter[List[MainDepot]]):
    def __init__(self, entry: List[Dict]) -> None:
        self.mappings: Dict[int, List[MainDepot]] = {}
        self.entries = [MainDepot(x) for x in entry]
        for x in self.entries:
            if x.depot_id not in self.mappings:
                self.mappings[x.depot_id] = []
            if x.weight is not None:
                self.mappings[x.depot_id].append(x)
        self.__class__.__inst__ = self


class AppendDepots(MappedAdapter[List[AppendDepot]]):
    def __init__(self, entry: List[Dict]) -> None:
        self.mappings: Dict[int, List[AppendDepot]] = {}
        self.entries = [AppendDepot(x) for x in entry]
        for x in self.entries:
            if x.depot_id not in self.mappings:
                self.mappings[x.depot_id] = []
            self.mappings[x.depot_id].append(x)
        self.__class__.__inst__ = self
