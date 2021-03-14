from genshin.items import WeaponConfig, WeaponEntry
from genshin.textmap import Localizable, LocalizeAdapter, TextMap
from typing import Dict, List
from genshin.adapter import Adapter, IdAdapter, JsonAdapter, ConfigAdapter, MappedAdapter
from genshin.entities import Avatar, AvatarConfig


class TrialAvatar(JsonAdapter):
    id = Adapter("TrialAvatarId", int)
    __avatar_param_list = Adapter("TrialAvatarParamList", list)
    __weapon_param_list = Adapter("TrialWeaponParamList", list)
    avatar = Avatar
    level = int
    weapon = WeaponEntry
    weapon_level = int

    def __init__(self, entry: Dict, avatar_config: AvatarConfig, weapon_config: WeaponConfig) -> None:
        super().__init__(entry)
        self.avatar = avatar_config[self.__avatar_param_list[0]]
        self.level = self.__avatar_param_list[1]
        self.weapon = weapon_config[self.__weapon_param_list[0]]
        self.weapon_level = self.__weapon_param_list[1]

    def __repr__(self) -> str:
        return f"<{self.avatar.name.localize()} {self.level} | {self.weapon.name.localize()} {self.weapon_level}>"


class TrialAvatarConfig(MappedAdapter[TrialAvatar]):
    def __init__(self, entries: List[Dict], avatars: AvatarConfig, weapons: WeaponConfig) -> None:
        super().__init__(entries, additional=[avatars, weapons])


class TrialData(LocalizeAdapter):
    id = Adapter("TrialAvatarIndexId", int)
    id_internal = Adapter("Id", int)
    avatar_data = IdAdapter("TrialAvatarId", TrialAvatarConfig)
    dungeon = Adapter("DungeonId", int)
    support_avatars = Adapter("BattleAvatarsList", List[Avatar], lambda x: [int(y) for y in x.split(",")])
    reward = Adapter("FirstPassReward", int)
    title = Adapter("TitleTextMapHash", Localizable)
    info = Adapter("BriefInfoTextMapHash", Localizable)

    def __init__(self, entry: Dict, trial_config: TrialAvatarConfig) -> None:
        super().__init__(entry)
        self.support_avatars = [trial_config[x] for x in self.support_avatars]

    def __repr__(self) -> str:
        return f"<{self.avatar_data.avatar.name.localize()} {self.avatar_data.level}>"


class TrialDataConfig(MappedAdapter[TrialData]):
    def __init__(self, entries: List[Dict], avatar: AvatarConfig) -> None:
        super().__init__(entries, additional=[avatar])


class TrialSet(JsonAdapter):
    id = Adapter("ScheduleId", int)
    trials = Adapter("AvatarIndexIdList", List[TrialData], lambda x: [y for y in x if y != 0])

    def __init__(self, entry: Dict, trials: TrialDataConfig) -> None:
        super().__init__(entry)
        self.trials = [trials[x] for x in self.trials]

    def __repr__(self) -> str:
        return self.trials.__repr__()


class TrialSetConfig(MappedAdapter[TrialSet]):
    def __init__(self, entries: List[Dict], trials: TrialDataConfig) -> None:
        super().__init__(entries, additional=[trials])


class Activity(LocalizeAdapter):
    id = Adapter("ActivityId", int)
    type = Adapter("ActivityType")
    name = Adapter("NameTextMapHash", Localizable)
    scene_tag = Adapter("ActivitySceneTag")
    cond_group = Adapter("CondGroupId", list)
    watcher_group = Adapter("WatcherId", list)

    def __repr__(self) -> str:
        return f"<{self.name.localize()} {self.id}>"


class ActivityConfig(MappedAdapter[Activity]):
    pass
