from tools.typing_tools import *
from tools.constants import Constants, DecisionMakingConstants
from tools.ability_names import AbilityTypeName
from tools.custom_exceptions import AbstractMethodCallError
from tools.decision_tools import *

@dataclass
class AbilityAction():
  """Abstract base class for all ability actions.
  
  Subclasses of `ParryAction`, `IgniteAction`, `DefendAction`, `WeakenAction`, `HealAction` and `PierceAction`."""
  initial_duration: Optional[int]
  is_unique: bool

  # built-in methods

  def __eq__(self, other) -> bool:
    return isinstance(other, self.__class__) and self.initial_duration == other.initial_duration and self.is_unique == other.is_unique
  
  # getter and setter methods

  def get_initial_duration(self) -> Optional[int]:
    return self.initial_duration
  
  def get_is_unique(self) -> bool:
    return self.is_unique

  # abstract methods

  def get_ability_type_name(self) -> AbilityTypeName: raise AbstractMethodCallError(AbilityAction.__name__, self.get_ability_type_name.__name__)

  def calculate_offensiveness(self) -> float: raise AbstractMethodCallError(AbilityAction.__name__, self.calculate_offensiveness.__name__)

@dataclass
class IgniteAction(AbilityAction):
  """Ignites the target, dealing a set amount of damage for a set amount of turns."""
  is_unique: bool = True
  initial_duration: int = Constants.IGNITE_DURATION

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.IGNITE

  def calculate_offensiveness(self) -> float:
    return DecisionMakingConstants.IGNITE_OFFENSIVENESS

@dataclass
class PierceAction(AbilityAction):
  """Pierce attacks will ignore parries."""
  is_unique: bool = True
  initial_duration: int = 1

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.PIERCE

  def calculate_offensiveness(self) -> float:
    return DecisionMakingConstants.PIERCE_OFFENSIVENESS

@dataclass
class ParryAction(AbilityAction):
  damage_threshold: float = 0
  reflection_proportion: float = 0
  initial_duration: int = 1
  is_unique: bool = True

  def __eq__(self, other) -> bool:
    return super().__eq__(other) and self.damage_threshold == other.damage_threshold and self.reflection_proportion == other.reflection_proportion

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.PARRY

  def calculate_offensiveness(self) -> float:
    return calculate_parry_aggressiveness(self.damage_threshold, self.reflection_proportion)

  @staticmethod
  def get_reflected_damage(damage: float, damage_threshold: float, reflection_proportion: float) -> float:
    if reflection_proportion > 1: raise ValueError(f"{reflection_proportion=} cannot be less than `1`.")
    return min(damage, damage_threshold) * reflection_proportion

  @staticmethod
  def parry_damage(damage: float, damage_threshold: float, reflection_proportion: float) -> tuple[float, float]:
    """
    :return: A pair of floats. The first is the amount of damage inflicted to the target. The second is the amount of damage reflected back to the attacker.
    :rtype: tuple[float, float]
    """
    target_damage: float = max(damage - damage_threshold, 0)
    
    reflected_damage = ParryAction.get_reflected_damage(damage, damage_threshold, reflection_proportion)

    return (target_damage, reflected_damage)

@dataclass
class DefendAction(AbilityAction):
  """Increases damage resistance."""
  resistance: float = 0

  def __eq__(self, other) -> bool:
    return super().__eq__(other) and self.resistance == other.resistance

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.DEFEND

  def calculate_offensiveness(self) -> float:
    return calculate_damage_resistance_aggressiveness(-1*self.resistance, False)

@dataclass
class WeakenAction(AbilityAction):
  """Increases damage vulnerability (inverse of `DefendAction`)."""
  vulnerability: float = 0

  def __eq__(self, other) -> bool:
    return super().__eq__(other) and self.vulnerability == other.vulnerability

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.WEAKEN

  def calculate_offensiveness(self) -> float:
    return calculate_damage_resistance_aggressiveness(self.vulnerability, False)

@dataclass
class HealAction(AbilityAction):
  initial_duration: Optional[int] = 1
  is_unique: bool = False
  heal_amount: float = 0

  def __eq__(self, other) -> bool:
    return super().__eq__(other) and self.heal_amount == other.heal_amount

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.HEAL

  def calculate_offensiveness(self) -> float:
    return calculate_healing_aggressiveness(self.heal_amount)