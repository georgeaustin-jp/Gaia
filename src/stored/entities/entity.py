from database.condition import Condition
from tools.typing_tools import *

from stored.stored import *

class Entity(Stored):
  def __init__(self, name: str, max_health: float, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.name = name
    self.max_health = max_health

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.name, self.max_health]
  
  @staticmethod
  def instantiate(entity_data: list[Any], loaded: bool = True):
    return instantiate_entity(entity_data, loaded)
  
  @staticmethod
  def identical_condition(entity_row) -> Condition:
    return Condition(lambda _, row: entity_row[0] == row[0])
  

def instantiate_entity(entity_data: list[Any], loaded: bool = True) -> Entity:
  name: str = entity_data[0]
  max_health: float = entity_data[1]
  return Entity(name, max_health, loaded)
