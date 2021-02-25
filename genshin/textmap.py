from genshin.adapter import AdapterInst, JsonAdapter
from io import UnsupportedOperation
from os import path
from typing import Dict, List, Union
import json


class TextMap():
    __inst__: 'TextMap'

    def __init__(self, textmap: str, name: str) -> None:
        self.__path__ = path.join(textmap, f"Text{name}.json")
        self.__maps__ = json.load(open(self.__path__))
        self.__class__.__inst__ = self

    def reload(self, name: str, textmap: str = None):
        self.__path__ = path.join(textmap if textmap is not None else path.dirname(self.__path__), f"Text{name}.json")
        self.__maps__ = json.load(open(self.__path__))

    def __getitem__(self, k: Union[str, int]) -> Union[None, str]:
        if type(k) is not str:
            k = str(k)
        return self.__maps__[k] if k in self.__maps__ else None


class Localizable():
    '''
    A localizable string, may varies from textmap.

    Uses the TextMapHash as translation key.
    '''

    def __init__(self, translation_key: Union[str, int], textmap: TextMap = None) -> None:
        if textmap is not None:
            self.__textmap__ = textmap
        self.key = str(translation_key)
        self.__localized__ = None

    def set(self, textmap: TextMap):
        self.__textmap__ = textmap

    def localize(self) -> Union[str, None]:
        return self.__textmap__[self.key] if self.key is not None else None

    def __repr__(self) -> str:
        text = self.localize()
        if text:
            return f"<{self.key} {text if len(text) <= 20 else text[:17]+'...'}>"
        else:
            return f"<{self.key} #No translation#>"

    def __eq__(self, o: object) -> bool:
        if type(o) is str:
            return self.localize() == o
        elif type(o) is Localizable:
            return self.localize() == o.localize()
        else:
            raise UnsupportedOperation

    def __contains__(self, o: object) -> bool:
        r = self.localize()
        if not r:
            return False
        else:
            return o in r


class LocalizeAdapter(JsonAdapter):

    def __init__(self, entries: List[Dict]) -> None:
        super().__init__(entries)
        for k, v in self.__annotations__.items():
            if isinstance(v, AdapterInst) and v.adapter == Localizable:
                self.__dict__[k].set(TextMap.__inst__)
