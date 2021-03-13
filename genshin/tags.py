from typing import Dict, List
from genshin.adapter import Adapter, ConfigAdapter, JsonAdapter, MappedAdapter


class Tag(JsonAdapter):
    id = Adapter("TagID", int)
    name = Adapter("TagName")
    desc = Adapter("TagDesp")

    def __repr__(self) -> str:
        return f"<{self.id} {self.name}>"


class TagConfig(MappedAdapter[Tag]):
    pass


class TagGroup(JsonAdapter):
    id = Adapter("GroupID", int)
    tags = Adapter("TagIDs", List[Tag], lambda x: [y for y in x if y != 0])

    def __init__(self, entry: Dict, tags: TagConfig) -> None:
        super().__init__(entry)
        self.tags = [tags.mappings[x] for x in self.tags]

    def __repr__(self) -> str:
        return self.tags.__repr__()


class TagGroupConfig(MappedAdapter[TagGroup]):
    def __init__(self, entries: List[Dict], tags: TagConfig) -> None:
        super().__init__(entries, [tags])
