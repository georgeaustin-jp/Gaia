import tkinter as tk
import customtkinter as ctk
import logging

from tools.typing_tools import *
from tools.dictionary_tools import add_if_vacant
from tools.tkinter_tools import *
from tools.constants import DefaultTkInitOptions, ScreenName

from game_data import GameData

from interface.base_frame import BaseFrame
from custom_tkinter.toggleable_button import ToggleableButton

def command_wrapper[T](func: Callable[[T], None], value: T) -> Callable[[], None]:
  def wrapper() -> None:
    func(value)
  return wrapper

class AbstractInterface(BaseFrame):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent)
    self.game_data = game_data

    self.body = unpack_optional(self.create_frame_on_root((0,1), True))
    self.footer = unpack_optional(self.create_frame_on_root((0,2), True, dimensions=(2,1)))

    self.default_frame = self.body

    self.buttons: dict[str, tk.Button] = {}
    self.message = tk.StringVar()
    self.message_exists: bool = False

    self.character_name = tk.StringVar()
    self.world_name = tk.StringVar()

    self.is_quitting: bool = False

    self.return_to_screen: ScreenName

    self.return_command: Callable[[ScreenName], None] = kwargs["return_command"]

    self.create(**kwargs)

  # getter and setter methods
  @property
  def active_user_id(self) -> Optional[int]:
    return self.game_data.active_user_id

  @property
  def active_character_id(self) -> Optional[int]:
    return self.game_data.active_character_id
  
  # widget creation methods

  def init_dynamic_button_container(self) -> None:
    self.dynamic_button_container = unpack_optional(self.create_frame(return_frame=True))

  def create_buttons_dynamically(self, command: Callable[[dict[str, Any]], None], button_data: dict[str, dict[str, Any]]) -> None:
    """
    Creates a button for each entry of `button_data`.
    Removes previously created buttons not found in `button_data`.

    :param button_data: Maps each button name to its arguments. The arguments of each button will be passed into `command` during execution.
    :type button_data: dict[str, dict[str, Any]]    
    """
    existing_button_names: list[str] = list(self.buttons.keys())

    for new_button_name in list(button_data.keys()): # adds buttons not in the list
      if not new_button_name in existing_button_names:
        button_opt = None
        command_data = button_data[new_button_name].copy()
        wrapped_command: ButtonCommand = command_wrapper(command, command_data)
        button_opt: Optional[tk.Widget] = self.create_button(container=self.dynamic_button_container, text=new_button_name, command=lambda: wrapped_command(), return_button=True)
        button = unpack_optional(button_opt) # `unpack_optional`` will never fail, as `self.create_widget` will always return a value
        self.buttons[new_button_name] = button

    new_button_names: list[str] = list(button_data.keys())

    for button_name in self.buttons.keys():
      if not button_name in new_button_names:
        deleting_button: tk.Button = self.buttons.pop(button_name)
        deleting_button.destroy()

  def create_confirm(self, command: ButtonCommand, position: Optional[Position] = None, text: str = "Confirm", placement_options: dict[str, Any] = {}, container: Optional[tk.Frame] = None, **kwargs) -> None:
    """Creates a button for confirming some action. Very similar in operation to \'self.create_button\'."""
    self.create_button(position=position, text=text, command=lambda: command(), container=container, placement_options=placement_options, **kwargs)

  def create_footer_widget[WidgetType: tk.Widget](self, widget_type: Type[WidgetType], position: Position, return_widget: bool = False, **kwargs) -> Optional[WidgetType]:
    widget = widget_type(self.footer, **kwargs)
    (column, row) = position
    widget.grid(column=column, row=row, **DefaultTkInitOptions().GRID)
    if return_widget: return widget

  def create_return(self, return_to_screen: Optional[ScreenName] = None, return_message: str = "Return", return_command: Optional[Callable[[ScreenName], None]] = None, **kwargs) -> tk.Button:
    if return_to_screen != None: self.return_to_screen = return_to_screen
    if return_command == None: return_command = self.return_command
    return unpack_optional(self.create_footer_widget(tk.Button, (0,0), text=return_message, command=lambda: return_command(self.return_to_screen), return_widget=True))

  def create_quit(self, quit_command: ButtonCommand, **kwargs) -> None:
    def full_quit_command() -> None:
      self.interrupt_waits()
      quit_command()
    self.create_footer_widget(tk.Button, (1,0), text="Quit", command=lambda: full_quit_command())

  def create_message(self) -> None:
    if self.message_exists: raise Exception("Trying to call 'AbstractInterface.create_message()' when 'self.message' already exists.")
    self.create_widget(tk.Label, textvariable=self.message, borderwidth=2, relief="groove")
    self.message_exists = True
    self.clear_message()

  def clear_message(self) -> None:
    if not self.message_exists: raise Exception("Trying to call 'AbstractInterface.clear_message()' when 'self.message' does not exist.")
    self.message.set("...")
  
  # specialised labels

  def create_special_label(self, variable_name: str, position: Optional[Position] = None, container: Optional[tk.Frame] = None, placement_options: dict[str, Any] = {}, **kwargs) -> None:
    text_variable: tk.StringVar = getattr(self, variable_name)
    if position == None: self.create_widget(tk.Label, container=container, textvariable=text_variable, **kwargs)
    else: self.create_widget_on_grid(tk.Label, position=position, container=container, textvariable=text_variable, placement_options=placement_options)
  
  def set_special_label(self, variable_name: str, text: str) -> None:
    text_variable: tk.StringVar = getattr(self, variable_name)
    text_variable.set(text)

  def create_character_name_label(self, position: Optional[Position] = None, container: Optional[tk.Frame] = None, placement_options: dict[str, Any] = {}, **kwargs) -> None:
    self.create_special_label("character_name", position, container, placement_options=placement_options, **kwargs)

  def set_character_name_label(self, name: str) -> None:
    self.set_special_label("character_name", f"Character: {name}")

  def create_world_name_label(self, position: Optional[Position], container: Optional[tk.Frame] = None, placement_options: dict[str, Any] = {}, **kwargs) -> None:
    self.create_special_label("world_name", position, container, placement_options=placement_options, **kwargs)
  
  def set_world_name_label(self, name: str) -> None:
    self.set_special_label("world_name", f"World: {name}")

  def interrupt_waits(self) -> None:
    self.is_quitting = True

  def load(self, **kwargs) -> None:
    pass

  def create(self, title: str = "", dimensions: Position = (1,3), exclude_columns: list[int] = [], exclude_rows: list[int] = [], **kwargs) -> None:
    self.grid(row=0, column=0, sticky="nesw")
    configure_grid(self, dimensions=dimensions, exclude_columns=exclude_columns, exclude_rows=exclude_rows, include_header=False, include_footer=False, is_main_grid=True)
    self.create_widget_on_grid(tk.Label, (0,0), container=self, text=title)
    self.load(**kwargs)
  