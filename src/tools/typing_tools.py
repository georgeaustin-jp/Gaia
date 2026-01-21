from collections.abc import Callable
from typing import Any, Concatenate, Self, Sized, Literal, Optional, Type, Union, cast
from enum import Enum, Flag, IntEnum, StrEnum, unique
from dataclasses import dataclass, field
from functools import reduce

# custom types

type ButtonCommand = Callable[[], None]
type Position = tuple[int, int]
"A discrete, `(x,y)` point on a 2D plane."
type ActionLocation = Optional[Position]
type EnemyActionTag = Union[Literal["Attack"], int]
"either \"Attack\" (denoting the enemy's attack), or the `AbilityID` of the `Ability` it will use"
type Numeric = Union[int, float]
"Any real number, being either a `float` or `int`."

type DynamicButtonInput = tuple[str, Union[Any, tuple[Any, ...]]]
"""
The significance of each value of the tuple is as follows:
1. `text` - what the text value of the button is set to
2. `args` - command positional arguments. If there is `0` or `1`, a collection need not be used, but any more requires a tuple.
"""

# functions

def unpack_optional[T](option: Optional[T]) -> T:
  """
  Converts an argument of unknown type from an optional to a non-optional. If the argument is `None`, a value error is raised.
  
  :param option: An optional variable. Must have a value not `None`, otherwise it will raise a value error.
  :type option: Optional[T]
  :return: The argument in non-optional form.
  :rtype: T
  """
  if option == None: raise ValueError(f"Tried to unpack argument \'option\'=`{option}`")
  return option

def unpack_optional_bool(option: Optional[bool], default: bool) -> bool:
  if option == True: return True
  return default

def unpack_optional_string(option: Optional[str], default: str = "") -> str:
  if option == None: return default
  return option