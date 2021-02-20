from genshin.battlepass import BPMissionConfig, BPScheduleConfig
from genshin.rewards import RewardConfig
from genshin.events import TrialAvatarConfig, TrialDataConfig, TrialSetConfig
from genshin.tags import TagConfig, TagGroupConfig
from genshin.items import ArtifactConfig, MaterialConfig, WeaponConfig
from genshin.artiprops import AppendDepots, MainDepots
from genshin.textmap import TextMap
from genshin.entities import AvatarConfig
import json
from os import path


class RepoData():
    def __init__(self, base_path: str, textmap: str = None, lang: str = None, excel: str = None) -> None:
        # Paths
        self.base_path = base_path
        self.textmap_path = path.join(base_path, "TextMap") if textmap is None else textmap
        self.excel_path = path.join(base_path, "Excel") if excel is None else excel

        # Supportives
        # TODO: Make everything lazy.
        self.textmap = TextMap(self.textmap_path, "EN" if lang is None else lang)
        self.main_depot = MainDepots(json.load(open(path.join(self.excel_path, "ReliquaryMainPropExcelConfigData.json"))))
        self.app_depot = AppendDepots(json.load(open(path.join(self.excel_path, "ReliquaryAffixExcelConfigData.json"))))
        self.tags = TagConfig(json.load(open(path.join(self.excel_path, "FeatureTagExcelConfigData.json"))))
        self.tag_groups = TagGroupConfig(json.load(open(path.join(self.excel_path, "FeatureTagGroupExcelConfigData.json"))), self.tags)
        self.skill_depot = None

        # Entities
        self.artifacts = ArtifactConfig(json.load(open(path.join(self.excel_path, "ReliquaryExcelConfigData.json"))))
        self.materials = MaterialConfig(json.load(open(path.join(self.excel_path, "MaterialExcelConfigData.json"))))
        self.weapons = WeaponConfig(json.load(open(path.join(self.excel_path, "WeaponExcelConfigData.json"))))
        self.avatars = AvatarConfig(json.load(open(path.join(self.excel_path, "AvatarExcelConfigData.json"))))

        self.rewards = RewardConfig(json.load(open(path.join(self.excel_path, "RewardExcelConfigData.json"))))

        # Trials
        self.trial_avatars = TrialAvatarConfig(json.load(open(path.join(self.excel_path, "TrialAvatarExcelConfigData.json"))), self.avatars)
        self.trials = TrialDataConfig(json.load(open(path.join(self.excel_path, "TrialAvatarActivityDataExcelConfigData.json"))), self.trial_avatars)
        self.trialsets = TrialSetConfig(json.load(open(path.join(self.excel_path, "TrialAvatarActivityExcelConfigData.json"))), self.trials)

        # BP
        self.bp_schedule = BPScheduleConfig(json.load(open(path.join(self.excel_path, "BattlePassScheduleExcelConfigData.json"))))
        self.bp_mission = BPMissionConfig(json.load(open(path.join(self.excel_path, "BattlePassMissionExcelConfigData.json"))))
