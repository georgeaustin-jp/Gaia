import tkinter as tk
import custom_tkinter as ctk
from tkinter import font

from tools.typing_tools import *
from tools.tkinter_tools import *
from tools.constants import DefaultTkInitOptions, ScreenName
from tools.dictionary_tools import *

from game_data import GameData

from interface.base_frame import BaseFrame

from custom_tkinter.dynamic_button import DynamicButton

class AbstractScreen(BaseFrame):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent)
    self.game_data = game_data

    self.header = unpack_optional(self.create_frame_on_root((0,0), True, dimensions=(1,1)))
    self.body = unpack_optional(self.create_frame_on_root((0,1), True))
    self.footer = unpack_optional(self.create_frame_on_root((0,2), True, dimensions=(2,1)))

    self.default_frame: tk.Frame = self.body

    self.dynamic_button_frame: ctk.CTkScrollableFrame

    self.buttons: dict[str, tk.Button] = {}
    self.message = tk.StringVar()
    self.message_exists: bool = False

    self.character_name = tk.StringVar()
    self.world_name = tk.StringVar()

    self.is_quitting: bool = False

    self.return_to_screen: ScreenName

    self.return_command: Callable[[ScreenName], None] = kwargs["return_command"]
    self.quit_command: ButtonCommand = kwargs["quit_command"]

    self.itallics_font = font.Font(root=root, family=Constants.DEFAULT_FONT, size=Constants.DEFAULT_FONT_SIZE, slant=font.ITALIC)

    self.create(**kwargs)

  # getter and setter methods
  @property
  def active_user_id(self) -> Optional[int]:
    return self.game_data.active_user_id

  @property
  def active_character_id(self) -> Optional[int]:
    return self.game_data.active_character_id
  
  # widget creation methods

  ## dynamic button creation
  def create_buttons_dynamically(self, button_inputs: list[DynamicButtonInput], command: Callable[..., None], frame_position: Position = (0,0), container: Optional[tk.Frame] = None, placement_options: Optional[dict[str, Any]] = None, **kwargs) -> None:
    if hasattr(self, "dynamic_button_frame"):
      self.dynamic_button_frame.destroy()
    self.dynamic_button_frame = unpack_optional(self.create_ctk_scrollable_frame_on_grid(frame_position, container=container, return_frame=True))
    if placement_options == None: placement_options = {}.copy()
    button_args: dict[str, Any] = add_if_vacant(kwargs, DefaultTkInitOptions().DYNAMIC_BUTTON)
    placement_args: dict[str, Any] = add_if_vacant(placement_options, DefaultTkInitOptions().DYNAMIC_BUTTON_GRID)
    dynamic_buttons: list[DynamicButton] = []
    command_args_dict: dict[str, Any] = {}
    for (i, (text, command_args)) in enumerate(button_inputs):
      position: Position = (0,i)
      new_dynamic_button = unpack_optional(self.create_widget(DynamicButton, position, container=self.dynamic_button_frame, return_widget=True, placement_options=placement_args, **button_args))
      new_dynamic_button.text = text
      dynamic_buttons.append(new_dynamic_button)
      command_args_dict[text] = command_args

    for dynamic_button in dynamic_buttons:
      dynamic_button.command_args_dict = command_args_dict
      dynamic_button.command = command

    configure_grid(self.dynamic_button_frame, dimensions=(1, len(button_inputs)))

  ## special widgets
  def create_confirm(self, command: ButtonCommand, position: Optional[Position] = None, text: str = "Confirm", return_button: bool = False, placement_options: dict[str, Any] = {}, container: Optional[tk.Frame] = None, **kwargs) -> Optional[tk.Button]:
    """Creates a button for confirming some action. Very similar in operation to `self.create_button`."""
    return self.create_button(position=position, text=text, command=lambda: command(), container=container, return_button=return_button,placement_options=placement_options, **kwargs)

  def create_header_widget[WidgetType: tk.Widget](self, widget_type: Type[WidgetType], position: Position, return_widget: bool = False, placement_options: Optional[dict[str, Any]] = None, **kwargs) -> Optional[WidgetType]:
    return self.create_widget_on_grid(widget_type, position, container=self.header, return_widget=return_widget, placement_options=placement_options, **kwargs)

  def create_footer_widget[WidgetType: tk.Widget](self, widget_type: Type[WidgetType], position: Position, return_widget: bool = False, placement_options: Optional[dict[str, Any]] = None, **kwargs) -> Optional[WidgetType]:
    return self.create_widget_on_grid(widget_type, position, container=self.footer, return_widget=return_widget, placement_options=placement_options, **kwargs)

  def create_return(self, return_to_screen: Optional[ScreenName] = None, return_message: str = "Return", return_command: Optional[Callable[[ScreenName], None]] = None, **kwargs) -> tk.Button:
    if return_to_screen != None: self.return_to_screen = return_to_screen
    if return_command == None: return_command = self.return_command
    return unpack_optional(self.create_footer_widget(tk.Button, (0,0), text=return_message, command=lambda: return_command(self.return_to_screen), return_widget=True, **kwargs))

  def create_quit(self, quit_command: Optional[ButtonCommand] = None, **kwargs) -> None:
    if quit_command == None: quit_command = self.quit_command
    def full_quit_command() -> None:
      self.interrupt_waits()
      quit_command()
    self.create_footer_widget(tk.Button, (1,0), text="Quit", command=lambda: full_quit_command(), **kwargs)

  def create_message(self) -> None:
    if self.message_exists: raise Exception("Trying to call 'AbstractScreen.create_message()' when 'self.message' already exists.")
    self.create_widget(tk.Label, textvariable=self.message, borderwidth=2, relief="groove")
    self.message_exists = True
    self.clear_message()

  def clear_message(self) -> None:
    if not self.message_exists: raise Exception("Trying to call 'AbstractScreen.clear_message()' when 'self.message' does not exist.")
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

  def create_world_name_label(self, position: Optional[Position] = None, container: Optional[tk.Frame] = None, placement_options: dict[str, Any] = {}, **kwargs) -> None:
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
    self.create_header_widget(tk.Label, (0,0), text=title, font=(Constants.DEFAULT_FONT, 11))
    self.load(**kwargs)
  