from tools.typing_tools import *

from database.condition import Condition
from stored.stored import *

class AbstractStorageItem(Stored):
  def __init__(self, item_id: int, stack_size: int, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.item_id = item_id
    self.stack_size = stack_size

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]:
    return [self.item_id, self.stack_size]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_abstract_storage_item(data, loaded)
  
  @staticmethod
  def identical_condition(abstract_storage_item_row: list[Any]) -> Condition:
    return lambda _, row: False

def instantiate_abstract_storage_item(abstract_storage_item_data: list[Any] = [], loaded: bool = True) -> AbstractStorageItem:
  item_id: int = abstract_storage_item_data[0]
  stack_size: int = abstract_storage_item_data[1]
  return AbstractStorageItem(item_id, stack_size, loaded)