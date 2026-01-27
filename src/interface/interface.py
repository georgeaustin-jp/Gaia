import tkinter as tk
from tkinter import font

from tools.typing_tools import *
from tools.constants import Constants, ScreenName

from interface.abstract_screen import AbstractScreen
from interface.character_selection import CharacterSelection
from interface.character_creation import CharacterCreation
from interface.world_selection import WorldSelection
from interface.world_creation import WorldCreation
from interface.combat_screen import CombatScreen
from interface.home_screen import HomeScreen
from interface.storage_screen import StorageScreen
from interface.exploration_screen import ExplorationScreen

from game_data import GameData

class Interface(tk.Tk):
  def __init__(self, game_data: GameData, start_screen: ScreenName = Constants.START_SCREEN, **kwargs) -> None:
    super().__init__()
    
    self.START_SCREEN: ScreenName = start_screen
    self.active_screen: ScreenName = self.START_SCREEN

    self.game_data: GameData = game_data

    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family=Constants.DEFAULT_FONT, size=Constants.DEFAULT_FONT_SIZE)

    game_title: str = f"Gaia v{game_data.VERSION}"
    self.title(game_title)

    self.geometry(f"{Constants.MIN_SCREEN_WIDTH}x{Constants.MIN_SCREEN_HEIGHT}")

    self.minsize(Constants.MIN_SCREEN_WIDTH, Constants.MIN_SCREEN_HEIGHT)
    self.maxsize(Constants.MAX_SCREEN_WIDTH, Constants.MAX_SCREEN_HEIGHT)

    container = tk.Frame(self)
    container.pack(fill="both", expand=True)

    container.grid_rowconfigure(0, weight=2)
    container.grid_columnconfigure(0, weight=2)

    screen_init_data: dict[ScreenName, Any] = {
      ScreenName.CHARACTER_SELECTION: CharacterSelection,
      ScreenName.CHARACTER_CREATION: CharacterCreation,
      ScreenName.WORLD_SELECTION: WorldSelection,
      ScreenName.WORLD_CREATION: WorldCreation,
      ScreenName.COMBAT: CombatScreen,
      ScreenName.HOME: HomeScreen,
      ScreenName.STORAGE: StorageScreen,
      ScreenName.EXPLORATION: ExplorationScreen,
    }

    self.screens: dict[ScreenName, AbstractScreen] = {}

    for (screen_name, Screen) in screen_init_data.items():
      self.screens[screen_name] = Screen(self, container, game_data, **kwargs)

  def show_screen(self, screen_name: ScreenName, **kwargs) -> None:
    self.game_data.previous_screen_name = self.game_data.active_screen_name
    self.game_data.active_screen_name = screen_name
    screen = self.screens[screen_name]
    screen.load(**kwargs)
    screen.tkraise()

  def update_character_name(self, character_name: str) -> None:
    for screen in self.screens.values():
      screen.set_character_name_label(character_name)

  def update_world_name(self, world_name: str) -> None:
    for screen in self.screens.values():
      screen.set_world_name_label(world_name)

  def get_combat_screen(self) -> CombatScreen:
    return cast(CombatScreen, self.screens[ScreenName.COMBAT])

  def run(self, **kwargs) -> None:
    self.show_screen(self.START_SCREEN, **kwargs)
    self.mainloop()