import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from game_data import GameData
from interface.abstract_interface import AbstractInterface

class Creation(AbstractInterface):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent, game_data, **kwargs)

  def create_entry(self, prompt: str, entry_string: tk.StringVar) -> None:
    self.create_widget(tk.Label, text=prompt)
    self.create_widget(tk.Entry, textvariable=entry_string)

  

  def fail_creation(self, message: str) -> None:
    self.message.set(message)

  def load(self, **kwargs) -> None:
    return super().load(**kwargs)
  
  def create(self, title: str = "", **kwargs) -> None:
    return super().create(title, **kwargs)