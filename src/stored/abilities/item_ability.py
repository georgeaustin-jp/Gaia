from tools.typing_tools import *

from database.condition import Condition
from stored.stored import *

class ItemAbility(Stored):
  """
  :param item_id: The item which this links to.
  :type item_id: int
  :param ability_id: The ability which this links to.
  :type ability_id: int
  """
  def __init__(self, item_id: int, ability_id: int, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.item_id = item_id
    self.ability_id = ability_id

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.ITEM_ABILITY

  def get_raw_data(self) -> list[Any]:
    return [self.item_id, self.ability_id]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_item_ability(data, loaded)
  
  @staticmethod
  def identical_condition(item_ability_row: list[Any]) -> Condition:
    return lambda _, row: False
  
  # built-in methods

  def __repr__(self) -> str:
    return f"ItemAbility({self.item_id=}, {self.ability_id=})"

def instantiate_item_ability(item_ability_data: list[Any] = [], loaded: bool = True) -> ItemAbility:
  item_id: int = item_ability_data[0]
  ability_id: int = item_ability_data[1]
  return ItemAbility(item_id, ability_id, loaded)