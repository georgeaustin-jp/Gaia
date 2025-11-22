from types import FunctionType

class Condition:
  def __init__(self, condition: FunctionType) -> None:
    self.condition: FunctionType = condition

  def set_condition(self, condition: FunctionType) -> None:
    self.condition: FunctionType = condition

  def get_condition(self) -> FunctionType:
    return self.condition
  
  def evaluate(self, identifier: int, row: list) -> bool:
    return self.condition(identifier, row)