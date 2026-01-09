from tools.typing_tools import *
from tools.logging_tools import *
from tools.constants import *

from database.condition import Condition, nothing

from interface.interface import Interface
from interface.combat_interface import CombatInterface

from game_data import GameData
from combat_management.combat_manager import CombatManager

from stored.entities.character import Character
from stored.world import World
from stored.items.storage import Storage

from time import sleep

class App:
  def __init__(self) -> None:
    self.game_data = GameData()
    self.game_data.load_game_data()

    interface_init_options: dict[str, Any] = {
      "quit_command": self.quit_command,
      "return_command": self.show_screen,
      "user_creator": self.create_user,
      "select_character": self.select_character,
      "begin_character_creation": self.begin_character_creation,
      "create_character": self.create_character,
      "select_world": self.select_world,
      "begin_world_creation": self.begin_world_creation,
      "create_world": self.create_world,
      "open_storage": self.open_storage,
      "go_exploring": self.go_exploring,
      "begin_combat": self.begin_combat,
      "end_combat": self.end_combat,
      "enter_structure": self.enter_structure, 
      "leave_structure": self.leave_structure,
    }

    self.interface = Interface(self.game_data, **interface_init_options)

    combat_interface: CombatInterface = self.interface.get_combat_interface()
    self.combat_manager = CombatManager(self.game_data, combat_interface)

    logging.info("App initialisation complete")

  def __del__(self) -> None:
    self.save()
    del self.game_data
    del self.interface
    del self.combat_manager

  def create_user(self, user_name: str, password_hash: str) -> None:
    self.game_data.insert_user([user_name, password_hash, 0, 0])

  def show_screen(self, screen_name: ScreenName, **kwargs) -> None:
    self.interface.show_screen(screen_name, **kwargs)

  def select_character(self, character_data: dict[str, Any]) -> None:
    logging.debug(f"{character_data=}")
    self.game_data.active_character_id = character_data["character_identifier"]
    character_name: str = self.game_data.get_character_name()
    self.interface.update_character_name(character_name)
    self.show_screen(ScreenName.WORLD_SELECTION)

  def create_character(self, character_name: str) -> None:
    active_user_id: int = unpack_optional(self.game_data.active_user_id)
    self.game_data.users[active_user_id].character_quantity += 1
    max_health: float = Character.get_default_max_health()
    character_identifier: int = self.game_data.insert_character([active_user_id, character_name, max_health, max_health])
    self.select_character({"character_identifier": character_identifier})
    self.interface.show_screen(ScreenName.WORLD_SELECTION)

  def begin_character_creation(self, _kwargs: dict[str, Any] = {}) -> None:
    self.show_screen(ScreenName.CHARACTER_CREATION)

  def select_world(self, kwargs: dict[str, Any]) -> None:
    world_identifier: int = kwargs["world_identifier"]
    self.game_data.active_world_id = world_identifier
    # selecting relevant storages (1 for home, 1 for away)
    find_world_storages: Callable[[StorageType], Condition] = lambda storage_type: Condition(lambda _, row: row[0] == world_identifier and row[1] == storage_type)
    # storage at home
    home_storages: dict[int, Storage] = self.game_data.select_from_storage(self.game_data.storages, find_world_storages(StorageType.HOME))
    if len(home_storages) != 1: raise Exception(f"{home_storages=} should have 1 element; {len(home_storages)} were found.")
    self.game_data.home_storage = list(home_storages.keys())[0]
    # storage for away
    away_storages: dict[int, Storage] = self.game_data.select_from_storage(self.game_data.storages, find_world_storages(StorageType.CHEST))
    if len(away_storages) != 1: raise Exception(f"{away_storages=} should have 1 element; {len(away_storages)} were found.")
    self.game_data.away_storage = list(away_storages.keys())[0]

    self.go_home()

  def go_home(self, screen_name: ScreenName = ScreenName.HOME, **kwargs) -> None:
    self.game_data.active_storage_id = self.game_data.home_storage
    self.show_screen(screen_name)

  def begin_world_creation(self, _kwargs: dict[str, Any] = {}) -> None:
    self.show_screen(ScreenName.WORLD_CREATION, world=self.game_data.worlds)

  def create_world(self, world_name: str, world_seed: str) -> None:
    active_user_id: int = unpack_optional(self.game_data.active_user_id)
    self.game_data.users[active_user_id].world_quantity += 1
    world_identifier: int = self.game_data.insert_world([active_user_id, world_name, world_seed])
    identical_condition = nothing()
    self.game_data.insert_stored(Storage, [world_identifier, StorageType.HOME], identical_condition, StorageAttrName.STORAGES)
    self.game_data.insert_stored(Storage, [world_identifier, StorageType.CHEST], identical_condition, StorageAttrName.STORAGES)
    self.select_world({"world_identifier": world_identifier})

  def load_active_weapons(self) -> list[int]:
    return list(self.game_data.weapons.keys())
  
  def get_weapon_name(self, weapon_id: int) -> str:
    return self.game_data.get_weapon_name(weapon_id)
  
  def open_storage(self) -> None:
    self.show_screen(ScreenName.STORAGE)

  def go_exploring(self) -> None:
    self.game_data.active_storage_id = self.game_data.away_storage
    self.show_screen(ScreenName.EXPLORATION)

  def begin_combat(self) -> None:
    self.game_data.encounter_combat()
    self.show_screen(ScreenName.COMBAT)
    self.combat_manager.begin_combat()

  def end_combat(self, screen_name: ScreenName) -> None:
    self.game_data.finish_combat_encounter()
    self.show_screen(screen_name)

  def enter_structure(self) -> None:
    self.game_data.encounter_structure()
    self.open_storage()

  def leave_structure(self, screen_name: ScreenName = ScreenName.EXPLORATION) -> None:
    self.game_data.finish_structure_encounter()
    self.show_screen(screen_name)

  def save(self) -> None:
    self.game_data.save()
    del self.game_data

  def run(self) -> None:
    options: dict[str, Any] = {"characters": self.game_data.characters}
    self.interface.run(**options)

  def quit_command(self, successfully: bool = True) -> None:
    self.save()
    if successfully: quit()
    quit(1)