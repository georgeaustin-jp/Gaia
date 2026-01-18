from tools.typing_tools import *

type Condition = Callable[[int, list[Any]], bool]

def everything() -> Condition: return lambda _identifier, _row: True

def nothing() -> Condition: return lambda _identifier, _row: False

def matching_identifiers(specific_identifier: int) -> Condition:
  return lambda identifier, _row: specific_identifier == identifier

def get_condition_inverse(condition: Condition) -> Condition:
  return lambda identifier, row: not condition(identifier, row)