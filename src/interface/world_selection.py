import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from interface.selection import Selection
from game_data import GameData

from stored.world import World

class WorldSelection(Selection):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent, game_data, **kwargs)
    self.select_world: Callable[[int], Any] = kwargs["select_world"]
    self.begin_world_creation: ButtonCommand = kwargs["begin_world_creation"]
    self.scrollable_world_frame_parent: tk.Frame

  # dynamic button methods

  def get_world_dynamic_button_input(self, world_id: int, world: World) -> DynamicButtonInput:
    return (world.name, world_id)

  def get_all_world_dynamic_button_inputs(self, worlds: dict[int, World]) -> list[DynamicButtonInput]:
    button_inputs: list[DynamicButtonInput] = []
    for (identifier, world) in worlds.items():
      button_inputs.append(self.get_world_dynamic_button_input(identifier, world))
    return button_inputs

  # creating and loading

  def load(self, **kwargs) -> None:
    super().load(**kwargs)
    worlds: dict[int, World] = self.game_data.worlds
    button_inputs: list[DynamicButtonInput] = self.get_all_world_dynamic_button_inputs(worlds)
    self.create_buttons_dynamically(button_inputs, command=lambda identifier: self.select_world(identifier), container=self.scrollable_world_frame_parent)

  def create(self, **kwargs) -> None:
    self.create_character_name_label()

    self.scrollable_world_frame_parent = unpack_optional(self.create_frame(return_frame=True, dimensions=(1,1)))

    super().create("World selection", **kwargs)

    self.create_widget(tk.Button, text="Create world", command=lambda: self.begin_world_creation())

    self.create_return(ScreenName.CHARACTER_SELECTION, **kwargs)
    self.create_quit(**kwargs)
    