import tkinter as tk

from interface.user_selection import UserSelection
from interface.user_creation import UserCreation
from interface.character_selection import CharacterSelection
from interface.character_creation import CharacterCreation
from interface.world_selection import WorldSelection
from interface.world_creation import WorldCreation
from interface.combat import Combat

class Interface(tk.Tk):
  def __init__(self) -> None:
    super().__init__()
    self.title("Gaia")

    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    screen_types: dict = {
      "user_selection": UserSelection,
      "user_creation": UserCreation,
      "character_selection": CharacterSelection,
      "character_creation": CharacterCreation,
      "world_selection": WorldSelection,
      "world_creation": WorldCreation,
      "combat": Combat
    }

    self.screens: dict = {}

    for (key, Screen) in screen_types.items():
      self.screens[key] = Screen(self, container)

  def show_screen(self, screen_name: str) -> None:
    screen = self.screens[screen_name]
    screen.tkraise()

  def run(self) -> None:
    self.show_screen("user_selection")
    self.mainloop()