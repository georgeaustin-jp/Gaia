from tools.typing_tools import *
from tools.constants import TableName

from database.condition import Condition
from stored.stored import Stored

class AbstractModifier(Stored):
  def __init__(self, loaded: bool = True) -> None:
    super().__init__(loaded)

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]: return []

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_abstract_modifier(data, loaded)
  
  @staticmethod
  def identical_condition(abstract_modifier_row: list[Any]) -> Condition:
    return lambda _, row: False

def instantiate_abstract_modifier(abstract_modifier_data: list[Any] = [], loaded: bool = True) -> AbstractModifier:
  return AbstractModifier()