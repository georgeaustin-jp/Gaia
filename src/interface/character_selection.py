import tkinter as tk
import customtkinter as ctk

from tools.typing_tools import *

from interface.selection import Selection
from game_data import GameData
from stored.entities.character import Character

class CharacterSelection(Selection):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.select_character: Callable[[int], None] = kwargs["select_character"]
    self.scrollable_character_frame_parent: tk.Frame
    self.scrollable_character_frame: ctk.CTkScrollableFrame

    super().__init__(root, parent, game_data, **kwargs)

  # creating buttons

  def get_character_dynamic_button_input(self, character_id: int, character: Character) -> DynamicButtonInput:
    return (character.name, character_id)
  
  def get_all_characters_dynamic_button_inputs(self, characters: dict[int, Character]) -> list[DynamicButtonInput]:
    button_inputs: list[DynamicButtonInput] = []
    for (character_id, character) in characters.items():
      character_button_input: DynamicButtonInput = self.get_character_dynamic_button_input(character_id, character)
      button_inputs.append(character_button_input)
    return button_inputs

  # loading and creating
  
  def load(self, **kwargs) -> None:
    super().load(**kwargs)
    characters: dict[int, Character] = self.game_data.characters
    button_inputs: list[DynamicButtonInput] = self.get_all_characters_dynamic_button_inputs(characters)
    self.create_buttons_dynamically(button_inputs, command=lambda identifier: self.select_character(identifier), container=self.scrollable_character_frame_parent)

  def create(self, **kwargs) -> None:
    self.scrollable_character_frame_parent = unpack_optional(self.create_frame(return_frame=True, dimensions=(1,1)))
    super().create(title="Character selection", dimensions=(1,3), **kwargs)

    creation_command: Callable[[Optional[dict[str, Any]]], None] = kwargs["begin_character_creation"]
    self.create_widget(tk.Button, text="Create character", command=lambda: creation_command(None))
    self.create_quit(**kwargs)