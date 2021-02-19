
from typing import Any, Callable, Dict, Generic, List, Type, TypeVar, Union
from types import FunctionType
import typing

'''
A simple json adapter for reducing redundant works.
'''

T = TypeVar("T")


def Adapter(source: str, adapter: T = str, transformer: None = None, fallback: Callable[[str], Any] = lambda x: None) -> T:
    '''
    Adapter marks a field in JsonAdapter's subclass to be able to take value from key `source`, and transform it with
    `adapter` or `transformer`, and return `fallback` when key doesn't exist.

    Notice the field was annotated by `adapter`. So you don't need to deal with `AdapterInst` object in any case.
    '''
    return AdapterInst(source=source, adapter=adapter if transformer is None else transformer, fallback=fallback)


class AdapterInst(Generic[T]):
    def __init__(self, source: str, adapter: T = str, fallback: FunctionType = None) -> None:
        self.source = source
        self.adapter = adapter
        self.fallback = fallback

    def transform(self, entry: Dict) -> Union[T, None]:
        if self.source in entry:
            return self.adapter(entry[self.source])
        elif self.fallback is not None:
            return self.fallback(entry)


class JsonAdapter():
    '''
    Marking class with JsonAdapter makes the class to be able to read from a json object,
    and construct itself.
    '''

    def __init__(self, entry: Dict) -> None:
        for k, v in self.__annotations__.items():
            if isinstance(v, AdapterInst):
                self.__dict__[k] = v.transform(entry)


class ConfigAdapter(Generic[T]):
    '''
    Marking class with ConfigAdapter makes the class able to receive a list of objects to
    construct itself, with corresponding JsonAdapter.
    '''

    def __init__(self, entries: List[Dict], additional: List = []) -> None:
        adapter = typing.get_args(self.__orig_bases__[0])[0]
        self.entries: List[T] = [adapter(x, *additional) for x in entries]
        self.__class__.__inst__ = self

    def find(self, property: str, value: Any) -> List[T]:
        result = []
        for entry in self.entries:
            if property in entry.__dict__ and entry.__dict__[property] == value:
                result.append(entry)
        return result

    def find_in(self, property: str, value: str) -> List[T]:
        result = []
        for entry in self.entries:
            if property in entry.__dict__ and value in entry.__dict__[property]:
                result.append(entry)
        return result

    def match(self, predicate: Callable[[T], bool]) -> List[T]:
        result = []
        for entry in self.entries:
            if predicate(entry):
                result.append(entry)
        return result

    def match_first(self, predicate: Callable[[T], bool]) -> Union[T, None]:
        for entry in self.entries:
            if predicate(entry):
                return entry
        return None


class MappedAdapter(ConfigAdapter[T]):
    def __init__(self, entries: List[Dict], additional: List = []) -> None:
        super().__init__(entries, additional)
        self.mappings = {x.id: x for x in self.entries}

    def __getitem__(self, k: object):
        return self.mappings[k]


def IdAdapter(source: str, config: Type[MappedAdapter[T]]) -> T:
    return AdapterInst(source, lambda x: config.__inst__[x])
