from database.condition import Condition
from tools.typing_tools import *
from tools.constants import TableName

from stored.stored import Stored

class User(Stored):
  def __init__(self, name: str, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.name: str = name

    self.weapon_indexes: list[int] = []

  @staticmethod
  def get_table_name() -> TableName: return TableName.USER

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.name]
  
  @staticmethod
  def instantiate(user_data: list[Any], loaded: bool = True):
    return instantiate_user(user_data, loaded)
  
  @staticmethod
  def identical_condition(user_row: list[Any]) -> Condition:
    return lambda _, row: user_row[0] == row[0]
  
def instantiate_user(user_data: list[Any], loaded: bool = True) -> User:
  name: str = user_data[0]
  return User(name, loaded)
