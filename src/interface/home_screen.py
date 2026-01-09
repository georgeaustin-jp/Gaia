import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from game_data import GameData
from interface.abstract_interface import AbstractInterface

class HomeScreen(AbstractInterface):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent, game_data, **kwargs)

  def load(self, **kwargs) -> None:
    self.game_data.active_storage_id = self.game_data.home_storage
    super().load(**kwargs)

  def create(self, **kwargs) -> None:
    super().create(title="Home screen", dimensions=(1,3), **kwargs)
    self.create_character_name_label()
    
    open_storage: Callable[[], None] = kwargs["open_storage"]
    self.create_widget(tk.Button, text="Open storage", command=lambda: open_storage())

    go_exploring: Callable[[], None] = kwargs["go_exploring"]
    self.create_widget(tk.Button, text="Go exploring", command=lambda: go_exploring())

    self.create_return(ScreenName.WORLD_SELECTION, text="Return to world selection", **kwargs)
    self.create_quit(**kwargs)