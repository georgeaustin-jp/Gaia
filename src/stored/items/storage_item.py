from tools.typing_tools import *

from database.condition import Condition
from stored.items.abstract_storage_item import *

class StorageItem(AbstractStorageItem):
  """
  Link between \'Storage\' and \'Item\' to allow items to be stored in an existing storage object.
  
  :param storage_id: The identifier for the storage whose contents the item is linked to.
  :type storage_id: int
  :param item_id: The identifier for the item stored in the storage.
  :type item_id: int
  :param stack_size: Amount of this item in the storage. Cannot go below 1.
  :type stack_size: int
  :param loaded: Whether the object has been loaded into memory or not. Defaults to \'True\'.
  :type loaded: bool
  """
  def __init__(self, storage_id: int, item_id: int, stack_size: int = 1, loaded: bool = True) -> None:
    super().__init__(item_id, stack_size, loaded)
    self.storage_id = storage_id

  @staticmethod
  def get_table_name() -> TableName: return TableName.STORAGE_ITEM

  def get_raw_data(self) -> list[Any]:
    return [self.storage_id] + super().get_raw_data()

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_storage_item(data, loaded)
  
  @staticmethod
  def identical_condition(storage_item_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_storage_item(storage_item_data: list[Any] = [], loaded: bool = True) -> StorageItem:
  storage_id: int = storage_item_data[0]
  item_id: int = storage_item_data[1]
  stack_size: int = storage_item_data[2]
  return StorageItem(storage_id, item_id, stack_size, loaded)