from genshin.enums.attr_type import ElementType
from genshin.enums.displays import DragType, LockShape
from genshin.adapter import Adapter, JsonAdapter
from genshin.textmap import Localizable


class SkillUpgrade(JsonAdapter):
    pass


class Skill(JsonAdapter):
    id: Adapter("Id", int)
    icon: Adapter("SkillIcon")
    buff_icon: Adapter("BuffIcon")
    ability_name: Adapter("AbilityName")

    cd: Adapter("CdTime", float)
    charge: Adapter("MaxChargeNum", int)
    stamina: Adapter("CostStamina", float)
    min_energy: Adapter("EnergyMin", float)
    cd_slot: Adapter("CdSlot", int)

    element_type: Adapter("CostElemType", ElementType)
    energy_required: Adapter("CostElemVal", float)

    ranged: Adapter("IsRanged", bool)
    camera_lock: Adapter("IsAttackCameraLock", bool)
    default_locked: Adapter("DefaultLocked", bool)
    no_cd_reduce: Adapter("IgnoreCDMinusRatio", bool)
    show_icon_arrow: Adapter("ShowIconArrow", bool)
    no_stagger_after_hit: Adapter("ForceCanDoSkill", bool)
    survive_lethal: Adapter("NeedStore", bool)

    name: Adapter("NameTextMapHash", Localizable)
    desc: Adapter("DescTextMapHash", Localizable)

    lock_shape: Adapter("LockShape", LockShape)
    drag_type: Adapter("DragType", DragType)


class SkillDepot(JsonAdapter):
    pass


class SkillUpgradeConfig():
    pass


class SkillConfig():
    pass


class SkillDepotConfig():
    pass
