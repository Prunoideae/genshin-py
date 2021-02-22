from __future__ import annotations
from typing import Dict
from genshin.adapter import JsonAdapter, MappedAdapter
from genshin.battlepass import BPMissionConfig, BPScheduleConfig
from genshin.rewards import RewardConfig
from genshin.events import ActivityConfig, TrialAvatarConfig, TrialDataConfig, TrialSetConfig
from genshin.tags import TagConfig, TagGroupConfig
from genshin.items import ArtifactConfig, MaterialConfig, WeaponConfig
from genshin.artiprops import AppendDepots, MainDepots
from genshin.textmap import TextMap
from genshin.entities import AvatarConfig
import json
from os import path


class RepoData():
    def __init__(self, base_path: str, textmap: str = None, lang: str = None, excel: str = None, encoding: str = None) -> None:

        # Paths
        self.base_path = base_path
        self.textmap_path = path.join(base_path, "TextMap") if textmap is None else textmap
        self.excel_path = path.join(base_path, "Excel") if excel is None else excel

        # Supportives
        self.textmap = TextMap(self.textmap_path, "EN" if lang is None else lang)
        self.main_depot = MainDepots(json.load(open(path.join(self.excel_path, "ReliquaryMainPropExcelConfigData.json"), encoding=encoding)))
        self.app_depot = AppendDepots(json.load(open(path.join(self.excel_path, "ReliquaryAffixExcelConfigData.json"), encoding=encoding)))
        self.tags = TagConfig(json.load(open(path.join(self.excel_path, "FeatureTagExcelConfigData.json"), encoding=encoding)))
        self.tag_groups = TagGroupConfig(
            json.load(open(path.join(self.excel_path, "FeatureTagGroupExcelConfigData.json"), encoding=encoding)), self.tags)

        # Entities
        self.artifacts = ArtifactConfig(json.load(open(path.join(self.excel_path, "ReliquaryExcelConfigData.json"), encoding=encoding)))
        self.materials = MaterialConfig(json.load(open(path.join(self.excel_path, "MaterialExcelConfigData.json"), encoding=encoding)))
        self.weapons = WeaponConfig(json.load(open(path.join(self.excel_path, "WeaponExcelConfigData.json"), encoding=encoding)))
        self.skill = None
        self.skill_depot = None  # TODO: Finish the structure.
        self.avatars = AvatarConfig(json.load(open(path.join(self.excel_path, "AvatarExcelConfigData.json"), encoding=encoding)))
        self.rewards = RewardConfig(json.load(open(path.join(self.excel_path, "RewardExcelConfigData.json"), encoding=encoding)))

        # Trials
        self.trial_avatars = TrialAvatarConfig(
            json.load(open(path.join(self.excel_path, "TrialAvatarExcelConfigData.json"), encoding=encoding)), self.avatars)
        self.trials = TrialDataConfig(
            json.load(open(path.join(self.excel_path, "TrialAvatarActivityDataExcelConfigData.json"), encoding=encoding)), self.trial_avatars)
        self.trialsets = TrialSetConfig(
            json.load(open(path.join(self.excel_path, "TrialAvatarActivityExcelConfigData.json"), encoding=encoding)), self.trials)
        self.activities = ActivityConfig(json.load(open(path.join(self.excel_path, "NewActivityExcelConfigData.json"), encoding=encoding)))

        # BP
        self.bp_schedule = BPScheduleConfig(json.load(open(path.join(self.excel_path, "BattlePassScheduleExcelConfigData.json"), encoding=encoding)))
        self.bp_mission = BPMissionConfig(json.load(open(path.join(self.excel_path, "BattlePassMissionExcelConfigData.json"), encoding=encoding)))

    def diff_id(self, previous: RepoData) -> Dict[str, Dict[int, JsonAdapter]]:
        result = {}
        for k, v in self.__dict__.items():
            if isinstance(v, MappedAdapter):
                p_v: MappedAdapter = previous.__dict__[k]
                result[k] = {k1: v1 for k1, v1 in v.mappings.items() if k1 not in p_v}
        return result
