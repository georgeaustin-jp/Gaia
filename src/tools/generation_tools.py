import random

from tools.typing_tools import *
from tools.constants import Constants

# decorators

def validate_input_probability[ReturnType](func: Callable[Concatenate[float, ...], ReturnType]) -> Callable[Concatenate[float, ...], ReturnType]:
  def wrapper(p: float, *args, **kwargs) -> ReturnType:
    validate_probability(p)
    return func(p, *args, **kwargs)
  return wrapper

def validate_output_probability(func: Callable[..., float]) -> Callable[..., float]:
  def wrapper(*args, **kwargs) -> float:
    p: float = func(*args, **kwargs)
    validate_probability(p)
    return p
  return wrapper

def validate_bounds[ReturnType](exclusive: bool = True) -> Callable[[Callable[..., ReturnType]], Callable[..., ReturnType]]:
  def decorator(func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
    def wrapper(lower: Numeric, upper: Numeric, *args, **kwargs) -> ReturnType:
      if lower > upper: raise ValueError(f"Bound {lower=} is greater than bound {upper=} ({exclusive=}).")
      if lower == upper and exclusive: raise ValueError(f"Bound {lower=} is equal to bound {upper=} ({exclusive=}).")
      return func(lower, upper, *args, **kwargs)
    return wrapper
  return decorator

# functions
## probabilities and floats
def validate_probability(p: float) -> None:
  """Returns successfully if `p` is in the interval [0,1] (inclusive). Otherwise, raises an appropriate error."""
  if p < 0: raise ValueError(f"Probability {p=} cannot be less than 0.")
  if p > 1: raise ValueError(f"Probability {p=} cannot be greater than 1.")
  return None

@validate_bounds()
def generate_float_in_range(lower: Numeric, upper: Numeric) -> float:
  return round(random.uniform(lower, upper), Constants.DEFAULT_ROUNDING_ACCURACY)

@validate_output_probability
def generate_probability_value() -> float:
  """Generates a random real number in the interval `[0,1]` (inclusive) using a distribution."""
  return generate_float_in_range(0,1)

@validate_input_probability
def evaluate_probability(p: float) -> bool:
  value: float = generate_probability_value()
  if p > value or p == 1: return True
  return False

def is_combat_encounter() -> bool: return evaluate_probability(Constants.COMBAT_ENCOUNTER_PROBABILITY)

def is_structure_encounter() -> bool: return evaluate_probability(Constants.STRUCTURE_ENCOUNTER_PROBABILITY)

def is_boss_encounter() -> bool: return evaluate_probability(Constants.BOSS_ENCOUNTER_PROBABILITY)

## integers
@validate_bounds()
def generate_random_int_in_range(lower: int, upper: int) -> int:
  """Returns an integer in the interval `[lower, upper)` (not inclusive)."""
  if lower >= upper: raise ValueError(f"Bound {lower=} cannot be greater than or equal to bound {upper=}.")
  return random.randrange(lower, upper)

def generate_structure_item_count() -> int: return generate_random_int_in_range(Constants.MIN_STRUCTURE_ITEM_COUNT, Constants.MAX_STRUCTURE_ITEM_COUNT)

def generate_enemy_count() -> int: return generate_random_int_in_range(Constants.MIN_ENEMIES, Constants.MAX_ENEMIES)

def select_random_identifier(dictionary: dict[int, Any]) -> int:
  identifiers: list[int] = list(dictionary.keys())
  selected_index: int = generate_random_int_in_range(0, len(identifiers))
  return identifiers[selected_index]

def get_random_position(dimensions: Position) -> Position:
  x: int = generate_random_int_in_range(0, dimensions[0])
  y: int = generate_random_int_in_range(0, dimensions[1])
  return (x,y)