from database.condition import Condition
from tools.typing_tools import *
from tools.constants import TableName

from stored.stored import Stored

class User(Stored):
  def __init__(self, name: str, password_hash: str, character_quantity: int = 0, world_quantity: int = 0, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.name: str = name
    self.password_hash: str = password_hash
    self.character_quantity: int = character_quantity
    self.world_quantity: int = world_quantity

    self.weapon_indexes: list[int] = []

  @staticmethod
  def get_table_name() -> TableName: return TableName.USER

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.name, self.password_hash, self.character_quantity, self.world_quantity]
  
  @staticmethod
  def instantiate(user_data: list[Any], loaded: bool = True):
    return instantiate_user(user_data, loaded)
  
  @staticmethod
  def identical_condition(user_row: list[Any]) -> Condition:
    return Condition(lambda _, row: user_row[0] == row[0])
  
def instantiate_user(user_data: list[Any], loaded: bool = True) -> User:
  name: str = user_data[0]
  password_hash: str = user_data[1]
  character_quantity: int = user_data[2]
  world_quantity = user_data[3]
  return User(name, password_hash, character_quantity, world_quantity, loaded)
