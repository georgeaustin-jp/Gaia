from tools.typing_tools import *
from tools.constants import Constants, DecisionMakingConstants
from tools.ability_names import AbilityTypeName

from database.condition import Condition
from stored.abilities.abstract_ability import *

from ability_action import *

class StatisticAbility(AbstractAbility):
  def __init__(self, ability_id: int, ability_type: AbilityTypeName, amount: float, initial_duration: Optional[int], is_unique: bool, loaded: bool = True) -> None:
    super().__init__(ability_id, loaded)
    self.ability_type: AbilityTypeName = ability_type
    self.amount: float = amount
    self.initial_duration: Optional[int] = initial_duration
    self.is_unique: bool = is_unique

  @staticmethod
  def get_table_name() -> TableName: return TableName.STATISTIC_ABILITY

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.ability_type, self.amount, self.initial_duration, self.is_unique]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_statistic_ability(data, loaded)
  
  @staticmethod
  def identical_condition(statistic_ability_row: list[Any]) -> Condition:
    return lambda _, row: statistic_ability_row[0] == row[0]
  
  # offensiveness and decision-making methods

  def calculate_offensiveness(self, **kwargs) -> float:
    match self.ability_type:
      case AbilityTypeName.HEAL:
        health: float = kwargs["health"]
        max_health: float = kwargs["max_health"]
        healing: float = self.amount
        return min(health/(max_health - healing), 0)
      case AbilityTypeName.WEAKEN:
        return calculate_damage_resistance_aggressiveness(self.amount, kwargs["is_pierced"])
      case AbilityTypeName.DEFEND:
        return calculate_damage_resistance_aggressiveness(-1*self.amount, kwargs["is_pierced"])
      case _:
        raise ValueError(f"`{self.ability_type=}` not recognised.")

  # ability action methods

  def get_ability_action(self) -> AbilityAction:
    match self.ability_type:
      case AbilityTypeName.HEAL:
        return HealAction(initial_duration=self.initial_duration, heal_amount=self.amount, is_unique=self.is_unique)
      case AbilityTypeName.WEAKEN:
        return WeakenAction(initial_duration=self.initial_duration, vulnerability=self.amount, is_unique=self.is_unique)
      case AbilityTypeName.DEFEND:
        return DefendAction(initial_duration=self.initial_duration, resistance=self.amount, is_unique=self.is_unique)
      case _:
        raise ValueError(f"`{self.ability_type=}` not recognised.")

def instantiate_statistic_ability(statistic_ability_data: list[Any], loaded: bool = True) -> StatisticAbility:
  ability_id: int = statistic_ability_data[0]
  ability_type: AbilityTypeName = statistic_ability_data[1]
  amount: float = statistic_ability_data[2]
  initial_duration: Optional[int] = statistic_ability_data[3]
  is_unique: bool = statistic_ability_data[4]
  return StatisticAbility(ability_id, ability_type, amount, initial_duration, is_unique, loaded)