import tkinter as tk

from interface.abstract_frame import AbstractFrame

class WorldCreation(AbstractFrame):
  def __init__(self, root, parent: tk.Frame, **kwargs) -> None:
    super().__init__(root, parent, **kwargs)

  def create(self, title: str = "") -> None:
    super().create(title)
