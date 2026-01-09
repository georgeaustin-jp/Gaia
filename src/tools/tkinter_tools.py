import tkinter as tk
import customtkinter as ctk

from tools.constants import Constants
from tools.typing_tools import *
from tools.logging_tools import *

ctk.set_appearance_mode("light")

def configure_grid(frame: tk.Frame, dimensions: Position = (1, 3),  exclude_columns: list[int] = [], exclude_rows: list[int] = [], include_header: bool = True, include_footer: bool = True, is_main_grid: bool = False) -> None:
  """
  Sets the columns and rows of a grid frame to expand with the window when it changes size. Includes some customisation options.
  
  :param frame: Frame being configured.
  :type frame: tk.Frame
  :param dimensions: The width and height of the frame in columns and rows. Defaults to `(1,3)`.
  :type dimensions: Position
  :param exclude_columns: Columns which will not expand with the window. Defaults to `[]`.
  :type exclude_columns: list[int]
  :param exclude_rows: Rows which will not expand with the window. Defaults to `[]`.
  :type exclude_rows: list[int]
  :param include_header: Whether the header will expand with the window if `is_main_grid` is `True`. Defaults to `True`.
  :type include_header: bool
  :param include_footer: Whether the footer will expand with the window if `is_main_grid` is `True`. Defaults to `True`.
  :type include_footer: bool
  :param is_main_grid: If the grid being configured is the outer-most grid. If it is, then the header and footer will be specially configured. Defaults to `False`.
  :type is_main_grid: bool

  :rtype: None
  """
  (x, y) = dimensions
  x_lower = 0
  x_upper = x
  y_lower = 0
  y_upper = y

  if is_main_grid:
    y_lower = 1
    y_upper = y-1
    if include_header:
      frame.grid_rowconfigure(0, weight=1)
    if include_footer:
      frame.grid_rowconfigure(y-1, weight=1)

  if x_lower < x_upper:
    for column in range(x_lower, x_upper):
      if column not in exclude_columns:
        frame.grid_columnconfigure(column, weight=2)
  if y_lower < y_upper:
    for row in range(y_lower, y_upper):
      if row not in exclude_rows:
        frame.grid_rowconfigure(row, weight=2)

def toggle_button_selection(button: tk.Button, command: Callable[[], Any]) -> None:
  logging.info("called")
  button_colour = button["bg"]
  if button_colour == Constants.OFF_COLOUR:
    button.config(bg=Constants.ON_COLOUR, relief=Constants.ON_RELIEF)
  elif button_colour == Constants.ON_COLOUR:
    button.config(bg=Constants.OFF_COLOUR, relief=Constants.OFF_RELIEF)
  command()

def button_state_to_bool(state: str) -> bool:
  if state == tk.NORMAL: return True
  elif state == tk.DISABLED: return False
  else: raise NameError(f"\'state\'=`{state}` doesn't match with any known state (\'NORMAL\', \'DISABLED\')")

def bool_to_button_state(is_enabled: bool) -> str:
  if is_enabled: return tk.DISABLED
  return tk.NORMAL