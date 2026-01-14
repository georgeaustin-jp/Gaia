from tools.typing_tools import *
from tools.tkinter_tools import *

class DynamicButton(tk.Button): 
  def __init__(self, master: Optional[tk.Misc] = None, **kwargs) -> None:
    super().__init__(master, **kwargs)
    self.__command_args_dict: dict[str, Any]
    text = kwargs.get("text")
    if type(text) == str: self.text = text

  # getter and setter methods

  @property
  def command(self) -> Callable[..., None]:
    return self["command"]
  
  @command.setter
  def command(self, command: Callable[..., None]) -> None:
    def command_generator() -> Callable[..., None]:
      text: Optional[str] = self.text
      if text == None: raise ValueError(f"`{self.text}` mustn't be `None` at this point.")
      command_inputs = self.command_args_dict[text]
      return lambda: command(command_inputs)
    self["command"] = command_generator()

  @property
  def command_args_dict(self) -> dict[str, Any]:
    return self.__command_args_dict
  
  @command_args_dict.setter
  def command_args_dict(self, command_args: dict[str, Any]) -> None:
    self.__command_args_dict = command_args

  @property
  def text(self) -> Optional[str]:
    try: return self["text"]
    except: return None
  
  @text.setter
  def text(self, text: str) -> None:
    self.config(text=text)