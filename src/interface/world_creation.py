import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from interface.creation import Creation
from game_data import GameData

from stored.world import World

class WorldCreation(Creation):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.world_name = tk.StringVar()
    self.world_seed = tk.StringVar()
    self.confirm_creation: Callable[[str, str], None] = kwargs["create_world"]
    super().__init__(root, parent, game_data, **kwargs)

  def create_world(self) -> None:
    """
    Handles whether a new world will be created and the information used by that process. Assumes \'self.world_name\' and \'self.world_seed\' have values inputted.

    World creation fails if:
      * The new world name matches with a world name already in \'self.game_data.worlds\'
      * The world name is empty (i.e. it is \"\")
      * The world seed is empty
    """
    new_world_name: str = self.world_name.get()
    new_world_seed: str = self.world_seed.get()
    existing_world_names: list[str] = list(map(lambda world: world.name, list(self.game_data.worlds.values())))
    fail_message: Optional[str] = None # if is `None`, then the world creation has not failed and thus can succeed. Otherwise, it fails and an appropriate message is passed as an argument to the 'self.fail_creation' function.
    if new_world_name in existing_world_names:
      fail_message = "World name already exists"
    elif new_world_name == "":
      fail_message = "World name cannot be nothing"
    elif new_world_seed == "":
      fail_message = "World seed cannot be nothing"
    
    if fail_message == None:
      self.confirm_creation(new_world_name, new_world_seed)
    else:
      self.fail_creation(fail_message)

  def load(self, **kwargs) -> None:
    super().load(**kwargs)

  def create(self, **kwargs) -> None:
    super().create("World creation", **kwargs)

    self.create_entry("Enter world name:", self.world_name)
    self.create_entry("Enter world seed:", self.world_seed)

    self.create_message()

    self.create_confirm(self.create_world)

    self.create_return(ScreenName.WORLD_SELECTION, **kwargs)
    self.create_quit(**kwargs)
