from tools.typing_tools import *

from database.condition import Condition
from stored.stored import *

class AbstractItem(Stored):
  def __init__(self, loaded: bool = True) -> None:
    super().__init__(loaded)

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]: return []

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_abstract_item(data, loaded)
  
  @staticmethod
  def identical_condition(abstract_item_row: list[Any]) -> Condition:
    return lambda _, row: False

def instantiate_abstract_item(abstract_item_data: list[Any] = [], loaded: bool = True) -> AbstractItem:
  return AbstractItem()