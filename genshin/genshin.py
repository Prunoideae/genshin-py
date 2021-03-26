from __future__ import annotations
from genshin.achievements import AchievementConfig
from genshin.hangout import HangoutCGConfig
from genshin.skills import ConstellationConfig, SkillConfig, SkillDepotConfig, SkillUpgradeConfig
from typing import Dict, List, Type
from genshin.adapter import ConfigAdapter, JsonAdapter, MappedAdapter, T
from genshin.battlepass import BPMissionConfig, BPScheduleConfig
from genshin.rewards import RewardConfig
from genshin.events import ActivityConfig, TrialAvatarConfig, TrialDataConfig, TrialSetConfig
from genshin.tags import TagConfig, TagGroupConfig
from genshin.items import ArtifactConfig, MaterialConfig, WeaponConfig
from genshin.artiprops import AppendDepots, MainDepots
from genshin.textmap import TextMap
from genshin.entities import AvatarCodexConfig, AvatarConfig
from genshin.cosmetics import WindGliderConfig
import json
from os import path


class RepoData():
    """
    A object representing DimBreath's GenshinData.

    Calls and fields should be stable overtime, and any changes
    in original json structure will be reflected as a change in 
    parsing, not the fields, unless there're critical changes.
    """

    def json(self, json_name) -> List[Dict]:
        return json.load(open(path.join(self.excel_path, json_name), encoding=self.encoding))

    def __init__(self, base_path: str, textmap: str = None, lang: str = None, excel: str = None, encoding: str = None) -> None:

        # Supportives
        self.base_path = base_path
        self.textmap_path = path.join(base_path, "TextMap") if textmap is None else textmap
        self.excel_path = path.join(base_path, "ExcelBinOutput") if excel is None else excel
        self.encoding = encoding
        self.textmap = TextMap(self.textmap_path, "EN" if lang is None else lang)

        self.main_depot = MainDepots(self.json("ReliquaryMainPropExcelConfigData.json"))
        self.app_depot = AppendDepots(self.json("ReliquaryAffixExcelConfigData.json"))
        self.tags = TagConfig(self.json("FeatureTagExcelConfigData.json"))
        self.tag_groups = TagGroupConfig(self.json("FeatureTagGroupExcelConfigData.json"), self.tags)

        # Entities
        self.artifacts = ArtifactConfig(self.json("ReliquaryExcelConfigData.json"))
        self.materials = MaterialConfig(self.json("MaterialExcelConfigData.json"))
        self.gliders = WindGliderConfig(self.json("AvatarFlycloakExcelConfigData.json"))
        self.weapons = WeaponConfig(self.json("WeaponExcelConfigData.json"))

        self.skill_upgrade = SkillUpgradeConfig(self.json("ProudSkillExcelConfigData.json"))
        self.constellations = ConstellationConfig(self.json("AvatarTalentExcelConfigData.json"))
        self.skill = SkillConfig(self.json("AvatarSkillExcelConfigData.json"))
        self.skill_depot = SkillDepotConfig(self.json("AvatarSkillDepotExcelConfigData.json"), self.skill, self.constellations)
        self.avatars = AvatarConfig(self.json("AvatarExcelConfigData.json"))
        self.avatar_codex = AvatarCodexConfig(self.json("AvatarCodexExcelConfigData.json"))
        self.rewards = RewardConfig(self.json("RewardExcelConfigData.json"))

        # Trials
        self.trial_avatars = TrialAvatarConfig(self.json("TrialAvatarExcelConfigData.json"), self.avatars, self.weapons)
        self.trials = TrialDataConfig(self.json("TrialAvatarActivityDataExcelConfigData.json"), self.trial_avatars)
        self.trialsets = TrialSetConfig(self.json("TrialAvatarActivityExcelConfigData.json"), self.trials)
        self.activities = ActivityConfig(self.json("NewActivityExcelConfigData.json"))

        # Achievements
        self.achievements = AchievementConfig(self.json("AchievementExcelConfigData.json"))

        # Hangouts
        self.hangout_cg = HangoutCGConfig(self.json("CoopCGExcelConfigData.json"))

        # BP
        self.bp_schedule = BPScheduleConfig(self.json("BattlePassScheduleExcelConfigData.json"))
        self.bp_mission = BPMissionConfig(self.json("BattlePassMissionExcelConfigData.json"))

    def diff(self, previous: RepoData) -> Dict[Type[MappedAdapter[T]], Dict[int, T]]:
        result = {}
        for k, v in self.__dict__.items():
            if isinstance(v, MappedAdapter):
                p_v: MappedAdapter = previous.__dict__[k]
                result[v.__class__] = v.diff(p_v)
        return {k: v for k, v in result.items() if v}
