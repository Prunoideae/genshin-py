# For gliders, and (possibly) incoming skins
from genshin.adapter import Adapter, IdAdapter, MappedAdapter
from genshin.textmap import Localizable, LocalizeAdapter
from genshin.items import MaterialConfig


class WindGlider(LocalizeAdapter):
    id = Adapter("FlycloakId", int)
    name = Adapter("NameTextMapHash", Localizable)
    desc = Adapter("DescTextMapHash", Localizable)
    json = Adapter("JsonName")
    item = IdAdapter("MaterialId", MaterialConfig)


class WindGliderConfig(MappedAdapter[WindGlider]):
    pass
