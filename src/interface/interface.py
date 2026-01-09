import tkinter as tk

from tools.typing_tools import *
from tools.constants import Constants, ScreenName

from interface.abstract_interface import AbstractInterface
from interface.user_selection import UserSelection
from interface.user_creation import UserCreation
from interface.user_login import UserLogin
from interface.character_selection import CharacterSelection
from interface.character_creation import CharacterCreation
from interface.world_selection import WorldSelection
from interface.world_creation import WorldCreation
from interface.combat_interface import CombatInterface
from interface.home_screen import HomeScreen
from interface.storage_interface import StorageInterface
from interface.exploration_screen import ExplorationScreen

from game_data import GameData

from stored.user import User
from stored.entities.character import Character

class Interface(tk.Tk):
  def __init__(self, game_data: GameData, **kwargs) -> None:
    super().__init__()
    self.title("Gaia")

    self.geometry(f"{Constants.MIN_SCREEN_WIDTH}x{Constants.MIN_SCREEN_HEIGHT}")

    self.minsize(Constants.MIN_SCREEN_WIDTH, Constants.MIN_SCREEN_HEIGHT)
    self.maxsize(Constants.MAX_SCREEN_WIDTH, Constants.MAX_SCREEN_HEIGHT)

    container = tk.Frame(self)
    container.pack(fill="both", expand=True)

    container.grid_rowconfigure(0, weight=2)
    container.grid_columnconfigure(0, weight=2)

    screen_init_data: dict[ScreenName, Any] = {
      ScreenName.USER_LOGIN: UserLogin,
      ScreenName.USER_SELECTION: UserSelection,
      ScreenName.USER_CREATION: UserCreation,
      ScreenName.CHARACTER_SELECTION: CharacterSelection,
      ScreenName.CHARACTER_CREATION: CharacterCreation,
      ScreenName.WORLD_SELECTION: WorldSelection,
      ScreenName.WORLD_CREATION: WorldCreation,
      ScreenName.COMBAT: CombatInterface,
      ScreenName.HOME: HomeScreen,
      ScreenName.STORAGE: StorageInterface,
      ScreenName.EXPLORATION: ExplorationScreen,
    }

    self.screens: dict[ScreenName, AbstractInterface] = {}

    for (screen_name, Screen) in screen_init_data.items():
      self.screens[screen_name] = Screen(self, container, game_data, **kwargs)

  def show_screen(self, screen_name: ScreenName, **kwargs) -> None:
    screen = self.screens[screen_name]
    screen.load(**kwargs)
    screen.tkraise()

  def update_character_name(self, character_name) -> None:
    for screen in self.screens.values():
      screen.set_character_name_label(character_name)

  def get_combat_interface(self) -> CombatInterface:
    return cast(CombatInterface, self.screens[ScreenName.COMBAT])

  def run(self, **kwargs) -> None:
    self.show_screen(Constants.START_SCREEN, **kwargs)
    self.mainloop()