from genshin.enums.displays import CGType
from genshin.adapter import Adapter, IdAdapter, MappedAdapter
from genshin.textmap import Localizable, LocalizeAdapter


class HangoutCG(LocalizeAdapter):
    id = Adapter("Id", int)
    title = Adapter("POKEBGGOPDK", Localizable)
    desc = Adapter("EDPEJIGGCMO", Localizable)

    gender = Adapter("CgType", CGType)

    chapter = Adapter("ChapterId", int)

    def __repr__(self) -> str:
        return self.title.__repr__()


class HangoutCGConfig(MappedAdapter[HangoutCG]):
    pass
