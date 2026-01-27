from math import exp2, sqrt, tanh

from tools.typing_tools import *
from tools.generation_tools import generate_float_in_range
from tools.constants import Constants, DecisionMakingConstants

# decision error

def get_decision_error_bound(intelligence: float) -> float:
  if intelligence == 0: raise ValueError(f"{intelligence=} cannot be 0.")
  return 5 / intelligence

def generate_decision_error(error_bound: float) -> float:
  return generate_float_in_range(-1*error_bound, error_bound)

def clip(x: float, lower_bound: float, upper_bound: float) -> float:
  return min(max(x, lower_bound), upper_bound)

# aggressiveness calculations

def calculate_health_aggressiveness(health: float, max_health: float) -> float:
  """
  :return: In interval `[-1,1]`.
  :rtype: float
  """
  return health * (2 / max_health) - 1

def calculate_ignited_aggressiveness(health: float, max_health: float, remaining_duration: Optional[int]) -> float:
  if remaining_duration == None: return 0.1
  m: float = (1 / 2*max_health) * (remaining_duration / Constants.IGNITE_DURATION - (1 / 5*max_health))
  c: float = - (remaining_duration / 2*Constants.IGNITE_DURATION)
  return m*health + c

def calculate_damage_resistance_aggressiveness(damage_resistance: float, is_pierced: bool) -> float:
  """
  :return: In interval `[-1,1]`.
  :rtype: float
  """
  if is_pierced: return DecisionMakingConstants.PIERCE_OFFENSIVENESS
  return exp2(damage_resistance)-1

def calculate_parry_aggressiveness(reflection_proportion: Optional[float], damage_threshold: Optional[float]) -> float:
  if reflection_proportion == None or damage_threshold == None: return 0.3
  return sqrt(reflection_proportion * (2-reflection_proportion)) * (1 - exp2(damage_threshold*(-1/2)))

def calculate_healing_aggressiveness(amount: float) -> float:
  return -0.75*tanh(amount/5)
