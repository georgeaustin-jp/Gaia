from math import pow, exp2

from tools.typing_tools import *
from tools.generation_tools import generate_float_in_range
from tools.constants import Constants

# decision error

def get_decision_error_bound(intelligence: float) -> float:
  if intelligence == 0: raise ValueError(f"{intelligence=} cannot be 0.")
  return 5 / intelligence

def generate_decision_error(error_bound: float) -> float:
  return generate_float_in_range(-1*error_bound, error_bound)

# aggressiveness calculations

def calculate_health_aggressiveness(health: float, max_health: float) -> float:
  """
  :return: In interval `[-1,1]`.
  :rtype: float
  """
  return health * (2 / max_health) - 1

def calculate_ignited_aggressiveness(health: float, max_health: float, remaining_duration: int, is_ignited: bool) -> float:
  if not is_ignited: return 0
  m: float = (1 / 2*max_health) * ((remaining_duration) / Constants.IGNITE_DURATION - (1 / 5*max_health))
  c: float = - (remaining_duration / 2*Constants.IGNITE_DURATION)
  return m*health + c

def calculate_damage_resistance_aggressiveness(damage_resistance: float, is_pierced: bool) -> float:
  """
  :return: In interval `[-1,1]`.
  :rtype: float
  """
  if is_pierced: return 0
  return exp2(damage_resistance)-1

def calculate_target_parry_aggressiveness(is_target_parrying: bool) -> float:
  if is_target_parrying: return -0.75
  return 0.1
