import tkinter as tk

from interface.abstract_frame import AbstractFrame

class Combat(AbstractFrame):
  def __init__(self, root, parent: tk.Frame) -> None:
    super().__init__(root, parent)

  def create(self) -> None:
    super().create()
    self.create_widget(tk.Label, text="Combat screen")