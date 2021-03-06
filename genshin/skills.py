from genshin.items import ItemStack
from typing import Dict, List
from genshin.enums.attr_type import ElementType
from genshin.enums.displays import DragType, LockShape
from genshin.adapter import Adapter, IdAdapter, JsonAdapter, MappedAdapter
from genshin.textmap import Localizable, LocalizeAdapter, TextMap


class SkillUpgrade(LocalizeAdapter):
    id = Adapter("ProudSkillId", int)
    group = Adapter("ProudSkillGroupId", int)
    level = Adapter("Level", int)
    skill_type = Adapter("ProudSkillType", int)

    name = Adapter("NameTextMapHash", Localizable)
    desc = Adapter("DescTextMapHash", Localizable)
    unlock = Adapter("UnlockDescTextMapHash", Localizable)
    param_desc = Adapter("ParamDescList", List[Localizable], lambda x: x)

    icon = Adapter("Icon")

    mora = Adapter("CoinCost", int)
    items = Adapter("CostItems", List[ItemStack], lambda x: [ItemStack(**y) for y in x if "Id" in y and "Count" in y])
    filter = Adapter("FilterConds", list)
    ascension = Adapter("BreakLevel", int)

    param_list = Adapter("ParamList", list)

    def __init__(self, entries: List[Dict]) -> None:
        super().__init__(entries)
        self.param_desc = [Localizable(x, TextMap.__inst__) for x in self.param_desc]

    def __repr__(self) -> str:
        return f"<{self.id} {self.level}>"


class SkillUpgradeConfig(MappedAdapter[SkillUpgrade]):

    def __init__(self, entries: List[Dict]) -> None:
        super().__init__(entries, additional=[])
        self.group_mappings: Dict[str, List[SkillUpgrade]] = {}
        for e in self.entries:
            if e.group not in self.group_mappings:
                self.group_mappings[e.group] = []
            self.group_mappings[e.group].append(e)
        for l in self.group_mappings.values():
            l.sort(key=lambda x: x.level)


class Constellation(LocalizeAdapter):
    id = Adapter("TalentId", int)
    name = Adapter("NameTextMapHash", Localizable)
    desc = Adapter("DescTextMapHash", Localizable)
    prev = Adapter("PrevTalent", int)


class ConstellationConfig(MappedAdapter[Constellation]):
    pass


class Skill(LocalizeAdapter):
    id = Adapter("Id", int)
    icon = Adapter("SkillIcon")
    buff_icon = Adapter("BuffIcon")
    ability_name = Adapter("AbilityName")

    cd = Adapter("CdTime", float)
    charge = Adapter("MaxChargeNum", int)
    stamina = Adapter("CostStamina", float)
    min_energy = Adapter("EnergyMin", float)
    cd_slot = Adapter("CdSlot", int)

    element_type = Adapter("CostElemType", ElementType)
    energy_required = Adapter("CostElemVal", float)

    ranged = Adapter("IsRanged", bool)
    camera_lock = Adapter("IsAttackCameraLock", bool)
    default_locked = Adapter("DefaultLocked", bool)
    no_cd_reduce = Adapter("IgnoreCDMinusRatio", bool)
    show_icon_arrow = Adapter("ShowIconArrow", bool)
    no_stagger_after_hit = Adapter("ForceCanDoSkill", bool)
    survive_lethal = Adapter("NeedStore", bool)

    upgrade_group = Adapter("ProudSkillGroupId", List[SkillUpgrade], lambda x: SkillUpgradeConfig.__inst__.group_mappings[x])

    name = Adapter("NameTextMapHash", Localizable)
    desc = Adapter("DescTextMapHash", Localizable)

    lock_shape = Adapter("LockShape", LockShape)
    drag_type = Adapter("DragType", DragType)


class SkillConfig(MappedAdapter[Skill]):
    pass


class SkillDepot(JsonAdapter):
    id = Adapter("Id", int)

    burst = IdAdapter("EnergySkill", SkillConfig)
    skills = Adapter("Skills", List[Skill], lambda x: [y for y in x if y != 0])
    subskills = Adapter("SubSkills", List[Skill], lambda x: [y for y in x if y != 0])
    normal = IdAdapter("AttackModeSkill", SkillConfig)
    constellations = Adapter("Talents", List[Constellation], lambda x: [y for y in x if y != 0])
    # TODO : fill the upgrade
    upgrades = Adapter("InherentProudSkillOpens", List, lambda x: [y["ProudSkillGroupId"] for y in x if "ProudSkillGroupId" in y])

    def __init__(self, entry: Dict, skill_config: SkillConfig, constellation_config: ConstellationConfig) -> None:
        super().__init__(entry)
        self.skills = [skill_config[x] for x in self.skills if x in skill_config.mappings]
        self.subskills = [skill_config[x] for x in self.subskills if x in skill_config.mappings]
        self.constellations = [constellation_config[x] for x in self.constellations if x in constellation_config.mappings]


class SkillDepotConfig(MappedAdapter[SkillDepot]):

    def __init__(self, entries: List[Dict], skill_config: SkillConfig, constellation_config: ConstellationConfig) -> None:
        super().__init__(entries, additional=[skill_config, constellation_config])
