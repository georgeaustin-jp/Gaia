import tkinter as tk

from interface.character_selection import CharacterSelection
from interface.combat import Combat

class Interface(tk.Tk):
  def __init__(self) -> None:
    super().__init__()
    self.title("Gaia")

    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.screens: dict = {"character_selection": CharacterSelection(self, container), "combat": Combat(self, container)}

  def show_screen(self, screen_name: str) -> None:
    screen = self.screens[screen_name]
    screen.tkraise()

  def run(self) -> None:
    self.show_screen("character_selection")
    self.mainloop()