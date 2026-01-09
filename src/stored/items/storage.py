from tools.typing_tools import *
from tools.constants import *

from database.condition import Condition
from stored.stored import *

class Storage(Stored):
  def __init__(self, world_id: int, storage_type: StorageType, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.world_id = world_id
    self.storage_type = storage_type

  @staticmethod
  def get_table_name() -> TableName: return TableName.STORAGE

  def get_raw_data(self) -> list[Any]:
    return [self.world_id, self.storage_type]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_storage(data, loaded)
  
  @staticmethod
  def identical_condition(storage_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_storage(storage_data: list[Any] = [], loaded: bool = True) -> Storage:
  world_id: int = storage_data[0]
  storage_type: StorageType = storage_data[1]
  return Storage(world_id, storage_type, loaded)