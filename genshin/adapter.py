
from typing import Any, Callable, Dict, Generic, List, Type, TypeVar, Union
from types import FunctionType

import typing

'''
A simple json adapter for reducing redundant works.
'''

T = TypeVar("T")
TF = TypeVar("TF")


def Adapter(source: str, adapter: Type[T] = str, transformer: Callable[[Any], T] = None, fallback: Callable[[str], TF] = lambda x: None) -> Union[T, TF]:
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

    __keys__: List[str]

    def __init__(self, entry: Dict) -> None:
        self.__keys__ = []
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, AdapterInst):
                self.__dict__[k] = v.transform(entry)
                self.__keys__.append(k)
        self.__keys__.sort()

    def __eq__(self, o: 'JsonAdapter') -> bool:
        return all(self.__dict__[x] == o.__dict__[y] for x, y in zip(self.__keys__, o.__keys__))


class ConfigAdapter(Generic[T]):
    '''
    Marking class with ConfigAdapter makes the class able to receive a list of objects to
    construct itself, with corresponding JsonAdapter.

    Note that this will also register `self` to `sele.__class__.__inst__`, as long as all the registry
    and parsing are done per `RepoData`, this should make no conflict of different versions of
    `RepoData`, since all data are stored in corresponding objects.
    '''
    __inst__: 'ConfigAdapter[T]'

    def __init__(self, entries: List[Dict], additional: List = []) -> None:
        adapter = typing.get_args(self.__orig_bases__[0])[0]
        self.entries: List[T] = [adapter(x, *additional) for x in entries]
        self.__class__.__inst__ = self

    def __iter__(self):
        yield from self.entries

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
    '''
    Mapped adapter of `ConfigAdapter[T]`.

    Automatically generates a id mapping by `id` field. This follows a
    duck-typing manner.

    It also provides set of functions like __getitem__ or __contains__.
    '''
    __inst__: 'MappedAdapter[T]'

    def __init__(self, entries: List[Dict], additional: List = []) -> None:
        super().__init__(entries, additional)
        self.mappings = {x.id: x for x in self.entries}

    def __getitem__(self, k: object) -> T:
        return self.mappings[k]

    def __contains__(self, k: object) -> bool:
        return k in self.mappings

    def diff(self, old: 'MappedAdapter[T]') -> Dict[Any, T]:
        return {k: v for k, v in self.mappings.items() if k not in old or v != old[k]}


def IdAdapter(source: str, config: Type[MappedAdapter[T]]) -> Union[T, None]:
    return AdapterInst(source, lambda x: config.__inst__[x] if x in config.__inst__.mappings else None)
