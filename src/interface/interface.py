import tkinter as tk

from interface.user_selection import UserSelection
from interface.user_creation import UserCreation
from interface.user_login import UserLogin
from interface.character_selection import CharacterSelection
from interface.character_creation import CharacterCreation
from interface.world_selection import WorldSelection
from interface.world_creation import WorldCreation
from interface.combat import Combat

class Interface(tk.Tk):
  def __init__(self, **kwargs) -> None:
    super().__init__()
    self.title("Gaia")

    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    users: list = kwargs["users"]
    print(f"users=`{users}` (in \'Interface\')")

    screen_init_data: dict = {
      "user_selection": [UserSelection, {"users": users}],
      "user_creation": [UserCreation, {"users": users}],
      "user_login": [UserLogin],
      "character_selection": [CharacterSelection],
      "character_creation": [CharacterCreation],
      "world_selection": [WorldSelection],
      "world_creation": [WorldCreation],
      "combat": [Combat]
    }

    self.screens: dict = {}

    for (key, data) in screen_init_data.items():
      Screen = data[0]
      if len(data) > 1:
        kwargs = data[1]
        self.screens[key] = Screen(self, container, **kwargs)
      else:
        self.screens[key] = Screen(self, container)

  def show_screen(self, screen_name: str, **kwargs) -> None:
    screen = self.screens[screen_name]
    screen.load(**kwargs)
    screen.tkraise()

  def run(self, users: list) -> None:
    self.show_screen("user_selection", users=users)
    self.mainloop()