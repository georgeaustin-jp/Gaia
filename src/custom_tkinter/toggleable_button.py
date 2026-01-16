import tkinter as tk

from tools.typing_tools import *
from tools.constants import *
from tools.tkinter_tools import *

class ToggleableButton(tk.Button):
  """A button whose state can be toggled each time it is pressed."""
  def __init__(self, master: Optional[tk.Misc] = None, initially_toggled: ToggleState = ToggleState.OFF, initially_enabled: bool = True, on_colour: str = Constants.ON_COLOUR, off_colour: str = Constants.OFF_COLOUR, disabled_colour: str = Constants.DISABLED_COLOUR, **kwargs) -> None:
    super().__init__(master, **kwargs)
    self.on_colour = on_colour
    self.off_colour = off_colour
    self.disabled_colour = disabled_colour
    self.__is_toggled: ToggleState = initially_toggled
    self.display_state()
    self.is_enabled = initially_enabled
    self.__command: ButtonCommand # the generic command for the button (i.e. not the one which toggles it) will be executed after the one which toggles it
    if "command" in kwargs.keys(): self.command = kwargs["command"]
    else: self.command = lambda: None

  # getters and setters
  @property
  def command(self) -> ButtonCommand:
    """Getter method for `__command`"""
    return self.__command
  
  @command.setter
  def command(self, command: ButtonCommand) -> None:
    """Setter method for `__command`"""
    new_command: ButtonCommand = self.toggle(command)
    self.__command = new_command
    self.config(command=lambda: self.__command())

  @property
  def is_toggled(self) -> ToggleState:
    """Getter method for `__is_toggled`"""
    return self.__is_toggled
  
  @is_toggled.setter
  def is_toggled(self, value: ToggleState) -> None:
    """Setter method for `__is_toggled`"""
    self.__is_toggled = value
    self.display_state()

  @property
  def is_enabled(self) -> bool:
    if self["state"] == tk.NORMAL: return True
    return False
  
  @is_enabled.setter
  def is_enabled(self, enable: Union[bool, str]):
    if type(enable) == str: button_state_to_bool(enable)

    if enable: self.config(state=tk.NORMAL)
    else: self.config(state=tk.DISABLED)
    self.display_state()

  # dict-style methods
  def __getitem__(self, key: str) -> Any:
    if key == "is_toggled": return self.is_toggled
    return super().__getitem__(key)
  
  def __setitem__(self, key: str, value: Any) -> None:
    if key == "is_toggled": self.is_toggled = value
    elif key == "state": self.is_enabled = button_state_to_bool(value)
    else: return super().__setitem__(key, value)

  # methods for toggling the button 
  def display_toggled(self) -> None:
    self.config(bg=self.on_colour, relief=Constants.ON_RELIEF)

  def display_untoggled(self) -> None:
    self.config(bg=self.off_colour, relief=Constants.OFF_RELIEF)

  def display_value(self, value: ToggleState) -> None: # TODO: maybe add an exception raise to the end of this if `value` is neither `ToggleState.ON` or `ToggleState.OFF`?
    if not self.is_enabled: raise ValueError(f"Trying to call \'display_value\' when button is not enabled (\'self.is_enabled\'=`{self.is_enabled}`)")
    if value == ToggleState.ON: self.display_toggled()
    elif value == ToggleState.OFF: self.display_untoggled()

  def display_disabled(self) -> None:
    self.config(bg=self.disabled_colour, relief=Constants.DISABLED_RELIEF)

  def display_state(self) -> None:
    if not self.is_enabled: self.display_disabled()
    else: self.display_value(self.is_toggled)

  def toggle_state(self) -> None:
    self.is_toggled = ~self.is_toggled

  def toggle(self, command: ButtonCommand) -> ButtonCommand:
    def inner() -> None:
      self.toggle_state()
      command()
    return inner