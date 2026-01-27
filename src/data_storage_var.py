from tools.typing_tools import *
from tools.dictionary_tools import *
from tools.constants import StorageAttrName

class DataStorageVar[DataStorageType](dict, Loggable):
  def __init__(self, storage_type: Type[DataStorageType], data: dict[int, DataStorageType] = {}, is_logging_enabled: bool = False, label: Optional[StorageAttrName] = None, include_call_stack: bool = False) -> None:
    Loggable.__init__(self, is_logging_enabled, label, include_call_stack)
    self.STORAGE_TYPE = storage_type
    self.__data: dict[int, DataStorageType] = {}
    if data != {}: self.__data = data

  # built-in methods
  def __repr__(self) -> str: return f"DataStorageVar[{self.STORAGE_TYPE}]({self.data})"

  ## dictionary methods
  def __getitem__(self, key: int) -> DataStorageType: return cast(DataStorageType, self.data[key])
  
  def __setitem__(self, key: int, value: DataStorageType) -> None:
    if type(value) != self.STORAGE_TYPE: raise TypeError(f"Value type of {value=} doesn't match with value type of {self.STORAGE_TYPE=}.")
    self.data[key] = value

  def __delitem__(self, key: int) -> None: del self.data[key]

  def __len__(self) -> int: return len(self.data)

  def clear(self): return self.data.clear()

  def copy(self) -> dict[int, DataStorageType]: return self.data.copy()

  def has_key(self, key: int) -> bool: return key in self.data

  def update(self, *args, **kwargs) -> None: return self.data.update(*args, **kwargs)

  def keys(self): return self.data.keys()

  def values(self): return self.data.values()

  def items(self): return self.data.items()

  def pop(self, *args) -> DataStorageType: return self.data.pop(*args)

  def __contains__(self, item: Union[int, DataStorageType]) -> bool: return item in self.data

  def __iter__(self) -> Iterator: return iter(self.data)

  # getter and setter methods

  @property
  def data(self) -> dict[int, DataStorageType]: return self.__data

  # dictionary methods

  def select_values(self, condition: Callable[[int, DataStorageType], bool]) -> dict[int, DataStorageType]:
    return filter_dictionary(self, condition)
  
  def insert_value_at(self, key: int, value: DataStorageType) -> None:
    if key in self: raise Exception()
    self[key] = value

  def update_value_at(self, key: int, value: DataStorageType) -> None:
    if not key in self: raise Exception()
    self[key] = value

  def get(self) -> dict[int, DataStorageType]: return cast(dict[int, DataStorageType], self.data)

  def set(self, data: dict[int, DataStorageType]) -> None:
    if len(data) > 0:
      data_value_type: Type = type(list(data.values())[0])
      if data_value_type != self.STORAGE_TYPE:
        raise TypeError(f"Value type of {data=} doesn't match with value type of {self.STORAGE_TYPE=}.")
    self.__data = data