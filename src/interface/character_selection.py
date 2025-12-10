import tkinter as tk

from interface.abstract_frame import AbstractFrame
from interface.selection import Selection

class CharacterSelection(Selection):
  def __init__(self, root, parent: tk.Frame, **kwargs) -> None:
    super().__init__(root, parent, **kwargs)
    
  # each 
  def create(self, **kwargs) -> None:
    super().create(title="Character selection", **kwargs)
    self.create_widget(tk.Label, text="Select character")
    self.create_widget(tk.Button, text="Character1")
    self.create_widget(tk.Button, text="Go to combat", command = lambda: self.root.show_screen("combat"))