import tkinter as tk

from tools.typing_tools import *

from game_data import GameData
from interface.abstract_screen import AbstractScreen

class Creation(AbstractScreen):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent, game_data, **kwargs)

  def create_entry(self, prompt: str, entry_string: tk.StringVar) -> None:
    self.create_widget(tk.Label, text=prompt)
    self.create_widget(tk.Entry, textvariable=entry_string)
  
  def get_name_invalidity_message(self, name: str, existing_names: list[str]) -> Optional[str]:
    """
    :returns: If the name is valid, `None` is returned. Otherwise, a message explaining why it is invalid is returned.
    :rtype: Optional[str]
    """
    if name == "": return f"Name field cannot be empty"
    if name in existing_names: return f"Item with the same name already exists"
    return None

  def fail_creation(self, message: str) -> None:
    self.message.set(message)

  def load(self, **kwargs) -> None:
    return super().load(**kwargs)
  
  def create(self, title: str = "", **kwargs) -> None:
    return super().create(title, **kwargs)