import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from interface.creation import Creation
from game_data import GameData

class CharacterCreation(Creation):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.entered_name = tk.StringVar()
    self.message = tk.StringVar()
    self.message.set("...")
    self.confirm_creation: Callable[[str], None] = kwargs["create_character"]
    super().__init__(root, parent, game_data, **kwargs)

  def create_character(self) -> None:
    new_character_name: str = self.entered_name.get()
    existing_character_names: list[str] = [character.name for character in self.game_data.characters.values()]
    if new_character_name in existing_character_names:
      self.fail_creation(f"Character with name `{new_character_name}` already exists.")
    else:
      self.confirm_creation(new_character_name)

  def load(self, **kwargs) -> None:
    super().load(**kwargs)
    try: self.clear_message()
    except: pass

  def create(self, **kwargs) -> None:
    super().create(title="Character creation", **kwargs)

    self.create_entry("Enter character name:", self.entered_name)

    self.create_message()

    self.create_confirm(self.create_character)

    self.create_return(ScreenName.CHARACTER_SELECTION)