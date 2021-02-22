from genshin.skills import SkillDepotConfig
from typing import Dict, List
from genshin.enums.attr_type import BodyType, IdentityType, QualityType, UseType, WeaponType
from genshin.adapter import Adapter, ConfigAdapter, IdAdapter, JsonAdapter, MappedAdapter
from genshin.tags import TagGroup, TagGroupConfig
from genshin.textmap import Localizable, LocalizeAdapter, TextMap


class Avatar(LocalizeAdapter):
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
    feature_tags: IdAdapter("FeatureTagGroupID", TagGroupConfig)

    skill_depot: IdAdapter("SkillDepotId", SkillDepotConfig)

    def __repr__(self) -> str:
        return f"<{self.name.localize()} {self.id}>"


class AvatarConfig(MappedAdapter[Avatar]):
    pass
