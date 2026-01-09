from math import exp2

from tools.typing_tools import *

from database.condition import Condition
from stored.abilities.abstract_ability import *

class ParryAbility(AbstractAbility):
  def __init__(self, ability_id: int, damage_threshold: float, reflection_proportion: float, loaded: bool = True) -> None:
    #"ParryAbilityID", "AbilityID", "DamageThreshold", "ReflectionProportion"
    super().__init__(ability_id, loaded)
    self.damage_threshold = damage_threshold
    self.reflection_proportion = reflection_proportion
  
  @staticmethod
  def get_table_name() -> TableName: return TableName.PARRY_ABILITY

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.damage_threshold, self.reflection_proportion]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_parry_ability(data, loaded)
  
  @staticmethod
  def identical_condition(parry_ability_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)
  
  # built-in methods

  def __repr__(self) -> str:
    return f"ParryAbility(`{self.ability_id=}`, `{self.damage_threshold=}`, `{self.reflection_proportion=}`)"
  
  # offensiveness and decision-making methods

  def calculate_offensiveness(self) -> float:
    return self.reflection_proportion * (1 - exp2(-1*self.damage_threshold))

def instantiate_parry_ability(parry_ability_data: list[Any] = [], loaded: bool = True) -> ParryAbility:
  ability_id: int = parry_ability_data[0]
  damage_threshold: float = parry_ability_data[1]
  reflection_proportion: float = parry_ability_data[2]
  return ParryAbility(ability_id, damage_threshold, reflection_proportion, loaded)