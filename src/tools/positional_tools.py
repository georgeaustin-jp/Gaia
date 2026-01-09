from tools.typing_tools import *
from tools.exceptions import InvalidPositionError
from math import sqrt, pow

# decorators

def validate_position(dimensions: Position) -> Callable[[Position], None]:
  def inner(position: Position) -> None:
    if position[0] >= dimensions[0] or position[1] >= dimensions[1] or position[0] < 0 or position[1] < 0:
      raise InvalidPositionError(position, dimensions)
  return inner

def validate_position_on[T](func: Callable[..., T]) -> Callable[..., T]:
  """When being applied to a method in `Matrix` or `FightingEnemyGraph`, `position` must always be the first argument."""
  def wrapper(self, position: Position, *args, **kwargs) -> T:
    validate_position(self.dimensions)(position)
    return func(self, position, *args, **kwargs)
  return wrapper

# functions

def length_to_point(length: int, dimensions: Position) -> Position:
    x: int = length % dimensions[0]
    y: int = length // dimensions[0]
    position: Position = (x,y)
    validate_position(dimensions)(position)
    return position

def calculate_distance(p1: Position, p2: Position) -> float:
    (x1, y1) = p1
    (x2, y2) = p2
    return sqrt(pow(x1-x2, 2) + pow(y1-y2, 2))