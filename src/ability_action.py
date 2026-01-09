from tools.typing_tools import *
from tools.constants import Constants
#from tools.ability_names import AbilityTypeName

#from stored.abilities.ability import Ability

@dataclass
class AbilityAction():
  """Abstract base class with subclasses of `ParryAction`, `IgniteAction`, `DefendAction`, `WeakenAction` and `PierceAction`"""
  initial_duration: Optional[int]

@dataclass
class IgniteAction(AbilityAction):
  """Ignites the target, dealing a set amount of damage for a set amount of turns."""
  initial_duration: int = Constants.IGNITE_DURATION

@dataclass
class PierceAction(AbilityAction):
  """Pierce attacks will ignore parries."""
  initial_duration: int = 1

@dataclass
class ParryAction(AbilityAction):
  damage_threshold: float = 0
  reflection_proportion: float = 0
  initial_duration: int = 1

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

@dataclass
class WeakenAction(AbilityAction):
  """Increases damage vulnerability (inverse of `DefendAction`)."""
  vulnerability: float = 0