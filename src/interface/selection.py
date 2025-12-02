import tkinter as tk

from interface.abstract_frame import AbstractFrame

class Selection(AbstractFrame):
  def __init__(self, root, parent: tk.Frame, **kwargs) -> None:
    super().__init__(root, parent, **kwargs)

  def create(self, title: str = "", **kwargs) -> None:
    super().create(title, **kwargs)