from tools.typing_tools import *

from database.condition import Condition
from stored.stored import *

from ability_action import AbilityAction

class AbstractAbility(Stored):
  def __init__(self, ability_id: int, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.ability_id: int = ability_id

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]:
    return [self.ability_id]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_abstract_ability(data, loaded)
  
  @staticmethod
  def identical_condition(abstract_ability_row: list[Any]) -> Condition:
    return lambda _, row: False
  
  # offensiveness and decision-making methods

  def calculate_offensiveness(self) -> float: raise NotImplementedError()

  def get_ability_action(self) -> AbilityAction: raise NotImplementedError()

def instantiate_abstract_ability(abstract_ability_data: list[Any] = [], loaded: bool = True) -> AbstractAbility:
  ability_id: int = abstract_ability_data[0]
  return AbstractAbility(ability_id, loaded)