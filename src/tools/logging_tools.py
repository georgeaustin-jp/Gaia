import logging
import colorama as cr

from tools.typing_tools import *

cr.init(autoreset=True)

logging.basicConfig(format=f"{cr.Fore.CYAN}%(levelname)s[%(name)s]{cr.Fore.WHITE} AT {cr.Fore.LIGHTMAGENTA_EX}\'%(filename)s\'{cr.Fore.WHITE} IN {cr.Fore.BLUE}\'%(funcName)s\'{cr.Fore.WHITE} {cr.Fore.LIGHTBLACK_EX}(line %(lineno)s):{cr.Style.RESET_ALL}\n >>> %(message)s", level=logging.DEBUG)

# decorators

## for functions
def log_all[ReturnType](func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
  def wrapper(*args, **kwargs) -> ReturnType:
    func_name: str = func.__name__
    log_return_func: Callable[..., ReturnType] = log_return(func)
    log_return_func.__name__ = func_name
    log_all_func: Callable[..., ReturnType] = log_args(log_return_func)
    return log_all_func(*args, **kwargs)
  return wrapper

def log_args[ReturnType](func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
  def wrapper(*args, **kwargs) -> ReturnType:
    log_message: str = f"""`{log_args.__name__}` CALLED:
\t| FUNC `{func.__name__}`"""
    log_message += f"\n\t| WITH `{len(args)}` ARGS:"
    for i in range(len(args)):
      log_message += f"\n\t  > args[{i}] == `{args[i]}`"
    logging.info(log_message)
    return func(*args, **kwargs)
  return wrapper

def log_return[ReturnType](func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
  def wrapper(*args, **kwargs) -> ReturnType:
    return_value: ReturnType = func(*args, **kwargs)
    log_message: str = f"""`{log_return.__name__}` CALLED:
\t| FUNC `{func.__name__}`"""
    log_message += f"\n\t  > `{return_value=}`, `{type(return_value)=}`"
    logging.info(log_message)
    return return_value
  return wrapper

## for loggable objects
def log_loggable_args[LoggableType: Loggable, ReturnType](func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
  def wrapper(self: LoggableType, *args, **kwargs) -> ReturnType:
    if self.is_logging_enabled:
      log_message: str = f"""`{log_loggable_args.__name__}` CALLED:
\t| ON `{self.__class__}`
\t| METHOD `{func.__name__}`"""
      label_message: Optional[str] = self.get_label_message()
      if label_message != None: log_message += f"\n\t| {label_message}"
      log_message += f"\n\t| WITH `{len(args)}` ARGS:"
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
\t| ON `{self.__class__}`
\t| METHOD `{func.__name__}`"""
      label_message: Optional[str] = self.get_label_message()
      if label_message != None: log_message += f"\n\t| {label_message}"
      log_message += f"\n\t  > `{return_value=}`, `{type(return_value)=}`"
      logging.info(log_message)
    return return_value
  return wrapper

# classes

class Loggable():
  def __init__(self, is_logging_enabled: bool, label: Optional[str] = None) -> None:
    self.is_logging_enabled = is_logging_enabled
    self.label = label

  def get_label_message(self) -> Optional[str]:
    if self.label == None: return None
    return f"LABEL `{self.label}`"
