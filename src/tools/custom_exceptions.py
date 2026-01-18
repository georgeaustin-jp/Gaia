from tools.typing_tools import *

type ErrorMessageInfo = tuple[str, Optional[str]]

class QuitInterrupt(InterruptedError):
  """
  For when the program quits. Contains information on if the quit was successful or not. Not a subclass of `AbstractError`.
  
  :param success: Communicates whether the exit was successful (`True`) or not (`False`).
  :type success: bool 
  """
  def __init__(self, success: bool = False, *args: object) -> None:
    self.success = success
    super().__init__(*args)

class AbstractError(Exception):
  """Base class for all custom errors."""
  def __init__(self, message: Optional[str] = None, *args: object) -> None:
    self.message = message
    if self.message != None:
      super().__init__(self.message, *args)
    else:
      super().__init__(*args)

  def info(self) -> ErrorMessageInfo:
    return (self.__class__.__name__, self.message)
  
class InsertAtExistingIdentifierError(AbstractError):
  def __init__(self, identifier: int, table_name: str, *args: object) -> None:
    self.message = f"Tried to insert value at `{identifier}` into `{table_name}` when record already exists."
    super().__init__(self.message, *args)
  
# GUI errors

class NoButtonsSelectedError(AbstractError):
  def __init__(self, *args: object) -> None:
    super().__init__(None, *args)

  def info(self) -> ErrorMessageInfo:
    return (NoButtonsSelectedError.__name__, None)

class TooManyButtonsSelectedError(AbstractError):
  def __init__(self, message: str = "Too many buttons selected", *args: object) -> None:
    self.message = message
    super().__init__(self.message, *args)

class NoCharacterSelectedError(NoButtonsSelectedError):
  def __init__(self, message: str = "No buttons selected", *args: object) -> None:
    self.message = message
    super().__init__(self.message, *args)

class NoEnemiesSelectedError(NoButtonsSelectedError):
  def __init__(self, message: str = "No enemies selected", *args: object) -> None:
    self.message = message
    super().__init__(self.message, *args)
  
class NoWeaponSelectedError(NoButtonsSelectedError):
  def __init__(self, message: str = "No attacks selected", *args: object) -> None:
    self.message = message
    super().__init__(self.message, *args)

class NoAttackSelectedForEnemyError(NoWeaponSelectedError):
  def __init__(self, message: str = "Enemy(s) selected when no attacks are selected", *args: object) -> None:
    self.message = message
    super().__init__(self.message, *args)

class TooManyEnemiesSelectedError(TooManyButtonsSelectedError):
  def __init__(self, position: Optional[Position] = None, *args) -> None:
    if position == None: self.message = f"Too many enemies selected"
    else: self.message = f"Too many enemies selected (second enemy selection detected at \'position\'=`{position}`)"
    super().__init__(self.message, *args)

class TooManyWeaponButtonsSelectedError(TooManyButtonsSelectedError):
  def __init__(self, weapon_number: Optional[int] = None, *args: object) -> None:
    if weapon_number == None: self.message = f"Too many weapon buttons selected"
    else: self.message = f"Too many weapon buttons selected (second weapon selection detected at weapon number `{weapon_number}`)"
    super().__init__(self.message, *args)

class UnknownActionError(AbstractError):
  def __init__(self, message: str = "Unknown action", *args: object) -> None:
    self.message = message
    super().__init__(self.message, *args)

# data structure errors

class StackError(AbstractError):
  def __init__(self, message: str = "", *args: object) -> None:
    self.message = message
    super().__init__(self.message, *args)

class QueueError(AbstractError):
  def __init__(self, message: str = "", *args: object) -> None:
    self.message = message
    super().__init__(self.message, *args)

# fighting entity errors

class HealthSetError(AbstractError):
  def __init__(self, health: float, max_health: Optional[float] = None, *args: object) -> None:
    self.message = f"Tried to set {health=} when value is invalid (less than `0` or greater than `max_health"
    if max_health != None: self.message += f"={max_health}"
    self.message += "`)."
    super().__init__(self.message, *args)

# abilities and effects errors

class InvalidTurnsError(AbstractError):
  def __init__(self, turns: int, *args: object) -> None:
    super().__init__(f"Tried to set `self.turns_remaining` to invalid {turns=}.", *args)

class NoParryError(AbstractError):
  def __init__(self, parry_data: Optional[tuple[float, float]], *args: object) -> None:
    super().__init__(f"Tried to parry when {parry_data=}.", *args)

# other

class InvalidPositionError(AbstractError):
  def __init__(self, position: Optional[Position] = None, dimensions: Optional[Position] = None, *args: object) -> None:
    self.message: str = "Invalid position"
    if position != None: self.message += f" {position=}"
    self.message += "; outside of valid "
    if dimensions != None: self.message += f"dimensions minimum=(0,0,), maximum={dimensions}"
    else: self.message += "dimensions"
    self.message += "."
    super().__init__(self.message, *args)

class PathError(AbstractError):
  def __init__(self, path: str, *args: object) -> None:
    super().__init__(f"Invalid path ({path=})", *args)