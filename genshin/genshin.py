from genshin.tags import TagConfig, TagGroupConfig
from genshin.items import ArtifactConfig, MaterialConfig
import json
from genshin.artiprops import AppendDepots, MainDepots
from genshin.textmap import TextMap
from genshin.entities import Avatar, AvatarConfig

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
        self.artifacts = ArtifactConfig(json.load(open(path.join(self.excel_path, "ReliquaryExcelConfigData.json"))),
                                        self.textmap, self.main_depot, self.app_depot)
        self.materials = MaterialConfig(json.load(open(path.join(self.excel_path, "MaterialExcelConfigData.json"))), self.textmap)
        self.avatars = AvatarConfig(json.load(open(path.join(self.excel_path, "AvatarExcelConfigData.json"))), self.textmap, self.tag_groups)

    def localize(self):
        pass
