from tools.typing_tools import *
from tools.constants import Constants
from tools.ability_names import AbilityTypeName

#from stored.abilities.ability import Ability

@dataclass
class AbilityAction():
  """Abstract base class for all ability actions.
  
  Subclasses of `ParryAction`, `IgniteAction`, `DefendAction`, `WeakenAction`, `HealAction` and `PierceAction`."""
  initial_duration: Optional[int]

  def get_ability_type_name(self) -> AbilityTypeName: raise NotImplementedError()

@dataclass
class IgniteAction(AbilityAction):
  """Ignites the target, dealing a set amount of damage for a set amount of turns."""
  initial_duration: int = Constants.IGNITE_DURATION

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.IGNITE

@dataclass
class PierceAction(AbilityAction):
  """Pierce attacks will ignore parries."""
  initial_duration: int = 1

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.PIERCE

@dataclass
class ParryAction(AbilityAction):
  damage_threshold: float = 0
  reflection_proportion: float = 0
  initial_duration: int = 1

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.PARRY

  @staticmethod
  def get_reflected_damage(damage: float, reflection_proportion: float) -> float:
    if reflection_proportion > 1: raise ValueError(f"{reflection_proportion=} cannot be less than `1`.")
    return damage * (1-reflection_proportion)

  @staticmethod
  def parry_damage(damage: float, damage_threshold: float, reflection_proportion: float) -> tuple[float, float]:
    """
    :return: A pair of floats. The first is the amount of damage inflicted to the target. The second is the amount of damage reflected back to the attacker.
    :rtype: tuple[float, float]
    """
    target_damage: float
    if damage <= damage_threshold:
      target_damage = 0
    else:
      target_damage = damage - damage_threshold
    
    reflected_damage: float = ParryAction.get_reflected_damage(damage, reflection_proportion)

    return (target_damage, reflected_damage)

@dataclass
class DefendAction(AbilityAction):
  """Increases damage resistance."""
  resistance: float = 0

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.DEFEND

@dataclass
class WeakenAction(AbilityAction):
  """Increases damage vulnerability (inverse of `DefendAction`)."""
  vulnerability: float = 0

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.WEAKEN

@dataclass
class HealAction(AbilityAction):
  initial_duration: int = 1
  heal_amount: float = 0

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.HEAL