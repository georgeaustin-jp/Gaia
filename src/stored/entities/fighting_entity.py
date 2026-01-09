from tools.typing_tools import *
from tools.exceptions import HealthSetError
from tools.decision_tools import *

from stored.stored import *

from data_structures.queue import Queue

from ability_action import *

class FightingEntity(Stored):
  def __init__(self, name: str, health: float, max_health: float, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.name = name
    self.max_health = max_health
    self.health = health
    # attributes not stored in the database, but which are still important
    self.damage_resistance: float = 0
    self.is_ignited: bool = False
    self.is_pierced: bool = False
    # parrying data
    self.is_parrying: bool = False
    self.parry_damage_threshold: Optional[float] = None
    self.parry_reflection_proportion: Optional[float] = None

    self.aggressiveness: float = 0

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.health]
  
  @staticmethod
  def instantiate(fighting_entity_data: list[Any], loaded: bool = True):
    return instantiate_fighting_entity(fighting_entity_data, loaded)
  
  # variable-setting methods

  def set_health(self, new_health: float) -> None:
    if new_health > self.max_health or new_health < 0:
      raise HealthSetError(new_health, self.max_health)
    self.health = new_health

  def change_health(self, amount: float) -> None:
    new_health: float = self.health + amount
    if new_health < 0: new_health = 0
    elif new_health > self.max_health:
      new_health = self.max_health
    self.set_health(new_health)

  def take_damage(self, damage_amount: float) -> None:
    if not self.is_pierced or self.damage_resistance < 0:
      damage_amount = self.apply_damage_resistance(damage_amount)
    if damage_amount < 0: raise ValueError(f"{damage_amount=} less than zero.")
    self.change_health(-1*damage_amount)

  def apply_damage_resistance(self, damage_amount: float) -> float:
    new_damage_amount: float = damage_amount * (1-self.damage_resistance)
    if new_damage_amount < 0: raise ValueError(f"`{new_damage_amount=}` is less than `0` after `{self.damage_resistance=}` was applied.")
    return new_damage_amount

  def heal(self, heal_amount: float) -> None:
    if heal_amount < 0:
      raise ValueError(f"{heal_amount=} less than zero.")
    self.change_health(heal_amount)

  # ability / modifier methods

  def apply_ability(self, ability: AbilityAction) -> None:
    if type(ability) == IgniteAction: self.ignite()
    elif type(ability) == DefendAction: self.defend(ability.resistance)
    elif type(ability) == WeakenAction: self.weaken(ability.vulnerability)
    elif type(ability) == PierceAction: self.pierce()
    elif type(ability) == ParryAction: self.engage_parry(ability.damage_threshold, ability.reflection_proportion)

  def inflict_active_effects(self) -> None:
    if self.is_ignited: self.deal_ignite()

  def remove_ability(self, ability: AbilityAction) -> None:
    if type(ability) == IgniteAction: self.unignite()
    elif type(ability) == DefendAction: self.undefend(ability.resistance)
    elif type(ability) == WeakenAction: self.unweaken(ability.vulnerability)
    elif type(ability) == PierceAction: self.unpierce()
    elif type(ability) == ParryAction: self.unengage_parry()

  ## ignition
  def ignite(self) -> None: self.is_ignited = True

  def deal_ignite(self) -> None:
    self.take_damage(Constants.IGNITE_DAMAGE)

  def unignite(self) -> None: self.is_ignited = False
  
  ## defending
  def defend(self, resistance: float) -> None:
    if resistance < 0: raise ValueError(f"{resistance=} cannot be less than `0`.")
    self.damage_resistance += resistance

  def undefend(self, resistance: float) -> None:
    if resistance < 0: raise ValueError(f"{resistance=} cannot be less than `0`.")
    self.damage_resistance -= resistance

  ## weakening
  def weaken(self, vulnerability: float) -> None:
    if vulnerability < 0: raise ValueError(f"{vulnerability=} cannot be less than `0`.")
    self.damage_resistance -= vulnerability

  def unweaken(self, vulnerability: float) -> None:
    if vulnerability < 0: raise ValueError(f"{vulnerability=} cannot be less than `0`.")
    self.damage_resistance += vulnerability

  ## piercing
  def pierce(self) -> None: self.is_pierced = True

  def unpierce(self) -> None: self.is_pierced = False

  ## parrying
  def engage_parry(self, damage_threshold: float, reflection_proportion: float) -> None:
    if damage_threshold <= 0: raise ValueError(f"`{damage_threshold=}` cannot be less than or equal to `0`.")
    if reflection_proportion < 0: raise ValueError(f"`{reflection_proportion=}` cannot be less than `0`.")
    self.is_parrying = True
    self.parry_damage_threshold = damage_threshold
    self.parry_reflection_proportion = reflection_proportion

  def unengage_parry(self) -> None:
    self.is_parrying = False
    self.parry_damage_threshold = None
    self.parry_reflection_proportion = None

  # decision-making

  def calculate_aggressiveness_info(self, remaining_ignition_duration: int, is_target_parrying: bool) -> tuple[float, int]:
    """
    :return: A pair of numbers, the first being the total aggressiveness and the second being the number of values computed.
    :rtype: tuple[float, int]
    """
    aggressiveness_values = Queue[float]()
    aggressiveness_values.put(self.calculate_health_aggressiveness())
    aggressiveness_values.put(self.calculate_ignited_aggressiveness(remaining_ignition_duration))
    aggressiveness_values.put(self.calculate_damage_resistance_aggressiveness())
    aggressiveness_values.put(self.calculate_target_parry_aggressiveness(is_target_parrying))
    n: int = 0
    total: float = 0
    while not aggressiveness_values.empty():
      total += aggressiveness_values.get()
      n += 1
    return (total, n)

  def calculate_aggressiveness(self, remaining_ignition_duration: int, is_target_parrying: bool) -> float:
    (total, n) = self.calculate_aggressiveness_info(remaining_ignition_duration, is_target_parrying)
    return total/n

  def calculate_health_aggressiveness(self) -> float:
    """
    :return: In interval `[-1,1]`.
    :rtype: float
    """
    return calculate_health_aggressiveness(self.health, self.max_health)
  
  def calculate_ignited_aggressiveness(self, remaining_duration: int) -> float:
    return calculate_ignited_aggressiveness(self.health, self.max_health, remaining_duration, self.is_ignited)
  
  def calculate_damage_resistance_aggressiveness(self) -> float:
    """
    :return: In interval `[-1,1]`.
    :rtype: float
    """
    return calculate_damage_resistance_aggressiveness(self.damage_resistance, self.is_pierced)
  
  def calculate_target_parry_aggressiveness(self, is_target_parrying: bool) -> float:
    return calculate_target_parry_aggressiveness(is_target_parrying)
  
  def calculate_aggressiveness_squared_deviation(self, offensiveness: float) -> float:
    return pow(self.aggressiveness - offensiveness, 2)

def instantiate_fighting_entity(fighting_entity_data: list[Any], loaded: bool = True) -> FightingEntity:
  name: str = fighting_entity_data[0]
  health: float = fighting_entity_data[1]
  max_health: float = fighting_entity_data[2]
  return FightingEntity(name, health, max_health, loaded)
