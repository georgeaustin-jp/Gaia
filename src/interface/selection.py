import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from interface.abstract_interface import AbstractInterface
from game_data import GameData

class Selection(AbstractInterface):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent, game_data, **kwargs)

  def load(self, **kwargs) -> None:
    super().load(**kwargs)

  def create(self, title: str = "", dimensions: Position = (1,3), **kwargs) -> None:
    super().create(title, dimensions, **kwargs)