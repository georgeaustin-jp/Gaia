from tools.typing_tools import *
from tools.constants import TableName

from stored.stored import Stored

class World(Stored):
  """
  Class to represent each world.

  :param user_id: The user which the world is linked to.
  :type user_id: int
  :param name: The unique name of the world.
  :type name: str
  :param seed: the string which uniquely identifies how the world was generated.
  :type seed: str
  """
  def __init__(self, user_id: int, name: str, seed: str, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.user_id = user_id
    self.name = name
    self.seed = seed

  @staticmethod
  def get_table_name() -> TableName: return TableName.WORLD

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.user_id, self.name, self.seed]
  
  @staticmethod
  def instantiate(world_data: list[Any], loaded: bool = True):
    return instantiate_world(world_data, loaded)

def instantiate_world(world_data: list[Any], loaded: bool = True) -> World:
  user_id: int = world_data[0]
  name: str = world_data[1]
  seed: str = world_data[2]
  return World(user_id, name, seed, loaded)
