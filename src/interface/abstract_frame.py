import tkinter as tk

class AbstractFrame(tk.Frame):
  def __init__(self, root, parent: tk.Frame) -> None:
    super().__init__(parent)
    self.root = root
    self.parent = parent
    self.create()

  # each widget will be packed to the frame upon creation
  #https://www.geeksforgeeks.org/python/python-tkinter-frame-widget/
  def create_widget(self, widget_type, **options) -> None:
    widget = widget_type(self, **options)
    widget.pack()

  def create(self, title: str = "") -> None:
    self.grid(row=0, column=0, sticky="nesw")
    self.create_widget(tk.Label, text=title)