from tools.typing_tools import *
from tools.constants import Constants

from database.condition import Condition
from stored.abilities.abstract_ability import *

from tools.ability_names import AbilityTypeName

class StatisticAbility(AbstractAbility):
  def __init__(self, ability_id: int, ability_type: AbilityTypeName, amount: float, initial_duration: Optional[int], loaded: bool = True) -> None:
    super().__init__(ability_id, loaded)
    self.ability_type: AbilityTypeName = ability_type
    self.amount: float = amount
    self.initial_duration: Optional[int] = initial_duration

  @staticmethod
  def get_table_name() -> TableName: return TableName.STATISTIC_ABILITY

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.ability_type, self.amount, self.initial_duration]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_statistic_ability(data, loaded)
  
  @staticmethod
  def identical_condition(statistic_ability_row: list[Any]) -> Condition:
    return Condition(lambda _, row: statistic_ability_row[0] == row[0])
  
  # offensiveness and decision-making methods

  def calculate_offensiveness(self, **kwargs) -> float:
    if self.ability_type == AbilityTypeName.HEAL:
      health: float = kwargs["health"]
      max_health: float = kwargs["max_health"]
      healing: float = self.amount
      return min(health/(max_health - healing), 0)
    elif self.ability_type == AbilityTypeName.PIERCE:
      return Constants.PIERCE_OFFENSIVENESS
    elif self.ability_type == AbilityTypeName.PIERCE:
      return Constants.PIERCE_OFFENSIVENESS
    raise ValueError(f"`{self.ability_type=}` is invalid.")

def instantiate_statistic_ability(statistic_ability_data: list[Any], loaded: bool = True) -> StatisticAbility:
  ability_id: int = statistic_ability_data[0]
  ability_type: AbilityTypeName = statistic_ability_data[1]
  amount: float = statistic_ability_data[2]
  initial_duration: Optional[int] = statistic_ability_data[3]
  return StatisticAbility(ability_id, ability_type, amount, initial_duration, loaded)