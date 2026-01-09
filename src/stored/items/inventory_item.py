from tools.typing_tools import *

from database.condition import Condition
from stored.items.abstract_storage_item import *

class InventoryItem(AbstractStorageItem):
  """
  Link between \'Character\' and \'Item\' to allow items to be stored in the character's inventory.
  
  :param character_id: The identifier for the character whose inventory the item is linked to.
  :type character_id: int
  :param item_id: The identifier for the item stored in the inventory.
  :type item_id: int
  :param stack_size: Amount of this item in the inventory. Cannot go below 1.
  :type stack_size: int
  :param equipped: Is `True` if this item has been equipped to the character. For specific item types.
  :type equipped: bool
  :param loaded: Whether the object has been loaded into memory or not. Defaults to `True`.
  :type loaded: bool
  """
  def __init__(self, character_id: int, item_id: int, stack_size: int = 1, equipped: bool = False, loaded: bool = True) -> None:
    super().__init__(item_id, stack_size, loaded)
    self.character_id = character_id
    self.equipped = equipped

  @staticmethod
  def get_table_name() -> TableName: return TableName.INVENTORY_ITEM

  def get_raw_data(self) -> list[Any]:
    return [self.character_id] + super().get_raw_data() + [self.equipped]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_inventory_item(data, loaded)
  
  @staticmethod
  def identical_condition(inventory_item_row: list[Any]) -> Condition:
    return Condition(lambda _, row: row[0] == inventory_item_row[0] and row[1] == inventory_item_row[1])
  
  # built-in methods
  
  def __repr__(self) -> str:
    return f"InventoryItem(`{self.character_id=}`, `{self.item_id=}`, `{self.stack_size=}`, `{self.equipped=}`)"

def instantiate_inventory_item(inventory_item_data: list[Any] = [], loaded: bool = True) -> InventoryItem:
  character_id: int = inventory_item_data[0]
  item_id: int = inventory_item_data[1]
  stack_size: int = inventory_item_data[2]
  equipped: bool = inventory_item_data[3]
  return InventoryItem(character_id, item_id, stack_size, equipped, loaded)