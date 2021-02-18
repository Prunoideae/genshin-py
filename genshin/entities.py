from typing import Dict, List
from genshin.enums.attr_type import BodyType, IdentityType, QualityType, UseType, WeaponType
from genshin.adapter import Adapter, ConfigAdapter, JsonAdapter, MappedAdapter
from genshin.tags import TagGroup, TagGroupConfig
from genshin.textmap import Localizable, TextMap


class Avatar(JsonAdapter):
    id: Adapter("Id", int)
    ranged: Adapter("IsRangeAttack", bool)

    quality: Adapter("QualityType", QualityType)
    use_type: Adapter("UseType", UseType)
    identity_type: Adapter("IdentityType", IdentityType)

    name: Adapter("NameTextMapHash", Localizable)
    desc: Adapter("DescTextMapHash", Localizable)
    info: Adapter("InfoDescTextMapHash", Localizable)

    initial_weapon: Adapter("InitialWeapon", int)

    hp_base: Adapter("HpBase", float)
    atk_base: Adapter("AttackBase", float)
    def_base: Adapter("DefenseBase", float)
    crit: Adapter("Critical", float)
    crit_dmg: Adapter("CriticalHurt", float)
    energy_recharge: Adapter("ChargeEfficiency", float)
    stamina_recover: Adapter("StaminaRecoverSpeed", float)

    body_type: Adapter("BodyType", BodyType)
    weapon_type: Adapter("WeaponType", WeaponType)
    feature_tags: Adapter("FeatureTagGroupID", TagGroup, lambda x: x)

    def __init__(self, entry: Dict, textmap: TextMap, tag_group: TagGroupConfig) -> None:
        super().__init__(entry)
        self.feature_tags = tag_group.mappings[self.feature_tags]
        self.name.set(textmap)
        self.desc.set(textmap)
        self.info.set(textmap)

    def __repr__(self) -> str:
        return f"<{self.name.localize()} {self.id}>"


class AvatarConfig(MappedAdapter[Avatar]):
    def __init__(self, entries: List[Dict], textmap: TextMap, tag_group: TagGroupConfig) -> None:
        super().__init__(entries, additional=[textmap, tag_group])
