from database.condition import Condition
from tools.typing_tools import *

from stored.items.abstract_item import *

class Equipable(AbstractItem):
  def __init__(self, item_id: int, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.item_id = item_id

  @staticmethod
  def get_table_name() -> TableName: return TableName.EQUIPABLE

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.item_id]
  
  @staticmethod
  def instantiate(equipable_data: list[Any], loaded: bool = True):
    return instantiate_equipable(equipable_data, loaded)
  
  @staticmethod
  def identical_condition(_stored_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_equipable(equipable_data: list[Any], loaded: bool = True) -> Equipable:
  item_id: int = equipable_data[0]
  return Equipable(item_id, loaded)