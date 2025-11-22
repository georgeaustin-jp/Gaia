import tkinter as tk

from interface.selection import Selection

class UserSelection(Selection):
  def __init__(self, root, parent: tk.Frame) -> None:
    super().__init__(root, parent)