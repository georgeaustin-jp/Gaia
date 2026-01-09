from database.condition import Condition
from stored.stored import *

from tools.typing_tools import *
from tools.ability_names import AbilityTypeName

class Ability(Stored):
  """
  :param text: The ability's description.
  :type text: str
  :param ability_type: The ability type table which the ability data can be found in.
  :type ability_type: AbilityTypeName
  """
  def __init__(self, text: str, ability_type: AbilityTypeName, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.text = text
    self.ability_type = ability_type

  @staticmethod
  def get_table_name() -> TableName: return TableName.ABILITY

  def get_raw_data(self) -> list[Any]:
    return [self.text, self.ability_type]
  
  @staticmethod
  def instantiate(ability_data: list[Any], loaded: bool = True):
    return instantiate_ability(ability_data, loaded)
  
  @staticmethod
  def identical_condition(stored_row: list[Any]) -> Condition:
    return Condition(lambda _identifier, row: stored_row[0] == row[0] and stored_row[1] == row[1])
  
  # built-in methods

  def __repr__(self) -> str:
    return f"Ability(`{self.text=}`, `{self.ability_type=}`)"
  
def instantiate_ability(ability_data: list[Any], loaded: bool = True) -> Ability:
  text: str = ability_data[0]
  ability_type: AbilityTypeName = ability_data[1]
  return Ability(text, ability_type, loaded)