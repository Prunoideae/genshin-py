from genshin.textmap import Localizable, LocalizeAdapter, TextMap
from typing import Dict, List
from genshin.adapter import Adapter, JsonAdapter, ConfigAdapter, MappedAdapter
from genshin.entities import Avatar, AvatarConfig


class TrialAvatar(JsonAdapter):
    id: Adapter("TrialAvatarId", int)
    __avatar_param_list: Adapter("TrialAvatarParamList", list)
    __weapon_param_list: Adapter("TrialWeaponParamList", list)
    avatar: Avatar
    level: int

    def __init__(self, entry: Dict, avatar_config: AvatarConfig) -> None:
        super().__init__(entry)
        self.avatar = avatar_config[self.__avatar_param_list[0]]
        self.level = self.__avatar_param_list[1]


class TrialAvatarConfig(MappedAdapter[TrialAvatar]):
    def __init__(self, entries: List[Dict], avatars: AvatarConfig) -> None:
        super().__init__(entries, additional=[avatars])


class TrialData(LocalizeAdapter):
    id: Adapter("TrialAvatarIndexId", int)
    id_internal: Adapter("Id", int)
    avatar: Adapter("TrialAvatarId", TrialAvatar, lambda x: x)
    dungeon: Adapter("DungeonId", int)
    support_avatars: Adapter("BattleAvatarsList", List[Avatar], lambda x: [int(y) for y in x.split(",")])
    reward: Adapter("FirstPassReward", int)
    title: Adapter("TitleTextMapHash", Localizable)
    info: Adapter("BriefInfoTextMapHash", Localizable)

    def __init__(self, entry: Dict, trial_config: TrialAvatarConfig) -> None:
        super().__init__(entry)
        self.avatar = trial_config[self.avatar]
        self.support_avatars = [trial_config[x] for x in self.support_avatars]

    def __repr__(self) -> str:
        return f"<{self.avatar.avatar.name.localize()} {self.avatar.level}>"


class TrialDataConfig(MappedAdapter[TrialData]):
    def __init__(self, entries: List[Dict], avatar: AvatarConfig) -> None:
        super().__init__(entries, additional=[avatar])


class TrialSet(JsonAdapter):
    id: Adapter("ScheduleId", int)
    trials: Adapter("AvatarIndexIdList", List[TrialData], lambda x: [y for y in x if y != 0])

    def __init__(self, entry: Dict, trials: TrialDataConfig) -> None:
        super().__init__(entry)
        self.trials = [trials[x] for x in self.trials]

    def __repr__(self) -> str:
        return [x for x in self.trials].__repr__()


class TrialSetConfig(ConfigAdapter[TrialSet]):
    def __init__(self, entries: List[Dict], trials: TrialDataConfig) -> None:
        super().__init__(entries, additional=[trials])
