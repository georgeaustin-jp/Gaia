from tools.typing_tools import *
from tools.decision_tools import *

from stored.entities.fighting_entity import *
from database.condition import Condition

from data_structures.queue import Queue

#"CharacterID", "UserID", "Name", "Health", "MaxHealth",
class Character(FightingEntity):
  def __init__(self, user_id: int, name: str, health: float, max_health: float, loaded: bool = True) -> None:
    """
    Docstring for __init__
    
    :param user_id: User who the `Character` object is attatched to.
    :type user_id: int
    :param name: Name of the character.
    :type name: str
    :param health: How much health the character currently has.
    :type health: float
    """
    super().__init__(name, health, max_health, loaded)
    self.user_id = user_id

  @staticmethod
  def get_table_name() -> TableName: return TableName.CHARACTER

  def get_raw_data(self) -> list[Any]:
    return [self.user_id, self.name, self.health, self.max_health]
  
  @staticmethod
  def instantiate(character_data: list[Any], loaded: bool = True):
    return instantiate_character(character_data, loaded)
  
  @staticmethod
  def identical_condition(entity_row: list[Any]) -> Condition:
    return Condition(lambda _, row: entity_row[0] == row[0] and entity_row[1] == row[1])
  
  @staticmethod
  def get_default_max_health() -> float: return 100

  # built-in methods

  def __repr__(self) -> str:
    return f"Character({self.user_id}, {self.name=}, {self.health=}, {self.max_health=})"
  
  # methods for enemy decision making

  

def instantiate_character(character_data: list[Any], loaded: bool = True) -> Character:
  user_id: int = character_data[0]
  name: str = character_data[1]
  health: float = character_data[2]
  max_health: float = character_data[3]
  return Character(user_id, name, health, max_health, loaded)