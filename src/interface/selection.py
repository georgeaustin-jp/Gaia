import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from interface.abstract_screen import AbstractScreen
from game_data import GameData

class Selection(AbstractScreen):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, is_logging_enabled: bool = False, include_call_stack: bool = False, **kwargs) -> None:
    super().__init__(root, parent, game_data, is_logging_enabled=is_logging_enabled, include_call_stack=include_call_stack, **kwargs)

  def load(self, **kwargs) -> None:
    super().load(**kwargs)

  def create(self, title: str = "", dimensions: Position = (1,3), **kwargs) -> None:
    super().create(title, dimensions, **kwargs)