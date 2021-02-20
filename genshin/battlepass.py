from genshin.adapter import Adapter, IdAdapter, MappedAdapter
from genshin.textmap import Localizable, LocalizeAdapter


class BattlePassSchedule(LocalizeAdapter):
    id: Adapter("Id", int)
    title: Adapter("TitleNameTextMapHash", Localizable)
    begin: Adapter("BeginDateStr")
    end: Adapter("EndDateStr")


class BPScheduleConfig(MappedAdapter[BattlePassSchedule]):
    pass


class BattlePassMission(LocalizeAdapter):
    id: Adapter("Id", int)
    exp: Adapter("AddPoint", int)
    desc: Adapter("DescTextMapHash", Localizable)
    trigger: Adapter("TriggerConfig", dict)
    counter: Adapter("Progress", int)

    schedule: IdAdapter("ScheduleId", BPScheduleConfig)
    activity: Adapter("ActivityId", int)


class BPMissionConfig(MappedAdapter[BattlePassMission]):
    pass
