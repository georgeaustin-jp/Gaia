from tools.typing_tools import *

from tools.logging_tools import *

from database.condition import Condition
from stored.items.abstract_item import *

class Weapon(AbstractItem):
  def __init__(self, item_id: int, damage: float, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.item_id = item_id
    self.damage = damage

  @staticmethod
  def get_table_name() -> TableName: return TableName.WEAPON

  def get_raw_data(self) -> list[Any]:
    return [self.item_id, self.damage]

  @staticmethod
  def instantiate(weapon_data: list[Any], loaded: bool = True):
    return instantiate_weapon(weapon_data, loaded)
  
  @staticmethod
  def identical_condition(weapon_row: list[Any]) -> Condition:
    return lambda _, row: weapon_row[0] == row[0]
  
  # built-in methods

  def __repr__(self) -> str:
    return f"Weapon({self.item_id=}, {self.damage=})"

def instantiate_weapon(weapon_data: list[Any], loaded: bool = True) -> Weapon:
  item_id: int = weapon_data[0]
  damage: float = weapon_data[1]
  return Weapon(item_id, damage, loaded)