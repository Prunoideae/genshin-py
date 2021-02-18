from genshin.artiprops import AppendDepot, AppendDepots, MainDepot, MainDepots
from types import FunctionType
from genshin.enums.target import EquipPart, UseTarget
from genshin.enums.item_type import ItemType, MaterialType, FoodQuality
from genshin.adapter import Adapter, JsonAdapter, MappedAdapter
from typing import Any, Callable, Dict, List, Text, Union
from genshin.textmap import Localizable, TextMap


class ItemStack():
    def __init__(self, id, count: int) -> None:
        self.id = id
        self.count = count


class WeightedItemStack(ItemStack):
    def __init__(self, id, count: int, weight: int) -> None:
        super().__init__(id, count)
        self.weight = weight


class MaterialEntry(JsonAdapter):
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

    name_text: Adapter("NameTextMapHash", Localizable)
    desc_text: Adapter("DescTextMapHash", Localizable)
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

    def __init__(self, entry: Dict, textmap: TextMap) -> None:
        super().__init__(entry)
        self.localize(textmap)
        if self.can_destroy:
            self.recover_list = list(ItemStack(*x) for x in zip(entry['DestroyReturnMaterial'], entry['DestroyReturnMaterialCount']))

    def __repr__(self) -> str:
        return f"<{self.name_text.localize()} {self.id}>"

    def localize(self, textmap: TextMap):
        self.name_text.set(textmap)
        self.desc_text.set(textmap)
        self.type_text.set(textmap)
        self.interaction_text.set(textmap)
        self.special_text.set(textmap)
        self.effect_text.set(textmap)


class MaterialConfig(MappedAdapter[MaterialEntry]):
    def __init__(self, entries: List[Dict], textmap: TextMap) -> None:
        super().__init__(entries, [textmap])


class ArtifactEntry(JsonAdapter):
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

    main_depot: Adapter("MainPropDepotId", List[MainDepot], lambda x: x)
    append_depot: Adapter("AppendPropDepotId", List[AppendDepot], lambda x: x)

    can_drop: Adapter("Dropable", bool)
    equip_type: Adapter("EquipType", EquipPart)

    name_text: Adapter("NameTextMapHash", Localizable)
    desc_text: Adapter("DescTextMapHash", Localizable)

    can_destroy: Adapter("DestroyRule", bool, lambda x: x == "DESTROY_RETURN_MATERIAL", lambda x: False)
    recover_list: Union[List, None]

    def __init__(self, entry: Dict, textmap: TextMap, main_depot: MainDepots, app_depot: AppendDepots) -> None:
        super().__init__(entry)
        self.localize(textmap)
        self.main_depot = main_depot.mappings[self.main_depot]
        self.append_depot = app_depot.mappings[self.append_depot]

        if self.can_destroy:
            self.recover_list = list(ItemStack(*x) for x in zip(entry['DestroyReturnMaterial'], entry['DestroyReturnMaterialCount']))

    def __repr__(self) -> str:
        return f"<{self.name_text.localize()} {self.id}>"

    def localize(self, textmap: TextMap):
        self.name_text.set(textmap)
        self.desc_text.set(textmap)


class ArtifactConfig(MappedAdapter[ArtifactEntry]):
    def __init__(self, entries: List[Dict], textmap: TextMap, main: MainDepots, app: AppendDepots) -> None:
        super().__init__(entries, [textmap, main, app])
