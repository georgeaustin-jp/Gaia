import tkinter as tk
import custom_tkinter as ctk

from tools.typing_tools import *
from tools.constants import *
from tools.dictionary_tools import filter_dictionary
from tools.tkinter_tools import *

from game_data import GameData
from interface.abstract_screen import AbstractScreen

from stored.items.item import Item
from stored.items.inventory_item import InventoryItem
from stored.items.storage_item import StorageItem
from stored.items.abstract_storage_item import AbstractStorageItem

from custom_tkinter.toggleable_button import ToggleableButton

class StorageScreen(AbstractScreen):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.storage_indicator = tk.StringVar()

    self.inventory_frame: ctk.CTkScrollableFrame
    self.storage_frame: ctk.CTkScrollableFrame

    self.inventory_item_frames: list[tk.Frame] = []
    self.inventory_item_swap_buttons: dict[int, ToggleableButton] = {} # an inventory item identifier maps to its respective button
    self.storage_item_frames: list[tk.Frame] = []
    self.storage_item_swap_buttons: dict[int, ToggleableButton] = {} # a storage item identifier maps to its respective button

    self.__equipped_weapon_amount: int = 0
    self.__equipped_weapon_text = tk.StringVar()
    self.__equipped_weapon_text.set("-")
    self.__equipped_equipable_amount: int = 0
    self.__equipped_equipable_text = tk.StringVar()
    self.__equipped_equipable_text.set("-")

    self.return_to_screen = ScreenName.HOME

    super().__init__(root, parent, game_data, **kwargs)

  # built-in methods

  def __getitem__(self, key: Union[ItemFrameCollectionName, str]) -> Any:
    if type(key) == ItemFrameCollectionName: return getattr(self, str(key))
    return super().__getitem__(key)
  
  def __setitem__(self, key: Union[ItemFrameCollectionName, str], value: Any) -> None:
    if type(key) == ItemFrameCollectionName: return setattr(self, str(key), value)
    return super().__setitem__(key, value)

  # getting/calculating basic values

  def get_character_inventory_item_amount(self) -> int:
    return len(self.game_data.get_character_inventory_items())
  
  def get_storage_item_amount(self, storage_id: int) -> int:
    return len(self.game_data.get_relevant_storage_items(storage_id))
  
  def get_storage_switch_button_text(self, is_character_inventory: bool) -> str:
    if is_character_inventory: return "Store"
    return "Take"
  
  def get_storage_attr_name(self, is_character_inventory: bool) -> StorageAttrName:
    if is_character_inventory: return StorageAttrName.INVENTORY_ITEMS
    return StorageAttrName.STORAGE_ITEMS
  
  def get_storage_frame(self, is_character_inventory: bool) -> tk.Frame:
    if is_character_inventory: return self.inventory_frame
    return self.storage_frame
  
  def get_item_frame_collection_name(self, is_character_inventory: bool) -> ItemFrameCollectionName:
    if is_character_inventory: return ItemFrameCollectionName.INVENTORY
    return ItemFrameCollectionName.STORAGE
  
  @property
  def equipped_weapon_amount(self) -> int:
    return self.__equipped_weapon_amount
  
  @equipped_weapon_amount.setter
  def equipped_weapon_amount(self, amount: int) -> None:
    if amount < 0: raise ValueError(f"{amount=} cannot be set to a value less than 0.")
    self.__equipped_weapon_amount = amount
    self.__equipped_weapon_text.set(f"Weapons equipped: {self.__equipped_weapon_amount}")

  @property
  def equipped_equipable_amount(self) -> int:
    return self.__equipped_equipable_amount
  
  @equipped_equipable_amount.setter
  def equipped_equipable_amount(self, amount: int) -> None:
    if amount < 0: raise ValueError(f"{amount=} cannot be set to a value less than 0.")
    self.__equipped_equipable_amount = amount
    self.__equipped_equipable_text.set(f"Equipables equipped: {self.__equipped_equipable_amount}")
  
  # swapping items between inventories

  def move_items_if_valid(self, **kwargs) -> None:
    """Ensures a swap is valid before it is executed. Calls `move_items` if no faults occur."""
    storage_id: Optional[int] = self.game_data.active_storage_id
    if storage_id == None: raise KeyError(f"Trying to access a storage when no storage is currently active ({self.game_data.active_storage_id=}).")
    self.move_items(storage_id, **kwargs)
    self.load(**kwargs)

  def move_items(self, storage_id: int, **kwargs) -> None:
    """Contains the functionality for swapping the items between the inventory and whatever storage is currently active."""
    activated_inventory_move_buttons: dict[int, ToggleableButton] = filter_dictionary(self.inventory_item_swap_buttons, lambda _, button: button.is_toggled == ToggleState.ON)
    activated_storage_move_buttons: dict[int, ToggleableButton] = filter_dictionary(self.storage_item_swap_buttons, lambda _, button: button.is_toggled == ToggleState.ON)
    inventory_items_to_move: list[int] = list(activated_inventory_move_buttons.keys())
    storage_items_to_move: list[int] = list(activated_storage_move_buttons.keys())

    for inventory_item_id in inventory_items_to_move:
      self.game_data.move_inventory_item_to_storage(inventory_item_id, storage_id)
      del self.inventory_item_swap_buttons[inventory_item_id]

    for storage_item_id in storage_items_to_move:
      self.game_data.move_storage_item_to_inventory(storage_item_id)
      del self.storage_item_swap_buttons[storage_item_id]

    self.load(**kwargs) # reloads buttons at the end
  
  # methods for loading the screen

  def equip_button_command_generator(self, equip_button: ToggleableButton, abstract_storage_item_id: int, switch_button: ToggleableButton) -> ButtonCommand:
    def equip_button_command() -> None:
      self.game_data.toggle_inventory_item_equipped(equip_button, abstract_storage_item_id)
      switch_button.is_enabled = not bool(equip_button.is_toggled)

    return equip_button_command

  def create_item_frame(self, abstract_storage_item_id: int, index: int, container: tk.Frame, is_character_inventory: bool = False, is_equipped: bool = False, **kwargs) -> tk.Frame:
    """
    Creates a frame that contains all required information about a single item. Includes the following (from left to right):
      1. Equip/unequip the item (optional)
      2. Item name
      3. Item type
      4. Stack size
      5. Button to select whether the item should be swapped
    
    :param container: The base frame which the item frame will be appended to.
    :type container: Frame
    """
    # getting information about the item
    storage_name: StorageAttrName = self.get_storage_attr_name(is_character_inventory)
    storage_item: AbstractStorageItem = self.game_data[storage_name][abstract_storage_item_id]
    stack_size: int = storage_item.stack_size
    item_id: int = storage_item.item_id
    item: Item = self.game_data.items[item_id]
    item_name: str = item.name
    # creating the frame
    item_frame: tk.Frame = unpack_optional(self.create_frame_on_grid((0,index), container=container, dimensions=(5,1), exclude_columns=[0,2,3,4], return_frame=True, placement_options={"sticky": "ew"}, **kwargs))
    # populating it
    ## inventory-switching button
    switch_button = unpack_optional(self.create_toggleable_button((4,0), container=item_frame, text=self.get_storage_switch_button_text(is_character_inventory), return_button=True)) # for switching between storage and inventory
    if is_character_inventory: self.inventory_item_swap_buttons[abstract_storage_item_id] = switch_button
    else: self.storage_item_swap_buttons[abstract_storage_item_id] = switch_button
    ## equipping button
    if item.item_type in [ItemType.WEAPON, ItemType.EQUIPABLE] and is_character_inventory:
      initially_toggled = ToggleState.bool_to_state(is_equipped)
      equip_button: ToggleableButton = unpack_optional(self.create_toggleable_button((0,0), container=item_frame, text="Equip", initially_toggled=initially_toggled, return_button=True)) # button for equipping / unequipping items
      equip_button.command = self.equip_button_command_generator(equip_button, abstract_storage_item_id, switch_button) # disables swap button when the item is equipped
      switch_button.is_enabled = not initially_toggled
    ## other
    self.create_widget_on_grid(tk.Label, (1,0), container=item_frame, text=item_name) # name of item
    unpack_optional(self.create_widget_on_grid(tk.Label, (2,0), container=item_frame, text=f"[{item.item_type}]", return_widget=True)).configure(font=self.itallics_font) # item type
    self.create_widget_on_grid(tk.Label, (3,0), container=item_frame, text=f"({str(stack_size)})") # stack size

    return item_frame
  
  def clear_item_frames(self, attribute_name: ItemFrameCollectionName) -> None:
    """
    Iterates over an attribute of item frames, destroying all of them and clearing the attribute's contents.

    :param attribute_name: The name of the target attribute containing the item frames. The attribute must be of the type `list[Frame]`.
    :type attribute_name: str
    """
    valid_attribute_names: list[ItemFrameCollectionName] = [ItemFrameCollectionName.INVENTORY, ItemFrameCollectionName.STORAGE]
    if not attribute_name in valid_attribute_names:
      raise NameError(f"Argument {attribute_name=} doesn't match with any {valid_attribute_names=}.")
    item_frames: list[tk.Frame] = self[attribute_name]
    for frame in item_frames:
      frame.destroy()
    item_frames = [].copy()
    self[attribute_name] = item_frames

  def load_abstract_storage_items[AbstractStorageItemType: AbstractStorageItem](self, storage_items: dict[int, AbstractStorageItemType], is_character_inventory: bool = False, **kwargs) -> None:
    """
    Loads all item frames into an abstract storage (either inventory or storage).
    
    :param storage_items: Contains all the items which are to be loaded. Maps an identifier to its respective storage item.
    :type storage_items: dict[int, AbstractStorageItemType]
    :param is_character_inventory: Indicates whether the items are to be loaded into the inventory or the external storage. Defaults to `False`.
    :type is_character_inventory: bool
    :param kwargs: Key-word arguments. Currently unused.
    """
    container: tk.Frame = self.get_storage_frame(is_character_inventory)
    item_frame_collection_name: ItemFrameCollectionName = self.get_item_frame_collection_name(is_character_inventory)
    for (list_index, (storage_item_id, storage_item)) in enumerate(list(storage_items.items())):
      is_equipped: bool = False
      if type(storage_item) == InventoryItem:
        is_equipped = storage_item.equipped
      item_frame: tk.Frame = self.create_item_frame(storage_item_id, list_index, container, is_character_inventory=is_character_inventory, is_equipped=is_equipped)
      self[item_frame_collection_name].append(item_frame)
  
  def load_inventory(self, **kwargs) -> None:
    item_amount: int = self.get_character_inventory_item_amount()
    configure_grid(self.inventory_frame, dimensions=(1, item_amount), exclude_rows=list(range(item_amount-1)))
    character_inventory_items: dict[int, InventoryItem] = self.game_data.get_character_inventory_items()
    self.load_abstract_storage_items(character_inventory_items, is_character_inventory=True, **kwargs)

  def load_storage(self, storage_id: int, **kwargs) -> None:
    item_amount: int = self.get_storage_item_amount(storage_id)
    configure_grid(self.storage_frame, dimensions=(1, item_amount), exclude_rows=list(range(item_amount-1)))
    storage_inventory_items: dict[int, StorageItem] = self.game_data.get_relevant_storage_items(storage_id)
    self.load_abstract_storage_items(storage_inventory_items, is_character_inventory=False, **kwargs)

  def load(self, **kwargs) -> None:
    super().load(**kwargs)
    try:
      self.is_inventory: bool = kwargs["is_inventory"]
    except:
      self.is_inventory = False
    self.clear_item_frames(ItemFrameCollectionName.INVENTORY)
    self.clear_item_frames(ItemFrameCollectionName.STORAGE)

    is_storage_at_home: Optional[bool] = self.game_data.is_storage_at_home()
    if is_storage_at_home == None: return
    storage_id: Optional[int] = self.game_data.active_storage_id
    if storage_id == None: raise ValueError(f"{storage_id=} cannot be `None` when {is_storage_at_home=}.")

    if is_storage_at_home:
      self.storage_indicator.set("At home")
      self.return_to_screen = ScreenName.HOME
    else:
      self.storage_indicator.set("Away")
      self.return_to_screen = ScreenName.EXPLORATION
    self.load_inventory(**kwargs)
    if not self.is_inventory:
      self.load_storage(storage_id, **kwargs)
      self.confirm_button.config(state=tk.NORMAL)
    else:
      self.confirm_button.config(state=tk.DISABLED)

    self.destroy_return()
    self.return_button = self.create_return(**kwargs)

  def create_return(self, **kwargs) -> tk.Button:
    if self.game_data.is_storage_at_home():
      return super().create_return(ScreenName.HOME, return_message="Return to home screen")
    else:
      return super().create_return(ScreenName.EXPLORATION, return_message="Return to exploration", return_command=self.leave_structure_command)
    
  def destroy_return(self) -> None:
    try: self.return_button.destroy()
    except: pass

  def create(self, **kwargs) -> None:
    self.leave_structure_command: Callable[[ScreenName], None] = kwargs["leave_structure"]

    self.base_frame: tk.Frame = unpack_optional(self.create_frame(dimensions=(2,5), exclude_rows=[0,1,3], return_frame=True))
    self.default_frame = self.base_frame

    self.create_widget_on_grid(tk.Label, (0,0), textvariable=self.storage_indicator, placement_options={"columnspan": 2})
    self.create_widget_on_grid(tk.Label, (0,1), text="Player inventory")
    self.create_widget_on_grid(tk.Label, (1,1), text="Storage")
    
    self.inventory_frame = unpack_optional(self.create_ctk_scrollable_frame_on_grid((0,2), return_frame=True))
    self.storage_frame = unpack_optional(self.create_ctk_scrollable_frame_on_grid((1,2), return_frame=True))
    # dimensions for both are set in 'self.load' by calling the `self.load_inventory` and `self.load_storage` methods respectively

    self.create_widget(tk.Label, position=(0,3), textvariable=self.__equipped_weapon_text)
    self.create_widget(tk.Label, position=(1,3), textvariable=self.__equipped_equipable_text)

    super().create(title="Storage interface", **kwargs)

    self.confirm_button: tk.Button = unpack_optional(self.create_confirm(lambda: self.move_items_if_valid(), position=(0,4), text="Confirm swap", return_button=True, placement_options={"columnspan": 2}))
    
    #self.create_quit(**kwargs)