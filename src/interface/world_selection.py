import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from interface.selection import Selection
from game_data import GameData

from stored.world import World

class WorldSelection(Selection):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent, game_data, **kwargs)

  def load(self, **kwargs) -> None:
    super().load(**kwargs)
    try: self.select_world: Callable[[dict[str, Any]], Any] = kwargs["select_world"] 
    except: pass
    worlds: dict[int, World] = self.game_data.worlds
    button_data: dict[str, dict[str, Any]] = {}
    for (identifier, world) in worlds.items():
      button_arguments: dict[str, Any] = {}.copy()
      button_arguments["world_identifier"] = identifier
      world_name: str = world.name
      button_data[world_name] = button_arguments
    self.create_buttons_dynamically(self.select_world, button_data)

  def create(self, **kwargs) -> None:
    self.create_character_name_label()

    self.init_dynamic_button_container()
    super().create("World selection", **kwargs)

    begin_world_creation: Callable = kwargs["begin_world_creation"]
    self.create_widget(tk.Button, text="Create world", command=lambda: begin_world_creation())

    self.create_return(ScreenName.CHARACTER_SELECTION, **kwargs)
    self.create_quit(**kwargs)
    