from tools.typing_tools import *

from tools.dictionary_tools import filter_dictionary

class Condition:
  def __init__(self, condition: Callable[[int, list[Any]], bool]) -> None:
    self.condition: Callable[[int, list[Any]], bool] = condition

  def set_condition(self, condition: Callable[[int, list[Any]], bool]) -> None:
    self.condition = condition

  def get_condition(self) -> Callable[[int, list[Any]], bool]:
    return self.condition
  
  def evaluate(self, identifier: int, row: list[Any]) -> bool:
    return self.condition(identifier, row)
  
def filter_dictionary_with_condition(dictionary: dict[int, list[Any]], condition: Condition) -> dict[int, list[Any]]:
  return filter_dictionary(dictionary, condition.get_condition())

def everything() -> Condition: return Condition(lambda _identifier, _row: True)

def nothing() -> Condition: return Condition(lambda _identifier, _row: False)

def matching_identifiers(specific_identifier: int) -> Condition:
  return Condition(lambda identifier, _row: specific_identifier == identifier)

def get_condition_inverse(condition: Condition) -> Condition:
  return Condition(lambda identifier, row: not condition.get_condition()(identifier, row))