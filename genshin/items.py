from os import name
from genshin.enums.attr_type import ArtiAttrType
from genshin.artiprops import AppendDepot, AppendDepots, MainDepot, MainDepots
from genshin.enums.target import EquipPart, UseTarget
from genshin.enums.item_type import ItemType, MaterialType, FoodQuality
from genshin.adapter import Adapter, ConfigAdapter, IdAdapter, JsonAdapter, MappedAdapter
from typing import Dict, List, Union
from genshin.textmap import Localizable, LocalizeAdapter, TextMap
from genshin.utils import ItemStack, WeightedItemStack


class MaterialEntry(LocalizeAdapter):
    id: Adapter("Id", int)
    rank: Adapter("RankLevel", int)
    stacksize: Adapter("StackLimit", int)
    max_use: Adapter("MaxUseCount", int)
    use_level: Adapter("UseLevel", int)
    weight: Adapter("Weight", int)
    cd: Adapter("CdTime", int)
    __rank: Adapter("Rank", int)
    global_limit: Adapter("GlobalItemLimit", int)

    hidden: Adapter("IsHidden", bool)
    is_split_drop: Adapter("IsSplitDrop", bool)
    use_on_gain: Adapter("UseOnGain", bool)
    close_bag_after_use: Adapter("CloseBagAfterUsed", bool)
    play_gain_effect: Adapter("PlayGainEffect", bool)
    no_first_get_hin: Adapter("NoFirstGetHint", bool)

    target: Adapter("UseTarget", UseTarget)
    item_type: Adapter("ItemType", ItemType)
    material_type: Adapter("MaterialType", MaterialType)
    icon: Adapter("Icon")
    gadget_id: Adapter("GadgetId", int)

    food_quality: Adapter("FoodQuality", FoodQuality)
    hunger_value: Adapter("SatiationParams", int, transformer=lambda x: x[1] if x else 0)

    name: Adapter("NameTextMapHash", Localizable)
    desc: Adapter("DescTextMapHash", Localizable)
    type_text: Adapter("TypeDescTextMapHash", Localizable)
    interaction_text: Adapter("InteractionTitleTextMapHash", Localizable)
    special_text: Adapter("SpecialDescTextMapHash", Localizable)
    effect_text: Adapter("EffectDescTextMapHash", Localizable)

    effect_icon: Adapter("EffectIcon")
    effect_name: Adapter("EffectName")
    effect_id: Adapter("EffectGadgetID")

    can_destroy: Adapter("DestroyRule", bool, lambda x: x == "DESTROY_RETURN_MATERIAL", lambda x: False)
    recover_list: Union[List, None]

    set_id: Adapter("SetID", int)

    item_use: Adapter("ItemUse", list, lambda x: x)
    pic_path: Adapter("PicPath", list, lambda x: x)

    def __init__(self, entry: Dict) -> None:
        super().__init__(entry)
        if self.can_destroy:
            self.recover_list = list(ItemStack(*x) for x in zip(entry['DestroyReturnMaterial'], entry['DestroyReturnMaterialCount']))
        else:
            self.recover_list = None

    def __repr__(self) -> str:
        return f"<{self.name.localize()} {self.id}>"


class MaterialConfig(MappedAdapter[MaterialEntry]):
    def __init__(self, entries: List[Dict]) -> None:
        super().__init__(entries)
        ItemStack.set_instance(self)


class ArtifactEntry(LocalizeAdapter):
    id: Adapter("Id", int)
    rank: Adapter("RankLevel", int)
    weight: Adapter("Weight", int)
    __rank: Adapter("Rank", int)
    set_id: Adapter("SetID", int)
    item_type: Adapter("ItemType", ItemType)
    icon: Adapter("Icon")
    gadget_id: Adapter("GadgetId", int)
    max_level: Adapter("MaxLevel", int)
    base_exp: Adapter("BaseConvExp", int)

    main_depot: IdAdapter("MainPropDepotId", MainDepots)
    append_depot: Adapter("AppendPropDepotId", List[AppendDepot], lambda x: x)

    can_drop: Adapter("Dropable", bool)
    equip_type: Adapter("EquipType", EquipPart)

    name: Adapter("NameTextMapHash", Localizable)
    desc: Adapter("DescTextMapHash", Localizable)

    can_destroy: Adapter("DestroyRule", bool, lambda x: x == "DESTROY_RETURN_MATERIAL", lambda x: False)
    recover_list: Union[List[ItemStack], None]

    def __init__(self, entry: Dict) -> None:
        super().__init__(entry)
        if self.can_destroy:
            self.recover_list = list(ItemStack(*x) for x in zip(entry['DestroyReturnMaterial'], entry['DestroyReturnMaterialCount']))
        else:
            self.recover_list = None

    def __repr__(self) -> str:
        return f"<{self.rank}* {self.name.localize()} {self.id}>"


class ArtifactConfig(MappedAdapter[ArtifactEntry]):
    def __init__(self, entries: List[Dict]) -> None:
        super().__init__(entries)
        ItemStack.set_instance(self)


class WeaponEntry(LocalizeAdapter):
    id: Adapter("Id", int)
    level: Adapter("RankLevel", int)
    exp: Adapter("WeaponBaseExp", int)
    skills: Adapter("SkillAffix", List[int], lambda x: [y for y in x if y != 0])
    item_type: Adapter("ItemType", ItemType)
    weight: Adapter("Weight", int)
    __rank: Adapter("Rank", int)
    name: Adapter("NameTextMapHash", Localizable)
    desc: Adapter("DescTextMapHash", Localizable)

    gadget_id: Adapter("GadgetId", int)

    __weapon_pros: Adapter("WeaponProp", List[Dict], lambda x: x)
    base_atk: float
    base_curve: str
    substat: Union[ArtiAttrType, None]
    substat_base: float
    substat_curve: str

    awaken_texture: Adapter("AwakenTexture")
    awaken_icon: Adapter("AwakenIcon")
    icon: Adapter("Icon")

    unrotate: Adapter("UnRotate", bool)

    promote_id: Adapter("WeaponPromoteId", int)
    refine_costs: Adapter("AwakenCosts", List[int], lambda x: x)

    story_id: Adapter("StoryId", int)

    def __init__(self, entry: Dict) -> None:
        super().__init__(entry)
        self.base_atk = self.__weapon_pros[0]["InitValue"]
        self.base_curve = self.__weapon_pros[0]["Type"]
        if "PropType" in self.__weapon_pros[1]:
            self.substat = ArtiAttrType(self.__weapon_pros[1]["PropType"])
            self.substat_base = self.__weapon_pros[1]["InitValue"]
            self.substat_curve = self.__weapon_pros[1]["Type"]
        else:
            self.substat = None
            self.substat_base = 0
            self.substat_curve = ""


class WeaponConfig(MappedAdapter[WeaponEntry]):
    def __init__(self, entries: List[Dict]) -> None:
        super().__init__(entries)
        ItemStack.set_instance(self)
