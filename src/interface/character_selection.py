import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName
from tools.logging_tools import *

from interface.abstract_interface import AbstractInterface
from interface.selection import Selection
from game_data import GameData
from stored.entities.character import Character

class CharacterSelection(Selection):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.select_character: Callable[[dict[str, Any]], None]
    super().__init__(root, parent, game_data, **kwargs)
  
  def load(self, **kwargs) -> None:
    super().load(**kwargs)
    characters: dict[int, Character] = self.game_data.characters
    button_data: dict[str, dict[str, Any]] = {}.copy()
    for (identifier, character) in characters.items():
      button_arguments: dict[str, Any] = {}.copy()
      button_arguments["character_identifier"] = identifier
      character_name: str = character.name
      button_data[character_name] = button_arguments
    self.create_buttons_dynamically(self.select_character, button_data)
    
  def create(self, **kwargs) -> None:
    self.init_dynamic_button_container()
    self.select_character: Callable[[dict[str, Any]], None] = kwargs["select_character"]
    super().create(title="Character selection", dimensions=(1,3), **kwargs)

    creation_command: Callable[[Optional[dict[str, Any]]], None] = kwargs["begin_character_creation"]
    self.create_widget(tk.Button, text="Create character", command=lambda: creation_command(None))
    self.create_quit(**kwargs)