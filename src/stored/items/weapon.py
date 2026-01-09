from tools.typing_tools import *

from database.condition import Condition
from stored.items.abstract_item import *

class Weapon(AbstractItem):
  def __init__(self, item_id: int, damage: float, uses_ammunition: bool = False, mana_used: float = 0, active: bool = False, loaded: bool = True) -> None: #TODO: add all parts of Weapon
    super().__init__(loaded)
    self.item_id = item_id
    self.damage = damage
    self.uses_ammunition = uses_ammunition
    self.mana_used = mana_used
    self.active = active

  @staticmethod
  def get_table_name() -> TableName: return TableName.WEAPON

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.item_id, self.damage, self.uses_ammunition, self.mana_used, self.active]

  @staticmethod
  def instantiate(weapon_data: list[Any], loaded: bool = True):
    return instantiate_weapon(weapon_data, loaded)
  
  @staticmethod
  def identical_condition(weapon_row: list[Any]) -> Condition:
    return Condition(lambda _, row: weapon_row[0] == row[0])
  
  # built-in methods

  def __repr__(self) -> str:
    return f"Weapon({self.item_id=}, {self.damage=}, {self.uses_ammunition=}, {self.mana_used=}, {self.active=})"

def instantiate_weapon(weapon_data: list[Any], loaded: bool = True) -> Weapon:
  item_id: int = weapon_data[0]
  damage: float = weapon_data[1]
  uses_ammunition: bool = weapon_data[2]
  mana_used: float = weapon_data[3]
  active: bool = weapon_data[4]
  return Weapon(item_id, damage, uses_ammunition, mana_used, active, loaded)