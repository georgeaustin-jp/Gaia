from tools.typing_tools import *
from tools.constants import TableName
from tools.logging_tools import * # required for `Loggable`

from database.condition import Condition

class Stored(Loggable):
  """
  Abstract class for all objects which represent something stored in the database.
  
  When a new subclass is defined, the following methods must be defined for it:
  * `get_table_name() -> str` *(static method)* - gets the name of the table which the objects will be stored and loaded from.
  * `get_raw_data(self) -> list[Any]` - gets the data of the object in the form it is stored in the `Database` object.
  * `instantiate(data: list[Any], loaded: bool = True) -> object` *(static method)* - calls an instantiation function defined outside of the function itself, providing a secondary constructor when being created using the raw data of the object. 
  * `identical_condition(_stored_row: list[Any]) -> Condition` *(static method)* - creates a `Condition` which defines what makes two objects identical.
  """
  def __init__(self, loaded: bool = True, is_logging_enabled: bool = False, label: Optional[str] = None, include_call_stack: bool = False) -> None:
    super().__init__(is_logging_enabled, label, include_call_stack)
    self.loaded = loaded

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]: return []

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_stored(data, loaded)
  
  @staticmethod
  def identical_condition(_stored_row: list[Any]) -> Condition:
    return lambda _, _row: False

def instantiate_stored(_stored_data: list[Any] = [], loaded: bool = True) -> Stored:
  return Stored()

"""
Subclass template:

from tools.typing_tools import *

from database.condition import Condition
from stored.stored import *

class SUBCLASS(Stored):
  def __init__(self, loaded: bool = True) -> None:
    super().__init__(loaded)

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.

  def get_raw_data(self) -> list[Any]: return []

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_sub_class(data, loaded)
  
  @staticmethod
  def identical_condition(sub_class_row: list[Any]) -> Condition:
    return lambda _, row: False

def instantiate_sub_class(sub_class_data: list[Any] = [], loaded: bool = True) -> SUBCLASS:
  return SUBCLASS()

"""