import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName
from tools.generation_tools import *

from game_data import GameData
from interface.abstract_screen import AbstractScreen

class ExplorationScreen(AbstractScreen):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.is_entering_combat: bool = False
    self.is_entering_structure: bool = False

    self.enter_combat_button: tk.Button
    self.enter_structure_button: tk.Button
    self.continue_exploration_button: tk.Button

    self.open_inventory: ButtonCommand = kwargs["open_inventory"]

    super().__init__(root, parent, game_data, **kwargs)

  def is_nothing_happening(self) -> bool:
    return not self.is_entering_combat and not self.is_entering_structure

  # gui methods

  def reset_gui(self) -> None:
    self.nothing_found()
    self.message.set("-")
    self.continue_exploration_button["state"] = tk.NORMAL

  def reload_gui(self) -> None:
    if self.is_nothing_happening(): self.reset_gui()
    elif self.is_entering_combat: # if the character has just finished combat
      self.make_combat_unavailable()
      self.is_entering_combat = False
      if self.is_entering_structure: # if the character will be looting a structure afterwards 
        self.make_structure_entry_available()
      else: # if the character will not be looting a structure
        self.make_structure_entry_unavailable()
        self.continue_exploration_button["state"] = tk.NORMAL
    elif self.is_entering_structure: # if the character has just finished looting a structure
      self.reset_gui()
      self.is_entering_structure = False
    
    if self.game_data.previous_screen_name == ScreenName.STORAGE:
      self.message.set("-")

  def continue_exploration(self) -> None:
    self.is_entering_combat = is_combat_encounter()
    self.is_entering_structure = is_structure_encounter()

    if not self.is_entering_combat:
      if self.is_entering_structure:
        self.make_structure_entry_available()
      elif not self.is_entering_structure:
        self.nothing_found()
    else:
      self.make_structure_entry_unavailable()
      self.make_combat_available()

  def make_combat_available(self) -> None:
    self.message.set("Enemies block your path...")
    self.continue_exploration_button["state"] = tk.DISABLED
    self.enter_combat_button["state"] = tk.NORMAL

  def make_structure_entry_available(self) -> None:
    self.message.set("Structure found")
    self.continue_exploration_button["state"] = tk.DISABLED
    self.enter_structure_button["state"] = tk.NORMAL

  def make_combat_unavailable(self) -> None:
    self.enter_combat_button["state"] = tk.DISABLED

  def make_structure_entry_unavailable(self) -> None:
    self.enter_structure_button["state"] = tk.DISABLED

  def nothing_found(self) -> None:
    self.message.set("Nothing happened (press again)")
    self.make_combat_unavailable()
    self.make_structure_entry_unavailable()

  # load and create

  def return_command_generator(self, return_command: Callable[[ScreenName], None]) -> Callable[[ScreenName], None]:
    def inner(screen_name: ScreenName) -> None:
      self.is_entering_combat = False
      self.is_entering_structure = False
      self.reset_gui()
      return_command(screen_name)
    return inner

  def load(self, **kwargs) -> None:
    self.reload_gui()
    self.game_data.active_storage_id = self.game_data.away_storage
    super().load(**kwargs)

  def create(self, enter_structure: ButtonCommand, begin_combat: ButtonCommand, **kwargs):
    self.create_button(text="Open inventory", command=lambda: self.open_inventory())

    self.continue_exploration_button = unpack_optional(self.create_button(text="Continue exploration", command=lambda: self.continue_exploration(), return_button=True))

    self.create_message()

    choice_grid: tk.Frame = unpack_optional(self.create_frame(return_frame=True, dimensions=(2,1)))

    self.enter_combat_button = unpack_optional(self.create_button((0,0), return_button=True, container=choice_grid, text="Enter combat", command=lambda: begin_combat(), state=tk.DISABLED))

    self.enter_structure_button = unpack_optional(self.create_button((1,0), return_button=True, container=choice_grid, text="Loot structure", command=lambda: enter_structure(), state=tk.DISABLED))

    super().create(title="Exploration", dimensions=(1,3), **kwargs)

    return_command: Callable[[ScreenName], None] = self.return_command_generator(kwargs["return_command"])
    self.create_return(ScreenName.HOME, return_command=return_command)
    self.create_quit()
    
    if self.game_data.is_dev_mode_enabled:
      self.create_button(text="DEV_MODE: Enter combat", command=lambda: begin_combat())
      self.create_button(text="DEV_MODE: Enter structure", command=lambda: enter_structure())