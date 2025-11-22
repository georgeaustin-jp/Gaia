import tkinter as tk

from interface.abstract_frame import AbstractFrame

class Selection(AbstractFrame):
  def __init__(self, root, parent: tk.Frame) -> None:
    super().__init__(root, parent)

  def create(self, title: str = "") -> None:
    super().create(title)