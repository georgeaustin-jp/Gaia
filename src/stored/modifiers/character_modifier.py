from tools.typing_tools import *
from tools.constants import TableName

from database.condition import Condition
from stored.stored import Stored

class CharacterModifier(Stored):
  def __init__(self, loaded: bool = True) -> None:
    # CharacterID, AbilityID, RemainingTurns
    super().__init__(loaded)

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]: return []

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_character_modifier(data, loaded)
  
  @staticmethod
  def identical_condition(character_modifier_row: list[Any]) -> Condition:
    return lambda _, row: False

def instantiate_character_modifier(character_modifier_data: list[Any] = [], loaded: bool = True) -> CharacterModifier:
  return CharacterModifier()