import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from interface.creation import Creation
from game_data import GameData

class WorldCreation(Creation):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.confirm_creation: Callable[[str], None] = kwargs["create_world"]
    super().__init__(root, parent, game_data, "", **kwargs)

  def create_world(self) -> None:
    """
    Handles whether a new world will be created and the information used by that process. Assumes `self.entry_field` has a value inputted.

    World creation fails if:
      * The new world name matches with a world name already in `self.game_data.worlds`
      * The world name is empty (i.e. it is \"\")
    """
    new_world_name: str = self.entry_field.get()
    existing_world_names: list[str] = list(map(lambda world: world.name, list(self.game_data.worlds.values())))
    name_invalidity_message: Optional[str] = self.get_name_invalidity_message(new_world_name, existing_world_names)
    if name_invalidity_message == None: return self.confirm_creation(new_world_name)
    self.fail_creation(name_invalidity_message)

  def load(self, **kwargs) -> None:
    super().load(**kwargs)

  def create(self, **kwargs) -> None:
    super().create("World creation", **kwargs)

    self.create_entry("Enter world name:", self.entry_field)

    self.create_message()

    self.create_confirm(self.create_world)

    self.create_return(ScreenName.WORLD_SELECTION)
    self.create_quit()
