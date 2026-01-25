import logging
import colorama as cr
import traceback
import re
import inspect

from tools.typing_tools import *
from tools.constants import Constants

cr.init(autoreset=True)

logging.basicConfig(
  level=logging.CRITICAL,
  format=f"{cr.Fore.CYAN}%(levelname)s[%(name)s]{cr.Fore.WHITE} AT {cr.Fore.LIGHTMAGENTA_EX}\'%(filename)s\'{cr.Fore.WHITE} IN {cr.Fore.BLUE}\'%(funcName)s\'{cr.Fore.WHITE} {cr.Fore.LIGHTBLACK_EX}(line %(lineno)s):{cr.Style.RESET_ALL}\n >>> %(message)s",
)

# decorators

## for functions
def log_all[ReturnType](func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
  def wrapper(*args, **kwargs) -> ReturnType:
    level: int = 2
    func_name: str = func.__qualname__
    log_return_func: Callable[..., ReturnType] = log_return(func, level)
    log_return_func.__qualname__ = func_name
    log_all_func: Callable[..., ReturnType] = log_args(log_return_func, level)
    return log_all_func(*args, **kwargs)
  return wrapper

def log_args[ReturnType](func: Callable[..., ReturnType], level: int = 0) -> Callable[..., ReturnType]:
  def wrapper(*args, **kwargs) -> ReturnType:
    log_message: str = f"""`{log_args.__name__}` CALLED:
\t{Constants.DARK_BAR} FUNC `{func.__qualname__}`"""
    log_message += f"\n\t{Constants.DARK_BAR} {get_caller_message(level)}"
    log_message += f"\n\t{Constants.DARK_BAR} WITH `{len(args)}` ARGS:"
    for i in range(len(args)):
      log_message += f"\n\t  > args[{i}] == `{args[i]}`"
    logging.info(log_message)
    return func(*args, **kwargs)
  return wrapper

def log_return[ReturnType](func: Callable[..., ReturnType], level: int = 0) -> Callable[..., ReturnType]:
  def wrapper(*args, **kwargs) -> ReturnType:
    return_value: ReturnType = func(*args, **kwargs)
    log_message: str = f"""`{log_return.__name__}` CALLED:
\t{Constants.DARK_BAR} FUNC `{func.__qualname__}`"""
    log_message += f"\n\t{Constants.DARK_BAR} {get_caller_message(level)}"
    log_message += f"\n\t  > `{return_value=}`, `{type(return_value)=}`"
    logging.info(log_message)
    return return_value
  return wrapper

## for loggable objects
def log_loggable_args[LoggableType: Loggable, ReturnType](func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
  def wrapper(self: LoggableType, *args, **kwargs) -> ReturnType:
    if self.is_logging_enabled:
      log_message: str = f"""`{log_loggable_args.__name__}` CALLED:
\t{Constants.DARK_BAR} ON `{self.__class__}`
\t{Constants.DARK_BAR} METHOD `{func.__qualname__}`"""
      log_message += f"\n\t{Constants.DARK_BAR} {get_caller_message()}"
      log_message = self.add_messages_to_log(log_message)
      log_message += f"\n\t{Constants.DARK_BAR} WITH `{len(args)}` ARGS:"
      for i in range(len(args)):
        log_message += f"\n\t  > args[{i}] == `{args[i]}`"
      logging.info(log_message)
    return func(self, *args, **kwargs)
  return wrapper

def log_loggable_return[LoggableType: Loggable, ReturnType](func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
  def wrapper(self: LoggableType, *args, **kwargs) -> ReturnType:
    return_value: ReturnType = func(self, *args, **kwargs)
    if self.is_logging_enabled:
      log_message: str = f"""`{log_loggable_return.__name__}` CALLED:
\t{Constants.DARK_BAR} ON `{self.__class__}`
\t{Constants.DARK_BAR} METHOD `{func.__qualname__}`"""
      log_message += f"\n\t{Constants.DARK_BAR} {get_caller_message()}"
      log_message = self.add_messages_to_log(log_message)
      log_message += f"\n\t  > `{return_value=}`, `{type(return_value)=}`"
      logging.info(log_message)
    return return_value
  return wrapper

# functions

def is_logging_path(path: str) -> bool:
  #if re.fullmatch(r".*logging_tools\.py.*", path): return True
  return False

def get_call_stack() -> list[str]:
  return traceback.format_stack()

def get_call_stack_as_str() -> str:
  call_stack: list[str] = get_call_stack()
  call_stack_message: str = "CALL STACK:"
  for line in call_stack:
    split_line: list[str] = line.splitlines()
    path: str = split_line[0].strip()
    if is_logging_path(path): continue
    called_line: str = split_line[1].strip()
    call_stack_message += f"\n\t{Constants.DARK_BAR} {Constants.DARK_BAR} {path}"
    call_stack_message += f"\n\t{Constants.DARK_BAR} {Constants.DARK_BAR} {Constants.DARK_BAR} {called_line}"
    call_stack_message += f"\n\t{Constants.DARK_BAR} {Constants.DARK_BAR}"
  return call_stack_message

def get_caller_message(level: int = 0) -> str:
  actual_level: int = level+2
  current_frame = inspect.currentframe()
  caller_frame = inspect.getouterframes(current_frame, 2)
  caller_frame_at_level = caller_frame[actual_level]
  caller_name: str = caller_frame_at_level.function
  file_path: list[str] = caller_frame_at_level.filename.split('\\')
  file_name: str = f"{file_path[-2]}/{file_path[-1]}"
  line_number: int = caller_frame_at_level.lineno
  return f"CALLED BY `{caller_name}` (FILE `{file_name}`, LINE `{line_number}`)"

# classes

class Loggable():
  def __init__(self, is_logging_enabled: bool, label: Optional[str] = None, include_call_stack: bool = False) -> None:
    self.is_logging_enabled: bool = is_logging_enabled
    self.label: Optional[str] = label
    self.include_call_stack: bool = include_call_stack

  # message-adding methods

  def add_messages_to_log(self, log_message: str) -> str:
    log_message = self.add_label_message_to_log(log_message)
    log_message = self.add_call_stack_message_to_log(log_message)
    return log_message

  ## label
  def get_label_message(self) -> Optional[str]:
    if self.label == None: return None
    return f"LABEL `{self.label}`"
  
  def add_label_message_to_log(self, log_message: str) -> str:
    label_message: Optional[str] = self.get_label_message()
    if label_message != None: log_message += f"\n\t{Constants.DARK_BAR} {label_message}"
    return log_message
  
  ## call stack
  def get_call_stack_message(self) -> Optional[str]:
    if self.include_call_stack == False: return None
    return f"\n\t{Constants.DARK_BAR} {get_call_stack_as_str()}"
  
  def add_call_stack_message_to_log(self, log_message: str) -> str:
    call_stack_message: Optional[str] = self.get_call_stack_message()
    if call_stack_message != None: log_message += f"\t{Constants.DARK_BAR} {call_stack_message}"
    return log_message

