from datetime import datetime
from typing import Dict, List
from genshin.adapter import Adapter, IdAdapter, MappedAdapter
from genshin.textmap import Localizable, LocalizeAdapter
from genshin.utils import ItemStack, genshin_datetime


class Shop(LocalizeAdapter):
    id = Adapter("ShopId", int)
    type = Adapter("ShopType")

    city_id = Adapter("CityId", int)
    city_discount_level = Adapter("CityDiscountLevel", int)
    city_discout = Adapter("ScoinDiscountRate", float, lambda x: float(x) / 100.0)

    goods_list: List['Good']

    def __init__(self, entries: List[Dict]) -> None:
        self.goods_list: List['Good'] = []
        super().__init__(entries)

    def __repr__(self) -> str:
        return f"<{self.id} {self.type}>"


class ShopConfig(MappedAdapter[Shop]):
    pass


class Good(LocalizeAdapter):
    id = Adapter("GoodsId", int)
    subtag = Adapter("SubTagNameTextMapHash", Localizable)

    __item = Adapter('ItemId', int)
    __count = Adapter("ItemCount", int)
    item: ItemStack
    buy_limit = Adapter("BuyLimit", int)

    coin_cost = Adapter("CostScoin", int, fallback=lambda x: 0)
    item_cost = Adapter("CostItems", lambda x: [ItemStack(y["Id"], y["Count"]) for y in x if y])

    shop = IdAdapter("ShopType", ShopConfig)

    refresh_type = Adapter("RefreshType")
    refresh_time = Adapter("RefreshParam", int)

    start_time = Adapter("BeginTime", adapter=datetime, transformer=genshin_datetime)
    end_time = Adapter("EndTime", adapter=datetime, transformer=genshin_datetime)

    min_level = Adapter("MinPlayerLevel", int)
    max_level = Adapter("MaxPlayerLevel", int)

    def __init__(self, entries: List[Dict]) -> None:
        super().__init__(entries)
        if self.shop is not None:
            ShopConfig.__inst__.mappings[self.shop.id].goods_list.append(self)
        self.item = ItemStack(self.__item, self.__count)

    def __repr__(self) -> str:
        return f"<{self.item.__repr__()} {self.buy_limit}>"


class GoodConfig(MappedAdapter[Good]):
    pass
