from tools.typing_tools import *

from stored.stored import *
from tools.constants import ItemType

class Item(Stored):
  def __init__(self, item_type: ItemType, name: str, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.item_type = item_type
    self.name = name

  @staticmethod
  def get_table_name() -> TableName: return TableName.ITEM

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.item_type, self.name]
  
  @staticmethod
  def instantiate(item_data: list[Any], loaded: bool = True):
    return instantiate_item(item_data, loaded)

def instantiate_item(item_data: list[Any], loaded: bool = True) -> Item:
  item_type: ItemType = item_data[0]
  name: str = item_data[1]
  return Item(item_type, name, loaded)