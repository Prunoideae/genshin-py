# genshin-py

A parser for all data from Dimbreath/GenshinData. This is written as a module, which provides a `RepoData` class, can be initialized from a path to DimBreath's repository folder, or by separately specifying `Excel` and `TextMap` folders.

As the nature of the fast-evolving of the repository data, `genshin-py` will not be provided in pypi, or other package distribution sites, please remember to `git pull` from the repository as new version of `GenshinData` released to keep up the changes, furthermore, please try to fetch the newest commit first when you come across bugs and errors, before submitting issues.

Using Python 3.9.1, still much work-in-progress. The parser is developed under Microsoft `Pylance` Language server, for difference in development experience, especially when comes with type-hinting and things alike, it should not be the problem in the code.

# 1. Object Abstraction

`genshin-py` comes with multiple objects to make a abstract and detailed summary over the complex json structure. Mainly, it comes with three classes : `JsonAdapter`, `ConfigAdapter` and `RepoData`.

## 1.1 RepoData

`RepoData` is simple : a collection of all json configs parsed in the currenct structure. There's no actual need to adjust most of the content in this object, as the config files should be stable, or you can write methods to extend its functions for more analytical usage.

## 1.2 ConfigAdapter

`ConfigAdapter` represents an abstraction for any single config file in the repository, with a assumption of the data starts as `[object1, object2...]` as basic structure. For extending the parser to parse config files that's not yet implemented, please write a subclass that inherits the `ConfigAdapter[T]` base class, or the `MappedAdapter[T]` base class if a `id` annotation is in the class to index the objects.

When you mark a class which inherits from `ConfigAdapter[T]`, this marks the class to accept a `List[T]` in `__init__` to construct the object, where `T` must be a instance of `JsonAdapter`:

```python
class Adapter(JsonAdapter):
    id : Adapter('Id', int)

class AdapterConfig(MappedAdapter[Adapter]):
    pass

# Instantiate
inst = AdapterConfig([{'Id':1},{'Id':2}])
print(inst.entries[0].id) # 1
print(inst[2].id) # 2
print(list(inst.mappings.keys())) # [1,2]
```

Please register corresponding json parsers in the `RepoData` class to keep everything simple.

## 1.3 JsonAdapter

`JsonAdapter` represents an entry in the `List[T]` parsed by json decoder. Which is designed to parse a json object into correct python object. Marking a class inherits from `JsonAdapter` makes the class to accept a `Dict` of json object to construct the object.

To ensure well-defined type hints and type-checking in both development and runtime, a annotation-based auto adapter was implemented in `JsonAdapter` to generate most of the logic automatically.

```python
class Adapter(JsonAdapter):
    id : Adapter('Id', int)
    is_even : Adapter('Number', bool, transformer=lambda x:x%2==0)
    fallback : Adapter('Fallible', int, fallback=lambda x: x["Id"] - 1)

# Instantiate 
inst = Adapter({"Id":1, "Number":3})
print(inst.id) # 1
print(inst.is_even) # False
print(inst.fallback) # 0
```

For advanced usages, please refer to docs and examples already written in configs.
