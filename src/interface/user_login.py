import tkinter as tk

from interface.abstract_frame import AbstractFrame

class UserLogin(AbstractFrame):
  def __init__(self, root, parent: tk.Frame, **kwargs) -> None:
    super().__init__(root, parent, **kwargs)