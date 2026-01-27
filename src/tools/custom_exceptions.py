from tools.typing_tools import *
import colorama as cr

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
    self.message = f"{cr.Fore.RED}{message}{cr.Fore.RESET}"
    if self.message != None: super().__init__(self.message, *args)
    else: super().__init__(*args)

  def info(self) -> ErrorMessageInfo:
    return (self.__class__.__name__, self.message)
  
class InsertAtExistingIdentifierError(AbstractError):
  def __init__(self, identifier: int, table_name: str, *args: object) -> None:
    super().__init__(f"Tried to insert value at `{identifier}` into `{table_name}` when record already exists.", *args)
  
# GUI errors

class NoButtonsSelectedError(AbstractError):
  def __init__(self, *args: object) -> None:
    super().__init__(None, *args)

class TooManyButtonsSelectedError(AbstractError):
  def __init__(self, message: str = "Too many buttons selected", *args: object) -> None:
    super().__init__(message, *args)

class NoEnemiesSelectedError(NoButtonsSelectedError):
  def __init__(self, message: str = "No enemies selected", *args: object) -> None:
    self.message = message
    super().__init__(self.message, *args)
  
class NoWeaponSelectedError(NoButtonsSelectedError):
  def __init__(self, message: str = "No attacks selected", *args: object) -> None:
    super().__init__(message, *args)

class NoAttackSelectedForEnemyError(NoWeaponSelectedError):
  def __init__(self, message: str = "Enemy(s) selected when no attacks are selected", *args: object) -> None:
    super().__init__(message, *args)

class TooManyEnemiesSelectedError(TooManyButtonsSelectedError):
  def __init__(self, position: Optional[Position] = None, *args) -> None:
    if position == None: message: str = f"Too many enemies selected"
    else: message = f"Too many enemies selected (second enemy selection detected at \'position\'=`{position}`)"
    super().__init__(message, *args)

class TooManyWeaponButtonsSelectedError(TooManyButtonsSelectedError):
  def __init__(self, weapon_number: Optional[int] = None, *args: object) -> None:
    if weapon_number == None: message: str = f"Too many weapon buttons selected"
    else: message = f"Too many weapon buttons selected (second weapon selection detected at weapon number `{weapon_number}`)"
    super().__init__(message, *args)

class TooManyAttackButtonsSelectedError(TooManyButtonsSelectedError):
  def __init__(self, message: str = "Too many attack buttons selected", *args: object) -> None:
    super().__init__(message, *args)

class TooManyParryButtonsSelectedError(TooManyButtonsSelectedError):
  def __init__(self, message: str = "Too many parry buttons selected", *args: object) -> None:
    super().__init__(message, *args)

class UnknownActionError(AbstractError):
  def __init__(self, message: str = "Unknown action", *args: object) -> None:
    super().__init__(message, *args)

# data structure errors

class StackError(AbstractError):
  def __init__(self, message: str = "", *args: object) -> None:
    super().__init__(message, *args)

class QueueError(AbstractError):
  def __init__(self, message: str = "", *args: object) -> None:
    super().__init__(message, *args)

# fighting entity errors

class HealthSetError(AbstractError):
  def __init__(self, health: float, max_health: Optional[float] = None, *args: object) -> None:
    message = f"Tried to set {health=} when value is invalid (less than `0` or greater than `max_health"
    if max_health != None: message += f"={max_health}"
    message += "`)."
    super().__init__(message, *args)

# abilities and effects errors

class InvalidTurnsError(AbstractError):
  def __init__(self, turns: int, *args: object) -> None:
    super().__init__(f"Tried to set `self.turns_remaining` to invalid {turns=}.", *args)

class NoParryError(AbstractError):
  def __init__(self, parry_data: Optional[tuple[float, float]], *args: object) -> None:
    super().__init__(f"Tried to parry when {parry_data=}.", *args)

class UnexpectedAbilityActionError(AbstractError):
  def __init__(self, ability_action: object, *args: object) -> None:
    super().__init__(f"Unexpected {ability_action=} of {type(ability_action)=}.", *args)

class MultipleIgnitionEffectsError(AbstractError):
  def __init__(self, ignition_effects: list, *args: object) -> None:
    super().__init__(f"Multiple ignition effects found: {ignition_effects=}.", *args)

# other

class InvalidPositionError(AbstractError):
  def __init__(self, position: Optional[Position] = None, dimensions: Optional[Position] = None, *args: object) -> None:
    message: str = "Invalid position"
    if position != None: message += f" {position=}"
    message += "; outside of valid "
    if dimensions != None: message += f"dimensions minimum=(0,0,), maximum={dimensions}"
    else: message += "dimensions"
    message += "."
    super().__init__(message, *args)

class PathError(AbstractError):
  def __init__(self, path: str, *args: object) -> None:
    super().__init__(f"Invalid path ({path=})", *args)

class AbstractMethodCallError(AbstractError):
  def __init__(self, class_name: str, method_name: str, *args: object) -> None:
    super().__init__(f"Tried to call abstract method `{method_name}` in class `{class_name}`.", *args)

class NoCharacterSelectedError(AbstractError):
  def __init__(self, message: str = "No buttons selected", *args: object) -> None:
    super().__init__(message, *args)