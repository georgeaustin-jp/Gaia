tools/ability_names.py

from tools.typing_tools import *

# enums

@unique
class AbilityTypeName(StrEnum):
  """The names of the different types of abilities.
  
  Includes `PARRY`, `IGNITE`, `PIERCE`, `WEAKEN`, `DEFEND` and `HEAL`."""
  PARRY = "Parry"
  IGNITE = "Ignite"
  PIERCE = "Pierce"
  WEAKEN = "Weaken"
  DEFEND = "Defend"
  HEAL = "Heal"

@unique
class AbstractAbilityClassName(StrEnum):
  """Class names for different abilities which inherit from `AbstractAbility`."""
  ABSTRACT = "AbstractAbility" # not used, but here for completion
  PARRY = "ParryAbility"
  STATISTIC = "StatisticAbility"

# functions

def ability_type_name_to_abstract_ability_class_name(ability_type_name: AbilityTypeName) -> Optional[AbstractAbilityClassName]:
  """Converts an `AbilityTypeName` to an `AbstractAbilityClassName` depending on which class it's defined by.
  
  * `PARRY` goes to `PARRY`.
  * `WEAKEN`, `DEFEND` and `HEAL` go to `STATISTIC`.
  * Anything not in a table returns `None`."""
  if ability_type_name == AbilityTypeName.PARRY:
    return AbstractAbilityClassName.PARRY
  if ability_type_name in [AbilityTypeName.WEAKEN, AbilityTypeName.DEFEND, AbilityTypeName.HEAL]:
    return AbstractAbilityClassName.STATISTIC
  return None

EOF
tools/constants.py

import tkinter as tk

from tools.typing_tools import *

@unique
class ScreenName(Enum):
  # main screen names
  CHARACTER_CREATION = "character_creation"
  CHARACTER_SELECTION = "character_selection"
  COMBAT = "combat_interface"
  EXPLORATION = "exploration_screen"
  HOME = "home_screen"
  INTERFACE = "interface"
  STORAGE = "storage_interface"
  WORLD_CREATION = "world_creation"
  WORLD_SELECTION = "world_selection"
  # abstract screens, implemented for completeness
  ABSTRACT_FRAME = "abstract_frame"
  CREATION = "creation"
  SELECTION = "selection"

@dataclass
class Constants:
  # constants related to the flow of combat:
  MIN_REMAINING_ACTIONS: int = 0
  MAX_REMAINING_PLAYER_ACTIONS: int = 2
  MAX_REMAINING_ENEMY_ACTIONS: int = 1
  MIN_ROUND_NUMBER: int = 1
  # constants related to the fighting part of combat:
  MAX_EQUIPPED_WEAPONS: int = 3
  MAX_EQUIPPED_EQUIPABLES: int = 4
  HEALTH_POTION_AMOUNT: float = 30
  GRID_WIDTH: int = 3
  GRID_HEIGHT: int = 3
  MIN_ENEMIES: int = 1
  MAX_ENEMIES: int = 5
  BOSS_ENCOUNTER_PROBABILITY: float = 0 # TODO: set back to `0.05` once some bosses exist
  IGNITE_DURATION: int = 3
  IGNITE_DAMAGE: float = 3
  PIERCE_OFFENSIVENESS: float = 0.5
  IGNITE_OFFENSIVENESS: float = 0.5
  # constants related to the GUI and screens:
  START_SCREEN: ScreenName = ScreenName.CHARACTER_SELECTION
  ON_COLOUR: str = "chartreuse2"
  ON_RELIEF = tk.RIDGE
  OFF_COLOUR: str = "light gray"
  OFF_RELIEF = tk.RAISED
  DISABLED_COLOUR: str = "gray85"
  DISABLED_RELIEF: Literal['flat'] = tk.FLAT
  ENEMY_ATTACK_LABEL_COLOUR: str = "#FF5C5C"
  ENEMY_HEAL_LABEL_COLOUR: str = "#8FFF87"
  MIN_SCREEN_WIDTH: int = 750
  MIN_SCREEN_HEIGHT: int = 450
  MAX_SCREEN_WIDTH: int = 1000
  MAX_SCREEN_HEIGHT: int = 600
  WEAPON_INTERFACE_DIMENSIONS: Position = (4,3)
  # constants related to exploration
  COMBAT_ENCOUNTER_PROBABILITY: float = 0 # TODO: set back to 0.4
  STRUCTURE_ENCOUNTER_PROBABILITY: float = 1 # TODO: set back to 0.25
  MIN_STRUCTURE_ITEM_COUNT: int = 1
  MAX_STRUCTURE_ITEM_COUNT: int = 2
  # misc
  DEFAULT_ROUNDING_ACCURACY: int = 2

@dataclass
class DefaultTkInitOptions():
  """
  Used when either initialising tkinter widgets or placing them in a container.

  When accessing attributes, the class **must** be called before attempting access. For example:
  ```python
  ... = DefaultTkInitOptions.FRAME # WRONG USAGE
  ... = DefaultTkInitOptions().FRAME # CORRECT USAGE
  ```
  """
  # placement
  ## general
  GRID: dict[str, Any] = field(default_factory=lambda: {"sticky": "nsew", "padx": 1, "pady": 1})
  PACK: dict[str, Any] = field(default_factory=lambda: {"expand": True, "fill": tk.NONE})
  ## widget specific
  FRAME_PACK: dict[str, Any] = field(default_factory=lambda: {"fill": tk.BOTH})

  # widget creation
  WIDGET: dict[str, Any] = field(default_factory=lambda: {"borderwidth": 2}) # applied to all widgets
  BUTTON: dict[str, Any] = field(default_factory=lambda: {"padx": 2, "pady": 2})
  FRAME: dict[str, Any] = field(default_factory=lambda: {"relief": tk.RIDGE, "padx": 2, "pady": 2})
  CTK_SCROLLABLE_FRAME: dict[str, Any] = field(default_factory=lambda: {"corner_radius": 0})
  WEAPON_INTERFACE_DESCRIPTORS: dict[str, Any] = field(default_factory=lambda: {"relief": tk.SOLID, "borderwidth": 1, "padx": 1, "pady": 1})

@unique
class TableName(StrEnum):
  """All table names. Used primarily in subclasses of `Stored` and `GameData`."""
  USER = "User"
  CHARACTER = "Character"
  WORLD = "World"

  ITEM = "Item"
  INVENTORY_ITEM = "InventoryItem"
  WEAPON = "Weapon"
  EQUIPABLE = "Equipable"

  STORAGE = "Storage"
  STORAGE_ITEM = "StorageItem"

  ENEMY = "Enemy"
  ENEMY_ABILITY = "EnemyAbility"

  ABILITY = "Ability"
  PARRY_ABILITY = "ParryAbility"
  STATISTIC_ABILITY = "StatisticAbility"
  ITEM_ABILITY = "ItemAbility"

  NONE = "" # for subclasses of `Stored` where the object won't be stored in the database

@unique
class StorageAttrName(StrEnum):
  """Names for attributes handling data storage of specific objects in \'GameData\'."""
  USERS = "users"
  WORLDS = "worlds"
  CHARACTERS = "characters"
  CHARACTER_MODIFIERS = "character_modifiers"

  ITEMS = "items"
  INVENTORY_ITEMS = "inventory_items"
  WEAPONS = "weapons"
  EQUIPABLES = "equipables"

  STORAGES = "storages"
  STORAGE_ITEMS = "storage_items"

  ENEMIES = "enemies"
  FIGHTING_ENEMIES = "fighting_enemies"
  FIGHTING_ENEMY_MODIFIERS = "fighting_enemy_modifiers"
  ENEMY_ABILITIES = "enemy_abilities"

  ABILITIES = "abilities"
  PARRY_ABILITIES = "parry_abilities"
  STATISTIC_ABILITIES = "statistic_abilities"

  ITEM_ABILITIES = "item_abilities"

@unique
class ToggleState(Flag):
  """Used primarily in the `toggleable_button` module."""
  ON = True
  OFF = False

  @staticmethod
  def bool_to_state(value: bool):
    if value == True: return ToggleState.ON
    return ToggleState.OFF

@unique
class ComparisonFlag(IntEnum):
  LESS = -1
  EQUAL = 0
  GREATER = 1

@unique
class ItemType(StrEnum):
  WEAPON = "Weapon"
  EQUIPABLE = "Equipable"

@unique
class StorageFrameName(StrEnum):
  INVENTORY = "inventory_frame"
  STORAGE = "storage_frame"

@unique
class ItemFrameCollectionName(StrEnum):
  """Names for attributes storing collections of frames containing information about stored items. Used in \'storage_interface\'."""
  INVENTORY = "inventory_item_frames"
  STORAGE = "storage_item_frames"

@unique
class StorageType(StrEnum):
  """Determines what type some storage is. Either the storage at home or a chest."""
  HOME = "Home"
  CHEST = "Chest"

@unique
class WeaponUIComponentName(StrEnum):
  """Used in accessing the different components of the weapon user interface in `CombatInterface`."""
  WEAPON_NAME = "weapon_name"
  ATTACK = "attack"
  ATTACK_DAMAGE = "attack_damage"
  PARRY = "parry"

@unique
class ActionName(StrEnum):
  """The names for the different types of actions can be used.
  
  One of `ATTACK`, `PARRY` or `HEAL`."""
  ATTACK = "Attack"
  PARRY = "Parry"
  HEAL = "Heal"

EOF
tools/decision_tools.py

from math import  exp2

from tools.typing_tools import *
from tools.generation_tools import generate_float_in_range
from tools.constants import Constants

# decision error

def get_decision_error_bound(intelligence: float) -> float:
  if intelligence == 0: raise ValueError(f"{intelligence=} cannot be 0.")
  return 5 / intelligence

def generate_decision_error(error_bound: float) -> float:
  return generate_float_in_range(-1*error_bound, error_bound)

def clip(x: float, lower_bound: float, upper_bound: float) -> float:
  return min(max(x, lower_bound), upper_bound)

# aggressiveness calculations

def calculate_health_aggressiveness(health: float, max_health: float) -> float:
  """
  :return: In interval `[-1,1]`.
  :rtype: float
  """
  return health * (2 / max_health) - 1

def calculate_ignited_aggressiveness(health: float, max_health: float, remaining_duration: Optional[int]) -> float:
  if remaining_duration == None: return 0
  m: float = (1 / 2*max_health) * ((remaining_duration) / Constants.IGNITE_DURATION - (1 / 5*max_health))
  c: float = - (remaining_duration / 2*Constants.IGNITE_DURATION)
  return m*health + c

def calculate_damage_resistance_aggressiveness(damage_resistance: float, is_pierced: bool) -> float:
  """
  :return: In interval `[-1,1]`.
  :rtype: float
  """
  if is_pierced: return 0
  return exp2(damage_resistance)-1

def calculate_target_parry_aggressiveness(is_target_parrying: bool) -> float:
  if is_target_parrying: return -0.75
  return 0.1


EOF
tools/dictionary_tools.py

from tools.typing_tools import *
from tools.logging_tools import *

def filter_dictionary[K, V](dictionary: dict[K, V], condition: Callable[[K, V], bool]) -> dict[K, V]:
  return {key: val for key, val in dictionary.items() if condition(key,val)}

def add_if_vacant[K, V](primary_dict: dict[K, V], secondary_dict: dict[K, V]) -> dict[K, V]:
  main_keys: list[K] = list(primary_dict.keys())
  for (key, value) in secondary_dict.items():
      if not key in main_keys:
        primary_dict[key] = value
  return primary_dict

def get_sorted_identifiers(dictionary: dict[int, Any]) -> list[int]:
  return sorted(list(dictionary.keys()))

def get_next_available_identifier[T](storage_attribute: dict[int, T]) -> int:
    """Calculates the smallest, non-zero identifier not in the given storage attribute."""
    previous_id: int = -1 # defining variables
    previous_id_successor: int = 0 
    sorted_identifiers: list[int] = get_sorted_identifiers(storage_attribute)
    for current_id in sorted_identifiers:
      previous_id_successor = previous_id+1
      if current_id > previous_id_successor: # if there is a hole in the sequence (e.g. [1,2,4,5] would return 3)
        return previous_id_successor
      previous_id = current_id # sets up for next iteration
    previous_id_successor = previous_id+1
    return previous_id_successor # in the case there are no holes, then it returns the id outside of the list 

EOF
tools/exceptions.py

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
    self.message = f"Tried to set `self.turns_remaining` to invalid {turns=}."
    super().__init__(self.message, *args)

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


EOF
tools/generation_tools.py

from tools.typing_tools import *
from tools.logging_tools import *
from tools.constants import Constants

import random

# decorators

def validate_input_probability[ReturnType](func: Callable[Concatenate[float, ...], ReturnType]) -> Callable[Concatenate[float, ...], ReturnType]:
  def wrapper(p: float, *args, **kwargs) -> ReturnType:
    validate_probability(p)
    return func(p, *args, **kwargs)
  return wrapper

def validate_output_probability(func: Callable[..., float]) -> Callable[..., float]:
  def wrapper(*args, **kwargs) -> float:
    p: float = func(*args, **kwargs)
    validate_probability(p)
    return p
  return wrapper

def validate_bounds[ReturnType](exclusive: bool = True) -> Callable[[Callable[..., ReturnType]], Callable[..., ReturnType]]:
  def decorator(func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
    def wrapper(lower: Numeric, upper: Numeric, *args, **kwargs) -> ReturnType:
      if lower > upper: raise ValueError(f"Bound {lower=} is greater than bound {upper=} ({exclusive=}).")
      if lower == upper and exclusive: raise ValueError(f"Bound {lower=} is equal to bound {upper=} ({exclusive=}).")
      return func(lower, upper, *args, **kwargs)
    return wrapper
  return decorator

# functions
## probabilities and floats
def validate_probability(p: float) -> None:
  """Returns successfully if `p` is in the interval [0,1] (inclusive). Otherwise, raises an appropriate error."""
  if p < 0: raise ValueError(f"Probability {p=} cannot be less than 0.")
  if p > 1: raise ValueError(f"Probability {p=} cannot be greater than 1.")
  return None

@validate_bounds()
def generate_float_in_range(lower: Numeric, upper: Numeric) -> float:
  return round(random.uniform(lower, upper), Constants.DEFAULT_ROUNDING_ACCURACY)

@validate_output_probability
def generate_probability_value() -> float:
  """Generates a random real number in the interval `[0,1]` (inclusive) using a distribution."""
  return generate_float_in_range(0,1)

@validate_input_probability
def evaluate_probability(p: float) -> bool:
  value: float = generate_probability_value()
  if p > value or p == 1: return True
  return False

def is_combat_encounter() -> bool: return evaluate_probability(Constants.COMBAT_ENCOUNTER_PROBABILITY)

def is_structure_encounter() -> bool: return evaluate_probability(Constants.STRUCTURE_ENCOUNTER_PROBABILITY)

def is_boss_encounter() -> bool: return evaluate_probability(Constants.BOSS_ENCOUNTER_PROBABILITY)

## integers
@validate_bounds()
def generate_random_int_in_range(lower: int, upper: int) -> int:
  """Returns an integer in the interval `[lower, upper)` (not inclusive)."""
  if lower >= upper: raise ValueError(f"Bound {lower=} cannot be greater than or equal to bound {upper=}.")
  return random.randrange(lower, upper)

def generate_structure_item_count() -> int:
  return generate_random_int_in_range(Constants.MIN_STRUCTURE_ITEM_COUNT, Constants.MAX_STRUCTURE_ITEM_COUNT)

def generate_enemy_count() -> int:
  return generate_random_int_in_range(Constants.MIN_ENEMIES, Constants.MAX_ENEMIES)

def select_random_identifier(dictionary: dict[int, Any]) -> int:
  identifiers: list[int] = list(dictionary.keys())
  selected_index: int = generate_random_int_in_range(0, len(identifiers))
  return identifiers[selected_index]

def get_random_position(dimensions: Position) -> Position:
  x: int = generate_random_int_in_range(0, dimensions[0])
  y: int = generate_random_int_in_range(0, dimensions[1])
  return (x,y)

## decision-making-related



EOF
tools/logging_tools.py

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


EOF
tools/positional_tools.py

from tools.typing_tools import *
from tools.exceptions import InvalidPositionError
from math import sqrt, pow

# decorators

def validate_position(dimensions: Position) -> Callable[[Position], None]:
  def inner(position: Position) -> None:
    if position[0] >= dimensions[0] or position[1] >= dimensions[1] or position[0] < 0 or position[1] < 0:
      raise InvalidPositionError(position, dimensions)
  return inner

def validate_position_on[T](func: Callable[..., T]) -> Callable[..., T]:
  """When being applied to a method in `Matrix` or `FightingEnemyGraph`, `position` must always be the first argument."""
  def wrapper(self, position: Position, *args, **kwargs) -> T:
    validate_position(self.dimensions)(position)
    return func(self, position, *args, **kwargs)
  return wrapper

# functions

def length_to_point(length: int, dimensions: Position) -> Position:
    x: int = length % dimensions[0]
    y: int = length // dimensions[0]
    position: Position = (x,y)
    validate_position(dimensions)(position)
    return position

def calculate_distance(p1: Position, p2: Position) -> float:
    (x1, y1) = p1
    (x2, y2) = p2
    return sqrt(pow(x1-x2, 2) + pow(y1-y2, 2))

EOF
tools/tkinter_tools.py

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

EOF
tools/typing_tools.py

import tkinter as tk

from collections.abc import Callable
from types import FunctionType
from typing import Any, Concatenate, Dict, Generic, Iterable, Self, Sized, Literal, Optional, Type, TypeVar, Union, cast
from multipledispatch import dispatch
from enum import Enum, Flag, IntEnum, StrEnum, unique
from dataclasses import dataclass, field
from functools import reduce

# custom types

type ButtonCommand = Callable[[], None]
type Position = tuple[int, int]
"A discrete, `(x,y)` point on a 2D plane."
type ActionLocation = Optional[Position]
type EnemyActionTag = Union[Literal["Attack"], int]
"either \"Attack\" (denoting the enemy's attack), or the `AbilityID` of the `Ability` it will use"
type Numeric = Union[int, float]
"Any real number, being either a `float` or `int`."

type DynamicButtonInput = tuple[str, Union[Any, tuple[Any, ...]]]
"""
The significance of each value of the tuple is as follows:
1. `text` - what the text value of the button is set to
2. `args` - command positional arguments. If there is `0` or `1`, a collection need not be used, but any more requires a tuple.
"""



# functions

def unpack_optional[T](option: Optional[T]) -> T:
  """
  Converts an argument of unknown type from an optional to a non-optional. If the argument is `None`, a value error is raised.
  
  :param option: An optional variable. Must have a value not `None`, otherwise it will raise a value error.
  :type option: Optional[T]
  :return: The argument in non-optional form.
  :rtype: T
  """
  if option == None: raise ValueError(f"Tried to unpack argument \'option\'=`{option}`")
  return option

def unpack_optional_bool(option: Optional[bool], default: bool) -> bool:
  if option == True: return True
  return default

def unpack_optional_string(option: Optional[str], default: str = "") -> str:
  if option == None: return default
  return option

# custom generic typ

EOF
tools/__init__.py

__all__ = ["ability_names", "constants", "decision_tools", "dictionary_tools", "exceptions", "generation_tools", "positional_tools", "typing_tools", "tkinter_tools", "logging_tools"]

from . import ability_names
from . import constants
from . import decision_tools
from . import dictionary_tools
from . import exceptions
from . import generation_tools
from . import logging_tools
from . import positional_tools
from . import tkinter_tools
from . import typing_tools

EOF
stored/modifiers/abstract_modifier.py

from tools.typing_tools import *
from tools.constants import TableName

from database.condition import Condition
from stored.stored import Stored

class AbstractModifier(Stored):
  def __init__(self, loaded: bool = True) -> None:
    super().__init__(loaded)

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]: return []

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_abstract_modifier(data, loaded)
  
  @staticmethod
  def identical_condition(abstract_modifier_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_abstract_modifier(abstract_modifier_data: list[Any] = [], loaded: bool = True) -> AbstractModifier:
  return AbstractModifier()

EOF
stored/modifiers/character_modifier.py

from tools.typing_tools import *
from tools.constants import TableName

from database.condition import Condition
from stored.stored import Stored

class CharacterModifier(Stored):
  def __init__(self, loaded: bool = True) -> None:
    # CharacterID, AbilityID, RemainingTurns
    super().__init__(loaded)

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]: return []

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_character_modifier(data, loaded)
  
  @staticmethod
  def identical_condition(character_modifier_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_character_modifier(character_modifier_data: list[Any] = [], loaded: bool = True) -> CharacterModifier:
  return CharacterModifier()

EOF
stored/modifiers/fighting_enemy_modifier.py

from tools.typing_tools import *
from tools.constants import TableName

from database.condition import Condition
from stored.stored import Stored

class FightingEnemyModifier(Stored):
  def __init__(self, loaded: bool = True) -> None:
    super().__init__(loaded)

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]: return []

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_fighting_enemy_modifier(data, loaded)
  
  @staticmethod
  def identical_condition(fighting_enemy_modifier_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_fighting_enemy_modifier(fighting_enemy_modifier_data: list[Any] = [], loaded: bool = True) -> FightingEnemyModifier:
  return FightingEnemyModifier()

EOF
stored/modifiers/__init__.py

__all__ = ["abstract_modifier", "character_modifier", "fighting_enemy_modifier"]

from . import abstract_modifier
from . import character_modifier
from . import fighting_enemy_modifier

EOF
stored/items/abstract_item.py

from tools.typing_tools import *

from database.condition import Condition
from stored.stored import *

class AbstractItem(Stored):
  def __init__(self, loaded: bool = True) -> None:
    super().__init__(loaded)

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]: return []

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_abstract_item(data, loaded)
  
  @staticmethod
  def identical_condition(abstract_item_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_abstract_item(abstract_item_data: list[Any] = [], loaded: bool = True) -> AbstractItem:
  return AbstractItem()

EOF
stored/items/abstract_storage_item.py

from tools.typing_tools import *

from database.condition import Condition
from stored.stored import *

class AbstractStorageItem(Stored):
  def __init__(self, item_id: int, stack_size: int, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.item_id = item_id
    self.stack_size = stack_size

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]:
    return [self.item_id, self.stack_size]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_abstract_storage_item(data, loaded)
  
  @staticmethod
  def identical_condition(abstract_storage_item_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_abstract_storage_item(abstract_storage_item_data: list[Any] = [], loaded: bool = True) -> AbstractStorageItem:
  item_id: int = abstract_storage_item_data[0]
  stack_size: int = abstract_storage_item_data[1]
  return AbstractStorageItem(item_id, stack_size, loaded)

EOF
stored/items/equipable.py

from database.condition import Condition
from tools.typing_tools import *

from stored.items.abstract_item import *

class Equipable(AbstractItem):
  def __init__(self, item_id: int, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.item_id = item_id

  @staticmethod
  def get_table_name() -> TableName: return TableName.EQUIPABLE

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.item_id]
  
  @staticmethod
  def instantiate(equipable_data: list[Any], loaded: bool = True):
    return instantiate_equipable(equipable_data, loaded)
  
  @staticmethod
  def identical_condition(_stored_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_equipable(equipable_data: list[Any], loaded: bool = True) -> Equipable:
  item_id: int = equipable_data[0]
  return Equipable(item_id, loaded)

EOF
stored/items/inventory_item.py

from tools.typing_tools import *

from database.condition import Condition
from stored.items.abstract_storage_item import *

class InventoryItem(AbstractStorageItem):
  """
  Link between \'Character\' and \'Item\' to allow items to be stored in the character's inventory.
  
  :param character_id: The identifier for the character whose inventory the item is linked to.
  :type character_id: int
  :param item_id: The identifier for the item stored in the inventory.
  :type item_id: int
  :param stack_size: Amount of this item in the inventory. Cannot go below 1.
  :type stack_size: int
  :param equipped: Is `True` if this item has been equipped to the character. For specific item types.
  :type equipped: bool
  :param loaded: Whether the object has been loaded into memory or not. Defaults to `True`.
  :type loaded: bool
  """
  def __init__(self, character_id: int, item_id: int, stack_size: int = 1, equipped: bool = False, loaded: bool = True) -> None:
    super().__init__(item_id, stack_size, loaded)
    self.character_id = character_id
    self.equipped = equipped

  @staticmethod
  def get_table_name() -> TableName: return TableName.INVENTORY_ITEM

  def get_raw_data(self) -> list[Any]:
    return [self.character_id] + super().get_raw_data() + [self.equipped]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_inventory_item(data, loaded)
  
  @staticmethod
  def identical_condition(inventory_item_row: list[Any]) -> Condition:
    return Condition(lambda _, row: row[0] == inventory_item_row[0] and row[1] == inventory_item_row[1])
  
  # built-in methods
  
  def __repr__(self) -> str:
    return f"InventoryItem(`{self.character_id=}`, `{self.item_id=}`, `{self.stack_size=}`, `{self.equipped=}`)"

def instantiate_inventory_item(inventory_item_data: list[Any] = [], loaded: bool = True) -> InventoryItem:
  character_id: int = inventory_item_data[0]
  item_id: int = inventory_item_data[1]
  stack_size: int = inventory_item_data[2]
  equipped: bool = inventory_item_data[3]
  return InventoryItem(character_id, item_id, stack_size, equipped, loaded)

EOF
stored/items/item.py

from tools.typing_tools import *

from stored.stored import *
from tools.constants import ItemType

class Item(Stored):
  def __init__(self, item_type: ItemType, name: str, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.item_type = item_type
    self.name = name

  @staticmethod
  def get_table_name() -> TableName: return TableName.ITEM

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.item_type, self.name]
  
  @staticmethod
  def instantiate(item_data: list[Any], loaded: bool = True):
    return instantiate_item(item_data, loaded)

def instantiate_item(item_data: list[Any], loaded: bool = True) -> Item:
  item_type: ItemType = item_data[0]
  name: str = item_data[1]
  return Item(item_type, name, loaded)

EOF
stored/items/storage.py

from tools.typing_tools import *
from tools.constants import *

from database.condition import Condition
from stored.stored import *

class Storage(Stored):
  def __init__(self, world_id: int, storage_type: StorageType, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.world_id = world_id
    self.storage_type = storage_type

  @staticmethod
  def get_table_name() -> TableName: return TableName.STORAGE

  def get_raw_data(self) -> list[Any]:
    return [self.world_id, self.storage_type]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_storage(data, loaded)
  
  @staticmethod
  def identical_condition(storage_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_storage(storage_data: list[Any] = [], loaded: bool = True) -> Storage:
  world_id: int = storage_data[0]
  storage_type: StorageType = storage_data[1]
  return Storage(world_id, storage_type, loaded)

EOF
stored/items/storage_item.py

from tools.typing_tools import *

from database.condition import Condition
from stored.items.abstract_storage_item import *

class StorageItem(AbstractStorageItem):
  """
  Link between \'Storage\' and \'Item\' to allow items to be stored in an existing storage object.
  
  :param storage_id: The identifier for the storage whose contents the item is linked to.
  :type storage_id: int
  :param item_id: The identifier for the item stored in the storage.
  :type item_id: int
  :param stack_size: Amount of this item in the storage. Cannot go below 1.
  :type stack_size: int
  :param loaded: Whether the object has been loaded into memory or not. Defaults to \'True\'.
  :type loaded: bool
  """
  def __init__(self, storage_id: int, item_id: int, stack_size: int = 1, loaded: bool = True) -> None:
    super().__init__(item_id, stack_size, loaded)
    self.storage_id = storage_id

  @staticmethod
  def get_table_name() -> TableName: return TableName.STORAGE_ITEM

  def get_raw_data(self) -> list[Any]:
    return [self.storage_id] + super().get_raw_data()

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_storage_item(data, loaded)
  
  @staticmethod
  def identical_condition(storage_item_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_storage_item(storage_item_data: list[Any] = [], loaded: bool = True) -> StorageItem:
  storage_id: int = storage_item_data[0]
  item_id: int = storage_item_data[1]
  stack_size: int = storage_item_data[2]
  return StorageItem(storage_id, item_id, stack_size, loaded)

EOF
stored/items/weapon.py

from tools.typing_tools import *

from database.condition import Condition
from stored.items.abstract_item import *

class Weapon(AbstractItem):
  def __init__(self, item_id: int, damage: float, uses_ammunition: bool = False, mana_used: float = 0, active: bool = False, loaded: bool = True) -> None: #TODO: add all parts of Weapon
    super().__init__(loaded)
    self.item_id = item_id
    self.damage = damage
    self.uses_ammunition = uses_ammunition
    self.mana_used = mana_used
    self.active = active

  @staticmethod
  def get_table_name() -> TableName: return TableName.WEAPON

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.item_id, self.damage, self.uses_ammunition, self.mana_used, self.active]

  @staticmethod
  def instantiate(weapon_data: list[Any], loaded: bool = True):
    return instantiate_weapon(weapon_data, loaded)
  
  @staticmethod
  def identical_condition(weapon_row: list[Any]) -> Condition:
    return Condition(lambda _, row: weapon_row[0] == row[0])
  
  # built-in methods

  def __repr__(self) -> str:
    return f"Weapon({self.item_id=}, {self.damage=}, {self.uses_ammunition=}, {self.mana_used=}, {self.active=})"

def instantiate_weapon(weapon_data: list[Any], loaded: bool = True) -> Weapon:
  item_id: int = weapon_data[0]
  damage: float = weapon_data[1]
  uses_ammunition: bool = weapon_data[2]
  mana_used: float = weapon_data[3]
  active: bool = weapon_data[4]
  return Weapon(item_id, damage, uses_ammunition, mana_used, active, loaded)

EOF
stored/items/__init__.py

__all__ = ["abstract_storage_item", "equipable", "inventory_item", "item", "weapon", "abstract_item", "storage_item", "storage"]

from . import abstract_storage_item
from . import equipable
from . import inventory_item
from . import item
from . import weapon
from . import storage_item
from . import storage
from . import abstract_item

EOF
stored/entities/character.py

from tools.typing_tools import *
from tools.decision_tools import *

from stored.entities.fighting_entity import *
from database.condition import Condition

from data_structures.queue import Queue

#"CharacterID", "UserID", "Name", "Health", "MaxHealth",
class Character(FightingEntity):
  def __init__(self, user_id: int, name: str, health: float, max_health: float, loaded: bool = True) -> None:
    """
    Docstring for __init__
    
    :param user_id: User who the `Character` object is attatched to.
    :type user_id: int
    :param name: Name of the character.
    :type name: str
    :param health: How much health the character currently has.
    :type health: float
    """
    super().__init__(name, health, max_health, loaded)
    self.user_id = user_id

  @staticmethod
  def get_table_name() -> TableName: return TableName.CHARACTER

  def get_raw_data(self) -> list[Any]:
    return [self.user_id, self.name, self.health, self.max_health]
  
  @staticmethod
  def instantiate(character_data: list[Any], loaded: bool = True):
    return instantiate_character(character_data, loaded)
  
  @staticmethod
  def identical_condition(entity_row: list[Any]) -> Condition:
    return Condition(lambda _, row: entity_row[0] == row[0] and entity_row[1] == row[1])
  
  @staticmethod
  def get_default_max_health() -> float: return 100

  # built-in methods

  def __repr__(self) -> str:
    return f"Character({self.user_id}, {self.name=}, {self.health=}, {self.max_health=})"
  
  # decision-making methods for enemies

  def calculate_aggressiveness_info(self, remaining_ignition_duration: Optional[int], is_target_parrying: bool) -> tuple[float, int]:
    return super().calculate_aggressiveness_info(remaining_ignition_duration, is_target_parrying)

def instantiate_character(character_data: list[Any], loaded: bool = True) -> Character:
  user_id: int = character_data[0]
  name: str = character_data[1]
  health: float = character_data[2]
  max_health: float = character_data[3]
  return Character(user_id, name, health, max_health, loaded)

EOF
stored/entities/enemy.py

from tools.typing_tools import *

from stored.stored import *
from database.condition import Condition

class Enemy(Stored):
  def __init__(self, name: str, max_health: float, attack_damage: float, intelligence: float, is_boss: bool, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.name = name
    self.max_health = max_health
    self.attack_damage = attack_damage
    self.intelligence = intelligence
    self.is_boss = is_boss

  @staticmethod
  def get_table_name() -> TableName: return TableName.ENEMY

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.name, self.max_health, self.attack_damage, self.intelligence, self.is_boss]
  
  @staticmethod
  def instantiate(enemy_data: list[Any], loaded: bool = True):
    return instantiate_enemy(enemy_data, loaded)

def instantiate_enemy(enemy_data: list[Any], loaded: bool = True) -> Enemy:
  name: str = enemy_data[0]
  max_health: float = enemy_data[1]
  attack_damage: float = enemy_data[2]
  intelligence: float = enemy_data[3]
  is_boss: bool = enemy_data[4]
  return Enemy(name, max_health, attack_damage, intelligence, is_boss, loaded)

EOF
stored/entities/entity.py

from database.condition import Condition
from tools.typing_tools import *

from stored.stored import *

class Entity(Stored):
  def __init__(self, name: str, max_health: float, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.name = name
    self.max_health = max_health

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.name, self.max_health]
  
  @staticmethod
  def instantiate(entity_data: list[Any], loaded: bool = True):
    return instantiate_entity(entity_data, loaded)
  
  @staticmethod
  def identical_condition(entity_row) -> Condition:
    return Condition(lambda _, row: entity_row[0] == row[0])
  

def instantiate_entity(entity_data: list[Any], loaded: bool = True) -> Entity:
  name: str = entity_data[0]
  max_health: float = entity_data[1]
  return Entity(name, max_health, loaded)


EOF
stored/entities/fighting_enemy.py

from tools.typing_tools import *
from tools.decision_tools import *
from tools.constants import *

from data_structures.action_type import ActionType

from stored.entities.fighting_entity import *
from stored.abilities.abstract_ability import AbstractAbility

from database.condition import Condition

from ability_action import *

def validate_action_name[FightingEnemyType: FightingEnemy, ReturnType](func: Callable[Concatenate[FightingEnemyType, ...], ReturnType]) -> Callable[Concatenate[FightingEnemyType, ...], ReturnType]:
  def wrapper(self: FightingEnemyType, action_name: ActionName, *args, **kwargs) -> ReturnType:
    if not action_name in self.VALID_ACTION_NAMES: raise ValueError(f"`{action_name=}` not in `{self.VALID_ACTION_NAMES}`.")
    return func(self, action_name, *args, **kwargs)
  return wrapper

class FightingEnemy(FightingEntity):
  def __init__(self, enemy_id: int, name: str, health: float, max_health: float, attack_damage: float, intelligence: float, loaded: bool = True) -> None:
    super().__init__(name, health, max_health, loaded)
    self.enemy_id: int = enemy_id
    self.attack_damage: float = attack_damage
    self.intelligence: float = intelligence
    self.decision_error_bound: float = get_decision_error_bound(self.intelligence)

    self.__action_offensiveness_table: dict[ActionName, float] = {
      ActionName.ATTACK: 0,
      ActionName.HEAL: 0,
    }
    self.ability_id_table: dict[ActionName, Optional[int]] = {}

    self.VALID_ACTION_NAMES: list[ActionName] = [ActionName.ATTACK, ActionName.HEAL]

    self.aggressiveness: float

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]:
    return [self.enemy_id] + super().get_raw_data() + [self.attack_damage, self.intelligence]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_fighting_enemy(data, loaded)
  
  @staticmethod
  def identical_condition(fighting_enemy_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)
  
  # built-in methods

  @validate_action_name
  def get_action_offensiveness(self, action_name: ActionName) -> float:
    return self.__action_offensiveness_table[action_name]
  
  @validate_action_name
  def set_action_offensiveness(self, action_name: ActionName, offensiveness: float) -> None:
    self.__action_offensiveness_table[action_name] = offensiveness
  
  # decision making methods

  def set_action_identifiers(self, attack_ability_id: Optional[int], heal_ability_id: Optional[int]) -> None:
    self.ability_id_table[ActionName.ATTACK] = attack_ability_id
    self.ability_id_table[ActionName.HEAL] = heal_ability_id

  ## calculating action values
  def calculate_action_offensiveness_value(self, ability: AbstractAbility, action_name: ActionName, store_result: bool = True) -> float:
    offensiveness_value: float = ability.calculate_offensiveness()
    if store_result:
      self.set_action_offensiveness(action_name, store_result)
    return offensiveness_value
      
  ## aggressiveness calculations
  def generate_decision_error(self) -> float:
    return generate_decision_error(self.decision_error_bound)
  
  def clip_aggressiveness(self, aggressiveness: float) -> float:
    return clip(aggressiveness, -self.decision_error_bound, self.decision_error_bound)

  def calculate_aggressiveness(self, remaining_ignition_duration: Optional[int], is_target_parrying: bool, negative_character_total: float, character_n: int) -> float:
    (total, n) = self.calculate_aggressiveness_info(remaining_ignition_duration, is_target_parrying)
    total += negative_character_total
    n += character_n
    self.aggressiveness = total / n
    decision_error: float = self.generate_decision_error()
    self.aggressiveness = self.clip_aggressiveness(self.aggressiveness + decision_error)
    return self.aggressiveness
  
  ## choosing the action
  def choose_action_name(self) -> ActionName:
    chosen_action: Optional[tuple[ActionName, float]] = None
    if len(self.__action_offensiveness_table) == 0: raise BufferError(f"{self.__action_offensiveness_table=} cannot be empty when choosing the action tag.")
    for (action_name, offensiveness) in self.__action_offensiveness_table.items():
      deviation: float = self.calculate_aggressiveness_squared_deviation(offensiveness)
      if chosen_action == None:
        chosen_action = (action_name, deviation)
      elif deviation < chosen_action[1]:
        chosen_action = (action_name, deviation)
    if chosen_action == None: raise ValueError(f"{chosen_action=} must not be `None` by this point.")
    return chosen_action[0]

def instantiate_fighting_enemy(fighting_enemy_data: list[Any] = [], loaded: bool = True) -> FightingEnemy:
  enemy_id: int = fighting_enemy_data[0]
  name: str = fighting_enemy_data[1]
  health: float = fighting_enemy_data[2]
  max_health: float = fighting_enemy_data[3]
  attack_damage: float = fighting_enemy_data[4]
  return FightingEnemy(enemy_id, name, health, max_health, attack_damage, loaded)


EOF
stored/entities/fighting_entity.py

from tools.typing_tools import *
from tools.exceptions import HealthSetError
from tools.decision_tools import *
from tools.logging_tools import *

from stored.stored import *

from data_structures.queue import Queue

from ability_action import *

# decorators and generators

type FormattableFightingEntityCallable[FightingEntityType: FightingEntity] = Callable[Concatenate[FightingEntityType, ...], str]

def format_message_info(message: str, descriptor: Optional[str] = None, units: str = "", add_brackets: bool = False, add_colon_at_end: bool = False, add_comma_at_end: bool = False, capitalise: bool = False) -> str:
  message = f"{message}{units}"
  if descriptor != None:
    message = f"{descriptor}={message}"
  if add_brackets:
    message = f"({message})"
  if add_colon_at_end:
    message = f"{message}:"
  if add_comma_at_end:
    message = f"{message},"
  if capitalise:
    message = f"{message.upper()}"
  return message

def prepend_message_info[FightingEntityType: FightingEntity](attribute_tag: Union[str, int], descriptor: Optional[str] = None, units: str = "", add_brackets: bool = False, add_colon_at_end: bool = False, add_comma_at_end: bool = False, capitalise: bool = False) -> Callable[[FormattableFightingEntityCallable[FightingEntityType]], FormattableFightingEntityCallable[FightingEntityType]]:
  """
  :param attribute_tag: If of type `str`, the name of the attribute in `FightingEntityType` which will be prepended. If of type `int`, it indexes the argument will be used in prepending.
  :type attribute_tag: Union[str, int]
  """
  def decorator(func: FormattableFightingEntityCallable[FightingEntityType]) -> FormattableFightingEntityCallable[FightingEntityType]:
    def wrapper(self: FightingEntityType, *args, **kwargs) -> str:
      attribute_str: str
      if type(attribute_tag) == int:
        attribute_str = args[attribute_tag]
      elif type(attribute_tag) == str:
        attribute_str = format(getattr(self, attribute_tag))
      info: str = format_message_info(attribute_str, descriptor, units, add_brackets, add_colon_at_end, add_comma_at_end, capitalise)
      body: str = func(self, *args, **kwargs)
      return f"{info} {body}"
    return wrapper
  return decorator

def append_message_info[FightingEntityType: FightingEntity](attribute_tag: Union[str, int], descriptor: Optional[str] = None, units: str = "", add_brackets: bool = False, add_colon_at_end: bool = False, add_comma_at_end: bool = False, capitalise: bool = False) -> Callable[[FormattableFightingEntityCallable[FightingEntityType]], FormattableFightingEntityCallable[FightingEntityType]]:
  """
  :param attribute_tag: If of type `str`, the name of the attribute in `FightingEntityType` which will be prepended. If of type `int`, it indexes the argument will be used in prepending.
  :type attribute_tag: Union[str, int]
  """
  def decorator(func: FormattableFightingEntityCallable[FightingEntityType]) -> FormattableFightingEntityCallable[FightingEntityType]:
    def wrapper(self: FightingEntityType, *args, **kwargs) -> str:
      attribute_str: str
      if type(attribute_tag) == int:
        attribute_str = args[attribute_tag]
      elif type(attribute_tag) == str:
        attribute_str = format(getattr(self, attribute_tag))
      body: str = func(self, *args, **kwargs)
      info: str = format_message_info(attribute_str, descriptor, units, add_brackets, add_colon_at_end, add_comma_at_end, capitalise)
      return f"{body} {info}"
    return wrapper
  return decorator

# class

class FightingEntity(Stored):
  def __init__(self, name: str, health: float, max_health: float, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.name = name
    self.health = health
    self.max_health = max_health
    # attributes not stored in the database, but which are still important
    self.damage_resistance: float = 0
    self.is_ignited: bool = False
    self.is_pierced: bool = False
    # parrying data
    self.is_parrying: bool = False
    self.parry_damage_threshold: Optional[float] = None
    self.parry_reflection_proportion: Optional[float] = None

    self.aggressiveness: float = 0

  # built-in methods

  def __repr__(self) -> str:
    return f"FightingEntity({self.name=}, {self.health=}, {self.max_health=})"

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.health]
  
  @staticmethod
  def instantiate(fighting_entity_data: list[Any], loaded: bool = True):
    return instantiate_fighting_entity(fighting_entity_data, loaded)
  
  # variable-setting methods

  def set_health(self, new_health: float) -> None:
    if new_health > self.max_health or new_health < 0:
      raise HealthSetError(new_health, self.max_health)
    self.health = new_health

  def reset_health(self) -> None:
    self.set_health(self.max_health)

  @append_message_info(0, descriptor="HEAL", units="HP", add_brackets=True)
  def change_health(self, amount: float) -> str:
    new_health: float = self.health + amount
    if new_health < 0: new_health = 0
    elif new_health > self.max_health:
      new_health = self.max_health
    self.set_health(new_health)
    return f"Health set to {self.health}"

  @append_message_info(0, descriptor="RAW", units="DMG", add_brackets=True)
  def take_damage(self, damage_amount: float) -> str:
    modified_damage_amount: float = damage_amount
    if not self.is_pierced or self.damage_resistance < 0:
      modified_damage_amount = self.apply_damage_resistance(damage_amount)
    if modified_damage_amount < 0: raise ValueError(f"{modified_damage_amount=} less than zero.")
    self.change_health(-1*modified_damage_amount)
    return f"Recieved {modified_damage_amount}DMG"

  def apply_damage_resistance(self, damage_amount: float) -> float:
    new_damage_amount: float = damage_amount * (1-self.damage_resistance)
    if new_damage_amount < 0: raise ValueError(f"`{new_damage_amount=}` is less than `0` after `{self.damage_resistance=}` was applied.")
    return new_damage_amount

  def heal(self, heal_amount: float) -> str:
    if heal_amount < 0:
      raise ValueError(f"{heal_amount=} less than zero.")
    return self.change_health(heal_amount)

  # ability / modifier methods

  @prepend_message_info("name", add_colon_at_end=True, capitalise=True)
  def apply_ability(self, ability: AbilityAction) -> str:
    if type(ability) == IgniteAction: return self.ignite()
    elif type(ability) == DefendAction: return self.defend(ability.resistance)
    elif type(ability) == WeakenAction: return self.weaken(ability.vulnerability)
    elif type(ability) == PierceAction: return self.pierce()
    elif type(ability) == ParryAction: return self.engage_parry(ability.damage_threshold, ability.reflection_proportion)
    raise TypeError(f"Unexpected {ability=} of {type(ability)=}")

  @prepend_message_info("name", add_colon_at_end=True, capitalise=True)
  def inflict_active_effects(self) -> str:
    if self.is_ignited: return self.deal_ignite()
    return ""

  @prepend_message_info("name", add_colon_at_end=True, capitalise=True)
  def remove_ability(self, ability: AbilityAction) -> str:
    if type(ability) == IgniteAction: return self.unignite()
    elif type(ability) == DefendAction: return self.undefend(ability.resistance)
    elif type(ability) == WeakenAction: return self.unweaken(ability.vulnerability)
    elif type(ability) == PierceAction: return self.unpierce()
    elif type(ability) == ParryAction: return self.unengage_parry()
    raise TypeError(f"Unexpected {ability=} of {type(ability)=}")

  ## ignition
  def ignite(self) -> str:
    self.is_ignited = True
    return f"Ignited"

  def deal_ignite(self) -> str:
    ignition_damage_message: str = self.take_damage(Constants.IGNITE_DAMAGE)
    return f"{ignition_damage_message} from being ignited"

  def unignite(self) -> str:
    self.is_ignited = False
    return f"Extinguished"
  
  ## defending
  @append_message_info(0, "RESIST", add_brackets=True, add_comma_at_end=True)
  @append_message_info("damage_resistance", "TOTAL", add_brackets=True)
  def defend(self, resistance: float) -> str:
    if resistance < 0: raise ValueError(f"{resistance=} cannot be less than `0`.")
    self.damage_resistance += resistance
    return f"Defending"

  @append_message_info("damage_resistance", "RESIST", add_brackets=True)
  def undefend(self, resistance: float) -> str:
    if resistance < 0: raise ValueError(f"{resistance=} cannot be less than `0`.")
    self.damage_resistance -= resistance
    return f"Defend ended"

  ## weakening
  @append_message_info(0, descriptor="VULN", add_brackets=True, add_comma_at_end=True)
  @append_message_info("damage_resistance", descriptor="TOTAL", add_brackets=True)
  def weaken(self, vulnerability: float) -> str:
    if vulnerability < 0: raise ValueError(f"{vulnerability=} cannot be less than `0`.")
    self.damage_resistance -= vulnerability
    return f"Weakened"

  @append_message_info("damage_resistance", descriptor="TOTAL", add_brackets=True)
  def unweaken(self, vulnerability: float) -> str:
    if vulnerability < 0: raise ValueError(f"{vulnerability=} cannot be less than `0`.")
    self.damage_resistance += vulnerability
    return f"Weaken ended"

  ## piercing
  def pierce(self) -> str:
    self.is_pierced = True
    return f"Pierced"

  def unpierce(self) -> str:
    self.is_pierced = False
    return f"Pierce ended"

  ## parrying
  @append_message_info("parry_reflection_proportion", descriptor="RFLC", add_brackets=True)
  @append_message_info("parry_damage_threshold", descriptor="DMG", add_brackets=True, add_comma_at_end=True)
  def engage_parry(self, damage_threshold: float, reflection_proportion: float) -> str:
    if damage_threshold <= 0: raise ValueError(f"`{damage_threshold=}` cannot be less than or equal to `0`.")
    if reflection_proportion < 0: raise ValueError(f"`{reflection_proportion=}` cannot be less than `0`.")
    self.is_parrying = True
    self.parry_damage_threshold = damage_threshold
    self.parry_reflection_proportion = reflection_proportion
    return f"Parry engaged"

  def unengage_parry(self) -> str:
    self.is_parrying = False
    self.parry_damage_threshold = None
    self.parry_reflection_proportion = None
    return f"Parry unengaged"

  # decision-making

  def calculate_aggressiveness_info(self, remaining_ignition_duration: Optional[int], is_target_parrying: bool) -> tuple[float, int]:
    """
    :return: A pair of numbers, the first being the total aggressiveness and the second being the number of values computed.
    :rtype: tuple[float, int]
    """
    aggressiveness_values = Queue[float]()
    aggressiveness_values.put(self.calculate_health_aggressiveness())
    aggressiveness_values.put(self.calculate_ignited_aggressiveness(remaining_ignition_duration))
    aggressiveness_values.put(self.calculate_damage_resistance_aggressiveness())
    aggressiveness_values.put(self.calculate_target_parry_aggressiveness(is_target_parrying))
    total: float = 0
    n: int = 0
    while not aggressiveness_values.empty():
      total += aggressiveness_values.get()
      n += 1
    return (total, n)

  def calculate_aggressiveness(self, remaining_ignition_duration: Optional[int], is_target_parrying: bool) -> float:
    (total, n) = self.calculate_aggressiveness_info(remaining_ignition_duration, is_target_parrying)
    return total/n

  def calculate_health_aggressiveness(self) -> float:
    """
    :return: In interval `[-1,1]`.
    :rtype: float
    """
    return calculate_health_aggressiveness(self.health, self.max_health)
  
  def calculate_ignited_aggressiveness(self, remaining_duration: Optional[int]) -> float:
    """
    :param remaining_duration: The number of turns the ignition will be active for. When it is `None`, it signifies not being ignited.
    :type remaining_duration: Optional[int]
    """
    return calculate_ignited_aggressiveness(self.health, self.max_health, remaining_duration)
  
  def calculate_damage_resistance_aggressiveness(self) -> float:
    """
    :return: In interval `[-1,1]`.
    :rtype: float
    """
    return calculate_damage_resistance_aggressiveness(self.damage_resistance, self.is_pierced)
  
  def calculate_target_parry_aggressiveness(self, is_target_parrying: bool) -> float:
    return calculate_target_parry_aggressiveness(is_target_parrying)
  
  def calculate_aggressiveness_squared_deviation(self, offensiveness: float) -> float:
    return pow(self.aggressiveness - offensiveness, 2)

def instantiate_fighting_entity(fighting_entity_data: list[Any], loaded: bool = True) -> FightingEntity:
  name: str = fighting_entity_data[0]
  health: float = fighting_entity_data[1]
  max_health: float = fighting_entity_data[2]
  return FightingEntity(name, health, max_health, loaded)


EOF
stored/entities/__init__.py

__all__ = ["character", "enemy", "entity", "fighting_entity"]

from . import character
from . import enemy
from . import entity
from . import fighting_entity

EOF
stored/abilities/ability.py

from tools.typing_tools import *
from tools.ability_names import *

from database.condition import Condition

from stored.stored import *
from stored.abilities.abstract_ability import AbstractAbility
from stored.abilities.parry_ability import ParryAbility
from stored.abilities.statistic_ability import AbstractAbility

from ability_action import *

class Ability(Stored):
  """
  :param text: The ability's description.
  :type text: str
  :param ability_type: The ability type table which the ability data can be found in.
  :type ability_type: AbilityTypeName
  """
  def __init__(self, text: str, ability_type: AbilityTypeName, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.text = text
    self.ability_type = ability_type

  @staticmethod
  def get_table_name() -> TableName: return TableName.ABILITY

  def get_raw_data(self) -> list[Any]:
    return [self.text, self.ability_type]
  
  @staticmethod
  def instantiate(ability_data: list[Any], loaded: bool = True):
    return instantiate_ability(ability_data, loaded)
  
  @staticmethod
  def identical_condition(stored_row: list[Any]) -> Condition:
    return Condition(lambda _identifier, row: stored_row[0] == row[0] and stored_row[1] == row[1])
  
  # built-in methods

  def __repr__(self) -> str:
    return f"Ability(`{self.text=}`, `{self.ability_type=}`)"
  
  # ability action and specialisation methods

  def get_abstract_ability_class_name(self) -> Optional[AbstractAbilityClassName]:
    """For more information, see `ability_type_name_to_abstract_ability_class_name` in `ability_names`."""
    return ability_type_name_to_abstract_ability_class_name(self.ability_type)
  
  def get_ability_action(self) -> AbilityAction:
    raise NotImplementedError()
  
def instantiate_ability(ability_data: list[Any], loaded: bool = True) -> Ability:
  text: str = ability_data[0]
  ability_type: AbilityTypeName = ability_data[1]
  return Ability(text, ability_type, loaded)

EOF
stored/abilities/abstract_ability.py

from tools.typing_tools import *

from database.condition import Condition
from stored.stored import *

from ability_action import AbilityAction

class AbstractAbility(Stored):
  def __init__(self, ability_id: int, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.ability_id: int = ability_id

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]:
    return [self.ability_id]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_abstract_ability(data, loaded)
  
  @staticmethod
  def identical_condition(abstract_ability_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)
  
  # offensiveness and decision-making methods

  def calculate_offensiveness(self) -> float: raise NotImplementedError()

  def get_ability_action(self) -> AbilityAction: raise NotImplementedError()

def instantiate_abstract_ability(abstract_ability_data: list[Any] = [], loaded: bool = True) -> AbstractAbility:
  ability_id: int = abstract_ability_data[0]
  return AbstractAbility(ability_id, loaded)

EOF
stored/abilities/enemy_ability.py

from tools.typing_tools import Any

from database.condition import Condition
from stored.stored import Stored, TableName

class EnemyAbility(Stored):
  def __init__(self, enemy_id: int, ability_id: int, is_used_in_attack: bool, loaded: bool = True) -> None: # "EnemyID", "AbilityID", "IsUsedInAttack"
    super().__init__(loaded)
    self.enemy_id = enemy_id
    self.ability_id = ability_id
    self.is_used_in_attack = is_used_in_attack

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.ENEMY_ABILITY

  def get_raw_data(self) -> list[Any]:
    return [self.enemy_id, self.ability_id, self.is_used_in_attack]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_enemy_ability(data, loaded)
  
  @staticmethod
  def identical_condition(enemy_ability_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_enemy_ability(enemy_ability_data: list[Any] = [], loaded: bool = True) -> EnemyAbility:
  enemy_id: int = enemy_ability_data[0]
  ability_id: int = enemy_ability_data[1]
  is_used_in_attack: bool = enemy_ability_data[1]
  return EnemyAbility(enemy_id, ability_id, is_used_in_attack, loaded)

EOF
stored/abilities/item_ability.py

from tools.typing_tools import *

from database.condition import Condition
from stored.stored import *

class ItemAbility(Stored):
  """
  :param item_id: The item which this links to.
  :type item_id: int
  :param ability_id: The ability which this links to.
  :type ability_id: int
  """
  def __init__(self, item_id: int, ability_id: int, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.item_id = item_id
    self.ability_id = ability_id

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.ITEM_ABILITY

  def get_raw_data(self) -> list[Any]:
    return [self.item_id, self.ability_id]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_item_ability(data, loaded)
  
  @staticmethod
  def identical_condition(item_ability_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)
  
  # built-in methods

  def __repr__(self) -> str:
    return f"ItemAbility({self.item_id=}, {self.ability_id=})"

def instantiate_item_ability(item_ability_data: list[Any] = [], loaded: bool = True) -> ItemAbility:
  item_id: int = item_ability_data[0]
  ability_id: int = item_ability_data[1]
  return ItemAbility(item_id, ability_id, loaded)

EOF
stored/abilities/parry_ability.py

from math import exp2

from tools.typing_tools import *

from database.condition import Condition
from stored.abilities.abstract_ability import *

from ability_action import *

class ParryAbility(AbstractAbility):
  def __init__(self, ability_id: int, damage_threshold: float, reflection_proportion: float, loaded: bool = True) -> None:
    #"ParryAbilityID", "AbilityID", "DamageThreshold", "ReflectionProportion"
    super().__init__(ability_id, loaded)
    self.damage_threshold = damage_threshold
    self.reflection_proportion = reflection_proportion
  
  @staticmethod
  def get_table_name() -> TableName: return TableName.PARRY_ABILITY

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.damage_threshold, self.reflection_proportion]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_parry_ability(data, loaded)
  
  @staticmethod
  def identical_condition(parry_ability_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)
  
  # built-in methods

  def __repr__(self) -> str:
    return f"ParryAbility(`{self.ability_id=}`, `{self.damage_threshold=}`, `{self.reflection_proportion=}`)"
  
  # offensiveness and decision-making methods

  def calculate_offensiveness(self) -> float:
    return self.reflection_proportion * (1 - exp2(-1*self.damage_threshold))

  def get_ability_action(self) -> AbilityAction:
    return ParryAction(damage_threshold=self.damage_threshold, reflection_proportion=self.reflection_proportion)

def instantiate_parry_ability(parry_ability_data: list[Any] = [], loaded: bool = True) -> ParryAbility:
  ability_id: int = parry_ability_data[0]
  damage_threshold: float = parry_ability_data[1]
  reflection_proportion: float = parry_ability_data[2]
  return ParryAbility(ability_id, damage_threshold, reflection_proportion, loaded)

EOF
stored/abilities/statistic_ability.py

from tools.typing_tools import *
from tools.constants import Constants
from tools.ability_names import AbilityTypeName

from database.condition import Condition
from stored.abilities.abstract_ability import *

from ability_action import *

class StatisticAbility(AbstractAbility):
  def __init__(self, ability_id: int, ability_type: AbilityTypeName, amount: float, initial_duration: Optional[int], loaded: bool = True) -> None:
    super().__init__(ability_id, loaded)
    self.ability_type: AbilityTypeName = ability_type
    self.amount: float = amount
    self.initial_duration: Optional[int] = initial_duration

  @staticmethod
  def get_table_name() -> TableName: return TableName.STATISTIC_ABILITY

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.ability_type, self.amount, self.initial_duration]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_statistic_ability(data, loaded)
  
  @staticmethod
  def identical_condition(statistic_ability_row: list[Any]) -> Condition:
    return Condition(lambda _, row: statistic_ability_row[0] == row[0])
  
  # offensiveness and decision-making methods

  def calculate_offensiveness(self, **kwargs) -> float:
    if self.ability_type == AbilityTypeName.HEAL:
      health: float = kwargs["health"]
      max_health: float = kwargs["max_health"]
      healing: float = self.amount
      return min(health/(max_health - healing), 0)
    elif self.ability_type == AbilityTypeName.PIERCE:
      return Constants.PIERCE_OFFENSIVENESS
    elif self.ability_type == AbilityTypeName.IGNITE:
      return Constants.IGNITE_OFFENSIVENESS
    raise ValueError(f"`{self.ability_type=}` not recognised.")

  # ability action methods

  def get_ability_action(self) -> AbilityAction:
    match self.ability_type:
      case AbilityTypeName.HEAL:
        return HealAction(heal_amount=self.amount)
      case AbilityTypeName.PIERCE:
        return PierceAction()
      case AbilityTypeName.IGNITE:
        return IgniteAction()
    raise ValueError(f"`{self.ability_type=}` not recognised.")

def instantiate_statistic_ability(statistic_ability_data: list[Any], loaded: bool = True) -> StatisticAbility:
  ability_id: int = statistic_ability_data[0]
  ability_type: AbilityTypeName = statistic_ability_data[1]
  amount: float = statistic_ability_data[2]
  initial_duration: Optional[int] = statistic_ability_data[3]
  return StatisticAbility(ability_id, ability_type, amount, initial_duration, loaded)

EOF
stored/abilities/__init__.py

__all__ = ["ability", "abstract_ability", "enemy_ability", "item_ability", "parry_ability", "statistic_ability",]

from . import ability
from . import abstract_ability
from . import enemy_ability
from . import item_ability
from . import parry_ability
from . import statistic_ability

EOF
stored/stored.py

from tools.typing_tools import *
from tools.constants import TableName

from database.condition import Condition

class Stored:
  """
  Abstract class for all objects which represent something stored in the database.
  
  When a new subclass is defined, the following methods must be defined for it:
  * `get_table_name() -> str` *(static method)* - gets the name of the table which the objects will be stored and loaded from.
  * `get_raw_data(self) -> list[Any]` - gets the data of the object in the form it is stored in the `Database` object.
  * `instantiate(data: list[Any], loaded: bool = True) -> object` *(static method)* - calls an instantiation function defined outside of the function itself, providing a secondary constructor when being created using the raw data of the object. 
  * `identical_condition(_stored_row: list[Any]) -> Condition` *(static method)* - creates a `Condition` which defines what makes two objects identical.
  """
  def __init__(self, loaded: bool = True) -> None:
    self.loaded = loaded

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]: return []

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_stored(data, loaded)
  
  @staticmethod
  def identical_condition(_stored_row: list[Any]) -> Condition:
    return Condition(lambda _, _row: False)

def instantiate_stored(_stored_data: list[Any] = [], loaded: bool = True) -> Stored:
  return Stored()

"""
Subclass template:

from tools.typing_tools import *

from database.condition import Condition
from stored.stored import *

class SUBCLASS(Stored):
  def __init__(self, loaded: bool = True) -> None:
    super().__init__(loaded)

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.

  def get_raw_data(self) -> list[Any]: return []

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_sub_class(data, loaded)
  
  @staticmethod
  def identical_condition(sub_class_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_sub_class(sub_class_data: list[Any] = [], loaded: bool = True) -> SUBCLASS:
  return SUBCLASS()

"""

EOF
stored/user.py

from database.condition import Condition
from tools.typing_tools import *
from tools.constants import TableName

from stored.stored import Stored

class User(Stored):
  def __init__(self, name: str, password_hash: str, character_quantity: int = 0, world_quantity: int = 0, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.name: str = name
    self.password_hash: str = password_hash
    self.character_quantity: int = character_quantity
    self.world_quantity: int = world_quantity

    self.weapon_indexes: list[int] = []

  @staticmethod
  def get_table_name() -> TableName: return TableName.USER

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.name, self.password_hash, self.character_quantity, self.world_quantity]
  
  @staticmethod
  def instantiate(user_data: list[Any], loaded: bool = True):
    return instantiate_user(user_data, loaded)
  
  @staticmethod
  def identical_condition(user_row: list[Any]) -> Condition:
    return Condition(lambda _, row: user_row[0] == row[0])
  
def instantiate_user(user_data: list[Any], loaded: bool = True) -> User:
  name: str = user_data[0]
  password_hash: str = user_data[1]
  character_quantity: int = user_data[2]
  world_quantity = user_data[3]
  return User(name, password_hash, character_quantity, world_quantity, loaded)


EOF
stored/world.py

from tools.typing_tools import *
from tools.constants import TableName

from stored.stored import Stored

class World(Stored):
  """
  Class to represent each world.

  :param user_id: The user which the world is linked to.
  :type user_id: int
  :param name: The unique name of the world.
  :type name: str
  :param seed: the string which uniquely identifies how the world was generated.
  :type seed: str
  """
  def __init__(self, user_id: int, name: str, seed: str, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.user_id = user_id
    self.name = name
    self.seed = seed

  @staticmethod
  def get_table_name() -> TableName: return TableName.WORLD

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.user_id, self.name, self.seed]
  
  @staticmethod
  def instantiate(world_data: list[Any], loaded: bool = True):
    return instantiate_world(world_data, loaded)

def instantiate_world(world_data: list[Any], loaded: bool = True) -> World:
  user_id: int = world_data[0]
  name: str = world_data[1]
  seed: str = world_data[2]
  return World(user_id, name, seed, loaded)


EOF
stored/__init__.py

__all__ = ["stored", "user", "world"]

from . import stored
from . import user
from . import world

from .entities import *
from .items import *
from .abilities import *

EOF
interface/abstract_screen.py

import tkinter as tk
import customtkinter as ctk
import logging

from tools.typing_tools import *
from tools.dictionary_tools import add_if_vacant
from tools.tkinter_tools import *
from tools.constants import DefaultTkInitOptions, ScreenName

from game_data import GameData

from interface.base_frame import BaseFrame

from custom_tkinter.dynamic_button import DynamicButton

type DynamicButtonCommand = Callable[[dict[str, Any]], None]
"""
The significance of each input is as follows:
1. `dynamic_button_list` - a list containing all buttons created during dynamic button creation
2. `button_args` - the arguments for each button. The key is the `text` of the button, and the value is the arguments passed into that button's command when it is called.
"""

class AbstractScreen(BaseFrame):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent)
    self.game_data = game_data

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
  
  def create_buttons_dynamically(self, button_inputs: list[DynamicButtonInput], command: Callable[..., None], container: Optional[tk.Frame] = None, placement_options: Optional[dict[str, Any]] = None, **kwargs) -> None:
    if hasattr(self, "dynamic_button_frame"):
      self.dynamic_button_frame.destroy()
    self.dynamic_button_frame = unpack_optional(self.create_ctk_scrollable_frame_on_grid((0,0), container=container, return_frame=True))
    dynamic_buttons: list[DynamicButton] = []
    command_args_dict: dict[str, Any] = {}
    for (i, (text, command_args)) in enumerate(button_inputs):
      position: Position = (0,i)
      logging.debug(f"{i=}, {text=}, {command_args=}")
      new_dynamic_button = unpack_optional(self.create_widget(DynamicButton, position, container=self.dynamic_button_frame, return_widget=True, placement_options=placement_options, **kwargs))
      new_dynamic_button.text = text
      dynamic_buttons.append(new_dynamic_button)
      command_args_dict[text] = command_args

    for dynamic_button in dynamic_buttons:
      dynamic_button.command_args_dict = command_args_dict
      dynamic_button.command = command

  ## special widgets
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
  

EOF
interface/base_frame.py

import tkinter as tk
import customtkinter as ctk

from tools.typing_tools import *
from tools.dictionary_tools import add_if_vacant
from tools.tkinter_tools import *
from tools.constants import Constants, DefaultTkInitOptions, ToggleState

from custom_tkinter.toggleable_button import ToggleableButton
from custom_tkinter.dynamic_button import DynamicButton

class BaseFrame(tk.Frame):
  def __init__(self, root, parent: tk.Misc, dimensions: Position = (1,1), **kwargs) -> None:
    self.root = root
    self.parent = parent
    super().__init__(master=self.parent)

    self.default_frame = self
    self.dimensions = dimensions

  # widget creation methods

  ## general
  def create_widget[WidgetType: tk.Widget](self, widget_type: Type[WidgetType], position: Optional[Position] = None, container: Optional[tk.Frame] = None, placement_options: Optional[dict[str, Any]] = None, return_widget: bool = False, **kwargs) -> Optional[WidgetType]:
    """Creates a new widget of the type specified, either on a grid or to be packed."""
    if container == None: container = self.default_frame
    init_args = add_if_vacant(kwargs.copy(), DefaultTkInitOptions().WIDGET)
    if issubclass(widget_type, ctk.CTkScrollableFrame): # `CTkScrollableFrame.__init__` takes a different name for defining the border width: this block handles that
      init_args["border_width"] = init_args["borderwidth"]
      del init_args["borderwidth"]
    widget: WidgetType = widget_type(container, **init_args)
    if placement_options == None: placement_options = {}.copy()

    # adding the widget to the container
    if position == None: # using `pack`
      placement_args = add_if_vacant(placement_options, DefaultTkInitOptions().PACK).copy()
      widget.pack(**placement_args)
    else: # using `grid`
      (column, row) = position
      placement_args = add_if_vacant(placement_options, DefaultTkInitOptions().GRID).copy()
      widget.grid(column=column, row=row, **placement_args)
    if return_widget: return widget

  def create_widget_on_grid[W: tk.Widget](self, widget_type: Type[W], position: Position, container: Optional[tk.Frame] = None, return_widget: bool = False, placement_options: Optional[dict[str, Any]] = None, **kwargs) -> Optional[W]:
    """Creates a new widget of the type specified and adds it to a grid."""
    return self.create_widget(widget_type, position=position, container=container, return_widget=return_widget, placement_options=placement_options, **kwargs)
  
  def create_widget_on_self[WidgetType: tk.Widget](self, widget_type: Type[WidgetType], position: Optional[Position] = None, placement_options: Optional[dict[str, Any]] = None, return_widget: bool = False, **kwargs) -> Optional[WidgetType]:
    return self.create_widget(widget_type, position=position, container=self, return_widget=return_widget, placement_options=placement_options, **kwargs)

  ## buttons
  def create_button(self, position: Optional[Position] = None, container: Optional[tk.Frame] = None, return_button: bool = False, placement_options: Optional[dict[str, Any]] = None, **kwargs) -> Optional[tk.Button]:
    """
    Creates a new button widget, either being packed (if `position=None`) or placed on a grid (otherwise).

    :param position: Where the button should be placed on the grid. Defaults to `None`, implying the button will packed instead.
    :type position: Optional[Position]
    :param container: Defaults to `None`, implying \'self.default_frame\' will be used.
    :type container: Optional[Frame]
    :param return_button: Whether the created button object should be returned. Defaults to `False`.
    :type return_button: bool
    :param placement_options: Options passed into the \'Button.grid\' method. Defaults to `{}`, implying that no grid options should be used (besides the defaults).
    :type placement_options: Optional[dict[str, Any]]
    :param kwargs: Keyword arguments. Passed into the initialisation function for the button instance.
    """
    try: kwargs["command"]
    except: kwargs["command"] = lambda: None
    if placement_options == None: placement_options = {}.copy()
    placement_args = add_if_vacant(placement_options, DefaultTkInitOptions().BUTTON).copy()
    return self.create_widget(tk.Button, position=position, container=container, placement_options=placement_args, return_widget=return_button, **kwargs)
  
  def create_toggleable_button(self, position: Optional[Position] = None, container: Optional[tk.Frame] = None, return_button: bool = False, initially_toggled: ToggleState = ToggleState.OFF, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[ToggleableButton]:
    """Creates a new toggleable button, either being packed (if `position=None`) or placed on a grid (otherwise)."""
    if container == None: container = self.default_frame
    try: kwargs["command"]
    except: kwargs["command"] = lambda: None
    button: Optional[ToggleableButton] = self.create_widget(ToggleableButton, position=position, container=container, placement_options=placement_options, return_widget=return_button, **kwargs)
    if button == None: return None
    button.is_toggled = initially_toggled
    return button
  
  def create_toggleable_button_on_self(self, position: Optional[Position] = None, return_button: bool = False, initially_toggled: ToggleState = ToggleState.OFF, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[ToggleableButton]:
    return self.create_toggleable_button(position=position, container=self, return_button=return_button, initially_toggled=initially_toggled, placement_options=placement_options, **kwargs)
  
  ## frames
  def create_frame(self, position: Optional[Position] = None, container: Optional[tk.Frame] = None, return_frame: bool = False, dimensions: Optional[Position] = None, exclude_columns: list[int] = [], exclude_rows: list[int] = [], is_main_grid: bool = False, placement_options: Optional[dict[str, Any]] = None, **kwargs) -> Optional[tk.Frame]:
    """Creates a new frame, either being packed (if `position=None`) or placed on a grid (otherwise)."""
    kwargs = add_if_vacant(kwargs, DefaultTkInitOptions().FRAME)
    if placement_options == None: placement_options = {}.copy()
    if position == None: placement_options = add_if_vacant(placement_options, DefaultTkInitOptions().FRAME_PACK) # add frame-specific packing options if the frame is being packed
    frame: tk.Frame = unpack_optional(self.create_widget(tk.Frame, position=position, container=container, return_widget=True, placement_options=placement_options, **kwargs)) # as `return_widget` is always `True`, `unpack_optional` will never raise an error
    if dimensions != None:
      configure_grid(frame, dimensions=dimensions, exclude_columns=exclude_columns, exclude_rows=exclude_rows, is_main_grid=is_main_grid)
    if return_frame: return frame

  def create_frame_on_grid(self, position: Position, container: Optional[tk.Frame] = None, return_frame: bool = False, dimensions: Optional[Position] = None, exclude_columns: list[int] = [], exclude_rows: list[int] = [], is_main_grid: bool = False, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[tk.Frame]:
    """Creates a new frame and places it to a grid."""
    return self.create_frame(position=position, container=container, return_frame=return_frame, dimensions=dimensions, exclude_columns=exclude_columns, exclude_rows=exclude_rows, is_main_grid=is_main_grid, placement_options=placement_options, **kwargs)
  
  def create_frame_on_root(self, position: Position, return_frame: bool = False, dimensions: Optional[Position] = None, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[tk.Frame]:
    return self.create_frame_on_grid(position=position, container=self, return_frame=return_frame, dimensions=dimensions, is_main_grid=True, placement_options=placement_options, **kwargs)

  def create_ctk_scrollable_frame_on_grid(self, position: Position, container: Optional[tk.Frame] = None, return_frame: bool = False, dimensions: Optional[Position] = None, exclude_columns: list[int] = [], exclude_rows: list[int] = [], is_main_grid: bool = False, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[ctk.CTkScrollableFrame]:
    """Creates a new scrollable frame on a grid."""
    kwargs = add_if_vacant(kwargs, DefaultTkInitOptions().CTK_SCROLLABLE_FRAME)
    scrollable_frame = unpack_optional(self.create_widget(ctk.CTkScrollableFrame, position=position, container=container, return_widget=True, placement_options=placement_options, **kwargs))
    if dimensions != None:
      configure_grid(scrollable_frame, dimensions=dimensions, exclude_columns=exclude_columns, exclude_rows=exclude_rows, is_main_grid=is_main_grid)
    if return_frame: return scrollable_frame

  ## other
  def create_scrollbar_on_grid(self, position: Position, container: Optional[tk.Frame] = None, return_scrollbar: bool = False, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[tk.Scrollbar]:
    """Creates a new scrollbar on a grid."""
    scrollbar: Optional[tk.Scrollbar] = self.create_widget(tk.Scrollbar, position=position, container=container, return_widget=return_scrollbar, placement_options=placement_options, **kwargs)
    if scrollbar == None: return
    return scrollbar

  # creating and loading self

  def load(self, **kwargs) -> None: pass
  def create(self, **kwargs) -> None: pass

EOF
interface/character_creation.py

import tkinter as tk

from tools.typing_tools import *
from tools.dictionary_tools import filter_dictionary
from tools.constants import ScreenName

from interface.creation import Creation
from game_data import GameData

class CharacterCreation(Creation):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.entered_name = tk.StringVar()
    self.message = tk.StringVar()
    self.message.set("...")
    self.confirm_creation: Callable[[str], None] = kwargs["create_character"]
    super().__init__(root, parent, game_data, **kwargs)

  def create_character(self) -> None:
    new_character_name: str = self.entered_name.get()
    existing_character_names: list[str] = [character.name for character in self.game_data.characters.values()]
    if new_character_name in existing_character_names:
      self.fail_creation(f"Character with name `{new_character_name}` already exists")
    else:
      self.confirm_creation(new_character_name)

  def load(self, **kwargs) -> None:
    super().load(**kwargs)
    try: self.clear_message()
    except: pass

  def create(self, **kwargs) -> None:
    super().create(title="Character creation", **kwargs)

    self.create_entry("Enter character name:", self.entered_name)

    self.create_message()

    self.create_confirm(self.create_character)

    self.create_return(ScreenName.CHARACTER_SELECTION, **kwargs)

EOF
interface/character_selection.py

import tkinter as tk
import customtkinter as ctk

from tools.typing_tools import *
from tools.constants import ScreenName
from tools.logging_tools import *

from interface.abstract_screen import AbstractScreen
from interface.selection import Selection
from game_data import GameData
from stored.entities.character import Character

class CharacterSelection(Selection):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.select_character: Callable[[int], None] = kwargs["select_character"]
    self.scrollable_character_frame_parent: tk.Frame
    self.scrollable_character_frame: ctk.CTkScrollableFrame

    super().__init__(root, parent, game_data, **kwargs)

  # creating buttons

  def get_character_dynamic_button_input(self, character_id: int, character: Character) -> DynamicButtonInput:
    return (character.name, character_id)
  
  def get_all_characters_dynamic_button_inputs(self, characters: dict[int, Character]) -> list[DynamicButtonInput]:
    button_inputs: list[DynamicButtonInput] = []
    for (character_id, character) in characters.items():
      character_button_input: DynamicButtonInput = self.get_character_dynamic_button_input(character_id, character)
      button_inputs.append(character_button_input)
    return button_inputs

  # loading and creating
  
  def load(self, **kwargs) -> None:
    super().load(**kwargs)
    characters: dict[int, Character] = self.game_data.characters
    button_inputs: list[DynamicButtonInput] = self.get_all_characters_dynamic_button_inputs(characters)
    self.create_buttons_dynamically(button_inputs, command=lambda identifier: self.select_character(identifier), container=self.scrollable_character_frame_parent)

  def create(self, **kwargs) -> None:
    self.scrollable_character_frame_parent = unpack_optional(self.create_frame(return_frame=True, dimensions=(1,1)))
    super().create(title="Character selection", dimensions=(1,3), **kwargs)

    creation_command: Callable[[Optional[dict[str, Any]]], None] = kwargs["begin_character_creation"]
    self.create_widget(tk.Button, text="Create character", command=lambda: creation_command(None))
    self.create_quit(**kwargs)

EOF
interface/combat_interface.py

import tkinter as tk
from functools import reduce

from tools.typing_tools import *
from tools.dictionary_tools import filter_dictionary
from tools.exceptions import *
from tools.constants import *
from tools.logging_tools import *
from tools.positional_tools import length_to_point

from combat_action import CombatAction
from data_structures.entity_type import *
from data_structures.action_type import *
from data_structures.matrix import Matrix

from custom_tkinter.weapon_interface import WeaponInterface, create_weapon_interface
from custom_tkinter.toggleable_button import ToggleableButton

from interface.abstract_screen import AbstractScreen
from game_data import GameData

from stored.items.weapon import Weapon
from stored.items.equipable import Equipable
from stored.items.inventory_item import InventoryItem

from stored.abilities.item_ability import ItemAbility
from stored.abilities.ability import Ability
#from stored.entities.fighting_enemy import FightingEnemy

from stored.abilities.parry_ability import ParryAbility

type EnemyInterfaceWidgets = tuple[ToggleableButton, tk.Label, tk.Label]
"""Elements are as follows:
1. Button used for enemy selection
2. Enemy attack damage label
3. Enemy heal quantity label"""
type EnemyInterfaceTextVariables = tuple[tk.StringVar, tk.StringVar, tk.StringVar]
"""Elements are as follows:
1. Enemy name and health
2. Amount of damage the enemy does
3. Amount of healing the enemy does"""

def access_info_box[ReturnType](func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
  def wrapper(self, info: Optional[str] = None, *args, **kwargs) -> ReturnType:
    self.info_box["state"] = tk.NORMAL
    result: ReturnType = func(self, info, *args, **kwargs)
    self.info_box["state"] = tk.DISABLED
    return result
  return wrapper

class CombatInterface(AbstractScreen):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.equipped_inventory_weapon_identifiers: list[Optional[int]] = []
    self.weapon_interfaces: list[WeaponInterface] = []

    self.equipped_inventory_equipable_identifiers: list[Optional[int]] = []
    self.equipable_text_variables: list[tk.StringVar] = []

    self.enemy_interface_widgets = Matrix[EnemyInterfaceWidgets]((Constants.GRID_WIDTH,Constants.GRID_HEIGHT))
    self.enemy_name_variables = Matrix[EnemyInterfaceTextVariables]((Constants.GRID_WIDTH,Constants.GRID_HEIGHT))

    self.displayed_health = tk.StringVar()
    self.displayed_damage_resistance = tk.StringVar()

    self.health_potion_button: ToggleableButton

    self.info_box: tk.Text
    self.info_scrollbar: tk.Scrollbar

    self.confirmation_button: tk.Button
    self.is_confirm_pressed = tk.BooleanVar(value=False)
    self.return_button: tk.Button

    self.parry_used: bool = False

    self.end_combat_command: Callable[[ScreenName], None] = kwargs["end_combat"]

    super().__init__(root, parent, game_data, **kwargs)

  # weapon label operations

  def get_equipped_inventory_weapon_identifiers(self) -> list[Optional[int]]:
    """
    Gets the `InventoryItemID` for all weapons the active character has equipped from their inventory.
    
    :return: A list of inventory item identifiers. Never contains `None` elements, but the typing describes it as such to match with the type of `self.equipped_inventory_weapon_identifiers`.
    :rtype: list[Optional[int]]
    """
    inventory_items: dict[int, InventoryItem] = self.game_data.get_character_inventory_items() # all items in the inventory of the currently active character
    equipped_inventory_items: dict[int, InventoryItem] = filter_dictionary(inventory_items, lambda _, inv_item: inv_item.equipped) # all items from their inventory which they have equipped
    equipped_inventory_weapons_dict: dict[int, InventoryItem] = filter_dictionary(equipped_inventory_items, lambda _, inv_item: self.game_data.items[inv_item.item_id].item_type == ItemType.WEAPON)
    return list(equipped_inventory_weapons_dict.keys())
  
  def get_equipped_inventory_weapon_identifiers_length(self) -> int:
    """
    Gets the number of elements in the `self.equipped_inventory_weapon_identifiers` attribute, including elements of value `None`.
    
    :return: The length of the `self.equipped_inventory_weapon_identifiers` attribute (value >= 0).
    :rtype: int
    """
    return len(self.equipped_inventory_weapon_identifiers)

  def get_non_null_equipped_inventory_weapon_ids(self) -> list[int]:
    is_weapon_id_not_null: Callable[[Optional[int]], bool] = lambda weapon_id: weapon_id != None
    filtered_weapon_ids: list[Optional[int]] = list(filter(is_weapon_id_not_null, self.equipped_inventory_weapon_identifiers)) # removes all `None` entries
    cast_optional_to_int: Callable[[Optional[int]], int] = lambda weapon_id: cast(int, weapon_id)
    return list(map(cast_optional_to_int, filtered_weapon_ids)) # converts from type `list[Optional[int]]` to `list[int]`

  def load_equipped_inventory_weapon_identifiers(self) -> None: 
    self.equipped_inventory_weapon_identifiers = [].copy() # clears active weapons
    self.equipped_inventory_weapon_identifiers = self.get_equipped_inventory_weapon_identifiers()
    weapons_length: int = self.get_equipped_inventory_weapon_identifiers_length()
    if weapons_length > Constants.MAX_EQUIPPED_WEAPONS:
      raise ValueError(f"`{weapons_length=}` should have maximum length `{Constants.MAX_EQUIPPED_WEAPONS}`; instead has length of `{len(self.equipped_inventory_weapon_identifiers)}`")
    if weapons_length < Constants.MAX_EQUIPPED_WEAPONS:
      for _ in range(weapons_length, Constants.MAX_EQUIPPED_WEAPONS):
        self.equipped_inventory_weapon_identifiers.append(None)
  
  def get_equipped_inventory_weapon_names(self) -> list[Optional[str]]:
    if len(self.equipped_inventory_weapon_identifiers) > Constants.MAX_EQUIPPED_WEAPONS:
      raise ValueError(f"`{self.equipped_inventory_weapon_identifiers=}` should have max length `{Constants.MAX_EQUIPPED_WEAPONS}`; instead has `{len(self.equipped_inventory_weapon_identifiers)=}`.")
    weapon_names: list[Optional[str]] = []
    for active_weapon_id in self.equipped_inventory_weapon_identifiers:
      if active_weapon_id == None: weapon_name = None
      else: weapon_name = self.game_data.get_inventory_item_name(active_weapon_id)
      weapon_names.append(weapon_name)
    return weapon_names
  
  def init_weapon_interfaces(self, weapon_grid: tk.Frame, placement_options: dict[str, Any] = {}, **kwargs) -> None:
    weapon_interfaces: list[WeaponInterface] = []
    for i in range(Constants.MAX_EQUIPPED_WEAPONS):
      weapon_interface = create_weapon_interface(self.root, parent=weapon_grid, position=(i,0), placement_options=placement_options,**kwargs)
      weapon_interfaces.append(weapon_interface)
    self.weapon_interfaces = weapon_interfaces
  
  def load_weapon_label_names(self) -> None:
    weapon_names: list[Optional[str]] = self.get_equipped_inventory_weapon_names()
    for (i, weapon_name) in enumerate(weapon_names):
      self.weapon_interfaces[i].weapon_name = weapon_name

  def load_weapon_interface_at(self, index: int) -> None:
    weapon_interface: WeaponInterface = self.weapon_interfaces[index]
    weapon_identifier: Optional[int] = self.equipped_inventory_weapon_identifiers[index]
    if weapon_identifier == None: 
      weapon_interface.load()
      return
    weapon_name: Optional[str] = self.get_equipped_inventory_weapon_names()[index]
    if weapon_name == None: 
      raise TypeError(f"Weapon name should not be of type `None` at `{index=}` in `{self.get_equipped_inventory_weapon_names()=}` (`{weapon_name=}`)")
    weapon: Weapon = self.game_data.weapons[weapon_identifier]
    attack_damage: float = weapon.damage
    weapon_parry: ParryAbility = self.game_data.get_weapon_parry(weapon)
    parry_damage_threshold: float = weapon_parry.damage_threshold
    parry_reflection_proportion: float = weapon_parry.reflection_proportion
    weapon_interface.load(weapon_name, attack_damage, parry_damage_threshold, parry_reflection_proportion)

  def load_weapon_interfaces(self) -> None:
    for i in range(Constants.MAX_EQUIPPED_WEAPONS):
      self.load_weapon_interface_at(i)

  # equipable label operations

  def get_equipped_inventory_equipable_identifiers(self) -> list[Optional[int]]:
    inventory_items: dict[int, InventoryItem] = self.game_data.get_character_inventory_items() # all items in the inventory of the currently active character
    equipped_inventory_items: dict[int, InventoryItem] = filter_dictionary(inventory_items, lambda _, inv_item: inv_item.equipped) # all items from their inventory which they have equipped
    equipped_inventory_equipables_dict: dict[int, InventoryItem] = filter_dictionary(equipped_inventory_items, lambda _, inv_item: self.game_data.items[inv_item.item_id].item_type == ItemType.EQUIPABLE)
    return list(equipped_inventory_equipables_dict.keys())

  def load_equipped_inventory_equipable_identifiers(self) -> None:
    self.equipped_inventory_equipable_identifiers = [].copy() # clear active weapons
    self.equipped_inventory_equipable_identifiers = self.get_equipped_inventory_equipable_identifiers()
    equipables_length: int = len(self.equipped_inventory_equipable_identifiers)
    if equipables_length > Constants.MAX_EQUIPPED_EQUIPABLES:
      raise ValueError(f"`{equipables_length=}` should have maximum length `{Constants.MAX_EQUIPPED_EQUIPABLES}`; instead has length of `{len(self.equipped_inventory_equipable_identifiers)}`")
    if equipables_length < Constants.MAX_EQUIPPED_EQUIPABLES:
      for _ in range(equipables_length, Constants.MAX_EQUIPPED_EQUIPABLES):
        self.equipped_inventory_equipable_identifiers.append(None)

  def get_equipped_inventory_equipable_texts(self) -> list[Optional[str]]:
    if len(self.equipped_inventory_equipable_identifiers) > Constants.MAX_EQUIPPED_EQUIPABLES:
      raise ValueError(f"`{self.equipped_inventory_equipable_identifiers=}` should have maximum length `{Constants.MAX_EQUIPPED_EQUIPABLES}`; instead has length of `{len(self.equipped_inventory_equipable_identifiers)}`")
    
    equipable_texts: list[Optional[str]] = []
    for active_equipable_id in self.equipped_inventory_equipable_identifiers:
      equipable_name: str = "-"
      if active_equipable_id == None:
        equipable_texts.append(equipable_name)
        continue
      equipable_name = self.game_data.get_inventory_item_name(active_equipable_id)
      ability_texts_list: list[str] = [].copy()
      ability_texts_list = self.get_inventory_item_equipable_ability_descriptors(active_equipable_id)
      ability_texts: str = reduce(lambda text, acc: f"{acc}; {text}", ability_texts_list)
      equipable_texts.append(f"{equipable_name}: {ability_texts}")
    return equipable_texts
  
  def get_inventory_item_equipable_ability_descriptors(self, inventory_item_id: int) -> list[str]:
    inventory_item: InventoryItem = self.game_data.inventory_items[inventory_item_id]
    if not inventory_item.equipped: raise ValueError(f"Expected `{inventory_item.equipped=}` for `{inventory_item}` (`{inventory_item_id=}`) to be `True`; got `{inventory_item.equipped}` instead.")
    item_id: int = inventory_item.item_id
    selected_item_abilities_dict: dict[int, ItemAbility] = filter_dictionary(self.game_data.item_abilities, lambda _, item_ability: item_ability.item_id == item_id)
    selected_item_abilities: list[ItemAbility] = list(selected_item_abilities_dict.values())
    ability_texts: list[str] = []
    for item_ability in selected_item_abilities:
      ability_id: int = item_ability.ability_id
      ability: Ability = self.game_data.abilities[ability_id]
      ability_text: str = ability.text
      ability_texts.append(ability_text)
    return ability_texts
  
  def init_equipable_text_variables(self) -> None:
    for _ in range(Constants.MAX_EQUIPPED_EQUIPABLES):
      self.equipable_text_variables.append(tk.StringVar())

  def init_equipable_labels(self, container: tk.Frame) -> None:
    for i in range(Constants.MAX_EQUIPPED_EQUIPABLES):
      self.create_widget_on_grid(tk.Label, position=(0,i), container=container, textvariable=self.equipable_text_variables[i])

  def load_equipable_label_texts(self) -> None:
    display: str
    equipable_texts: list[Optional[str]] = self.get_equipped_inventory_equipable_texts()
    for (i, equipable_name) in enumerate(equipable_texts):
      if equipable_name == None: equipable_name = "-"
      display = f"{equipable_name}"
      self.equipable_text_variables[i].set(display)

  # info box

  @access_info_box
  def add_info(self, info: Optional[str] = None) -> None:
    info = unpack_optional_string(info, default="")
    self.info_box.insert(tk.END, f"{info}\n")
    self.info_box.see(tk.END)

  @access_info_box
  def clear_info(self, _info: Optional[str] = None) -> None:
    self.info_box.delete("1.0", tk.END)

  # user buttons
  def set_user_buttons_attributes(self, attribute: str, value: Any, include_attack: bool = True, include_parry: bool = True, include_confirm: bool = True) -> None:
    if include_attack or include_parry: # skips the attack buttons if neither `include_attack` nor `include_parry` is active
      for i in range(len(self.weapon_interfaces)):
        if include_attack: self.set_attack_button_attribute(i, attribute, value)
        if include_parry: self.set_parry_button_attribute(i, attribute, value)
    
    (enemy_interface_widgets_width, enemy_interface_widgets_height) = self.enemy_interface_widgets.dimensions
    for x in range(enemy_interface_widgets_width):
      for y in range(enemy_interface_widgets_height):
        enemy_interface: Optional[EnemyInterfaceWidgets] = self.enemy_interface_widgets[(x,y)]
        if enemy_interface == None: continue
        enemy_button: ToggleableButton = enemy_interface[0]
        enemy_button[attribute] = value

    self.health_potion_button[attribute] = value

    if include_confirm: self.confirmation_button[attribute] = value

  def set_user_buttons_toggled(self, is_toggled: ToggleState, include_attack: bool = True, include_parry: bool = True) -> None:
    self.set_user_buttons_attributes("is_toggled", is_toggled, include_attack, include_parry, include_confirm=False)

  def reset_toggleable_user_buttons_state(self) -> None:
    self.set_user_buttons_toggled(ToggleState.OFF)

  def set_user_buttons_state(self, state: str, include_attack: bool = True, include_parry: bool = True, include_confirm: bool = True) -> None:
    """Sets whether the user buttons are enabled or not"""
    self.set_user_buttons_attributes("state", state, include_attack, include_parry, include_confirm)

  def enable_user_buttons(self, include_attack: bool = True, include_parry: bool = True, include_confirm: bool = True) -> None:
    self.set_user_buttons_state(tk.NORMAL, include_attack, include_parry, include_confirm)

  def disable_user_buttons(self, include_attack: bool = True, include_parry: bool = True, include_confirm: bool = True) -> None:
    self.set_user_buttons_state(tk.DISABLED, include_attack, include_parry, include_confirm)

  # weapon buttons
  def set_weapon_button_attribute(self, weapon_index: int, button_type: WeaponUIComponentName, attribute: str, value: Any) -> None:
    if button_type not in [WeaponUIComponentName.ATTACK, WeaponUIComponentName.PARRY]: raise TypeError(f"\'button_type\'=`{button_type}` not one of `{WeaponUIComponentName.ATTACK}`, `{WeaponUIComponentName.PARRY}`.")
    weapon_interface: WeaponInterface = self.weapon_interfaces[weapon_index]
    selected_button: ToggleableButton = weapon_interface[button_type]
    selected_button[attribute] = value

  def set_attack_button_attribute(self, weapon_index: int, attribute: str, value: Any) -> None:
    self.set_weapon_button_attribute(weapon_index, WeaponUIComponentName.ATTACK, attribute, value)

  def set_parry_button_attribute(self, weapon_index: int, attribute: str, value: Any) -> None:
    self.set_weapon_button_attribute(weapon_index, WeaponUIComponentName.PARRY, attribute, value)

  def enable_attack_button(self, weapon_index: int) -> None:
    self.set_attack_button_attribute(weapon_index, "state", tk.NORMAL)

  def disable_attack_button(self, weapon_index: int) -> None:
    self.set_attack_button_attribute(weapon_index, "state", tk.DISABLED)

  def enable_parry_button(self, weapon_index: int) -> None:
    self.set_parry_button_attribute(weapon_index, "state", tk.NORMAL)

  def disable_parry_button(self, weapon_index: int) -> None:
    self.set_parry_button_attribute(weapon_index, "state", tk.DISABLED)

  def update_weapon_states(self) -> None:
    """Operates under the assumption that all weapon buttons are initially enabled."""
    for i in range(Constants.MAX_EQUIPPED_WEAPONS):
      weapon_id: Optional[int] = self.equipped_inventory_weapon_identifiers[i]
      selected_weapon_interface: WeaponInterface = self.weapon_interfaces[i]
      weapon_used: bool = cast(bool, selected_weapon_interface.is_weapon_used)
      if weapon_used or weapon_id == None:self.disable_attack_button(i)
      if self.parry_used or weapon_used or weapon_id == None: self.disable_parry_button(i)

  def reset_weapon_states(self) -> None:
    for i in range(Constants.MAX_EQUIPPED_WEAPONS):
      weapon_id: Optional[int] = self.equipped_inventory_weapon_identifiers[i]
      if weapon_id != None:
        self.enable_attack_button(i)
        self.enable_parry_button(i)
        self.weapon_interfaces[i].is_weapon_used = False
    self.parry_used = False

  def find_active_weapon_index(self) -> Optional[int]:
    for i in range(Constants.MAX_EQUIPPED_WEAPONS):
      weapon_interface: WeaponInterface = self.weapon_interfaces[i]
      if weapon_interface.is_attack_toggled ^ weapon_interface.is_parry_toggled: # XOR operation. If neither buttons are toggled, the weapon cannot be active, but if they are both toggled, then an invalid move is being made.
        return i
    return None
      
  # character labels

  def set_health_label(self, health: float) -> None:
    if health < 0:
      raise ValueError(f"Cannot set \'displayed_health\' to be less than zero (`{health}` < 0)")
    display: str = f"{health}HP"
    self.displayed_health.set(display)

  def update_health_label(self) -> None:
    character_health: float = self.game_data.get_active_character().health
    self.set_health_label(character_health)

  def set_damage_resistance_label(self, damage_resistance: float) -> None:
    display: str = f"{damage_resistance*100:.2f}%"
    self.displayed_damage_resistance.set(display)

  def update_damage_resistance_label(self) -> None:
    character_damage_resistance: float= self.game_data.get_active_character().damage_resistance
    logging.debug(f"{character_damage_resistance=}")
    self.set_damage_resistance_label(character_damage_resistance)

  def wait_until_confirmed(self) -> None:
    if self.is_quitting: return None
    logging.info("WAIT_VARIABLE START")
    self.wait_variable(self.is_confirm_pressed)
    logging.info("WAIT_VARIABLE END")
    self.is_confirm_pressed.set(False)

  def get_character_action(self) -> CombatAction:
    self.wait_until_confirmed()
    if self.is_quitting: raise QuitInterrupt(True)
    target_type: Optional[EntityType] = self.get_targeted_tile_type()
    action_type: ActionType = self.get_action_type()

    if target_type == None and type(action_type) == Heal:
      target_type = CharacterType()
    elif type(action_type) in [Attack, Parry]: 
      weapon_index: Optional[int] = self.find_active_weapon_index()
      if weapon_index == None: raise NoWeaponSelectedError()
      self.weapon_interfaces[weapon_index].is_weapon_used = True # TODO: update the `update` and `reset` methods
    return CombatAction(CharacterType(), target_type, action_type)
  
  def get_targeted_tile_type(self) -> Optional[EntityType]:
    if self.is_no_enemy_interface_widgets_toggled(): return None
    position: Position = self.find_active_enemy_position()
    enemy_identifier: Optional[int] = self.game_data.get_fighting_enemy_id_at(position)
    if enemy_identifier == None: return EmptyType(position)
    return EnemyType(enemy_identifier, position)
  
  def find_active_enemy_position(self) -> Position:
    enemy_interface: EnemyInterfaceWidgets
    tile_button: ToggleableButton
    selected_enemy_amount: int = 0
    position: Optional[Position] = None

    for i in range(9):
      x: int = i % 3
      y: int = i // 3
      enemy_interface = unpack_optional(self.enemy_interface_widgets[(x,y)]) # there will always be a button on a tile
      tile_button = enemy_interface[0]
      if tile_button.is_toggled:
        selected_enemy_amount += 1
        position = (x,y)
      if selected_enemy_amount > 1 and position != None: raise TooManyEnemiesSelectedError(position)
    if selected_enemy_amount == 0 or position == None: raise NoEnemiesSelectedError()
    return position
  
  def is_one_enemy_button_toggled(self) -> ComparisonFlag:
    try: self.find_active_enemy_position()
    except NoEnemiesSelectedError: return ComparisonFlag.LESS
    except TooManyEnemiesSelectedError: return ComparisonFlag.GREATER
    return ComparisonFlag.EQUAL
  
  def is_no_enemy_interface_widgets_toggled(self) -> bool:
    if self.is_one_enemy_button_toggled() == ComparisonFlag.LESS: return True
    return False
  
  def is_no_weapon_buttons_toggled(self) -> bool:
    return self.is_no_attack_buttons_toggled() and self.is_no_parry_buttons_toggled()
  
  def is_no_attack_buttons_toggled(self) -> bool:
    for weapon_interface in self.weapon_interfaces:
      if weapon_interface.is_attack_toggled: return False
    return True
  
  def is_no_parry_buttons_toggled(self) -> bool:
    for weapon_interface in self.weapon_interfaces:
      if weapon_interface.is_parry_toggled: return False
    return True
  
  def is_health_potion_button_toggled(self) -> bool:
    return bool(self.health_potion_button.is_toggled)

  def get_action_type(self) -> ActionType: # TODO: remove placeholders, give functionality
    action: ActionType
    using_health_potion: bool = self.is_health_potion_button_toggled()
    using_weapons: bool = not self.is_no_weapon_buttons_toggled()
    is_attacking: bool = not self.is_no_attack_buttons_toggled()
    is_parrying: bool = not self.is_no_parry_buttons_toggled()

    targeting_one_enemy_comparison: ComparisonFlag = self.is_one_enemy_button_toggled()
    if targeting_one_enemy_comparison == ComparisonFlag.GREATER: raise TooManyEnemiesSelectedError() # only 0 or 1 enemies can be selected
    targeting_no_enemies: bool = targeting_one_enemy_comparison == ComparisonFlag.LESS # to check if targeting 1 enemy, use `not targeting_no_enemies`, as 2 or more enemies cannot be selected

    if not using_health_potion and not using_weapons and targeting_no_enemies: # character can never select no buttons for an action
      raise NoButtonsSelectedError() 
    elif using_health_potion and targeting_no_enemies and not using_weapons: # handles using the health potion
      action = Heal(Constants.HEALTH_POTION_AMOUNT)
    elif using_health_potion: # health potion button can't be toggled from this point
      raise TooManyButtonsSelectedError(f"\'health_potion_button\' is toggled when other buttons are as well") 
    elif is_parrying and not is_attacking and targeting_no_enemies: # handles character parries
      (damage_threshold, reflection_proportion) = self.get_selected_weapon_parry_data()
      action = Parry(damage_threshold, reflection_proportion) # TODO: implement parrying
      self.parry_used = True
    elif not targeting_no_enemies and not is_attacking: # handles the case where an enemy is selected, but the character has no attack selected
      raise NoAttackSelectedForEnemyError()
    elif targeting_no_enemies: # all actions after this point require one enemy to be selected
      raise NoEnemiesSelectedError()
    elif is_attacking and not is_parrying: # handles character attacks
      damage: float = self.get_selected_weapon_attack_damage()
      action = Attack(damage)
    else:
      raise UnknownActionError()
    return action
  
  def get_selected_weapon_attack_damage(self) -> float: # TODO: introduce abilities
    weapon_buttons_selected: int = 0 # if weapon_interface.is_attack_toggled: return False
    for (i, weapon_interface) in enumerate(self.weapon_interfaces):
      is_attack_toggled: ToggleState = weapon_interface.is_attack_toggled
      if is_attack_toggled:
        weapon_buttons_selected += 1
        selected_weapon_identifier_index = i
      if weapon_buttons_selected > 1:
        raise TooManyWeaponButtonsSelectedError(i)
    weapon_identifier: Optional[int] = self.equipped_inventory_weapon_identifiers[selected_weapon_identifier_index]
    if weapon_identifier == None: raise TypeError("\'weapon_identifier\' can never be \'None\'")
    return self.game_data.weapons[weapon_identifier].damage
  
  def get_selected_weapon_parry_data(self) -> tuple[float, float]:
    """
    :return: A pair of floats. The first number is the parry damage threshold. The second is the parry reflection proportion.
    :rtype: tuple[float, float]
    """
    weapon_buttons_selected: int = 0 # if weapon_interface.is_attack_toggled: return False
    for (i, weapon_interface) in enumerate(self.weapon_interfaces):
      is_parry_toggled: ToggleState = weapon_interface.is_parry_toggled
      if is_parry_toggled:
        weapon_buttons_selected += 1
        selected_weapon_identifier_index = i
      if weapon_buttons_selected > 1:
        raise TooManyWeaponButtonsSelectedError(i)
    weapon_identifier: Optional[int] = self.equipped_inventory_weapon_identifiers[selected_weapon_identifier_index]
    if weapon_identifier == None: raise TypeError("\'weapon_identifier\' can never be \'None\'")
    weapon: Weapon = self.game_data.weapons[weapon_identifier]
    parry_ability = self.game_data.get_weapon_parry(weapon)
    return (parry_ability.damage_threshold, parry_ability.reflection_proportion)
  
  def init_enemy_name_variables(self) -> None:
    grid_dimensions: Position = self.enemy_interface_widgets.dimensions
    for i in range(len(self.enemy_name_variables)):
      position: Position = length_to_point(i, grid_dimensions)
      self.enemy_name_variables[position] = (tk.StringVar(), tk.StringVar(), tk.StringVar())
  
  def init_enemy_interface_widgets(self) -> None:
    grid_dimensions: Position = self.enemy_interface_widgets.dimensions
    for i in range(len(self.enemy_interface_widgets)):
      position: Position = length_to_point(i, grid_dimensions)
      enemy_info_container: tk.Frame = unpack_optional(self.create_frame_on_grid(position, container=self.enemy_grid, return_frame=True, dimensions=(2,2), exclude_rows=[1]))

      enemy_text_variables: Optional[EnemyInterfaceTextVariables] = unpack_optional(self.enemy_name_variables[position])
      enemy_button: ToggleableButton = unpack_optional(self.create_toggleable_button((0,0), container=enemy_info_container, return_button=True, textvariable=enemy_text_variables[0], placement_options={"columnspan": 2}))
      enemy_attack_damage: tk.Label = unpack_optional(self.create_widget_on_grid(tk.Label, (0,1), container=enemy_info_container, return_widget=True, textvariable=enemy_text_variables[1]))
      enemy_heal_amount: tk.Label = unpack_optional(self.create_widget_on_grid(tk.Label, (1,1), container=enemy_info_container, return_widget=True, textvariable=enemy_text_variables[2]))
      self.enemy_interface_widgets[position] = (enemy_button, enemy_attack_damage, enemy_heal_amount)
  
  def display_enemy_info_on_grid(self) -> None:
    fighting_enemy_graph_dimensions: Position = self.game_data.fighting_enemy_graph.dimensions
    for i in range(len(self.game_data.fighting_enemy_graph)):
      button_display: str = "-"
      damage_str: str = "-"
      heal_str: str = "-"
      position: Position = length_to_point(i, fighting_enemy_graph_dimensions)
      fighting_enemy_id: Optional[int] = self.game_data.fighting_enemy_graph[position]
      text_variables: EnemyInterfaceTextVariables = unpack_optional(self.enemy_name_variables[position])
      enemy_interface_widgets: EnemyInterfaceWidgets = unpack_optional(self.enemy_interface_widgets[position])
      enemy_interface_widgets[1].config(bg=Constants.DISABLED_COLOUR)
      enemy_interface_widgets[2].config(bg=Constants.DISABLED_COLOUR)

      heal_ability_id: Optional[int] = None
      if fighting_enemy_id != None:
        enemy_interface_widgets[1].config(bg=Constants.ENEMY_ATTACK_LABEL_COLOUR)
        enemy_interface_widgets[2].config(bg=Constants.ENEMY_HEAL_LABEL_COLOUR)

        fighting_enemy = unpack_optional(self.game_data.get_fighting_enemy_at(position))

        fighting_enemy_name: str = self.game_data.get_fighting_enemy_name(fighting_enemy_id)
        fighting_enemy_heath: Optional[float] = self.game_data.get_fighting_enemy_health(fighting_enemy_id)
        fighting_enemy_max_heath: Optional[float] = self.game_data.get_fighting_enemy_max_health(fighting_enemy_id)

        button_display = f"{fighting_enemy_name}"
        if fighting_enemy_heath != None and fighting_enemy_max_heath != None:
          button_display += f"\n{fighting_enemy_heath}/{fighting_enemy_max_heath}HP"

        damage_str = format(fighting_enemy.attack_damage)

        heal_ability_id = fighting_enemy.ability_id_table[ActionName.HEAL]

      if heal_ability_id != None:
        heal_ability: Ability = self.game_data.abilities[heal_ability_id]
        heal_ability_action: HealAction = cast(HealAction, heal_ability.get_ability_action())
        heal_str = format(heal_ability_action.heal_amount)

      text_variables[0].set(button_display)
      text_variables[1].set(damage_str)
      text_variables[2].set(heal_str)

  def generate_return_command(self) -> Callable[[ScreenName], None]:
    def return_command(screen_name: ScreenName) -> None:
      self.end_combat_command(screen_name)
      self.return_button.destroy()
    return return_command

  def enable_return(self, player_won: bool) -> None:
    return_to_screen: ScreenName
    return_message: str
    if player_won == True:
      self.add_info("PLAYER WON")
      return_to_screen = ScreenName.EXPLORATION
      return_message = "Return to exploration"
    else:
      self.add_info("PLAYER LOST")
      return_to_screen = ScreenName.HOME
      return_message = "Return home"
    return_command: Callable[[ScreenName], None] = self.generate_return_command()
    self.return_button = self.create_return(return_to_screen, return_message, lambda screen: return_command(screen))
  
  def interrupt_waits(self) -> None:
    super().interrupt_waits()
    self.is_confirm_pressed.set(True)

  # loading and creating
    
  def load(self, **kwargs) -> None:
    self.load_equipped_inventory_weapon_identifiers()
    self.load_weapon_interfaces()
    self.load_equipped_inventory_equipable_identifiers()
    self.load_equipable_label_texts()
    self.display_enemy_info_on_grid()
    super().load(**kwargs)

  def create(self, **kwargs) -> None:
    self.base_grid: tk.Frame = unpack_optional(self.create_frame(return_frame=True, dimensions=(4,6)))
    self.default_frame = self.base_grid

    self.enemy_grid: tk.Frame = unpack_optional(self.create_frame_on_grid((2, 1), return_frame=True, dimensions=(Constants.GRID_WIDTH, Constants.GRID_HEIGHT), placement_options={"columnspan": 3, "rowspan": 4}))

    # creates buttons for using weapons
    weapon_grid: tk.Frame = unpack_optional(self.create_frame_on_grid((0, 1), return_frame=True, dimensions=(3, 1), placement_options={"columnspan": 2, "rowspan": 2}))
    self.init_weapon_interfaces(weapon_grid)

    # where the character's equipables will be displayed
    self.init_equipable_text_variables()
    equipables_grid: tk.Frame = unpack_optional(self.create_frame_on_grid((0,5), return_frame=True, dimensions=(1,4), placement_options={"columnspan": 2}))
    self.init_equipable_labels(equipables_grid)

    # creates buttons for selecting enemies to attack
    self.init_enemy_name_variables()
    self.init_enemy_interface_widgets()
    
    super().create(title="Combat", dimensions=(1,3), **kwargs)
    self.create_character_name_label((0,0))

    # health potion button
    self.health_potion_button = unpack_optional(self.create_toggleable_button(position=(0, 3), return_button=True, text=f"Use health potion (+{Constants.HEALTH_POTION_AMOUNT} HP)", placement_options={"columnspan": 2}))

    # where character information will be displayed
    character_info_grid: tk.Frame = unpack_optional(self.create_frame_on_grid((0,4), return_frame=True, dimensions=(2,2), exclude_rows=[0]))
    # where character health will be displayed
    self.create_widget_on_grid(tk.Label, (0,0), container=character_info_grid, text="Health:")
    self.create_widget_on_grid(tk.Label, (0,1), container=character_info_grid, textvariable=self.displayed_health)
    # where character dodge chance will be displayed
    self.create_widget_on_grid(tk.Label, (1,0), container=character_info_grid, text="Damage resistance:")
    self.create_widget_on_grid(tk.Label, (1,1), container=character_info_grid, textvariable=self.displayed_damage_resistance)

    # what will be pressed when the player wants to confirm their action
    self.confirmation_button = unpack_optional(self.create_button(position=(1,4), return_button=True, text="Confirm", placement_options={"sticky": "ew"}, command=lambda: self.is_confirm_pressed.set(True)))

    # where the information of what is happening will be sent through
    self.info_box = unpack_optional(self.create_widget_on_grid(tk.Text, (2,5), return_widget=True, state=tk.DISABLED, height=10, width=40))
    self.info_scrollbar = unpack_optional(self.create_scrollbar_on_grid((4,5), return_scrollbar=True, placement_options={"columnspan": 2}, command=self.info_box.yview))
    self.info_box.configure(yscrollcommand=self.info_scrollbar.set)

    self.create_quit(**kwargs)

EOF
interface/creation.py

import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from game_data import GameData
from interface.abstract_screen import AbstractScreen

class Creation(AbstractScreen):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent, game_data, **kwargs)

  def create_entry(self, prompt: str, entry_string: tk.StringVar) -> None:
    self.create_widget(tk.Label, text=prompt)
    self.create_widget(tk.Entry, textvariable=entry_string)

  

  def fail_creation(self, message: str) -> None:
    self.message.set(message)

  def load(self, **kwargs) -> None:
    return super().load(**kwargs)
  
  def create(self, title: str = "", **kwargs) -> None:
    return super().create(title, **kwargs)

EOF
interface/exploration_screen.py

import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName
from tools.generation_tools import *

from game_data import GameData
from interface.abstract_screen import AbstractScreen

class ExplorationScreen(AbstractScreen):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.is_entering_combat: bool = False
    self.is_entering_structure: bool = False

    self.enter_combat_button: tk.Button
    self.enter_structure_button: tk.Button
    self.continue_exploration_button: tk.Button

    super().__init__(root, parent, game_data, **kwargs)

  def is_nothing_happening(self) -> bool:
    return not self.is_entering_combat and not self.is_entering_structure

  # gui methods

  def reset_gui(self) -> None:
    self.nothing_found()
    self.message.set("-")
    self.continue_exploration_button["state"] = tk.NORMAL

  def reload_gui(self) -> None:
    logging.debug(f"{self.is_entering_combat=}, {self.is_entering_structure=}")
    if self.is_nothing_happening(): self.reset_gui()
    elif self.is_entering_combat: # if the character has just finished combat
      self.make_combat_unavailable()
      self.is_entering_combat = False
      if self.is_entering_structure: # if the character will be looting a structure afterwards 
        self.make_structure_entry_available()
      else: # if the character will not be looting a structure
        self.make_structure_entry_unavailable()
        self.continue_exploration_button["state"] = tk.NORMAL
    elif self.is_entering_structure: # if the character has just finished looting a structure
      self.reset_gui()
      self.is_entering_structure = False

  def continue_exploration(self) -> None:
    self.is_entering_combat = is_combat_encounter()
    self.is_entering_structure = is_structure_encounter()

    if not self.is_entering_combat:
      if self.is_entering_structure:
        self.make_structure_entry_available()
      elif not self.is_entering_structure:
        self.nothing_found()
    else:
      self.make_structure_entry_unavailable()
      self.make_combat_available()

  def make_combat_available(self) -> None:
    self.message.set("Enemies block your path...")
    self.continue_exploration_button["state"] = tk.DISABLED
    self.enter_combat_button["state"] = tk.NORMAL

  def make_structure_entry_available(self) -> None:
    self.message.set("Structure found")
    self.continue_exploration_button["state"] = tk.DISABLED
    self.enter_structure_button["state"] = tk.NORMAL

  def make_combat_unavailable(self) -> None:
    self.enter_combat_button["state"] = tk.DISABLED

  def make_structure_entry_unavailable(self) -> None:
    self.enter_structure_button["state"] = tk.DISABLED

  def nothing_found(self) -> None:
    self.message.set("Nothing happened")
    self.make_combat_unavailable()
    self.make_structure_entry_unavailable()

  # load and create

  def return_command_generator(self, return_command: Callable[[ScreenName], None]) -> Callable[[ScreenName], None]:
    def inner(screen_name: ScreenName) -> None:
      self.is_entering_combat = False
      self.is_entering_structure = False
      self.reset_gui()
      return_command(screen_name)
    return inner

  def load(self, **kwargs) -> None:
    self.reload_gui()
    self.game_data.active_storage_id = self.game_data.away_storage
    super().load(**kwargs)

  def create(self, enter_structure: ButtonCommand, begin_combat: ButtonCommand, **kwargs):
    self.create_widget(tk.Button, text="Combat (placeholder)", command=lambda: begin_combat()) # TODO: remove

    self.continue_exploration_button = unpack_optional(self.create_widget(tk.Button, text="Continue exploration", command=lambda: self.continue_exploration(), return_widget=True))

    self.create_message()

    choice_grid: tk.Frame = unpack_optional(self.create_frame(return_frame=True, dimensions=(2,1)))

    self.enter_combat_button = unpack_optional(self.create_button((0,0), return_button=True, container=choice_grid, text="Enter combat", command=lambda: begin_combat(), state=tk.DISABLED))

    self.enter_structure_button = unpack_optional(self.create_button((1,0), return_button=True, container=choice_grid, text="Loot structure", command=lambda: enter_structure(), state=tk.DISABLED))

    super().create(title="Exploration", dimensions=(1,3), **kwargs)

    return_command: Callable[[ScreenName], None] = self.return_command_generator(kwargs["return_command"])
    self.create_return(ScreenName.HOME, return_command=return_command)
    self.create_quit(**kwargs)

EOF
interface/home_screen.py

import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from game_data import GameData
from interface.abstract_screen import AbstractScreen

class HomeScreen(AbstractScreen):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent, game_data, **kwargs)

  def load(self, **kwargs) -> None:
    self.game_data.active_storage_id = self.game_data.home_storage
    super().load(**kwargs)

  def create(self, **kwargs) -> None:
    super().create(title="Home screen", dimensions=(1,3), **kwargs)
    self.create_character_name_label()
    
    open_storage: Callable[[], None] = kwargs["open_storage"]
    self.create_widget(tk.Button, text="Open storage", command=lambda: open_storage())

    go_exploring: Callable[[], None] = kwargs["go_exploring"]
    self.create_widget(tk.Button, text="Go exploring", command=lambda: go_exploring())

    self.create_return(ScreenName.WORLD_SELECTION, text="Return to world selection", **kwargs)
    self.create_quit(**kwargs)

EOF
interface/interface.py

import tkinter as tk

from tools.typing_tools import *
from tools.constants import Constants, ScreenName
from tools.logging_tools import *

from interface.abstract_screen import AbstractScreen
from interface.character_selection import CharacterSelection
from interface.character_creation import CharacterCreation
from interface.world_selection import WorldSelection
from interface.world_creation import WorldCreation
from interface.combat_interface import CombatInterface
from interface.home_screen import HomeScreen
from interface.storage_interface import StorageInterface
from interface.exploration_screen import ExplorationScreen

from game_data import GameData

class Interface(tk.Tk):
  def __init__(self, game_data: GameData, start_screen: ScreenName = Constants.START_SCREEN, **kwargs) -> None:
    super().__init__()
    
    self.START_SCREEN: ScreenName = start_screen

    self.title("Gaia")

    self.geometry(f"{Constants.MIN_SCREEN_WIDTH}x{Constants.MIN_SCREEN_HEIGHT}")

    self.minsize(Constants.MIN_SCREEN_WIDTH, Constants.MIN_SCREEN_HEIGHT)
    self.maxsize(Constants.MAX_SCREEN_WIDTH, Constants.MAX_SCREEN_HEIGHT)

    container = tk.Frame(self)
    container.pack(fill="both", expand=True)

    container.grid_rowconfigure(0, weight=2)
    container.grid_columnconfigure(0, weight=2)

    screen_init_data: dict[ScreenName, Any] = {
      ScreenName.CHARACTER_SELECTION: CharacterSelection,
      ScreenName.CHARACTER_CREATION: CharacterCreation,
      ScreenName.WORLD_SELECTION: WorldSelection,
      ScreenName.WORLD_CREATION: WorldCreation,
      ScreenName.COMBAT: CombatInterface,
      ScreenName.HOME: HomeScreen,
      ScreenName.STORAGE: StorageInterface,
      ScreenName.EXPLORATION: ExplorationScreen,
    }

    self.screens: dict[ScreenName, AbstractScreen] = {}

    for (screen_name, Screen) in screen_init_data.items():
      self.screens[screen_name] = Screen(self, container, game_data, **kwargs)

  def show_screen(self, screen_name: ScreenName, **kwargs) -> None:
    screen = self.screens[screen_name]
    screen.load(**kwargs)
    screen.tkraise()

  def update_character_name(self, character_name) -> None:
    for screen in self.screens.values():
      screen.set_character_name_label(character_name)

  def get_combat_interface(self) -> CombatInterface:
    return cast(CombatInterface, self.screens[ScreenName.COMBAT])

  def run(self, **kwargs) -> None:
    self.show_screen(self.START_SCREEN, **kwargs)
    self.mainloop()

EOF
interface/selection.py

import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from interface.abstract_screen import AbstractScreen
from game_data import GameData

class Selection(AbstractScreen):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent, game_data, **kwargs)

  def load(self, **kwargs) -> None:
    super().load(**kwargs)

  def create(self, title: str = "", dimensions: Position = (1,3), **kwargs) -> None:
    super().create(title, dimensions, **kwargs)

EOF
interface/storage_interface.py

import tkinter as tk
import customtkinter as ctk

from tools.typing_tools import *
from tools.constants import *
from tools.dictionary_tools import filter_dictionary
from tools.tkinter_tools import *

from game_data import GameData
from interface.abstract_screen import AbstractScreen

from stored.items.item import Item
from stored.items.storage import Storage
from stored.items.inventory_item import InventoryItem
from stored.items.storage_item import StorageItem
from stored.items.abstract_storage_item import AbstractStorageItem

from custom_tkinter.toggleable_button import ToggleableButton

class StorageInterface(AbstractScreen):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.storage_indicator = tk.StringVar()

    self.inventory_frame: ctk.CTkScrollableFrame
    self.storage_frame: ctk.CTkScrollableFrame

    self.inventory_item_frames: list[tk.Frame] = []
    self.inventory_item_swap_buttons: dict[int, ToggleableButton] = {} # an inventory item identifier maps to its respective button
    self.storage_item_frames: list[tk.Frame] = []
    self.storage_item_swap_buttons: dict[int, ToggleableButton] = {} # a storage item identifier maps to its respective button

    self.__equipped_weapon_amount: int = 0
    self.__equipped_weapon_text = tk.StringVar()
    self.__equipped_weapon_text.set("-")
    self.__equipped_equipable_amount: int = 0
    self.__equipped_equipable_text = tk.StringVar()
    self.__equipped_equipable_text.set("-")

    self.return_to_screen = ScreenName.HOME

    super().__init__(root, parent, game_data, **kwargs)

  # built-in methods

  def __getitem__(self, key: Union[ItemFrameCollectionName, str]) -> Any:
    if type(key) == ItemFrameCollectionName: return getattr(self, str(key))
    return super().__getitem__(key)
  
  def __setitem__(self, key: Union[ItemFrameCollectionName, str], value: Any) -> None:
    if type(key) == ItemFrameCollectionName: return setattr(self, str(key), value)
    return super().__setitem__(key, value)

  # getting/calculating basic values

  def get_character_inventory_item_amount(self) -> int:
    return len(self.game_data.get_character_inventory_items())
  
  def get_storage_item_amount(self, storage_id: int) -> int:
    return len(self.game_data.get_relevant_storage_items(storage_id))
  
  def get_storage_switch_button_text(self, is_character_inventory: bool) -> str:
    if is_character_inventory: return "Store"
    return "Take"
  
  def get_storage_attr_name(self, is_character_inventory: bool) -> StorageAttrName:
    if is_character_inventory: return StorageAttrName.INVENTORY_ITEMS
    return StorageAttrName.STORAGE_ITEMS
  
  def get_storage_frame(self, is_character_inventory: bool) -> tk.Frame:
    if is_character_inventory: return self.inventory_frame
    return self.storage_frame
  
  def get_item_frame_collection_name(self, is_character_inventory: bool) -> ItemFrameCollectionName:
    if is_character_inventory: return ItemFrameCollectionName.INVENTORY
    return ItemFrameCollectionName.STORAGE
  
  @property
  def equipped_weapon_amount(self) -> int:
    return self.__equipped_weapon_amount
  
  @equipped_weapon_amount.setter
  def equipped_weapon_amount(self, amount: int) -> None:
    if amount < 0: raise ValueError(f"{amount=} cannot be set to a value less than 0.")
    self.__equipped_weapon_amount = amount
    self.__equipped_weapon_text.set(f"Weapons equipped: {self.__equipped_weapon_amount}")

  @property
  def equipped_equipable_amount(self) -> int:
    return self.__equipped_equipable_amount
  
  @equipped_equipable_amount.setter
  def equipped_equipable_amount(self, amount: int) -> None:
    if amount < 0: raise ValueError(f"{amount=} cannot be set to a value less than 0.")
    self.__equipped_equipable_amount = amount
    self.__equipped_equipable_text.set(f"Equipables equipped: {self.__equipped_equipable_amount}")
  
  # swapping items between inventories

  def move_items_if_valid(self, **kwargs) -> None:
    """Ensures a swap is valid before it is executed. Calls \'self.move_items\' if no faults occur."""
    storage_id: Optional[int] = self.game_data.active_storage_id
    if storage_id == None: raise KeyError(f"Trying to access a storage when no storage is currently active (\'self.game_data.active_storage_id\'=`{self.game_data.active_storage_id}`).")
    self.move_items(storage_id, **kwargs)
    self.load(**kwargs)

  def move_items(self, storage_id: int, **kwargs) -> None:
    """Contains the functionality for swapping the items between the inventory and whatever storage is currently active."""
    activated_inventory_move_buttons: dict[int, ToggleableButton] = filter_dictionary(self.inventory_item_swap_buttons, lambda _, button: button.is_toggled == ToggleState.ON)
    activated_storage_move_buttons: dict[int, ToggleableButton] = filter_dictionary(self.storage_item_swap_buttons, lambda _, button: button.is_toggled == ToggleState.ON)
    inventory_items_to_move: list[int] = list(activated_inventory_move_buttons.keys())
    storage_items_to_move: list[int] = list(activated_storage_move_buttons.keys())

    for inventory_item_id in inventory_items_to_move:
      self.game_data.move_inventory_item_to_storage(inventory_item_id, storage_id)
      del self.inventory_item_swap_buttons[inventory_item_id]

    for storage_item_id in storage_items_to_move:
      self.game_data.move_storage_item_to_inventory(storage_item_id)
      del self.storage_item_swap_buttons[storage_item_id]

    self.load(**kwargs) # reloads buttons at the end
  
  # methods for loading the screen

  def create_item_frame(self, abstract_storage_item_id: int, index: int, container: tk.Frame, is_character_inventory: bool = False, is_equipped: bool = False, **kwargs) -> tk.Frame:
    """
    Creates a frame that contains all required information about a single item. Includes the following (from left to right):
      1. Equip/unequip the item (optional)
      2. Item name
      3. Stack size
      4. Button to select whether the item should be swapped
    
    :param container: The base frame which the item frame will be appended to.
    :type container: Frame
    """
    # getting information about the item
    storage_name: StorageAttrName = self.get_storage_attr_name(is_character_inventory)
    storage_item: AbstractStorageItem = self.game_data[storage_name][abstract_storage_item_id]
    stack_size: int = storage_item.stack_size
    item_id: int = storage_item.item_id
    item: Item = self.game_data.items[item_id]
    item_name: str = item.name
    # creating the frame
    item_frame: tk.Frame = unpack_optional(self.create_frame_on_grid((0,index), container=container, dimensions=(4,1), exclude_columns=[0,2,3], return_frame=True, placement_options={"sticky": "ew"}, **kwargs))
    # populating it
    if item.item_type in [ItemType.WEAPON, ItemType.EQUIPABLE] and is_character_inventory:
      initially_toggled = ToggleState.bool_to_state(is_equipped)
      equip_button: ToggleableButton = unpack_optional(self.create_toggleable_button((0,0), container=item_frame, text="Equip", initially_toggled=initially_toggled, return_button=True)) # button for equipping / unequipping items
      equip_button.command = lambda: self.game_data.toggle_inventory_item_equipped(equip_button, abstract_storage_item_id)
    self.create_widget_on_grid(tk.Label, (1,0), container=item_frame, text=item_name) # name of item
    self.create_widget_on_grid(tk.Label, (2,0), container=item_frame, text=f"({str(stack_size)})") # stack size

    switch_button = unpack_optional(self.create_toggleable_button((3,0), container=item_frame, text=self.get_storage_switch_button_text(is_character_inventory), return_button=True)) # for switching between storage and inventory
    if is_character_inventory: self.inventory_item_swap_buttons[abstract_storage_item_id] = switch_button
    else: self.storage_item_swap_buttons[abstract_storage_item_id] = switch_button

    return item_frame
  
  def clear_item_frames(self, attribute_name: ItemFrameCollectionName) -> None:
    """
    Iterates over an attribute of item frames, destroying all of them and clearing the attribute's contents.

    :param attribute_name: The name of the target attribute containing the item frames. The attribute must be of the type `list[Frame]`.
    :type attribute_name: str
    """
    valid_attribute_names: list[ItemFrameCollectionName] = [ItemFrameCollectionName.INVENTORY, ItemFrameCollectionName.STORAGE]
    if not attribute_name in valid_attribute_names:
      raise NameError(f"arg \'attribute_name\'=`{attribute_name}` doesn't match with any of \'valid_attribute_names\'=`{valid_attribute_names}`")
    item_frames: list[tk.Frame] = self[attribute_name]
    for frame in item_frames:
      frame.destroy()
    item_frames = [].copy()
    self[attribute_name] = item_frames

  def load_abstract_storage_items[AbstractStorageItemType: AbstractStorageItem](self, storage_items: dict[int, AbstractStorageItemType], is_character_inventory: bool = False, **kwargs) -> None:
    """
    Loads all item frames into an abstract storage (either inventory or storage).
    
    :param storage_items: Contains all the items which are to be loaded. Maps an identifier to its respective storage item.
    :type storage_items: dict[int, AbstractStorageItemType]
    :param is_character_inventory: Indicates whether the items are to be loaded into the inventory or the external storage. Defaults to `False`.
    :type is_character_inventory: bool
    :param kwargs: Key-word arguments. Currently unused.
    """
    container: tk.Frame = self.get_storage_frame(is_character_inventory)
    item_frame_collection_name: ItemFrameCollectionName = self.get_item_frame_collection_name(is_character_inventory)
    for (list_index, (storage_item_id, storage_item)) in enumerate(list(storage_items.items())):
      is_equipped: bool = False
      if type(storage_item) == InventoryItem:
        is_equipped = storage_item.equipped
      item_frame: tk.Frame = self.create_item_frame(storage_item_id, list_index, container, is_character_inventory=is_character_inventory, is_equipped=is_equipped)
      self[item_frame_collection_name].append(item_frame)
  
  def load_inventory(self, **kwargs) -> None:
    item_amount: int = self.get_character_inventory_item_amount()
    configure_grid(self.inventory_frame, dimensions=(1, item_amount), exclude_rows=list(range(item_amount-1)))
    character_inventory_items: dict[int, InventoryItem] = self.game_data.get_character_inventory_items()
    self.load_abstract_storage_items(character_inventory_items, is_character_inventory=True, **kwargs)

  def load_storage(self, storage_id: int, **kwargs) -> None:
    item_amount: int = self.get_storage_item_amount(storage_id)
    configure_grid(self.storage_frame, dimensions=(1, item_amount), exclude_rows=list(range(item_amount-1)))
    storage_inventory_items: dict[int, StorageItem] = self.game_data.get_relevant_storage_items(storage_id)
    self.load_abstract_storage_items(storage_inventory_items, is_character_inventory=False, **kwargs)

  def load(self, **kwargs) -> None:
    super().load(**kwargs)
    self.clear_item_frames(ItemFrameCollectionName.INVENTORY)
    self.clear_item_frames(ItemFrameCollectionName.STORAGE)

    is_storage_at_home: Optional[bool] = self.game_data.is_storage_at_home()
    if is_storage_at_home == None: return
    storage_id: Optional[int] = self.game_data.active_storage_id
    if storage_id == None: raise ValueError(f"\'storage_id\' cannot be \'None\' when \'is_storage_at_home\'=`{is_storage_at_home}`")

    if is_storage_at_home:
      self.storage_indicator.set("At home")
      self.return_to_screen = ScreenName.HOME
    else:
      self.storage_indicator.set("Away")
      self.return_to_screen = ScreenName.EXPLORATION
    self.load_inventory(**kwargs)
    self.load_storage(storage_id, **kwargs)

    self.destroy_return()
    self.return_button = self.create_return(**kwargs)

  def create_return(self, **kwargs) -> tk.Button:
    logging.debug(f"{self.game_data.is_storage_at_home()=}")
    if self.game_data.is_storage_at_home():
      return super().create_return(ScreenName.HOME, return_message="Return to home screen", **kwargs)
    else:
      return super().create_return(ScreenName.EXPLORATION, return_message="Return to exploration", return_command=self.leave_structure_command)
    
  def destroy_return(self) -> None:
    try: self.return_button.destroy()
    except: pass

  def create(self, **kwargs) -> None:
    self.leave_structure_command: Callable[[ScreenName], None] = kwargs["leave_structure"]

    self.base_frame: tk.Frame = unpack_optional(self.create_frame(dimensions=(2,5), exclude_rows=[0,1,3], return_frame=True))
    self.default_frame = self.base_frame

    self.create_widget_on_grid(tk.Label, (0,0), textvariable=self.storage_indicator, placement_options={"columnspan": 2})
    self.create_widget_on_grid(tk.Label, (0,1), text="Player inventory")
    self.create_widget_on_grid(tk.Label, (1,1), text="Storage")
    
    self.inventory_frame = unpack_optional(self.create_ctk_scrollable_frame_on_grid((0,2), return_frame=True))
    self.storage_frame = unpack_optional(self.create_ctk_scrollable_frame_on_grid((1,2), return_frame=True))
    # dimensions for both are set in 'self.load' by calling the `self.load_inventory` and `self.load_storage` methods respectively

    self.create_widget(tk.Label, position=(0,3), textvariable=self.__equipped_weapon_text)
    self.create_widget(tk.Label, position=(1,3), textvariable=self.__equipped_equipable_text)

    super().create(title="Storage interface", **kwargs)

    self.create_confirm(lambda: self.move_items_if_valid(), position=(0,4), text="Confirm swap", placement_options={"columnspan": 2})
    
    #self.create_quit(**kwargs)

EOF
interface/world_creation.py

import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from interface.creation import Creation
from game_data import GameData

from stored.world import World

class WorldCreation(Creation):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.world_name = tk.StringVar()
    self.world_seed = tk.StringVar()
    self.confirm_creation: Callable[[str, str], None] = kwargs["create_world"]
    super().__init__(root, parent, game_data, **kwargs)

  def create_world(self) -> None:
    """
    Handles whether a new world will be created and the information used by that process. Assumes \'self.world_name\' and \'self.world_seed\' have values inputted.

    World creation fails if:
      * The new world name matches with a world name already in \'self.game_data.worlds\'
      * The world name is empty (i.e. it is \"\")
      * The world seed is empty
    """
    new_world_name: str = self.world_name.get()
    new_world_seed: str = self.world_seed.get()
    existing_world_names: list[str] = list(map(lambda world: world.name, list(self.game_data.worlds.values())))
    fail_message: Optional[str] = None # if is `None`, then the world creation has not failed and thus can succeed. Otherwise, it fails and an appropriate message is passed as an argument to the 'self.fail_creation' function.
    if new_world_name in existing_world_names:
      fail_message = "World name already exists"
    elif new_world_name == "":
      fail_message = "World name cannot be nothing"
    elif new_world_seed == "":
      fail_message = "World seed cannot be nothing"
    
    if fail_message == None:
      self.confirm_creation(new_world_name, new_world_seed)
    else:
      self.fail_creation(fail_message)

  def load(self, **kwargs) -> None:
    super().load(**kwargs)

  def create(self, **kwargs) -> None:
    super().create("World creation", **kwargs)

    self.create_entry("Enter world name:", self.world_name)
    self.create_entry("Enter world seed:", self.world_seed)

    self.create_message()

    self.create_confirm(self.create_world)

    self.create_return(ScreenName.WORLD_SELECTION, **kwargs)
    self.create_quit(**kwargs)


EOF
interface/world_selection.py

import tkinter as tk

from tools.typing_tools import *
from tools.constants import ScreenName

from interface.selection import Selection
from game_data import GameData

from stored.world import World

class WorldSelection(Selection):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    super().__init__(root, parent, game_data, **kwargs)
    self.select_world: Callable[[int], Any] = kwargs["select_world"]
    self.begin_world_creation: ButtonCommand = kwargs["begin_world_creation"]
    self.scrollable_world_frame_parent: tk.Frame

  # dynamic button methods

  def get_world_dynamic_button_input(self, world_id: int, world: World) -> DynamicButtonInput:
    return (world.name, world_id)

  def get_all_world_dynamic_button_inputs(self, worlds: dict[int, World]) -> list[DynamicButtonInput]:
    button_inputs: list[DynamicButtonInput] = []
    for (identifier, world) in worlds.items():
      button_inputs.append(self.get_world_dynamic_button_input(identifier, world))
    return button_inputs

  # creating and loading

  def load(self, **kwargs) -> None:
    super().load(**kwargs)
    worlds: dict[int, World] = self.game_data.worlds
    button_inputs: list[DynamicButtonInput] = self.get_all_world_dynamic_button_inputs(worlds)
    self.create_buttons_dynamically(button_inputs, command=lambda identifier: self.select_world(identifier), container=self.scrollable_world_frame_parent)

  def create(self, **kwargs) -> None:
    self.create_character_name_label()

    self.scrollable_world_frame_parent = unpack_optional(self.create_frame(return_frame=True, dimensions=(1,1)))

    super().create("World selection", **kwargs)

    self.create_widget(tk.Button, text="Create world", command=lambda: self.begin_world_creation())

    self.create_return(ScreenName.CHARACTER_SELECTION, **kwargs)
    self.create_quit(**kwargs)
    

EOF
interface/__init__.py

__all__ = ["abstract_screen", "base_frame", "character_creation", "character_selection", "combat_interface", "creation", "exploration_screen", "home_screen", "interface", "selection", "storage_interface", "world_creation", "world_selection",]

from . import abstract_screen
from . import base_frame
from . import character_selection
from . import character_creation
from . import combat_interface
from . import creation
from . import exploration_screen
from . import home_screen
from . import interface
from . import selection
from . import storage_interface
from . import world_creation
from . import world_selection

EOF
data_structures/action_type.py

from tools.typing_tools import *

from ability_action import *
from data_structures.queue import Queue

@dataclass
class ActionType:
  """
  Which action an instance of `CombatAction` will use on its target, alongside any relevant information which comes with that.

  Abstract base class, with subclasses of `Attack`, `Parry` and `Heal`.
  """
  quantity: float

@dataclass
class Attack(ActionType):
  """
  Docstring for Attack

  :param quantity: Amount of base damage the attack does.
  :type quantity: float
  """
  effects: Queue[AbilityAction] = Queue()

  def add_ability_action(self, ability_action: AbilityAction) -> None:
    self.effects.put(ability_action)

  def get_next_ability(self) -> AbilityAction:
    return self.effects.get()

@dataclass
class Parry(ActionType):
  """
  Docstring for Parry

  :param quantity: Threshold of damage received before the sender starts taking damage.
  :type quantity: float
  :param reflect_proportion: The percentage of damage blocked by the parry which will be reflected at the attacker.
  :type reflect_proportion: float
  """
  reflect_proportion: float

@dataclass
class Heal(ActionType):
  """
  Docstring for Heal

  :param quantity: The amount the target is healed. Greater than or equal to `0`.
  :type quantity: float
  """
  ...

EOF
data_structures/entity_type.py

from tools.typing_tools import *

class EntityType:
  """
  Abstract base class for representing which type of fighting entity an object is addressing.
  """
  ...
  
@dataclass
class CharacterType(EntityType):
  def __repr__(self) -> str:
    return "Character"

@dataclass
class EnemyType(EntityType):
  identifier: int
  position: Position

  def __repr__(self) -> str:
    return f"Enemy (at {self.position})"

@dataclass
class EmptyType(EntityType):
  position: Position

  def __repr__(self) -> str:
    return f"Empty tile (at {self.position})"

EOF
data_structures/fighting_enemy_graph.py

import networkx as nx

from tools.typing_tools import *
from tools.constants import Constants
from tools.logging_tools import *
from tools.positional_tools import *

class FightingEnemyGraph(Sized):
  """
  Stores instances of `FightingEnemy` in an undirected graph data structure.
  """
  def __init__(self) -> None:
    self.dimensions: Position = (Constants.GRID_WIDTH, Constants.GRID_HEIGHT)
    self.__graph: nx.Graph[Position] = nx.grid_graph(dim=self.dimensions) # TODO: put stuff about Graphs in my documentation
    self.init_storage()
    self.add_edges()

  # built-in methods

  @validate_position_on
  def __call__(self, position: Position) -> Optional[int]:
    return self.get_fighting_enemy_id(position)
  
  @validate_position_on
  def __setitem__(self, position: Position, value: Optional[int]) -> None:
    self.set_fighting_enemy_id(position, value)

  @validate_position_on
  def __getitem__(self, position: Position) -> Optional[int]:
    return self.get_fighting_enemy_id(position)
  
  def __len__(self) -> int:
    return self.dimensions[0]*self.dimensions[1]
  
  def __iter__(self):
    self.l: int = 0
    return self
  
  def __next__(self) -> Optional[int]:
    if self.l >= len(self): raise StopIteration
    p: Position = self.length_to_point(self.l)
    self.l += 1
    return self.get_fighting_enemy_id(p)
  
  # other methods

  def length_to_point(self, length: int) -> Position:
    x: int = length % self.dimensions[1]
    y: int = length // self.dimensions[0]
    return (x,y)

  def apply_to_all(self, function: Callable[..., None], **kwargs) -> None:
    """
    Applies a given function, taking inputs of the node position with the kwargs, to every node of the graph.
    
    :param function: Takes an input of `position: Position` first, taking `**kwargs` afterward.
    :type function: Callable[..., None]
    """
    node_count: int = len(self)
    for i in range(node_count):
      position = self.length_to_point(i)
      function(position=position, **kwargs)

  def init_storage(self) -> None:
    node_count: int = len(self)
    for i in range(node_count):
      position = self.length_to_point(i)
      self.__graph.add_node(position, fighting_enemy_id=None)

  @validate_position_on
  def set_fighting_enemy_id(self, position: Position, fighting_enemy_id: Optional[int]) -> None:
    self.__graph.nodes[position]["fighting_enemy_id"] = fighting_enemy_id

  @validate_position_on
  def get_fighting_enemy_id(self, position: Position) -> Optional[int]:
    return self.__graph.nodes[position]["fighting_enemy_id"]
  
  @validate_position_on
  def is_fighting_enemy_at(self, position: Position) -> bool:
    if self.get_fighting_enemy_id(position) == None: return False
    return True
  
  @validate_position_on
  def add_fighting_enemy_id(self, position: Position, fighting_enemy_id: int) -> None:
    if self.is_fighting_enemy_at(position):
      raise MemoryError(f"Attempting to add fighting enemy (id=`{fighting_enemy_id}`) at position `{position}` when there is already an enemy there")
    self.set_fighting_enemy_id(position, fighting_enemy_id)
  
  @validate_position_on
  def clear_fighting_enemy_id(self, position: Position) -> None:
    self.set_fighting_enemy_id(position, None)

  def clear_graph(self) -> None:
    self.apply_to_all(self.clear_fighting_enemy_id)

  def add_edges(self) -> None:
    node_count: int = len(self)
    for l1 in range(node_count-1):
      p1 = self.length_to_point(l1)
      for l2 in range(l1+1, node_count):
        p2 = self.length_to_point(l2)
        distance: float = calculate_distance(p1, p2)
        self.__graph.add_edge(p1, p2, distance=distance)

EOF
data_structures/matrix.py

from tools.typing_tools import *
from tools.logging_tools import *
from tools.positional_tools import validate_position_on

class Matrix[T](Sized):
  """
  Items are stored at position (x,y), being accessed by calling a `Matrix` object with the position tuple.
  """
  def __init__(self, dimensions: Position) -> None:
    """
    Constructor.

    :param dimensions: In the form (x_length, y_length).
    :type dimensions: tuple[int, int]
    """
    self.dimensions = dimensions
    self.__matrix: list[list[Optional[T]]] = []
    self.init_matrix()

  # built-in methods
    
  @validate_position_on
  def __setitem__(self, position: Position, value: T) -> None:
    (x,y) = position
    self.__matrix[x][y] = value

  @validate_position_on
  def __getitem__(self, position: Position) -> Optional[T]:
    (x,y) = position
    return self.__matrix[x][y]

  def __len__(self) -> int:
    return self.dimensions[0]*self.dimensions[1]
  
  # other methods
  
  def init_matrix(self) -> None:
    """
    Requires `self.dimensions` to already be initialised.
    
    :param self: Object being called on.
    """
    (x_length, y_length) = self.dimensions
    for x in range(x_length):
      self.__matrix.append([])
      for _ in range(y_length):
        self.__matrix[x].append(None)


EOF
data_structures/queue.py

from tools.typing_tools import *
from tools.exceptions import *
from tools.logging_tools import *

class Queue[QueueType](Sized, Loggable):
  def __init__(self, queue: list[QueueType] = [], is_logging_enabled: bool = False, label: Optional[str] = None) -> None:
    self.__queue: list[QueueType]
    if queue == []: self.__queue = [].copy()
    else: self.__queue = queue.copy()
    super().__init__(is_logging_enabled, label)

  # built-in methods

  def __len__(self) -> int:
    return len(self.__queue)
  
  def __repr__(self) -> str:
    return f"{self.__queue}"

  # queue operations
  
  def empty(self) -> bool:
    return len(self) == 0

  @log_loggable_return
  def get(self) -> QueueType:
    if self.empty(): raise QueueError(f"Tried to pop value from empty queue.")
    return self.__queue.pop(0)
  
  @log_loggable_return
  def peek(self) -> Optional[QueueType]:
    if self.empty(): return None
    return self.__queue[0]

  @log_loggable_args
  def put(self, value: QueueType) -> None:
    self.__queue.append(value)

EOF
data_structures/stack.py

from tools.typing_tools import *
from tools.exceptions import StackError

class Stack[T](Sized):
  def __init__(self) -> None:
    self.__stack: list[T] = []

  # built-in methods

  def __len__(self) -> int:
    return len(self.__stack)
  
  def __repr__(self) -> str:
    return f"{self.__stack}"
  
  # stack operations
  
  def is_empty(self) -> bool:
    return len(self) == 0

  def pop(self) -> T:
    if self.is_empty(): raise StackError(f"Tried to pop value from empty stack.")
    return self.__stack.pop()
  
  def peek(self) -> Optional[T]:
    if self.is_empty(): return None
    return self.__stack[-1]
  
  def push(self, value: T) -> None:
    self.__stack.append(value)

EOF
data_structures/__init__.py

__all__ = ["action_type", "entity_type", "fighting_enemy_graph", "matrix", "stack"]

from . import action_type
from . import entity_type
from . import fighting_enemy_graph
from . import matrix
from . import stack

EOF
database/condition.py

from tools.typing_tools import *

from tools.dictionary_tools import filter_dictionary

class Condition:
  def __init__(self, condition: Callable[[int, list[Any]], bool]) -> None:
    self.condition: Callable[[int, list[Any]], bool] = condition

  def set_condition(self, condition: Callable[[int, list[Any]], bool]) -> None:
    self.condition = condition

  def get_condition(self) -> Callable[[int, list[Any]], bool]:
    return self.condition
  
  def evaluate(self, identifier: int, row: list[Any]) -> bool:
    return self.condition(identifier, row)
  
def filter_dictionary_with_condition(dictionary: dict[int, list[Any]], condition: Condition) -> dict[int, list[Any]]:
  return filter_dictionary(dictionary, condition.get_condition())

def everything() -> Condition: return Condition(lambda _identifier, _row: True)

def nothing() -> Condition: return Condition(lambda _identifier, _row: False)

def matching_identifiers(specific_identifier: int) -> Condition:
  return Condition(lambda identifier, _row: specific_identifier == identifier)

def get_condition_inverse(condition: Condition) -> Condition:
  return Condition(lambda identifier, row: not condition.get_condition()(identifier, row))

EOF
database/database.py

from tools.typing_tools import *
from tools.logging_tools import *

from database.table import Table
from database.condition import Condition
from database.file_handler import FileHandler

class Database:
  def __init__(self, name: str, tables: dict[str, Table] = {}, table_names: list[str] = []) -> None:
    self.name: str = name
    self.tables: dict[str, Table] = tables
    self.file_handler = FileHandler()
    self.table_names: list[str] = table_names
    self.deleted_table_names: list[str] = []

    self.save_on_delete: bool = True

  def __del__(self) -> None:
    if self.save_on_delete:
      self.save()
  
  def exists(self) -> bool:
    """Uses the \'self.file_handler.does_data_directory_exist()\' method to determine whether the database has already been created in memory or not."""
    if self.file_handler.does_data_directory_exist(): return True
    return False
  
  def create_main(self, table_names: list[str] = []) -> None:
    if not self.file_handler.does_data_directory_exist():
      self.file_handler.create_directory("data")
    if table_names != []: self.table_names = table_names
    formatted_table_names: dict[str, Any] = {"tables": self.table_names}
    self.file_handler.save_file("MAIN", formatted_table_names)

  def load(self) -> None:
    """Fetches the database from storage, loading all tables specified in \'self.table_names\'.
    
    Raises a `ValueError` if \'self.table_names\' is empty."""
    self.table_names = self.load_main_data()
    if self.table_names == []: raise ValueError(f"Expected a non-empty list of table names, instead got `{self.table_names}`")
    for table_name in self.table_names:
      raw_table: dict = self.file_handler.load_file(table_name)
      self.load_table(table_name, raw_table)

  # fetches each table from secondary storage
  def load_table(self, table_name: str, raw_table: dict[str, Any]) -> None:
    column_names: list = raw_table["column_names"] 

    table = Table(table_name, column_names)

    identifier_name: str = column_names[0] # identifier name will always be the first element in the column_names list
    identifier: int = 0
    rows: list[Any] = raw_table["rows"]
    for row in rows: # stores each value in the table
      identifier = row[identifier_name]
      table.insert_with_identifier(row, identifier)
    self.tables[table_name] = table

  def load_main_data(self) -> list[str]:
    if self.file_handler.does_data_directory_exist():
      main_data: list[str] = self.file_handler.load_file("MAIN")["tables"]
    elif list(self.tables.keys()) != []:
      main_data = list(self.tables.keys())
    else:
      main_data = []
    return main_data

  def save(self) -> None:
    self.save_main_data()
    for table_name in self.table_names:
      self.save_table(table_name)
    for deleted_table_name in self.deleted_table_names:
      self.file_handler.delete_file(deleted_table_name)

  def save_main_data(self) -> None:
    main_data: dict[str, list[str]] = {"tables": self.table_names}
    if main_data["tables"] == []:
      main_data["tables"] = self.load_main_data()
    self.file_handler.save_file("MAIN", main_data)

  def save_table(self, table_name: str) -> None:
    table: Table = self.find_table(table_name)
    file: dict = table.to_file()
    self.file_handler.save_file(table_name, file)

  def find_table(self, table_name: str) -> Table:
    try:
      table: Table = self.tables[table_name]
    except:
      raise NameError(f"Table `{table_name}` does not exist.")
    return table

  # SELECT columns FROM table WHERE condition ORDER BY order
  def select(self, table_name: str, columns: list[str], condition: Condition) -> dict[int, list[Any]]:
    return self.find_table(table_name).select(columns, condition)
  
  #update
  def update(self, table_name: str, columns_to_values: dict[str, Any], condition: Condition) -> None:
    table: Table = self.find_table(table_name)
    table.update(columns_to_values, condition)

  def delete_from(self, table_name: str, condition: Condition) -> None:
    table: Table = self.find_table(table_name)
    table.delete_from(condition)

  def insert(self, table_name: str, columns_to_values: dict[str, Any], identifier: Optional[int] = None) -> Optional[int]:
    """Inserts a new record into a specified table, returning the identifier of the newly created record."""
    table: Table = self.find_table(table_name)
    if identifier == None: return table.insert(columns_to_values)
    else: return table.insert_with_identifier(columns_to_values, identifier)

  def create_table(self, table_name: str, column_names: list[str]) -> None:
    if table_name in self.table_names:
      raise BufferError(f"Table `{table_name}` already exists.")
    table = Table(table_name, column_names)
    self.tables[table_name] = table
    self.table_names.append(table_name)

  def delete_table(self, table_name: str) -> None:
    self.table_names = list(filter(lambda element : element != table_name, self.table_names))
    self.deleted_table_names.append(table_name)
    self.tables.pop(table_name)

  #add_column
  def add_column(self, table_name: str, column_name: str) -> None:
    self.find_table(table_name).add_column(column_name)

  #drop_column
  def drop_column(self, table_name: str, column_name: str) -> None:
    self.find_table(table_name).drop_column(column_name)

  #rename_column
  def rename_column(self, table_name: str, name: str, new_name: str) -> None:
    self.find_table(table_name).rename_column(name, new_name)

  #rename_table
  def rename_table(self, table_name: str, new_name: str) -> None:
    table: Table = self.find_table(table_name)
    table.rename_table(new_name)
    self.tables[new_name] = self.tables.pop(table_name)

EOF
database/file_handler.py

import toml
import os
import sys

from tools.typing_tools import *

# Note: added because it makes code more readable, more modular and is a different thing to the database itself.

class FileHandler:
  def __init__(self) -> None:
    pass

  @staticmethod
  def data_path() -> str:
    return os.path.join("src", "data")

  @staticmethod
  def file_path(file_name: str) -> str:
    toml_suffix: str = ".toml"
    file_name_length: int = len(file_name)
    file_name_suffix: str = file_name[file_name_length-5:]
    if file_name_suffix != toml_suffix:
      file_name = file_name + toml_suffix
    return os.path.join(FileHandler.data_path(), file_name)
  
  def does_data_directory_exist(self) -> bool:
    return os.path.isdir(self.data_path())
  
  def create_directory(self, directory_name: str) -> None:
    directory_path: str = os.path.join("src", directory_name)
    os.mkdir(directory_path)

  def save_file(self, file_name: str, data: dict[str, Any]) -> None:
    file_path: str = self.file_path(file_name)
    with open(file_path, 'w') as f:
      toml.dump(data, f)
    
  def load_file(self, file_name: str) -> dict[str, Any]:
    file_path: str = self.file_path(file_name)
    return toml.load(file_path)
  
  def delete_file(self, file_name: str) -> None:
    file_path: str = self.file_path(file_name)
    os.remove(file_path)

EOF
database/table.py

from tools.typing_tools import *
from tools.logging_tools import *
from tools.dictionary_tools import *

from database.condition import Condition, filter_dictionary_with_condition, get_condition_inverse

from tools.exceptions import InsertAtExistingIdentifierError

class Table:
  def __init__(self, name: str, column_names: list[str]) -> None:
    self.name: str = name
    self.column_names: list[str] = column_names
    self.rows: dict[int, list[Any]] = {}

  # built-in methods

  def __repr__(self) -> str:
    formatted_table: str = ""
    formatted_table += f"Table: name=`{self.name}`"
    formatted_table += f"\ncolumn_names=`{self.column_names}`"
    formatted_table += "\nrows = {"
    for (identifier, row) in self.rows.items():
      formatted_table += f"\n\t{identifier}: [{row[0]}"
      if len(row) > 1:
        for field in row[1:]:
          formatted_table += f",\t{field}"
        formatted_table += "],"
    formatted_table += "\n}"
    return formatted_table

  # basic getter and setter methods

  @property
  def identifiers(self) -> list[int]:
    return sorted(list(self.rows.keys()))

  def get_identifier_name(self) -> str:
    return self.column_names[0]  # identifier name will always be the first element in the column_names list
  
  def get_non_identifier_column_names(self) -> list[str]:
    if len(self.column_names) == 1:
      return []
    return self.column_names[1:]

  def to_file(self) -> dict[str, Any]:
    file: dict[str, Any] = {}

    file["column_names"] = self.column_names

    rows: list[dict[str, Any]] = []
    identifier_name: str = self.get_identifier_name()
    remaining_columns: list[str] = []
    file_row: dict[str, Any] = {}
    for (identifier, table_row) in self.rows.items():
      file_row[identifier_name] = identifier # sets the first value to be the identifier
      remaining_columns = self.get_non_identifier_column_names() # goes through every column except the identifier
      for (i, column_name) in enumerate(remaining_columns):
        file_row[column_name] = table_row[i]
      rows.append(file_row.copy()) # a copy is used, as if it were not, then all of the rows would be stored with the same data as the most recently saved one

    file["rows"] = rows
    return file

  # SELECT columns FROM rows WHERE condition ORDER BY order
  # Wildcard 
  def select(self, columns: list[str], condition: Condition) -> dict[int, list[Any]]:
    non_identifier_column_names: list[str] = self.get_non_identifier_column_names()
    if columns[0] == "*":
      columns = non_identifier_column_names
    selected_column_indexes: list[int] = []
    for (i, column_name) in enumerate(non_identifier_column_names):
      if column_name in columns:
        selected_column_indexes.append(i)

    selected_rows: dict[Any, Any] = filter_dictionary_with_condition(self.rows, condition)
    for (identifier, row) in selected_rows.items():
      filtered_row = []
      for i in selected_column_indexes:
        filtered_row.append(row[i])
      selected_rows[identifier] = filtered_row

    return selected_rows
  
  def update(self, columns_to_values: dict[str, Any], condition: Condition) -> None:
    rows_to_update: dict[int, list[Any]] = filter_dictionary_with_condition(self.rows, condition)
    identifiers_to_update: list[int] = list(rows_to_update.keys())
    column_name: str = ""
    updated_rows: dict[int, list[Any]] = {}
    non_identifier_column_names: list[str] = self.get_non_identifier_column_names()
    for identifier in identifiers_to_update:
      fields_to_update = rows_to_update[identifier]
      for (i, column_name) in enumerate(non_identifier_column_names):
        try:
          column_value = columns_to_values[column_name]
        except:
          continue
        fields_to_update[i] = column_value
      updated_rows[identifier] = fields_to_update
    for identifier in updated_rows:
      self.rows[identifier] = updated_rows[identifier]

  def delete_from(self, condition: Condition) -> None:
    """Deletes all values from the table where the condition statement evaluates to `True`."""
    condition_inverse: Condition = get_condition_inverse(condition)
    undeleted_rows: dict[int, list[Any]] = filter_dictionary_with_condition(self.rows, condition_inverse)
    self.rows = undeleted_rows
  
  def format_raw_row(self, raw_row: dict[str, Any]) -> list[Any]:
    """Turns a dictionary of the form `column: field` to an array of fields in order *without* the identifier"""
    formatted_row: list[Any] = []
    non_identifier_column_names: list[str] = self.get_non_identifier_column_names()
    for column_name in non_identifier_column_names:
      try:
        value = raw_row[column_name]
      except:
        value = None
      formatted_row.append(value)
    return formatted_row
  
  def insert_with_identifier(self, raw_row: dict[str, Any], identifier: int) -> None:
    """Inserts a new record at a given identifier. Raises an error if the identifier has already been assigned."""
    existing_identifiers: list[int] = list(self.rows.keys())
    if identifier in existing_identifiers: raise InsertAtExistingIdentifierError(identifier, self.name)
    self.rows[identifier] = self.format_raw_row(raw_row)

  #insert
  def insert(self, raw_row: dict[str, Any]) -> int:
    identifier: int = get_next_available_identifier(self.rows)
    self.insert_with_identifier(raw_row, identifier)
    return identifier
  
  def get_next_available_identifier(self) -> int:
    """Calculates the smallest, non-zero identifier not in the table."""
    previous_id: int = -1 # defining variables
    previous_id_successor: int = 0 
    for current_id in self.identifiers:
      previous_id_successor = previous_id+1
      if current_id > previous_id_successor: # if there is a hole in the sequence (e.g. [1,2,4,5] would return 3)
        return previous_id_successor
      previous_id = current_id # sets up for next iteration
    previous_id_successor = previous_id+1
    return previous_id_successor # in the case there are no holes, then it returns the id outside of the list 

  #add_column
  def add_column(self, name: str) -> None:
    if name in self.column_names:
      raise Exception(f"Column `{name}` already exists.")
    self.column_names.append(name)
    for identifier in self.rows.keys():
      self.rows[identifier].append(None)

  #drop_column
  def drop_column(self, name: str) -> None:
    if not (name in self.column_names):
      raise Exception(f"Cannot remove column `{name}` which does not exist.")
    non_identifier_column_names: list[str] = self.get_non_identifier_column_names()
    new_column_names: list[str] = []
    dropped_index: int = -1
    for (i, column_name) in enumerate(non_identifier_column_names):
      if column_name == name:
        dropped_index = i
      else:
        new_column_names.append(column_name)
    
    self.column_names = new_column_names
    
    for (identifier, row) in self.rows.items():
      new_row = []
      for (i, field) in enumerate(row):
        if i != dropped_index:
          new_row.append(field)
      self.rows[identifier] = new_row

  #rename_column
  def rename_column(self, name: str, new_name: str) -> None:
    for (i, column_name) in enumerate(self.column_names):
      if column_name == name:
        self.column_names[i] = new_name

  #rename_table
  def rename_table(self, new_name) -> None:
    self.name = new_name

EOF
database/__init__.py

__all__ = ["condition", "database", "file_handler", "table"]

from . import condition
from . import database
from . import file_handler
from . import table

EOF
data/Ability.toml

column_names = [ "AbilityID", "Text", "Type",]
[[rows]]
AbilityID = 0
Text = "Sets fire to the target for 3 turns."
Type = "Ignite"

[[rows]]
AbilityID = 1
Text = "Ignores any damage resistances."
Type = "Pierce"

[[rows]]
AbilityID = 2
Text = "Increases damage resistance by 15%."
Type = "Defend"

[[rows]]
AbilityID = 3
Text = "Knight's Sword parry."
Type = "Parry"

[[rows]]
AbilityID = 4
Text = "Glass Dagger parry."
Type = "Parry"

[[rows]]
AbilityID = 5
Text = "Mace parry."
Type = "Parry"

[[rows]]
AbilityID = 6
Text = "Slightly heals."
Type = "Heal"

[[rows]]
AbilityID = 7
Text = "Moderately heals."
Type = "Heal"

[[rows]]
AbilityID = 8
Text = "Greatly heals."
Type = "Heal"



EOF
data/Character.toml

column_names = [ "CharacterID", "UserID", "Name", "Health", "MaxHealth",]
[[rows]]
CharacterID = 0
UserID = 0
Name = "Jeremiah"
Health = 100.0
MaxHealth = 100

[[rows]]
CharacterID = 1
UserID = 0
Name = "Testing"
Health = 100
MaxHealth = 100

[[rows]]
CharacterID = 2
UserID = 0
Name = "gibble"
Health = 100
MaxHealth = 100



EOF
data/CharacterModifier.toml

column_names = [ "CharacterModifierID", "CharacterID", "AbilityID", "RemainingTurns",]
rows = []


EOF
data/Enemy.toml

column_names = [ "EnemyID", "Name", "MaxHealth", "AttackDamage", "Intelligence", "IsBoss",]
[[rows]]
EnemyID = 0
Name = "Skeleton"
MaxHealth = 30
AttackDamage = 10
Intelligence = 1
IsBoss = false

[[rows]]
EnemyID = 1
Name = "Flaming Skeleton"
MaxHealth = 25
AttackDamage = 10
Intelligence = 1
IsBoss = false

[[rows]]
EnemyID = 2
Name = "Armoured Skeleton"
MaxHealth = 30
AttackDamage = 7
Intelligence = 2
IsBoss = false

[[rows]]
EnemyID = 3
Name = "Giant Skeleton"
MaxHealth = 200
AttackDamage = 20
Intelligence = 10
IsBoss = true



EOF
data/EnemyAbility.toml

column_names = [ "EnemyAbilityID", "EnemyID", "AbilityID", "IsUsedInAttack",]
[[rows]]
EnemyAbilityID = 0
EnemyID = 1
AbilityID = 0
IsUsedInAttack = 0



EOF
data/Equipable.toml

column_names = [ "EquipableID", "ItemID",]
[[rows]]
EquipableID = 0
ItemID = 3

[[rows]]
EquipableID = 1
ItemID = 4

[[rows]]
EquipableID = 2
ItemID = 5

[[rows]]
EquipableID = 3
ItemID = 6



EOF
data/FightingEnemyModifier.toml

column_names = [ "FightingEnemyModifierID", "FightingEnemyID", "AbilityID", "RemainingTurns",]
rows = []


EOF
data/InventoryItem.toml

column_names = [ "InventoryItemID", "CharacterID", "ItemID", "StackSize", "Equipped",]
[[rows]]
InventoryItemID = 0
CharacterID = 0
ItemID = 0
StackSize = 1
Equipped = true

[[rows]]
InventoryItemID = 1
CharacterID = 0
ItemID = 2
StackSize = 1
Equipped = true

[[rows]]
InventoryItemID = 2
CharacterID = 0
ItemID = 1
StackSize = 1
Equipped = true

[[rows]]
InventoryItemID = 3
CharacterID = 0
ItemID = 3
StackSize = 1
Equipped = true



EOF
data/Item.toml

column_names = [ "ItemID", "ItemType", "Name",]
[[rows]]
ItemID = 0
ItemType = "Weapon"
Name = "Knight's Sword"

[[rows]]
ItemID = 1
ItemType = "Weapon"
Name = "Mace"

[[rows]]
ItemID = 2
ItemType = "Weapon"
Name = "Glass Dagger"

[[rows]]
ItemID = 3
ItemType = "Equipable"
Name = "Bronze Anklet"

[[rows]]
ItemID = 4
ItemType = "Equipable"
Name = "Helmate of the Traveller"

[[rows]]
ItemID = 5
ItemType = "Equipable"
Name = "Swiftness Boots"

[[rows]]
ItemID = 6
ItemType = "Equipable"
Name = "Cast-Iron Mask"

[[rows]]
ItemID = 7
ItemType = "Weapon"
Name = "Red Katana"

[[rows]]
ItemID = 8
ItemType = "Weapon"
Name = "Leviathan Sword"



EOF
data/ItemAbility.toml

column_names = [ "ItemAbilityID", "ItemID", "AbilityID",]
[[rows]]
ItemAbilityID = 0
ItemID = 0
AbilityID = 3

[[rows]]
ItemAbilityID = 1
ItemID = 1
AbilityID = 4

[[rows]]
ItemAbilityID = 2
ItemID = 2
AbilityID = 5

[[rows]]
ItemAbilityID = 3
ItemID = 3
AbilityID = 2



EOF
data/MAIN.toml

tables = [ "User", "Character", "ItemAbility", "CharacterModifier", "World", "FightingEnemyModifier", "InventoryItem", "Storage", "StorageItem", "Item", "Weapon", "Equipable", "Ability", "StatisticAbility", "Enemy", "EnemyAbility", "ParryAbility",]


EOF
data/ParryAbility.toml

column_names = [ "ParryAbilityID", "AbilityID", "DamageThreshold", "ReflectionProportion",]
[[rows]]
ParryAbilityID = 0
AbilityID = 3
DamageThreshold = 15
ReflectionProportion = 0.6

[[rows]]
ParryAbilityID = 1
AbilityID = 4
DamageThreshold = 5
ReflectionProportion = 0.95

[[rows]]
ParryAbilityID = 2
AbilityID = 5
DamageThreshold = 25
ReflectionProportion = 0.1



EOF
data/StatisticAbility.toml

column_names = [ "StatisticAbilityID", "AbilityID", "AbilityType", "Amount", "InitialDuration",]
[[rows]]
StatisticAbilityID = 0
AbilityID = 2
AbilityType = "Defend"
Amount = 0.15

[[rows]]
StatisticAbilityID = 1
AbilityID = 6
AbilityType = "Heal"
Amount = 10

[[rows]]
StatisticAbilityID = 2
AbilityID = 7
AbilityType = "Heal"
Amount = 20

[[rows]]
StatisticAbilityID = 3
AbilityID = 8
AbilityType = "Heal"
Amount = 30



EOF
data/Storage.toml

column_names = [ "StorageID", "WorldID", "StorageType",]
[[rows]]
StorageID = 0
WorldID = 0
StorageType = "Home"

[[rows]]
StorageID = 1
WorldID = 0
StorageType = "Chest"

[[rows]]
StorageID = 2
WorldID = 1
StorageType = [ "H", "o", "m", "e",]

[[rows]]
StorageID = 3
WorldID = 1
StorageType = [ "C", "h", "e", "s", "t",]



EOF
data/StorageItem.toml

column_names = [ "StorageItemID", "StorageID", "ItemID", "StackSize",]
[[rows]]
StorageItemID = 1
StorageID = 0
ItemID = 4
StackSize = 1

[[rows]]
StorageItemID = 2
StorageID = 0
ItemID = 5
StackSize = 1

[[rows]]
StorageItemID = 3
StorageID = 0
ItemID = 6
StackSize = 1



EOF
data/User.toml

column_names = [ "UserID", "Name", "PasswordHash", "CharacterQuantity", "WorldQuantity",]
[[rows]]
UserID = 0
Name = "User"
PasswordHash = "1234"
CharacterQuantity = 5
WorldQuantity = 3



EOF
data/Weapon.toml

column_names = [ "WeaponID", "ItemID", "Damage", "UsesAmmunition", "ManaUsed", "Active",]
[[rows]]
WeaponID = 0
ItemID = 0
Damage = 10
UsesAmmunition = false
ManaUsed = 0
Active = false

[[rows]]
WeaponID = 1
ItemID = 1
Damage = 15
UsesAmmunition = false
ManaUsed = 0
Active = false

[[rows]]
WeaponID = 2
ItemID = 2
Damage = 5
UsesAmmunition = false
ManaUsed = 0
Active = false

[[rows]]
WeaponID = 3
ItemID = 7
Damage = 20
UsesAmmunition = false
ManaUsed = 0
Active = false

[[rows]]
WeaponID = 4
ItemID = 8
Damage = 30
UsesAmmunition = false
ManaUsed = 0
Active = false



EOF
data/World.toml

column_names = [ "WorldID", "UserID", "Name", "Seed",]
[[rows]]
WorldID = 0
UserID = 0
Name = "Terraria"
Seed = "1234"

[[rows]]
WorldID = 1
UserID = 0
Name = "miggle"
Seed = "67"



EOF
custom_tkinter/dynamic_button.py

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

EOF
custom_tkinter/toggleable_button.py

import tkinter as tk

from tools.logging_tools import *
from tools.typing_tools import *
from tools.constants import *
from tools.tkinter_tools import *

class ToggleableButton(tk.Button):
  """A button whose state can be toggled each time it is pressed."""
  def __init__(self, master: Optional[tk.Misc] = None, initially_toggled: ToggleState = ToggleState.OFF, initially_enabled: bool = True, on_colour: str = Constants.ON_COLOUR, off_colour: str = Constants.OFF_COLOUR, disabled_colour: str = Constants.DISABLED_COLOUR, **kwargs) -> None:
    if "toggleable" in kwargs.keys():
      raise NameError("Constructor for `ToggleableButton` no longer takes the parameter `toggleable`")
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

EOF
custom_tkinter/weapon_interface.py

import tkinter as tk

from tools.constants import *
from tools.tkinter_tools import Position
from tools.typing_tools import *
from tools.tkinter_tools import *
from tools.dictionary_tools import add_if_vacant

from custom_tkinter.toggleable_button import ToggleableButton
from interface.base_frame import BaseFrame
from tools.typing_tools import Position

class WeaponInterface(BaseFrame):
  def __init__(self, root: tk.Misc, parent: tk.Frame, weapon_name: Optional[str] = None, attack_damage: Optional[float] = None, parry_damage_threshold: Optional[float] = None, parry_reflection_proportion: Optional[float] = None, dimensions: Position = Constants.WEAPON_INTERFACE_DIMENSIONS, **kwargs) -> None:
    super().__init__(root=root, parent=parent)
    
    self.__weapon_name_label: tk.Label
    self.__attack_button: ToggleableButton
    self.__attack_damage_label: tk.Label
    self.__parry_button: ToggleableButton
    self.__parry_damage_threshold_label: tk.Label
    self.__parry_reflection_proportion_label: tk.Label

    self.__weapon_name_text = tk.StringVar()
    self.__attack_button_text = tk.StringVar()
    self.__attack_damage_text = tk.StringVar()
    self.__parry_button_text = tk.StringVar()
    self.__parry_damage_threshold_text = tk.StringVar()
    self.__parry_reflection_proportion_text = tk.StringVar()

    self.__attack_damage: Optional[float]
    self.__parry_damage_threshold: Optional[float]
    self.__parry_reflection_proportion: Optional[float]

    self.__is_weapon_used: bool = False

    self.dimensions = dimensions
    
    self.weapon_name = weapon_name

    configure_grid(self, dimensions=self.dimensions, exclude_rows=[0,2])

    self.create(weapon_name, attack_damage, parry_damage_threshold, parry_reflection_proportion, **kwargs)

  # built-in methods

  def __getitem__(self, key: Union[WeaponUIComponentName, str]) -> Any:
    match key:
      case WeaponUIComponentName.WEAPON_NAME:
        return self.__weapon_name
      case WeaponUIComponentName.ATTACK:
        return self.__attack_button
      case WeaponUIComponentName.PARRY:
        return self.__parry_button
      case _:
        return super().__getitem__(key)

  # getter and setter methods

  @property
  def is_weapon_used(self) -> bool:
    return self.__is_weapon_used
  
  @is_weapon_used.setter
  def is_weapon_used(self, is_weapon_used: bool) -> None:
    """Disables the buttons if it is set to `True` and enables them if set to `False`."""
    if is_weapon_used: self.set_buttons_state(tk.DISABLED)
    else: self.set_buttons_state(tk.NORMAL)
    self.__is_weapon_used = is_weapon_used

  @property
  def is_attack_toggled(self) -> ToggleState:
    return self.__attack_button.is_toggled
  
  @is_attack_toggled.setter
  def is_attack_toggled(self, is_attack_toggled: ToggleState) -> None:
    self.__attack_button.is_toggled = is_attack_toggled 

  @property
  def is_parry_toggled(self) -> ToggleState:
    return self.__parry_button.is_toggled
  
  @is_parry_toggled.setter
  def is_parry_toggled(self, is_parry_toggled: ToggleState) -> None:
    self.__parry_button.is_toggled = is_parry_toggled

  @property
  def weapon_name(self) -> str:
    return self.__weapon_name
  
  @weapon_name.setter
  def weapon_name(self, weapon_name: Optional[str]) -> None:
    self.__weapon_name = unpack_optional_string(weapon_name, default="")
    self.weapon_name_text = self.__weapon_name

  @property
  def weapon_name_text(self) -> str:
    return self.__weapon_name_text.get()
  
  @weapon_name_text.setter
  def weapon_name_text(self, weapon_name: Optional[str]) -> None:
    weapon_name = unpack_optional_string(weapon_name, default="")
    self.__weapon_name_text.set(weapon_name)

  ## button text
  @property
  def attack_button_text(self) -> str:
    return self.__attack_button_text.get()
  
  @attack_button_text.setter
  def attack_button_text(self, text: str) -> None:
    self.__attack_button_text.set(text)
 
  @property
  def parry_button_text(self) -> str:
    return self.__parry_button_text.get()
  
  @parry_button_text.setter
  def parry_button_text(self, text: str) -> None:
    self.__parry_button_text.set(text)
  
  ## attack information
  @property
  def attack_damage_text(self) -> str:
    return self.__attack_damage_text.get()
  
  @attack_damage_text.setter
  def attack_damage_text(self, text: str) -> None:
    self.__attack_damage_text.set(text)

  @property
  def attack_damage(self) -> Optional[float]:
    return self.__attack_damage
  
  @attack_damage.setter
  def attack_damage(self, damage: Optional[float]) -> None:
    self.__attack_damage = damage
    if damage == None: self.attack_damage_text = "-"
    else: self.attack_damage_text = f"DMG: {self.attack_damage}"

  ## parry information
  ### damage threshold
  @property
  def parry_damage_threshold_text(self) -> str:
    return self.__parry_damage_threshold_text.get()
  
  @parry_damage_threshold_text.setter
  def parry_damage_threshold_text(self, text: str) -> None:
    self.__parry_damage_threshold_text.set(text)

  @property
  def parry_damage_threshold(self) -> Optional[float]:
    return self.__parry_damage_threshold
  
  @parry_damage_threshold.setter
  def parry_damage_threshold(self, damage_threshold: Optional[float]) -> None:
    self.__parry_damage_threshold = damage_threshold
    if damage_threshold == None: self.parry_damage_threshold_text = "-"
    else: self.parry_damage_threshold_text = f"MAX: {self.parry_damage_threshold}"

  ### reflection proportion
  @property
  def parry_reflection_proportion_text(self) -> str:
    return self.__parry_reflection_proportion_text.get()
  
  @parry_reflection_proportion_text.setter
  def parry_reflection_proportion_text(self, text: str) -> None:
    self.__parry_reflection_proportion_text.set(text)

  @property
  def parry_reflection_proportion(self) -> Optional[float]:
    return self.__parry_reflection_proportion
  
  @parry_reflection_proportion.setter
  def parry_reflection_proportion(self, reflection_proportion: Optional[float]) -> None:
    self.__parry_reflection_proportion = reflection_proportion
    if reflection_proportion == None: self.parry_reflection_proportion_text = "-"
    else: self.parry_reflection_proportion_text = f"RFLCT: {unpack_optional(self.parry_reflection_proportion)*100}%" # `self.parry_reflection_proportion` cannot be `None` if the program reaches this point, so `unpack_optional` will never raise an error
  
  # creating UI elements

  def create_weapon_name_label(self) -> None:
    weapon_name_label_opt: Optional[tk.Label] = self.create_widget_on_self(tk.Label, position=(0,0), return_widget=True, textvariable=self.__weapon_name_text, placement_options={"columnspan": 4})
    self.__name_label = unpack_optional(weapon_name_label_opt)

  ## buttons
  def create_attack_button(self) -> None:
    attack_button_opt: Optional[ToggleableButton] = self.create_toggleable_button_on_self((0,1), return_button=True, textvariable=self.__attack_button_text, placement_options={"columnspan": 2, "sticky": "ew"}, height=2)
    self.__attack_button = unpack_optional(attack_button_opt)
    self.attack_button_text = "A"
  
  def create_parry_button(self) -> None:
    parry_button_opt: Optional[ToggleableButton] = self.create_toggleable_button_on_self((2,1), return_button=True, textvariable=self.__parry_button_text, placement_options={"columnspan": 2, "sticky": "ew"}, height=2)
    self.__parry_button = unpack_optional(parry_button_opt)

  ## button descriptors
  def create_attack_damage_label(self) -> None:
    kwargs: dict[str, Any] = add_if_vacant({}, DefaultTkInitOptions().WEAPON_INTERFACE_DESCRIPTORS)
    attack_damage_label_opt: Optional[tk.Label] = self.create_widget_on_self(tk.Label, position=(0,2), return_widget=True, textvariable=self.__attack_damage_text, placement_options={"columnspan": 2}, **kwargs)
    self.__attack_damage_label = unpack_optional(attack_damage_label_opt)

  def create_parry_damage_threshold_label(self) -> None:
    kwargs: dict[str, Any] = add_if_vacant({}, DefaultTkInitOptions().WEAPON_INTERFACE_DESCRIPTORS)
    parry_damage_threshold_label_opt: Optional[tk.Label] = self.create_widget_on_self(tk.Label, position=(2,2), return_widget=True, textvariable=self.__parry_damage_threshold_text, **kwargs)
    self.__parry_damage_threshold_label = unpack_optional(parry_damage_threshold_label_opt)

  def create_parry_reflection_proportion_label(self) -> None:
    kwargs: dict[str, Any] = add_if_vacant({}, DefaultTkInitOptions().WEAPON_INTERFACE_DESCRIPTORS)
    parry_reflection_proportion_label_opt: Optional[tk.Label] = self.create_widget_on_self(tk.Label, position=(3,2), return_widget=True, textvariable=self.__parry_reflection_proportion_text, **kwargs)
    self.__parry_reflection_proportion_label = unpack_optional(parry_reflection_proportion_label_opt)

  # state-setting methods

  def set_attack_button_attribute(self, attribute: str, value: Any) -> None:
    self.__attack_button[attribute] = value

  def set_parry_button_attribute(self, attribute: str, value: Any) -> None:
    self.__parry_button[attribute] = value

  def set_buttons_attribute(self, attribute: str, value: Any) -> None:
    self.set_attack_button_attribute(attribute, value)
    self.set_parry_button_attribute(attribute, value)

  def set_buttons_state(self, state: str) -> None:
    self.set_buttons_attribute("state", state)

  def reset_buttons_toggle(self) -> None:
    self.set_buttons_attribute("is_toggled", ToggleState.OFF)
  
  # creating and loading self

  def load(self, weapon_name: Optional[str] = None, attack_damage: Optional[float] = None, parry_damage_threshold: Optional[float] = None, parry_reflection_proportion: Optional[float] = None, **kwargs) -> None:
    self.weapon_name = weapon_name

    self.attack_damage = attack_damage
    self.parry_damage_threshold = parry_damage_threshold
    self.parry_reflection_proportion = parry_reflection_proportion

  def create(self, weapon_name: Optional[str] = None, attack_damage: Optional[float] = None, parry_damage_threshold: Optional[float] = None, parry_reflection_proportion: Optional[float] = None, **kwargs) -> None:
    self.create_weapon_name_label()

    self.create_attack_button()
    self.attack_button_text = "Attack"
    self.create_attack_damage_label()

    self.create_parry_button()
    self.parry_button_text = "Parry"
    self.create_parry_damage_threshold_label()
    self.create_parry_reflection_proportion_label()

    self.load(weapon_name, attack_damage, parry_damage_threshold, parry_reflection_proportion, **kwargs)

def create_weapon_interface(root: tk.Misc, parent: tk.Frame, position: Position, weapon_name: Optional[str] = None, attack_damage: Optional[float] = None, parry_damage_threshold: Optional[float] = None, parry_reflection_proportion: Optional[float] = None, placement_options: dict[str, Any] = {}, **kwargs) -> WeaponInterface:
  weapon_interface = WeaponInterface(root, parent, weapon_name, attack_damage, parry_damage_threshold, parry_reflection_proportion, **kwargs)
  (column,row) = position
  placement_options = add_if_vacant(placement_options, DefaultTkInitOptions().GRID)
  weapon_interface.grid(column=column, row=row, **placement_options)
  return weapon_interface

EOF
custom_tkinter/__init__.py

__all__ = ["dynamic_button", "toggleable_button", "weapon_interface"]

from . import dynamic_button
from . import toggleable_button
from . import weapon_interface

EOF
combat_management/active_effect.py

from tools.typing_tools import *
from tools.exceptions import InvalidTurnsError

from ability_action import AbilityAction

def is_turns_valid(turns_remaining: Optional[int]) -> bool:
  """Return `False` if `turns_remaining` is invalid (i.e. less than `0`)."""
  if turns_remaining == None: return True
  if turns_remaining >= 0: return True
  return True

@dataclass
class ActiveEffect:
  """
  :param turns_remaining: `None` if permanent, otherwise is a non-negative integer.
  :type turns_remaining: Optional[int]
  :param effect_ability: The ability which is being applied.
  :type effect_ability: AbilityAction
  """
  turns_remaining: Optional[int]
  effect_ability: AbilityAction

  def is_no_turns_remaining(self) -> bool:
    if self.turns_remaining == 0: return True
    return False
  
  def is_permanent(self) -> bool:
    if self.turns_remaining == None: return True
    return False

  def decrement_remaining_turns(self) -> None:
    if self.turns_remaining == None: raise ValueError(f"Cannot decrement `self.turns_remaining` when it is `None`.")
    decremented_turns_remaining: int = self.turns_remaining - 1
    if not is_turns_valid(decremented_turns_remaining): raise InvalidTurnsError(decremented_turns_remaining)
    self.turns_remaining = decremented_turns_remaining
    

EOF
combat_management/combat_manager.py

from tools.constants import *
from tools.typing_tools import *
from tools.logging_tools import *
from tools.exceptions import *
from tools.positional_tools import length_to_point

import game_data as gd

from interface.combat_interface import CombatInterface

from stored.entities.character import Character
from stored.entities.fighting_enemy import FightingEnemy
from stored.entities.fighting_entity import FightingEntity

from stored.abilities.ability import Ability

from data_structures.action_type import *
from combat_action import CombatAction
from data_structures.entity_type import *
from data_structures.queue import Queue

from data_structures.fighting_enemy_graph import FightingEnemyGraph

from combat_management.effect_manager import EffectManager

class CombatManager:
  def __init__(self, game_data: gd.GameData, combat_interface: CombatInterface) -> None:
    self.game_data = game_data

    self.combat_interface = combat_interface

    self.effect_manager = EffectManager(self.game_data)

    self.actions: Queue[CombatAction] = Queue()

    self.enemy_graph = FightingEnemyGraph()

    self.__remaining_actions: int = 0
    self.__round_number: int = 1

    self.is_character_turn: bool = True

  # getter and setter methods
  @property
  def remaining_actions(self) -> int:
    """Getter method for `__remaining_actions`"""
    return self.__remaining_actions
  
  @remaining_actions.setter
  def remaining_actions(self, value: int) -> None:
    """Setter method for `__remaining_actions`"""
    if value > Constants.MAX_REMAINING_PLAYER_ACTIONS:
      raise ValueError(f"Cannot set \'__remaining_actions\' to value=`{value}` greater than \'Constants.MAX_REMAINING_PLAYER_ACTIONS\' (`{value}` > `{Constants.MAX_REMAINING_PLAYER_ACTIONS}`)")
    if value < Constants.MIN_REMAINING_ACTIONS:
      raise ValueError(f"Cannot set \'__remaining_actions\' to value=`{value}` less than \'Constants.MIN_REMAINING_ACTIONS\' (`{value}` < `{Constants.MIN_REMAINING_ACTIONS}`)")
    self.__remaining_actions = value

  @property
  def round_number(self) -> int:
    """Getter method for `__round_number`"""
    return self.__round_number

  @round_number.setter
  def round_number(self, value: int) -> None:
    """Setter method for `__round_number`"""
    if value < Constants.MIN_ROUND_NUMBER:
      raise ValueError(f"Cannot set \'__round_number\' to value=`{value}` less than \'Constants.MIN_ROUND_NUMBER\' (`{value}` < `{Constants.MIN_ROUND_NUMBER}`)")
    self.__round_number = value

  @property
  def active_character_id(self) -> int:
    if self.game_data.active_character_id == None: raise NoCharacterSelectedError()
    return self.game_data.active_character_id

  # basic methods for operating on some numeric values

  def reset_remaining_actions(self) -> None:
    self.remaining_actions = Constants.MAX_REMAINING_PLAYER_ACTIONS
  
  def decrement_remaining_actions(self) -> None:
    self.remaining_actions -= 1

  def is_remaining_actions_zero(self) -> bool:
    return self.remaining_actions == 0

  def reset_round_number(self) -> None:
    self.round_number = Constants.MIN_ROUND_NUMBER

  def increment_round_number(self) -> None:
    self.round_number += 1

  # methods for controlling user buttons

  def enable_user_buttons(self, include_confirm: bool = True) -> None:
    self.combat_interface.enable_user_buttons(include_confirm)

  def disable_user_buttons(self, include_confirm: bool = True) -> None:
    self.combat_interface.disable_user_buttons(include_confirm)

  def reset_toggleable_user_buttons_state(self) -> None:
    self.combat_interface.reset_toggleable_user_buttons_state()

  # methods for adding information to `self.combat_interface`

  def add_info(self, message: str = "") -> None:
    logging.info(f"Adding info ({message=})...")
    """Adds a newline at the end of the message."""
    _ = self.combat_interface.add_info(message)
    logging.info(f"Info added ({message=})")

  def add_newline_info(self) -> None:
    self.add_info()

  def clear_info(self) -> None:
    self.combat_interface.clear_info()
  
  def add_remaining_actions_info(self) -> None:
    self.add_info(f" > Remaining actions: {self.remaining_actions}")

  def add_round_start_info(self, round: int) -> None:
    self.add_info(f" --- ROUND {round} --- ")

  def add_character_created_action_info(self, action: CombatAction) -> None:
    self.add_info(f" > {action}") 

  def add_entity_turn_begin_info(self, character_turn: bool) -> None:
    message: str
    if character_turn: message = "Character's turn:"
    else: message = "Enemies' turn:"
    self.add_info(message)

  def add_error_info(self, action_descriptor: str, error_message: str) -> None:
    message: str = f"{action_descriptor.upper()} ERROR: {error_message}"
    self.add_info(message)

  def add_action_input_error_info(self, error_type: str, error_message: Optional[str] = None) -> None:
    error_description: str = ""
    if error_message == None: error_description = f"{error_type}"
    else: error_description = f"{error_message} (`{error_type=}`)"
    self.add_error_info("ACTION INPUT", error_description)

  def add_info_list(self, messages: list[str], apply_formatting: bool = True) -> None:
    for message in messages:
      if apply_formatting:
        message = f" > {message}"
      self.add_info(message)

  # methods for interacting with enemies and the enemy grid
  ## visual

  # actual combat stuff
  def begin_combat(self) -> None:
    self.clear_info()
    self.reset_round_number()
    self.combat_interface.parry_used = False

    self.game_data.get_active_character().reset_health()

    equipables_messages: list[str] = self.effect_manager.apply_equipped_equipables_effects()
    self.add_info_list(equipables_messages)

    self.effect_manager.init_fighting_enemy_effects()

    self.combat_interface.update_health_label()
    self.combat_interface.update_damage_resistance_label()

    character_won: bool = self.play_round() # recursive function

    self.combat_interface.enable_return(character_won)
    self.effect_manager.remove_all_effects_from_active_character()

  def play_round(self) -> bool:
    """
    Handles the execution of each round in play.

    :return: `True` if the character succeeded, `False` if not.
    :rtype: bool
    """
    is_character_winner: Optional[bool] = self.has_character_won_combat()
    if is_character_winner != None: return is_character_winner # base_case
  
    self.add_round_start_info(self.round_number)

    self.start_character_turn()
    self.end_character_turn()

    self.start_enemies_turn()
    self.end_enemies_turn()

    self.increment_round_number()

    self.add_newline_info()
    return self.play_round() # recursive call

  ## character turn
  def start_character_turn(self) -> None:
    self.is_character_turn = True
    self.combat_interface.parry_used = False
    self.reset_remaining_actions()
    self.add_entity_turn_begin_info(character_turn=self.is_character_turn)

    self.effect_manager.decrement_character_effects_durations()
    self.effect_manager.remove_finished_effects_from_active_character()
    
    self.enable_user_buttons(include_confirm=True)
    self.combat_interface.reset_weapon_states()
    self.combat_interface.update_weapon_states()
    character_actions: list[CombatAction] = self.get_character_actions()

    for action in character_actions:
      self.actions.put(action)

  def get_character_actions(self) -> list[CombatAction]:
    character_action: CombatAction

    if self.remaining_actions == 0: return [] # base case
    self.add_remaining_actions_info()

    character_action = self.input_character_action()

    if type(character_action) == Parry:
      self.combat_interface.parry_used = True
    self.combat_interface.update_weapon_states()

    self.decrement_remaining_actions()
    return [character_action] + self.get_character_actions()

  def input_character_action(self) -> CombatAction:
    """Requires user to select the buttons they want before being called. Automatically untoggles user buttons after the user inputs a valid action (i.e. when the function returns)."""
    successful_input: bool = False
    while not successful_input:
      error_message_info: Optional[ErrorMessageInfo] = None
      try:
        character_action: CombatAction = self.combat_interface.get_character_action()
      except QuitInterrupt as error:
        raise error
      except UnknownActionError as error:
        raise error # this should never occur. If it does, then the program should properly raise the error
      except AbstractError as error:
        error_message_info = error.info()
      finally:
        if error_message_info == None:
          successful_input = True
        else:
          (error_type, error_message) = error_message_info
          self.add_action_input_error_info(error_type, error_message)

    self.reset_toggleable_user_buttons_state()
    return character_action

  def end_character_turn(self) -> None:
    self.is_character_turn = False

  ## enemies turn
  def start_enemies_turn(self) -> None:
    self.disable_user_buttons(include_confirm=True)
    self.add_entity_turn_begin_info(character_turn=self.is_character_turn)

    self.effect_manager.decrement_all_fighting_enemy_effects_durations()
    self.effect_manager.remove_finished_effects_from_all_fighting_enemies()

    enemies_actions: list[CombatAction] = self.get_enemies_actions()

    for action in enemies_actions:
      self.actions.put(action)

  def get_enemies_actions(self) -> list[CombatAction]:
    character: Character = self.game_data.get_active_character()
    character_remaining_ignition_duration: Optional[int] = self.effect_manager.get_entity_remaining_ignition_duration()
    is_character_parrying: bool = character.is_parrying
    (positive_character_total, character_n) = character.calculate_aggressiveness_info(character_remaining_ignition_duration, is_character_parrying)
    negative_character_total: float = -1*positive_character_total

    dimensions: Position = self.game_data.fighting_enemy_graph.dimensions

    enemies_actions: list[CombatAction] = []
    for i in range(len(self.game_data.fighting_enemy_graph)):
      position: Position = length_to_point(i, dimensions)
      fighting_enemy_id: Optional[int] = self.game_data.fighting_enemy_graph[position]
      if fighting_enemy_id == None: continue
      remaining_ignition_duration: Optional[int] = self.effect_manager.get_entity_remaining_ignition_duration(fighting_enemy_id)

      enemy_action: Optional[CombatAction] = self.get_fighting_enemy_action_at(position, remaining_ignition_duration, is_character_parrying, negative_character_total, character_n)
      if enemy_action == None: continue
      enemies_actions.append(enemy_action)
    return enemies_actions
  
  def get_fighting_enemy_action_at(self, position: Position, remaining_ignition_duration: Optional[int], is_target_parrying: bool, negative_character_total: float, character_n: int) -> Optional[CombatAction]:
    """
    :return: `None` if there is no enemy at the position, `CombatAction` otherwise.
    :rtype: Optional[CombatAction]
    """
    fighting_enemy_id: Optional[int] = self.game_data.fighting_enemy_graph[position]
    if fighting_enemy_id == None: return None
    fighting_enemy: FightingEnemy = self.game_data.fighting_enemies[fighting_enemy_id]

    fighting_enemy.calculate_aggressiveness(remaining_ignition_duration, is_target_parrying, negative_character_total, character_n)
    enemy_action_name: ActionName = fighting_enemy.choose_action_name()

    sender = EnemyType(fighting_enemy_id, position)

    target = self.get_enemy_target(fighting_enemy_id, position, enemy_action_name)

    action: ActionType = self.get_enemy_action_type(fighting_enemy, enemy_action_name)

    return CombatAction(sender, target, action)
  
  def get_enemy_target(self, fighting_enemy_id: int, position: Position, action_name: ActionName) -> Optional[EntityType]:
    if action_name == ActionName.ATTACK: return CharacterType()
    elif action_name == ActionName.HEAL: return EnemyType(fighting_enemy_id, position)
    raise ValueError(f"`{action_name=}` not recognised.")
  
  def get_enemy_action_type(self, fighting_enemy: FightingEnemy, action_name: ActionName) -> ActionType:
    """
    For a specific action name, the given fighting enemy's `ActionType` is returned, containing all required information for that action.
    
    :param fighting_enemy: The fighting enemy being operated on.
    :type fighting_enemy: FightingEnemy
    :param action_name: The name of the action being used. Must be one of `ATTACK` or `HEAL`.
    :type action_name: ActionName
    :return: The action information. Always one of `Attack` and `Heal`.
    :rtype: ActionType
    """
    # attacking
    if action_name == ActionName.ATTACK:
      # initialising attack
      attack_damage: float = fighting_enemy.attack_damage
      attack = Attack(attack_damage)
      # adding abilities
      attack_ability_id: Optional[int] = fighting_enemy.ability_id_table[ActionName.ATTACK]
      if attack_ability_id != None:
        attack_ability: Ability = self.game_data.abilities[attack_ability_id]
        attack_ability_action: AbilityAction = attack_ability.get_ability_action()
        attack.add_ability_action(attack_ability_action)
      return attack
    # healing
    if action_name == ActionName.HEAL:
      # initialising
      heal_ability_id: Optional[int] = fighting_enemy.ability_id_table.get(ActionName.HEAL)
      if heal_ability_id == None: raise ValueError(f"Tried to get `{action_name=}` for `{fighting_enemy=}` when no healing ability exists.")
      # adding ability
      heal_ability: Ability = self.game_data.abilities[heal_ability_id]
      heal_ability_action: AbilityAction = heal_ability.get_ability_action()
      if type(heal_ability_action) != HealAction: raise TypeError(f"`{heal_ability_action=}` not of type `HealAction`.")
      heal_amount: float = heal_ability_action.heal_amount
      return Heal(heal_amount)
    raise Exception(f"TODO: fix this ({fighting_enemy=}, {action_name=}).")

  def end_enemies_turn(self) -> None:
    self.execute_all_actions()
    self.effect_manager.inflict_active_effects_to_all_fighting_entities()
    self.remove_dead_fighting_enemies()
    self.combat_interface.display_enemy_info_on_grid()
    self.combat_interface.update_health_label()
    self.combat_interface.update_damage_resistance_label()
  
  def has_character_won_combat(self) -> Optional[bool]:
    if self.is_character_dead():
      return False
    if self.is_all_enemies_dead():
      return True
    return None
  
  def is_character_dead(self) -> bool:
    if self.active_character_id == None: raise NoCharacterSelectedError()
    character: Character = self.fetch_active_character()
    if character.health <= 0: return True
    return False
  
  def is_all_enemies_dead(self) -> bool:
    return self.game_data.is_all_fighting_enemies_dead()
  
  def remove_fighting_enemy_at(self, position: Position) -> None:
    fighting_enemy_id: Optional[int] = self.game_data.fighting_enemy_graph[position]
    if fighting_enemy_id == None: raise ValueError(f"Cannot remove fighting enemy at {position=} when no fighting enemy exists there.")
    self.game_data.fighting_enemy_graph.clear_fighting_enemy_id(position)
    del self.game_data.fighting_enemies[fighting_enemy_id]

  def remove_dead_fighting_enemies(self) -> None:
    for i in range(len(self.game_data.fighting_enemy_graph)):
      position: Position = length_to_point(i, dimensions=self.game_data.fighting_enemy_graph.dimensions)
      fighting_enemy_id: Optional[int] = self.game_data.fighting_enemy_graph[position]
      if fighting_enemy_id == None: continue
      fighting_enemy: FightingEnemy = self.game_data.fighting_enemies[fighting_enemy_id]
      if fighting_enemy.health > 0: continue
      self.remove_fighting_enemy_at(position)

  # action execution

  def get_next_action(self) -> CombatAction:
    return self.actions.get()

  def execute_next_action(self) -> list[str]:
    """
    Pops the next action from `self.actions` and executes it.

    :returns: The information from the action to be printed to the console.
    :rtype: str
    """
    next_action: CombatAction = self.get_next_action()
    sender_type: EntityType = next_action.sender_type
    sender: FightingEntity = unpack_optional(self.fetch_referenced_entity(sender_type))
    target_type: Optional[EntityType] = next_action.target_type
    target: Optional[FightingEntity] = self.fetch_referenced_entity(target_type)

    action_information: list[str] = [next_action(sender, target)] # action function is executed here

    action_type: ActionType = next_action.action_type
    if type(action_type) == Parry:
      damage_threshold: float = action_type.quantity
      reflection_proportion: float = action_type.reflect_proportion
      parry_action = ParryAction(damage_threshold=damage_threshold, reflection_proportion=reflection_proportion)
      if type(sender) == Character:
        action_information.append(self.effect_manager.apply_ability_action_to_active_character(parry_action))
      # no branch for enemies as they cannot parry
    return action_information

  def execute_all_actions(self) -> None:
    """Gets and inflicts all actions in `self.actions`, both to the player and active fighting enemies. Doesn't decrement active effects."""
    while not self.actions.empty():
      action_information: list[str] = self.execute_next_action()
      self.add_info_list(action_information)

  def fetch_referenced_entity(self, entity_type: Optional[EntityType]) -> Optional[FightingEntity]:
    if entity_type == None: return entity_type
    if type(entity_type) == CharacterType: return self.fetch_active_character()
    enemy_type = cast(EnemyType, entity_type)
    fighting_enemy_position: Position = enemy_type.position
    return self.fetch_fighting_enemy_at(fighting_enemy_position)
    
  def fetch_active_character(self) -> Character:
    return self.game_data.get_active_character()
  
  def fetch_fighting_enemy_at(self, position: Position) -> Optional[FightingEnemy]:
    #if position == None: raise ValueError(f"Enemy location at \'position\'=`{position}` cannot be \'None\'")
    return self.game_data.get_fighting_enemy_at(position)
  
  # misc functions
  def quit(self) -> None:
    logging.info("called")
    if not self.combat_interface.is_quitting: raise ValueError(f"\'self.quit()\' called when \'self.combat_interface.is_quitting\'=`{self.combat_interface.is_quitting}` (should be \'True\')")
    del self

EOF
combat_management/effect_manager.py

from tools.typing_tools import *
from tools.ability_names import AbilityTypeName
from tools.constants import ItemType
from tools.dictionary_tools import filter_dictionary
from tools.logging_tools import *

from game_data import GameData

from stored.entities.character import Character
from stored.entities.fighting_enemy import FightingEnemy

from stored.items.item import Item
from stored.items.inventory_item import InventoryItem
from stored.items.weapon import Weapon
from stored.items.equipable import Equipable

from stored.abilities.ability import Ability
from stored.abilities.item_ability import ItemAbility
from stored.abilities.parry_ability import ParryAbility
from stored.abilities.statistic_ability import StatisticAbility

from ability_action import *

from combat_management.active_effect import ActiveEffect

class EffectManager:
  def __init__(self, game_data: GameData) -> None:
    self.game_data = game_data
    self.character_effects: list[ActiveEffect] = []
    self.fighting_enemy_effects: dict[int, list[ActiveEffect]] = {} # maps FightingEnemyID to the effects applied to them

  # preparations made at the start of combat

  def init_fighting_enemy_effects(self) -> None:
    self.fighting_enemy_effects.clear()
    for identifier in list(self.game_data.fighting_enemies.keys()):
      self.fighting_enemy_effects[identifier] = []

  # getting abilities

  def get_ability_identifiers_for(self, item_id: int) -> list[int]:
    item_abilities: dict[int, ItemAbility] = filter_dictionary(self.game_data.item_abilities, lambda _, item_ability: item_ability.item_id == item_id)
    ability_identifiers: list[int] = []
    for item_ability in list(item_abilities.values()):
      ability_identifiers.append(item_ability.ability_id)
    return ability_identifiers

  def get_abilities_for(self, item_id: int) -> list[Ability]:
    ability_identifiers: list[int] = self.get_ability_identifiers_for(item_id)
    abilities: dict[int, Ability] = filter_dictionary(self.game_data.abilities, lambda identifier, _: identifier in ability_identifiers)
    return list(abilities.values())
  
  def get_parry_ability(self, ability_id: int) -> ParryAbility:
    parry_abilities: dict[int, ParryAbility] = filter_dictionary(self.game_data.parry_abilities, lambda _, parry_ability: parry_ability.ability_id == ability_id)
    if len(parry_abilities) == 0 or len(parry_abilities) > 1: raise ValueError(f"Multiple or no parry abilities ({parry_abilities=}) found for {ability_id=}.")
    return list(parry_abilities.values())[0]
  
  def get_defend_ability(self, ability_id: int) -> StatisticAbility:
    defend_abilities: dict[int, StatisticAbility] = filter_dictionary(self.game_data.statistic_abilities, lambda _, statistic_ability: statistic_ability.ability_id == ability_id and statistic_ability.ability_type == AbilityTypeName.DEFEND)
    if len(defend_abilities) == 0 or len(defend_abilities) > 1: raise ValueError(f"Multiple or no defend abilities ({defend_abilities=}) found for {ability_id=}.")
    return list(defend_abilities.values())[0]

  def get_weaken_ability(self, ability_id: int) -> StatisticAbility:
    weaken_abilities: dict[int, StatisticAbility] = filter_dictionary(self.game_data.statistic_abilities, lambda _, statistic_ability: statistic_ability.ability_id == ability_id and statistic_ability.ability_type == AbilityTypeName.WEAKEN)
    if len(weaken_abilities) == 0 or len(weaken_abilities) > 1: raise ValueError(f"Multiple or no weaken abilities ({weaken_abilities=}) found for {ability_id=}.")
    return list(weaken_abilities.values())[0]
  
  def ability_id_to_ability_action(self, ability_id: int) -> AbilityAction:
    ability_action: AbilityAction
    ability: Ability = self.game_data.abilities[ability_id]
    ability_type: AbilityTypeName = ability.ability_type
    match ability_type:
      case AbilityTypeName.IGNITE:
        ability_action = IgniteAction()
      case AbilityTypeName.PIERCE:
        ability_action = PierceAction()
      case AbilityTypeName.PARRY:
        parry: ParryAbility = self.get_parry_ability(ability_id)
        ability_action = ParryAction(damage_threshold=parry.damage_threshold, reflection_proportion=parry.reflection_proportion)
      case AbilityTypeName.DEFEND:
        defend: StatisticAbility = self.get_defend_ability(ability_id)
        ability_action = DefendAction(initial_duration=defend.initial_duration, resistance=defend.amount)
      case AbilityTypeName.WEAKEN:
        weaken: StatisticAbility = self.get_weaken_ability(ability_id)
        ability_action = WeakenAction(initial_duration=weaken.initial_duration, vulnerability=weaken.amount)
      case _: raise ValueError(f"Unknown value for {ability_type=} ({ability=}).")
    return ability_action
  
  def get_ability_actions_for(self, item_id: int) -> list[AbilityAction]: 
    ability_identifiers: list[int] = self.get_ability_identifiers_for(item_id)
    ability_actions: list[AbilityAction] = list(map(lambda ability_id: self.ability_id_to_ability_action(ability_id), ability_identifiers))
    return ability_actions

  def get_inventory_item_abilities(self, inventory_item_id: int) -> tuple[ItemType, list[AbilityAction]]:
    inventory_item: InventoryItem = self.game_data.inventory_items[inventory_item_id]
    item_id: int = inventory_item.item_id
    abilities: list[AbilityAction] = self.get_ability_actions_for(item_id)
    item: Item = self.game_data.items[item_id]
    item_type: ItemType = item.item_type
    return (item_type, abilities)

  def get_equipable_abilities(self, equipable_id: int) -> list[AbilityAction]:
    equipable: Equipable = self.game_data.equipables[equipable_id]
    item_id: int = equipable.item_id
    return self.get_ability_actions_for(item_id)

  def get_weapon_abilities(self, weapon_id: int) -> list[AbilityAction]:
    weapon: Weapon = self.game_data.weapons[weapon_id]
    item_id: int = weapon.item_id
    return self.get_ability_actions_for(item_id)
  
  # methods for getting characters and fighting enemies

  def get_active_character(self) -> Character:
    return self.game_data.get_active_character()
  
  def get_fighting_enemy(self, fighting_enemy_id: int) -> FightingEnemy:
    return self.game_data.fighting_enemies[fighting_enemy_id]
  
  # inflicting effects
  
  def ability_action_to_active_effect(self, ability_action: AbilityAction) -> ActiveEffect:
    duration: Optional[int] = ability_action.initial_duration
    new_effect = ActiveEffect(duration, ability_action)
    return new_effect

  ## character
  def apply_ability_action_to_active_character(self, ability_action: AbilityAction) -> str:
    """
    :returns: Message to be added to the info box by `CombatManager`.
    :rtype: str
    """
    character: Character = self.get_active_character()
    message: str = character.apply_ability(ability_action)
    new_effect: ActiveEffect = self.ability_action_to_active_effect(ability_action)
    self.character_effects.append(new_effect)
    return message

  def apply_ability_action_list_to_active_character(self, ability_actions: list[AbilityAction]) -> list[str]:
    messages: list[str] = []
    for ability_action in ability_actions:
      next_message: str = self.apply_ability_action_to_active_character(ability_action)
      messages.append(next_message)
    return messages

  def apply_equipped_equipables_effects(self) -> list[str]:
    messages: list[str] = []
    character_inventory_items: dict[int, InventoryItem] = self.game_data.get_character_inventory_items()
    for (inventory_item_id, inventory_item) in character_inventory_items.items():
      (item_type, item_ability_actions) = self.get_inventory_item_abilities(inventory_item_id)
      if item_type != ItemType.EQUIPABLE: continue # must be an equipable
      if not inventory_item.equipped: continue # must be equipped
      item_messages: list[str] = self.apply_ability_action_list_to_active_character(item_ability_actions)
      messages += item_messages
    return messages

  ## fighting enemies
  def apply_effect_to_fighting_enemy_with_identifier(self, fighting_enemy_id: int, ability_action: AbilityAction) -> str:
    fighting_enemy: FightingEnemy = self.get_fighting_enemy(fighting_enemy_id)
    message: str = fighting_enemy.apply_ability(ability_action)
    new_effect: ActiveEffect = self.ability_action_to_active_effect(ability_action)
    self.fighting_enemy_effects[fighting_enemy_id].append(new_effect)
    return message

  # applying and decrementing effects in the course of combat

  def inflict_active_effects_to_all_fighting_entities(self) -> list[str]:
    messages: list[str] = []
    character: Character = self.get_active_character()
    character.inflict_active_effects()
    self.decrement_character_effects_durations()
    for fighting_enemy in list(self.game_data.fighting_enemies.values()):
      message: str = fighting_enemy.inflict_active_effects()
      messages.append(message)
    self.decrement_all_fighting_enemy_effects_durations()
    return messages

  ## character
  def decrement_character_effects_durations(self) -> None:
    for active_effect in self.character_effects:
      if active_effect.is_permanent(): continue
      active_effect.decrement_remaining_turns()
  
  ## fighting enemies
  def decrement_fighting_enemy_effects_durations(self, fighting_enemy_id: int) -> None:
    specific_fighting_enemy_effects: list[ActiveEffect] = self.fighting_enemy_effects[fighting_enemy_id]
    for active_effect in specific_fighting_enemy_effects:
      if active_effect.is_permanent(): continue
      active_effect.decrement_remaining_turns()

  def decrement_all_fighting_enemy_effects_durations(self) -> None:
    for fighting_enemy_id in list(self.fighting_enemy_effects.keys()):
      self.decrement_fighting_enemy_effects_durations(fighting_enemy_id)

  # removing effects
  ## character
  def remove_effect_from_active_character(self, ability_action: AbilityAction) -> str:
    """Doesn't remove the effect from `self.character_effects`."""
    character: Character = self.get_active_character()
    return character.remove_ability(ability_action)

  def remove_finished_effects_from_active_character(self) -> list[str]:
    messages: list[str] = []
    for (i, active_effect) in enumerate(self.character_effects):
      if active_effect.is_no_turns_remaining():
        self.character_effects.pop(i)
        ability_action: AbilityAction = active_effect.effect_ability
        message: str = self.remove_effect_from_active_character(ability_action)
        messages.append(message)
    return messages

  def remove_all_effects_from_active_character(self) -> None:
    for (i, active_effect) in enumerate(self.character_effects):
      self.character_effects.pop(i)
      ability_action: AbilityAction = active_effect.effect_ability
      self.remove_effect_from_active_character(ability_action)

  ## fighting enemies
  def remove_effect_from_fighting_enemy_with_identifier(self, fighting_enemy_id: int, ability_action: AbilityAction) -> str:
    """Doesn't remove the effect from `self.fighting_enemy_effects`."""
    fighting_enemy: FightingEnemy = self.get_fighting_enemy(fighting_enemy_id)
    return fighting_enemy.remove_ability(ability_action)

  def remove_finished_effects_from_fighting_enemy_with_identifier(self, fighting_enemy_id: int) -> list[str]:
    messages: list[str] = []
    specific_fighting_enemy_effects: list[ActiveEffect] = self.fighting_enemy_effects[fighting_enemy_id]
    for (i, active_effect) in enumerate(specific_fighting_enemy_effects):
      if active_effect.is_no_turns_remaining():
        self.fighting_enemy_effects[fighting_enemy_id].pop(i)
        ability_action: AbilityAction = active_effect.effect_ability
        message: str = self.remove_effect_from_fighting_enemy_with_identifier(fighting_enemy_id, ability_action)
        messages.append(message)
    return messages

  def remove_finished_effects_from_all_fighting_enemies(self) -> None:
    for fighting_enemy_id in list(self.fighting_enemy_effects.keys()):
      self.remove_finished_effects_from_fighting_enemy_with_identifier(fighting_enemy_id)

  # getting effects

  def get_entity_remaining_ignition_duration(self, fighting_enemy_id: Optional[int] = None) -> Optional[int]:
    effects: list[ActiveEffect] = []
    if fighting_enemy_id == None:
      effects = self.character_effects
    else:
      logging.debug(f"{self.fighting_enemy_effects=}")
      effects = self.fighting_enemy_effects[fighting_enemy_id]
    is_ignite_ability: Callable[[ActiveEffect], bool] = lambda effect: effect.effect_ability.get_ability_type_name() == AbilityTypeName.IGNITE
    ignition_effects: list[ActiveEffect] = list(filter(lambda effect: is_ignite_ability(effect), effects))
    if len(ignition_effects) == 0: return None
    elif len(ignition_effects) == 1:
      ignition_duration: Optional[int] = ignition_effects[0].turns_remaining
      if ignition_duration == None: raise ValueError(f"`{ignition_effects[0]=}` has `{ignition_duration=}`, which cannot be `None`.")
      return ignition_duration
    raise BufferError(f"Multiple ignition effects found: `{ignition_effects=}`.") # TODO: edit effect application to make it impossible to have multiple ignitions applied at once 

EOF
combat_management/__init__.py

__all__ = ["active_effect", "combat_manager", "effect_manager"]

from . import active_effect
from . import combat_manager
from . import effect_manager

EOF
ability_action.py

from tools.typing_tools import *
from tools.constants import Constants
from tools.ability_names import AbilityTypeName

#from stored.abilities.ability import Ability

@dataclass
class AbilityAction():
  """Abstract base class for all ability actions.
  
  Subclasses of `ParryAction`, `IgniteAction`, `DefendAction`, `WeakenAction`, `HealAction` and `PierceAction`."""
  initial_duration: Optional[int]

  def get_ability_type_name(self) -> AbilityTypeName: raise NotImplementedError()

@dataclass
class IgniteAction(AbilityAction):
  """Ignites the target, dealing a set amount of damage for a set amount of turns."""
  initial_duration: int = Constants.IGNITE_DURATION

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.IGNITE

@dataclass
class PierceAction(AbilityAction):
  """Pierce attacks will ignore parries."""
  initial_duration: int = 1

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.PIERCE

@dataclass
class ParryAction(AbilityAction):
  damage_threshold: float = 0
  reflection_proportion: float = 0
  initial_duration: int = 1

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.PARRY

  @staticmethod
  def get_reflected_damage(damage: float, reflection_proportion: float) -> float:
    if reflection_proportion > 1: raise ValueError(f"{reflection_proportion=} cannot be less than `1`.")
    return damage * (1-reflection_proportion)

  @staticmethod
  def parry_damage(damage: float, damage_threshold: float, reflection_proportion: float) -> tuple[float, float]:
    """
    :return: A pair of floats. The first is the amount of damage inflicted to the target. The second is the amount of damage reflected back to the attacker.
    :rtype: tuple[float, float]
    """
    target_damage: float
    if damage <= damage_threshold:
      target_damage = 0
    else:
      target_damage = damage - damage_threshold
    
    reflected_damage: float = ParryAction.get_reflected_damage(damage, reflection_proportion)

    return (target_damage, reflected_damage)

@dataclass
class DefendAction(AbilityAction):
  """Increases damage resistance."""
  resistance: float = 0

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.DEFEND

@dataclass
class WeakenAction(AbilityAction):
  """Increases damage vulnerability (inverse of `DefendAction`)."""
  vulnerability: float = 0

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.WEAKEN

@dataclass
class HealAction(AbilityAction):
  initial_duration: int = 1
  heal_amount: float = 0

  def get_ability_type_name(self) -> AbilityTypeName: return AbilityTypeName.HEAL

EOF
app.py

from tools.typing_tools import *
from tools.logging_tools import *
from tools.constants import *

from database.condition import Condition, nothing

from interface.interface import Interface
from interface.combat_interface import CombatInterface

from game_data import GameData
from combat_management.combat_manager import CombatManager

from stored.entities.character import Character
from stored.world import World
from stored.items.storage import Storage

class App:
  def __init__(self) -> None:
    self.game_data = GameData()
    self.game_data.load_game_data()

    interface_init_options: dict[str, Any] = {
      "quit_command": self.quit_command,
      "return_command": self.show_screen,
      "select_character": self.select_character,
      "begin_character_creation": self.begin_character_creation,
      "create_character": self.create_character,
      "select_world": self.select_world,
      "begin_world_creation": self.begin_world_creation,
      "create_world": self.create_world,
      "open_storage": self.open_storage,
      "go_exploring": self.go_exploring,
      "begin_combat": self.begin_combat,
      "end_combat": self.end_combat,
      "enter_structure": self.enter_structure, 
      "leave_structure": self.leave_structure,
    }

    self.interface = Interface(self.game_data, **interface_init_options)

    combat_interface: CombatInterface = self.interface.get_combat_interface()
    self.combat_manager = CombatManager(self.game_data, combat_interface)

    logging.info("App initialisation complete")

  def __del__(self) -> None:
    self.save()
    del self.game_data
    del self.interface
    del self.combat_manager

  def show_screen(self, screen_name: ScreenName, **kwargs) -> None:
    self.interface.show_screen(screen_name, **kwargs)

  @log_all
  def select_character(self, character_id: int) -> None:
    self.game_data.active_character_id = character_id
    character_name: str = self.game_data.get_character_name()
    self.interface.update_character_name(character_name)
    self.show_screen(ScreenName.WORLD_SELECTION)

  def create_character(self, character_name: str) -> None:
    active_user_id: int = unpack_optional(self.game_data.active_user_id)
    self.game_data.users[active_user_id].character_quantity += 1
    max_health: float = Character.get_default_max_health()
    character_identifier: int = self.game_data.insert_character([active_user_id, character_name, max_health, max_health])
    self.select_character(character_identifier)
    self.interface.show_screen(ScreenName.WORLD_SELECTION)

  def begin_character_creation(self, _kwargs: dict[str, Any] = {}) -> None:
    self.show_screen(ScreenName.CHARACTER_CREATION)

  def select_world(self, world_identifier: int) -> None:
    self.game_data.active_world_id = world_identifier
    # selecting relevant storages (1 for home, 1 for away)
    find_world_storages: Callable[[StorageType], Condition] = lambda storage_type: Condition(lambda _, row: row[0] == world_identifier and row[1] == storage_type)
    # storage at home
    home_storages: dict[int, Storage] = self.game_data.select_from_storage(self.game_data.storages, find_world_storages(StorageType.HOME))
    if len(home_storages) != 1: raise Exception(f"{home_storages=} should have 1 element; {len(home_storages)} were found.")
    self.game_data.home_storage = list(home_storages.keys())[0]
    # storage for away
    away_storages: dict[int, Storage] = self.game_data.select_from_storage(self.game_data.storages, find_world_storages(StorageType.CHEST))
    if len(away_storages) != 1: raise Exception(f"{away_storages=} should have 1 element; {len(away_storages)} were found.")
    self.game_data.away_storage = list(away_storages.keys())[0]

    self.go_home()

  def go_home(self, screen_name: ScreenName = ScreenName.HOME, **kwargs) -> None:
    self.game_data.active_storage_id = self.game_data.home_storage
    self.show_screen(screen_name)

  def begin_world_creation(self, _kwargs: dict[str, Any] = {}) -> None:
    self.show_screen(ScreenName.WORLD_CREATION, world=self.game_data.worlds)

  def create_world(self, world_name: str, world_seed: str) -> None:
    active_user_id: int = unpack_optional(self.game_data.active_user_id)
    self.game_data.users[active_user_id].world_quantity += 1
    world_identifier: int = self.game_data.insert_world([active_user_id, world_name, world_seed])
    identical_condition = nothing()
    self.game_data.insert_stored(Storage, [world_identifier, StorageType.HOME], identical_condition, StorageAttrName.STORAGES)
    self.game_data.insert_stored(Storage, [world_identifier, StorageType.CHEST], identical_condition, StorageAttrName.STORAGES)
    self.select_world(world_identifier)

  def load_active_weapons(self) -> list[int]:
    return list(self.game_data.weapons.keys())
  
  def get_weapon_name(self, weapon_id: int) -> str:
    return self.game_data.get_weapon_name(weapon_id)
  
  def open_storage(self) -> None:
    self.show_screen(ScreenName.STORAGE)

  def go_exploring(self) -> None:
    self.game_data.active_storage_id = self.game_data.away_storage
    self.show_screen(ScreenName.EXPLORATION)

  def begin_combat(self) -> None:
    self.game_data.generate_fighting_enemies()
    self.show_screen(ScreenName.COMBAT)
    self.combat_manager.begin_combat()

  def end_combat(self, screen_name: ScreenName) -> None:
    self.game_data.finish_combat_encounter()
    self.show_screen(screen_name)

  def enter_structure(self) -> None:
    self.game_data.encounter_structure()
    self.open_storage()

  def leave_structure(self, screen_name: ScreenName = ScreenName.EXPLORATION) -> None:
    self.game_data.finish_structure_encounter()
    self.show_screen(screen_name)

  def save(self) -> None:
    self.game_data.save()
    del self.game_data

  def run(self) -> None:
    options: dict[str, Any] = {"characters": self.game_data.characters}
    self.interface.run(**options)

  def quit_command(self, successfully: bool = True) -> None:
    self.save()
    if successfully: quit()
    quit(1)

EOF
combat_action.py

import logging

from tools.typing_tools import *

from ability_action import AbilityAction
from data_structures.action_type import *
from data_structures.entity_type import *

from stored.entities.fighting_entity import FightingEntity

def only_for_attacks[ReturnType](func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
  def wrapper(self, *args, **kwargs) -> ReturnType:
    if type(self.action_type) != Attack: raise TypeError(f"Cannot apply method to `{type(self.action_type)=}` not of type `Attack`.")
    return func(self, *args, **kwargs)
  return wrapper

class CombatAction():
  """
  Represents a single action taken in combat. All methods handle attacks on individual entities.

  :param sender_type: The entity who made the action.
  :type sender_type: EntityType
  :param target_type: The entity who will receive the action. Is `None` in the case of a parry.
  :type target_type: Optional[EntityType]
  :param action_type: What action is being carried out.
  :type action_type: ActionType
  """
  def __init__(self, sender_type: EntityType, target_type: Optional[EntityType], action_type: ActionType) -> None:
    self.sender_type: EntityType = sender_type
    self.target_type: Optional[EntityType] = target_type
    self.action_type: ActionType = action_type

  # built-in methods

  def __repr__(self) -> str:
    return f"ACTION {self.action_type}\n  [ {self.sender_type} -> {self.target_type} ]"

  def __call__(self, sender: FightingEntity, target: Optional[FightingEntity]) -> str:
    type_of_action: Type[ActionType] = type(self.action_type)
    if type_of_action == Attack: return self.attack_fighting_entity(sender, target)
    elif type_of_action == Parry: return f"{sender.name} parried" # parrying is handled in `CombatManager`
    elif type_of_action == Heal: return self.heal_fighting_entity(sender, target)
    else:
      raise TypeError(f"Action type `{type_of_action}` does not match with any known action types (\'Attack\', \'Parry\', \'Heal\')")
    
  # abilities and modifiers

  @only_for_attacks
  def add_ability_to_attack(self, ability: AbilityAction) -> None:
    if type(self.action_type) != Attack: raise TypeError(f"Cannot add abilities to `{type(self.action_type)=}`. Must be of type `Attack`.")
    return self.action_type.add_ability_action(ability)
  
  @only_for_attacks
  def add_abilities_to_attack(self, abilities: Queue[AbilityAction]) -> None:
    if type(self.action_type) != Attack: raise TypeError(f"Cannot add abilities to `{type(self.action_type)=}`. Must be of type `Attack`.")
    next_ability: AbilityAction
    while not abilities.empty():
      next_ability = abilities.get()
      self.add_ability_to_attack(next_ability)

  @only_for_attacks
  def apply_next_ability_to(self, recipient: FightingEntity) -> None:
    if type(self.action_type) != Attack: return # this never evaluates to true; if the action were not an attack, the `only_for_attacks` decorator would've caught it and raised an error
    next_ability: AbilityAction = self.action_type.get_next_ability()
    recipient.apply_ability(next_ability)

  # action methods

  def apply_abilities(self) -> None: raise NotImplementedError()

  def attack_fighting_entity(self, sender: FightingEntity, target: Optional[FightingEntity]) -> str:
    if type(self.action_type) != Attack:
      raise TypeError(f"Expected type `Attack` for `type(self.action_type)`; got `{type(self.action_type)=}` instead.")
    if target == None:
      return f"{sender.name.upper()} attacked nothing."
    damage: float = self.action_type.quantity
    message: str = f"{sender.name.upper()} attacked {target.name.upper()} ({damage}DMG)"
    if target.is_parrying:
      parry_damage_threshold: Optional[float] = target.parry_damage_threshold
      parry_reflection_proportion: Optional[float] = target.parry_reflection_proportion
      if parry_damage_threshold == None or parry_reflection_proportion == None:
        raise ValueError(f"One of {parry_damage_threshold=} and/or {parry_reflection_proportion=} is `None`; both should be defined.")
      (damage, reflected_damage) = ParryAction.parry_damage(damage, parry_damage_threshold, parry_reflection_proportion)
      sender.take_damage(reflected_damage)
    target.take_damage(damage)
    return message

  def heal_fighting_entity(self, sender: FightingEntity, target: Optional[FightingEntity]) -> str:
    if type(self.action_type) != Heal:
      raise TypeError(f"Expected type `Heal` for `type(self.action_type)`; got `{type(self.action_type)=}` instead.")
    healing: float = self.action_type.quantity
    if target == None:
      return f"{sender.name.upper()}: healed nothing"
    return target.heal(healing)

EOF
game_data.py

from tools.typing_tools import *
from tools.logging_tools import *
from tools.constants import *
from tools.dictionary_tools import filter_dictionary, get_next_available_identifier
from tools.generation_tools import *
from tools.ability_names import *

from database.database import Database
from database.condition import Condition, everything, nothing, matching_identifiers

from stored.stored import Stored
from stored.user import User
from stored.entities.character import Character
from stored.modifiers.character_modifier import CharacterModifier
from stored.world import World

from stored.items.item import Item
from stored.items.inventory_item import InventoryItem
from stored.items.weapon import Weapon
from stored.items.equipable import Equipable
from stored.items.storage import Storage
from stored.items.storage_item import StorageItem

from stored.abilities.ability import Ability
from stored.abilities.parry_ability import ParryAbility
from stored.abilities.statistic_ability import StatisticAbility
from stored.abilities.item_ability import ItemAbility
from stored.abilities.enemy_ability import EnemyAbility

from data_structures.fighting_enemy_graph import FightingEnemyGraph
from custom_tkinter.toggleable_button import ToggleableButton
from stored.entities.enemy import Enemy
from stored.entities.fighting_enemy import FightingEnemy
from stored.modifiers.fighting_enemy_modifier import FightingEnemyModifier

from data_structures.queue import Queue

class GameData:
  def __init__(self) -> None:
    self.save_on_delete: bool = True # determines whether the current state of the database will be saved once it is deleted

    self.database = Database("game_data")

    self.users: dict[int, User] = {}
    self.active_user_id: Optional[int] = 0 # defaults as 0

    self.characters: dict[int, Character] = {}
    self.active_character_id = None
    self.character_modifiers: dict[int, CharacterModifier] = {}

    self.worlds: dict[int, World] = {}
    self.active_world_id: Optional[int] = None

    self.items: dict[int, Item] = {}
    self.inventory_items: dict[int, InventoryItem] = {}

    self.storages: dict[int, Storage] = {}
    self.storage_items: dict[int, StorageItem] = {}
    self.active_storage_id: Optional[int] = None # placeholder, TODO: set default value to `None`
    self.home_storage: Optional[int] = None
    self.away_storage: Optional[int] = None

    self.weapons: dict[int, Weapon] = {}
    self.equipables: dict[int, Equipable] = {}

    self.enemies: dict[int, Enemy] = {}
    self.fighting_enemies: dict[int, FightingEnemy] = {}
    self.fighting_enemy_graph = FightingEnemyGraph()
    self.fighting_enemy_modifiers: dict[int, FightingEnemyModifier] = {}
    self.enemy_abilities: dict[int, EnemyAbility] = {}

    self.abilities: dict[int, Ability] = {}
    self.parry_abilities: dict[int, ParryAbility] = {}
    self.statistic_abilities: dict[int, StatisticAbility] = {}

    self.item_abilities: dict[int, ItemAbility] = {}

    # Each entry contains target type as the key with a tuple as the value
    # The first element is the variable name to which the `Stored` type should be stored in within the `GameData` object
    # The next element is a boolean value denoting whether that target will be saved or loaded to the database as well
    self.save_load_targets: dict[type[Stored], Union[StorageAttrName, tuple[StorageAttrName, bool]]] = { 
      User: StorageAttrName.USERS,
      Character: StorageAttrName.CHARACTERS,
      CharacterModifier: (StorageAttrName.CHARACTER_MODIFIERS, False),

      World: StorageAttrName.WORLDS,

      Item: StorageAttrName.ITEMS,
      InventoryItem: StorageAttrName.INVENTORY_ITEMS,
      Weapon: StorageAttrName.WEAPONS,
      Equipable: StorageAttrName.EQUIPABLES,

      Storage: StorageAttrName.STORAGES,
      StorageItem: StorageAttrName.STORAGE_ITEMS,

      Enemy: StorageAttrName.ENEMIES,
      FightingEnemy: (StorageAttrName.FIGHTING_ENEMIES, False),
      FightingEnemyModifier: (StorageAttrName.FIGHTING_ENEMY_MODIFIERS, False),
      EnemyAbility: StorageAttrName.ENEMY_ABILITIES,

      Ability: StorageAttrName.ABILITIES,
      ParryAbility: StorageAttrName.PARRY_ABILITIES,
      StatisticAbility: StorageAttrName.STATISTIC_ABILITIES,
      ItemAbility: StorageAttrName.ITEM_ABILITIES,
    }

    self.table_templates: dict[TableName, list[str]] = { # comments next to templates indicate whether each has been given their own storage variables in `GameData`
      TableName.USER: ["UserID", "Name", "PasswordHash", "CharacterQuantity", "WorldQuantity"], # Y
      TableName.CHARACTER: ["CharacterID", "UserID", "Name", "Health", "MaxHealth"], # Y
      TableName.WORLD: ["WorldID", "UserID", "Name", "Seed"], # Y
      TableName.INVENTORY_ITEM: ["InventoryItemID", "CharacterID", "ItemID", "StackSize", "Equipped"], # Y
      TableName.STORAGE: ["StorageID", "WorldID", "StorageType"], # Y
      TableName.STORAGE_ITEM: ["StorageItemID", "StorageID", "ItemID", "StackSize"], # Y

      TableName.ITEM: ["ItemID", "ItemType", "Name"], # Y
      TableName.ITEM_ABILITY: ["ItemAbilityID", "ItemID", "AbilityID"], # Y
      TableName.WEAPON: ["WeaponID", "ItemID", "Damage", "UsesAmmunition", "ManaUsed", "Active"], # Y
      TableName.EQUIPABLE: ["EquipableID", "ItemID"], # Y
      TableName.ABILITY: ["AbilityID", "Text", "Type"], # Y
      TableName.PARRY_ABILITY: ["ParryAbilityID", "AbilityID", "DamageThreshold", "ReflectionProportion"], # Y
      TableName.STATISTIC_ABILITY: ["StatisticAbilityID", "AbilityID", "AbilityType", "Amount", "InitialDuration"], # Y
      TableName.ENEMY: ["EnemyID", "Name", "MaxHealth", "AttackDamage", "Intelligence", "IsBoss"], # Y
      TableName.ENEMY_ABILITY: ["EnemyAbilityID", "EnemyID", "AbilityID", "IsUsedInAttack"], # Y
    }

  # built-in methods

  def __del__(self) -> None:
    if self.save_on_delete:
      self.finish_combat_encounter()
      self.finish_structure_encounter()
      self.save()

  def __getitem__(self, storage_name: StorageAttrName) -> Any:
    return getattr(self, str(storage_name))
  
  # getter and setter methods

  @property
  def active_character_id(self) -> Optional[int]:
    return self.__active_character_id
  
  @active_character_id.setter
  def active_character_id(self, identifier: Optional[int]) -> None:
    if type(identifier) != int and identifier != None: raise TypeError(f"{identifier=} with type {type(identifier)} is not `int` or `None`.")
    self.__active_character_id = identifier

  # database and data loading methods

  def database_exists(self) -> bool:
    """Determines whether the database has already been created in memory or not by calling the \'self.database.exists()\' method."""
    return self.database.exists()

  def load_database(self) -> None:
    """Calls \'self.database.load()\'"""
    self.database.load()

  def load_game_data(self) -> None:
    """Called only once: by parent `App` after being initialised. Loads the database into memory, creating it if it doesn't already exist in storage. If the database doesn't already exist in storage, some default data is created."""
    database_exists: bool = self.database_exists()
    if not database_exists:
      self.init_database_main() # creates a database with an empty `MAIN.toml` file.
      self.load_default_data() # default data is loaded into `GameData` memory ONLY.
    existing_table_names: list[str] = self.database.load_main_data()
    self.load_database()
    self.create_tables(existing_table_names) 
    self.save()
    self.load()
    logging.debug(f"{self.characters}")
  
  def init_database_main(self, table_names: list[str] = []) -> None:
    """
    Called when no database exists in order to create a new one for use. Only creates the `MAIN.toml` file.
    
    :param table_names: The names of the tables which are to be created.
    :type table_names: list[str]
    """
    self.database.create_main(table_names)
    self.save()

  def load_default_data(self) -> None:
    """Loads data into `self` after a new database has been initialised."""
    self.users = {0: User("User", "1234", loaded=False)}
    self.items = {
      0: Item(ItemType.WEAPON, "Bronze sword", loaded=False),
      1: Item(ItemType.WEAPON, "Mace", loaded=False),
      2: Item(ItemType.WEAPON, "Dagger", loaded=False),
    }
    self.weapons = {
      0: Weapon(0, 10, loaded=False),
      1: Weapon(1, 15, loaded=False),
      2: Weapon(2, 5, loaded=False),
    }
    self.equipables = {

    }
    self.inventory_items = {
      0: InventoryItem(0, 0, 1, True, loaded=False),
      1: InventoryItem(0, 1, 1, True, loaded=False),
      2: InventoryItem(0, 2, 1, True, loaded=False),
    }
    self.enemies = {
      0: Enemy("Shep", 5, 1, 0.1, False),
      1: Enemy("Skeleton", 10, 5, 0.5, False),
    }
    self.abilities = {
      0: Ability("Small heal", AbilityTypeName.HEAL),
      1: Ability("Moderate heal", AbilityTypeName.HEAL),
      2: Ability("Significant heal", AbilityTypeName.HEAL),
    }
    self.statistic_abilities = {
      0: StatisticAbility(0, AbilityTypeName.HEAL, 10, 1),
      1: StatisticAbility(1, AbilityTypeName.HEAL, 20, 1),
      2: StatisticAbility(2, AbilityTypeName.HEAL, 30, 1),
    }


  def create_tables(self, existing_table_names: list[str]) -> None:
    for (table_name, table_columns) in self.table_templates.items():
      if not table_name in existing_table_names:
        self.database.create_table(table_name, table_columns)

  def select_from_table(self, table_name: TableName, columns: list[Any], condition: Condition) -> dict[int, list[Any]]:
    return self.database.select(table_name, columns, condition)
  
  def select_all_from_table(self, table_name: TableName) -> dict[int, list[Any]]:
    return self.select_from_table(table_name, ["*"], everything())
  
  def load_stored_from_database[StoredType: Stored](self, stored_type: Type[StoredType]) -> dict[int, StoredType]:
    entities: dict[int, StoredType] = {} # type `StoredType` is a generic which can take any type, as long as it is a subtype of `Stored`
    table_name: TableName = stored_type.get_table_name()
    raw_stored_data: dict[int, list[Any]] = self.select_all_from_table(table_name)
    for (identifier, stored_data) in raw_stored_data.items():
      stored: StoredType = cast(StoredType, stored_type.instantiate(stored_data, True))
      entities[identifier] = stored
    return entities
  
  @staticmethod
  def get_save_load_storage_options(storage_options: Union[StorageAttrName, tuple[StorageAttrName, bool]]) -> tuple[StorageAttrName, bool]:
    storage_name: StorageAttrName # can be anything, so there is no default value
    is_in_database: bool = True # defaults to true as this is the most common case
    if type(storage_options) == StorageAttrName:
      storage_name = storage_options
    elif type(storage_options) == tuple and len(storage_options) == 2:
      storage_name = storage_options[0]
      is_in_database = storage_options[1]
    else:
      raise TypeError(f"`{storage_options=}`, with `{type(storage_options)=}`, doesn't match with any expected type (`StorageAttrName`, `tuple[StorageAttrName, bool]`).")

    return (storage_name, is_in_database)

  def load(self) -> None:
    self.load_database()
    for (target, storage_options) in self.save_load_targets.items():
      (storage_name, is_in_database) = self.get_save_load_storage_options(storage_options)
      if not is_in_database: continue # skips if the target won't be saved to / loaded from the database
      setattr(self, storage_name, self.load_stored_from_database(target))

  def format_data_to_dictionary(self, table_name: TableName, raw_data: list) -> dict[str, Any]:
    formatted_data: dict[str, Any] = {}
    non_identifier_column_names: list[str] = self.database.find_table(table_name).get_non_identifier_column_names()
    for (i, column_name) in enumerate(non_identifier_column_names):
      try:
        formatted_data[column_name] = raw_data[i]
      except IndexError as e:
        raise IndexError(f"Trying to access '{raw_data=}' (`{len(raw_data)=}`) at index `{i=}` out of list range. `{table_name=}` (`Exception={e}`).")
    return formatted_data

  def update_database(self, table_name: TableName, raw_data: list[Any], condition: Condition) -> None:
    formatted_data: dict[str, Any] = self.format_data_to_dictionary(table_name, raw_data)
    self.database.update(table_name, formatted_data, condition)

  def update_database_record(self, table_name: TableName, identifier: int, raw_data: list[Any]) -> None:
    """
    Updates the fields of an existing record in the database. Only updates the database.
    
    :param table_name: The table to which the record will be updated.
    :type table_name: TableName
    :param identifier: The identifier of the record which is to be updated.
    :type identifier: int
    :param raw_data: The data which is to take the place of the existing data found in the database.
    :type raw_data: list[Any]
    """
    match_condition = Condition(lambda id, _row: id == identifier) 
    self.update_database(table_name, raw_data, match_condition)

  def insert_into_database(self, table_name: TableName, raw_data: list[Any], identifier: Optional[int] = None) -> Optional[int]:
    """Inserts a new record into a table, returning the new value's identifier afterward."""
    formatted_data: dict[str, Any] = self.format_data_to_dictionary(table_name, raw_data)
    return self.database.insert(table_name, formatted_data, identifier)
  
  def insert_into_storage[StoredType: Stored](self, storage_name: StorageAttrName, identifier: int, data: StoredType) -> None:
    """Inserts a record into the storage attribute in `self` whose name matches the one given."""
    storage: dict[int, StoredType] = getattr(self, storage_name)
    if identifier in storage: raise IndexError(f"Tried to insert {data=} with {identifier=} into {storage_name=} when the index is already being used {storage[identifier]=}.")
    storage[identifier] = data
    setattr(self, storage_name, storage)
  
  def is_stored_unique_in_table(self, table_name: TableName, identical_condition: Condition) -> bool:
    identifier_column: str = table_name + "ID"
    identical_identifiers: list[int] = list(self.select_from_table(table_name, [identifier_column], identical_condition).keys())
    if len(identical_identifiers) > 0: return False
    return True
    
  def select_from_storage[StoredType: Stored](self, storage: dict[int, StoredType], condition: Condition) -> dict[int, StoredType]:
    return {identifier: stored for identifier, stored in storage.items() if condition.evaluate(identifier, stored.get_raw_data())}

  def is_stored_unique_in_self[StoredType: Stored](self, storage_name: StorageAttrName, identical_condition: Condition) -> bool:
    storage: dict[int, StoredType] = getattr(self, storage_name)
    identical_identifiers: list[int] = list(self.select_from_storage(storage, identical_condition).keys())
    if len(identical_identifiers) > 0: return False
    return True
  
  def is_stored_unique[StoredType: Stored](self, stored_type: Type[StoredType], storage_name: StorageAttrName, identical_condition: Condition) -> bool:
    table_name: TableName = stored_type.get_table_name()
    return self.is_stored_unique_in_table(table_name, identical_condition) and self.is_stored_unique_in_self(storage_name, identical_condition) # if either are false, then the stored must not be unique

  # returns the stored's identifier and the stored which was created
  def insert_stored[StoredType: Stored](self, stored_type: Type[StoredType], stored_data: list[Any], identical_condition: Condition, storage_name: StorageAttrName) -> tuple[int, StoredType]:
    """
    Inserts a record both into the database and the appropriate storage attribute in `self`. Automatically finds the next insertion point.
    
    :param stored_type: The type of object which is being inserted.
    :type stored_type: type[StoredType]
    :param stored_data: The raw data of a single `StoredType` object. Does not include the identifier of the object.
    :type stored_data: list[Any]
    :param identical_condition: What must be true if 2 objects are identical.
    :type identical_condition: Condition
    :param storage_name: The storage attribute of `self` which the created object will be stored at.
    :type storage_name: StorageAttrName
    :return: A tuple, with the first element being the stored identifier and the second element being the newly created object.
    :rtype: tuple[int, StoredType]
    """
    table_name: TableName = stored_type.get_table_name()
    new_stored: StoredType = cast(StoredType, stored_type.instantiate(stored_data))
    if not self.is_stored_unique(stored_type, storage_name, identical_condition):
      del new_stored
      raise Exception(f"stored object (type `{stored_type}`) with data `{stored_data}` already exists in table `{table_name}`.")
    identifier: int = get_next_available_identifier(getattr(self, storage_name)) # generates its own identifier instead of relying on the database to generate it
    logging.debug(f"{identifier=}, {stored_type=}, {stored_data=}")
    self.insert_into_database(table_name, stored_data, identifier)
    self.insert_into_storage(storage_name, identifier, new_stored)
    return (identifier, new_stored)

  def insert_user(self, raw_data: list[Any]) -> int:
    identical_condition = Condition(lambda _identifier, row: row[0] == raw_data[0]) # checks if user
    (identifier, _) = self.insert_stored(User, raw_data, identical_condition, StorageAttrName.USERS)
    return identifier

  def insert_character(self, raw_data: list[Any]) -> int:
    identical_condition = Condition(lambda _identifier, row: row[1] == raw_data[1])
    (identifier, _) = self.insert_stored(Character, raw_data, identical_condition, StorageAttrName.CHARACTERS)
    return identifier

  def insert_world(self, raw_data: list[Any]) -> int:
    identical_condition = Condition(lambda _identifier, row: row[1] == raw_data[1])
    (identifier, _) = self.insert_stored(World, raw_data, identical_condition, StorageAttrName.WORLDS)
    return identifier

  def save_stored[StoredType: Stored](self, stored_type: Type[StoredType], storage_name: StorageAttrName) -> None:
    """
    Saves from one variable in the `GameData` object to `Database`. Does not insert objects into their respective variables in `self`.
    
    :param self: Object the method is called on.
    :param stored_type: The object type that is to be saved, being a subclass of `StoredType`.
    :type stored_type: Type[StoredType]
    :param storage_name: Name of the variable being saved to memory.
    :type storage_name: StorageAttrName
    """
    storage: dict[int, StoredType] = getattr(self, storage_name)
    for (identifier, stored) in storage.items():
      table_name: TableName = stored_type.get_table_name()
      raw_data: list = stored.get_raw_data()
      if stored.loaded:
        self.update_database_record(table_name, identifier, raw_data)
      else:
        self.insert_into_database(table_name, raw_data)

  def save(self) -> None:
    """Saves all targeted data stored in memory (in \'self\') to the database."""
    for (target, storage_options) in self.save_load_targets.items():
      (storage_name, is_in_database) = self.get_save_load_storage_options(storage_options)
      if not is_in_database: continue # skips if not stored in database
      self.save_stored(target, storage_name)
    self.database.save()

  def delete_stored[StoredType: Stored](self, stored_type: Type[StoredType], identifier: int, storage_name: StorageAttrName) -> None:
    """Deletes a specific value from both the appropriate storage attribute in \'self\' and the subsequent table in \'Database\'."""
    # deleting from 'self'
    updated_storage: dict[int, StoredType] = getattr(self, storage_name)
    del updated_storage[identifier]
    setattr(self, storage_name, updated_storage)
    # deleting from 'Database'
    table_name: TableName = stored_type.get_table_name()
    condition: Condition = matching_identifiers(identifier)
    self.database.delete_from(table_name, condition)

  # user methods

  def set_active_user(self, user: User) -> None:
    self.active_user = user

  def get_user_names(self) -> list:
    user_names: list = []
    for user in self.users.values():
      user_names.append(user.name) 
    return user_names
  
  # weapon methods
  
  def get_weapon_name(self, weapon_id: int) -> str:
    selected_weapon: Weapon = self.weapons[weapon_id]
    weapon_item_id: int = selected_weapon.item_id
    selected_item: Item = self.items[weapon_item_id]
    weapon_name: str = selected_item.name
    return weapon_name
  
  def get_weapon_abilities(self, weapon: Weapon) -> dict[int, Ability]:
    item_id: int = weapon.item_id
    weapon_item_abilities: dict[int, ItemAbility] = filter_dictionary(self.item_abilities, lambda _, item_ability: item_ability.item_id == item_id)
    weapon_item_abilities_ability_identifiers: list[int] = []
    for item_ability in list(weapon_item_abilities.values()):
      weapon_item_abilities_ability_identifiers.append(item_ability.ability_id)
    return filter_dictionary(self.abilities, lambda identifier, _: identifier in weapon_item_abilities_ability_identifiers)
  
  def get_weapon_parry(self, weapon: Weapon) -> ParryAbility:
    weapon_abilities: dict[int, Ability] = self.get_weapon_abilities(weapon)
    weapon_parry_abilities: dict[int, Ability] = filter_dictionary(weapon_abilities, lambda _, ability: ability.ability_type == AbilityTypeName.PARRY)
    weapon_parry_abilities_identifiers: list[int] = list(weapon_parry_abilities.keys())
    parries_dict: dict[int, ParryAbility] = filter_dictionary(self.parry_abilities, lambda _, parry_ability: parry_ability.ability_id in weapon_parry_abilities_identifiers)
    parries_list: list[ParryAbility] = list(parries_dict.values())
    if len(parries_list) != 1: raise LookupError(f"Multiple or no parry abilities found for `{weapon=}`: `{parries_dict=}`.")
    return parries_list[0]
  
  # character methods
  
  def get_active_character(self) -> Character:
    if self.active_character_id == None:
      raise AttributeError(f"Trying to access \'self.active_character_id\' when no active character has been selected (\'self.active_character_id\'=\'None\')")
    active_character: Character = self.characters[self.active_character_id]
    return active_character
  
  def get_character_name(self) -> str:
   return self.get_active_character().name
  
  # enemy and fighting_enemy methods
  
  def get_fighting_enemy_id_at(self, position: Position) -> Optional[int]:
    fighting_enemy_id: Optional[int] = self.fighting_enemy_graph.get_fighting_enemy_id(position)
    if fighting_enemy_id == None: return None
    return fighting_enemy_id
  
  def get_fighting_enemy_at(self, position: Position) -> Optional[FightingEnemy]:
    fighting_enemy_id: Optional[int] = self.get_fighting_enemy_id_at(position)
    if fighting_enemy_id == None: return None
    fighting_enemy: FightingEnemy = self.fighting_enemies[fighting_enemy_id]
    return fighting_enemy
  
  def set_fighting_enemy_at(self, position: Position, fighting_enemy_id: int) -> None:
    self.fighting_enemy_graph.set_fighting_enemy_id(position, fighting_enemy_id)

  def get_fighting_enemy_name(self, fighting_enemy_id: Optional[int]) -> str:
    if fighting_enemy_id == None: return ""
    fighting_enemy: Optional[FightingEnemy] = self.fighting_enemies[fighting_enemy_id]
    if fighting_enemy == None: return ""
    return fighting_enemy.name
  
  def get_fighting_enemy_health(self, fighting_enemy_id: Optional[int]) -> Optional[float]:
    if fighting_enemy_id == None: return None
    fighting_enemy: Optional[FightingEnemy] = self.fighting_enemies[fighting_enemy_id]
    if fighting_enemy == None: return None
    return fighting_enemy.health
  
  def get_fighting_enemy_max_health(self, fighting_enemy_id: Optional[int]) -> Optional[float]:
    if fighting_enemy_id == None: return None
    fighting_enemy: FightingEnemy = self.fighting_enemies[fighting_enemy_id]
    return fighting_enemy.max_health
  
  def get_enemy_attack_ability(self, enemy_id: int) -> Optional[tuple[int, Ability]]:
    """Assumes enemy has only one ability used in an attack."""
    enemy_attack_abilities_dict: dict[int, EnemyAbility] = filter_dictionary(self.enemy_abilities, lambda _, enemy_ability: enemy_ability.enemy_id == enemy_id and enemy_ability.is_used_in_attack)

    if len(enemy_attack_abilities_dict) == 0: return None
    if len(enemy_attack_abilities_dict) > 1: raise BufferError(f"{enemy_attack_abilities_dict=}; expected a dictionary of length `1`.")

    enemy_attack_ability: EnemyAbility = list(enemy_attack_abilities_dict.values())[0]
    ability_id: int = enemy_attack_ability.ability_id
    ability: Ability = self.abilities[ability_id]
    return (ability_id, ability)
  
  def get_enemy_heal_ability(self, enemy_id: int) -> Optional[tuple[int, Ability]]:
    """Gets the enemy's healing ability."""
    heal_abilities_dict: dict[int, StatisticAbility] = filter_dictionary(self.statistic_abilities, lambda _, statistic_ability: statistic_ability.ability_type == AbilityTypeName.HEAL)
    heal_ability_identifiers: list[int] = list(heal_abilities_dict.keys())
    enemy_heal_abilities_dict: dict[int, EnemyAbility] = filter_dictionary(self.enemy_abilities, lambda _, enemy_ability: enemy_ability.enemy_id == enemy_id and enemy_ability.ability_id in heal_ability_identifiers)

    if len(enemy_heal_abilities_dict) == 0: return None
    if len(enemy_heal_abilities_dict) > 1: raise BufferError(f"{enemy_heal_abilities_dict=}; expected a dictionary of length `1`.")

    enemy_heal_ability: EnemyAbility = list(enemy_heal_abilities_dict.values())[0]
    ability_id: int = enemy_heal_ability.ability_id
    ability: Ability = self.abilities[ability_id]
    return (ability_id, ability)
  
  # inventory and inventory item methods

  def get_character_inventory_items(self, character_id: Optional[int] = None) -> dict[int, InventoryItem]:
    if character_id == None: character_id = self.active_character_id
    filter_expression: Callable[[int, InventoryItem], bool] = lambda _, inv_item: inv_item.character_id == character_id
    return filter_dictionary(self.inventory_items, filter_expression)
  
  def set_inventory_item_equipped(self, inventory_item_id: int, being_equipped: bool) -> None:
    """Equips or unequips an inventory item depending on the \'being_equipped\' parameter."""
    self.inventory_items[inventory_item_id].equipped = being_equipped

  def toggle_inventory_item_equipped(self, toggleable_button: ToggleableButton, inventory_item_id: int) -> None:
    being_equipped: bool = bool(toggleable_button.is_toggled)
    self.set_inventory_item_equipped(inventory_item_id, being_equipped)
    logging.debug(f"\'self.inventory_items\'=`{self.inventory_items}`")
  
  def get_relevant_storage_items(self, storage_id: int) -> dict[int, StorageItem]:
    filter_expression: Callable[[int, StorageItem], bool] = lambda _, storage_item: storage_item.storage_id == storage_id
    return filter_dictionary(self.storage_items, filter_expression)
  
  def move_inventory_item_to_storage(self, inventory_item_id: int, storage_id: int) -> None:
    # get inventory item data
    inventory_item: InventoryItem = self.inventory_items[inventory_item_id]
    item_id: int = inventory_item.item_id
    stack_size: int = inventory_item.stack_size
    # TODO: handle what happens if the item is equipped such that it doesn't throw an error
    if inventory_item.equipped: raise Exception("Moving inventory items while they are equipped is not yet implemented")
    raw_storage_item_data: list[Any] = [storage_id, item_id, stack_size]
    
    same_item: Callable[[int, StorageItem], bool] = lambda _, storage_item: storage_id == storage_item.storage_id and item_id == storage_item.item_id
    matching_items: dict[int, StorageItem] = filter_dictionary(self.storage_items, same_item)
    matching_items_quantity: int = len(matching_items)
    logging.debug(f"| BEFORE MOVE (inv->store): \'matching_items_quantity\'=`{matching_items_quantity}`")

    if matching_items_quantity == 0: # if there are no items of the same type (in the target storage)
      identical_condition = Condition(lambda _identifier, _row: False) # there must be no matching items for this block to execute, so there is no need for a functional identical condition
      self.insert_stored(StorageItem, raw_storage_item_data, identical_condition, StorageAttrName.STORAGE_ITEMS)
    elif matching_items_quantity == 1: # if there is one instance of same-type items (in the target storage)
      matched_item_id: int = list(matching_items.keys())[0] # there will always be an item at index 0
      matched_item: StorageItem = list(matching_items.values())[0] 
      new_stack_size: int = stack_size + matched_item.stack_size # update stack size
      raw_storage_item_data[2] = new_stack_size
      self.update_database_record(StorageItem.get_table_name(), matched_item_id, raw_storage_item_data)
      self.storage_items[matched_item_id].stack_size = new_stack_size
    else: # erroneous case where there are 2 or more matches
      raise Exception(f"\'matching_items_quantity\'=`{matching_items_quantity}` greater than \'1\' (\'matching_items\'=`{matching_items}`)")
    
    self.delete_stored(InventoryItem, inventory_item_id, StorageAttrName.INVENTORY_ITEMS)
    logging.debug(f"| AFTER MOVE (inv->store): \'matching_items_quantity\'=`{matching_items_quantity}`")

  def move_storage_item_to_inventory(self, storage_item_id: int) -> None:
    character_id: int = unpack_optional(self.active_character_id) # 'unpack_optional' should never throw an exception here
    storage_item: StorageItem = self.storage_items[storage_item_id]
    item_id: int = storage_item.item_id
    stack_size: int = storage_item.stack_size
    equipped: bool = False # items should only equip when the player requests to
    raw_inventory_item_data: list[Any] = [character_id, item_id, stack_size, equipped]

    same_item: Callable[[int, InventoryItem], bool] = lambda _,inv_item: character_id == inv_item.character_id and item_id == inv_item.item_id
    matching_items: dict[int, InventoryItem] = filter_dictionary(self.inventory_items, same_item)
    matching_items_quantity: int = len(matching_items)
    logging.debug(f"| BEFORE MOVE (store->inv): \'matching_items_quantity\'=`{matching_items_quantity}`")

    if matching_items_quantity == 0: # if there are no items of the same type in the target storage
      identical_condition = Condition(lambda _identifier, _row: False) # there must be no matching items for this block to execute, so there is no need for a functional identical condition
      self.insert_stored(InventoryItem, raw_inventory_item_data, identical_condition, StorageAttrName.INVENTORY_ITEMS)
    elif matching_items_quantity == 1: # if there is one instance of items of the same type in the target storage
      matched_item_id: int = list(matching_items.keys())[0]
      matched_item: InventoryItem = list(matching_items.values())[0] # there will always be an item at index 0
      new_stack_size: int = stack_size + matched_item.stack_size
      raw_inventory_item_data[2] = new_stack_size
      self.update_database_record(InventoryItem.get_table_name(), matched_item_id, raw_inventory_item_data)
      self.inventory_items[matched_item_id].stack_size = new_stack_size
    else: # erroneous case where there are 2 or more matches
      raise Exception(f"\'matching_items_quantity\'=`{matching_items_quantity}` greater than \'1\' (\'matching_items\'=`{matching_items}`)")
    
    self.delete_stored(StorageItem, storage_item_id, StorageAttrName.STORAGE_ITEMS)
    logging.debug(f"| AFTER MOVE (store->inv): \'matching_items_quantity\'=`{matching_items_quantity}`")

  def is_storage_at_home(self) -> Optional[bool]:
    """Determines whether the storage is a \"Home\" storage or not."""
    storage_id: Optional[int] = self.active_storage_id
    if storage_id == None: return None
    logging.debug(f"{storage_id=}")
    storage_type: StorageType = self.storages[storage_id].storage_type
    if storage_type == StorageType.HOME: return True
    elif storage_type == StorageType.CHEST: return False
    else: raise ValueError(f"Unknown \'storage_type\'=`{storage_type}`")

  def get_inventory_item_name(self, inventory_item_id: int) -> str:
    selected_inventory_item: InventoryItem = self.inventory_items[inventory_item_id]
    selected_item_id: int = selected_inventory_item.item_id
    selected_item: Item = self.items[selected_item_id]
    return selected_item.name
  
  # methods for encountering enemies
  
  def get_random_enemy_identifier(self, get_boss: bool) -> int:
    matching_enemy_type: Callable[[int, Enemy], bool] = lambda _, enemy: enemy.is_boss == get_boss
    enemies: dict[int, Enemy] = filter_dictionary(self.enemies, matching_enemy_type)
    return select_random_identifier(enemies)
  
  def get_multiple_random_enemy_identifiers(self, n: int, get_boss: bool) -> list[int]:
    if n < 0: raise ValueError(f"{n=} cannot be less than 0.")
    if n > 1 and get_boss: raise Exception(f"Cannot get more than {n=} bosses.")
    if n == 0: return [] # base case
    enemy_id: int = self.get_random_enemy_identifier(get_boss)
    return [enemy_id] + self.get_multiple_random_enemy_identifiers(n-1, get_boss) # recursive call
  
  def add_fighting_enemy_to_grid_at_random_position(self, fighting_enemy_id: int) -> None:
    position: Position = get_random_position(self.fighting_enemy_graph.dimensions)
    if self.get_fighting_enemy_at(position) != None:
      return self.add_fighting_enemy_to_grid_at_random_position(fighting_enemy_id) # recursive call
    return self.set_fighting_enemy_at(position, fighting_enemy_id)
  
  def generate_fighting_enemies(self) -> None:
    enemy_count: int = generate_enemy_count()
    is_boss: bool = is_boss_encounter()
    enemy_identifiers: Queue[int] = Queue(self.get_multiple_random_enemy_identifiers(enemy_count, is_boss))
    while not enemy_identifiers.empty():
      enemy_id: int = enemy_identifiers.get()
      enemy: Enemy = self.enemies[enemy_id]
      # initialisation
      fighting_enemy = FightingEnemy(enemy_id, enemy.name, enemy.max_health, enemy.max_health, enemy.attack_damage, enemy.intelligence)
      self.set_fighting_enemy_abilities(fighting_enemy)
      # inserting into storage
      fighting_enemy_id: int = get_next_available_identifier(self.fighting_enemies)
      self.insert_into_storage(StorageAttrName.FIGHTING_ENEMIES, fighting_enemy_id, fighting_enemy)
      self.add_fighting_enemy_to_grid_at_random_position(fighting_enemy_id)

  def set_fighting_enemy_abilities(self, fighting_enemy: FightingEnemy) -> None:
    """Sets the attack and heal abilities for a given fighting enemy. Having no attack ability means the enemy has only a standard attack. Having no heal ability means the enemy cannot heal."""
    enemy_id: int = fighting_enemy.enemy_id
    # attack ability
    attack_data: Optional[tuple[int, Ability]] = self.get_enemy_attack_ability(enemy_id)
    if attack_data == None: attack_ability_id = None
    else: (attack_ability_id, _) = attack_data
    # heal ability
    heal_data: Optional[tuple[int, Ability]] = self.get_enemy_heal_ability(enemy_id)
    if heal_data == None: heal_ability_id = None
    else: (heal_ability_id, _) = heal_data

    fighting_enemy.set_action_identifiers(attack_ability_id, heal_ability_id)
  
  def finish_combat_encounter(self) -> None:
    for i in range(len(self.fighting_enemy_graph)):
      p: Position = self.fighting_enemy_graph.length_to_point(i)
      fighting_enemy_id: Optional[int] = self.fighting_enemy_graph[p]
      if fighting_enemy_id == None: continue
      del self.fighting_enemies[fighting_enemy_id]
    self.fighting_enemy_graph.clear_graph()
  
  # methods for handling the generation / deletion of structure items
  
  def get_random_item_identifier(self) -> int:
    return select_random_identifier(self.items)
  
  def get_unique_random_item_identifier(self, selected_item_identifiers: list[int] = []) -> int:
    item_id: int = self.get_random_item_identifier()
    if item_id in selected_item_identifiers:
      return self.get_unique_random_item_identifier(selected_item_identifiers)
    return item_id
  
  def get_multiple_unique_random_item_identifiers(self, n: int, selected_item_identifiers: list[int] = []) -> list[int]:
    if n < 0: raise ValueError(f"{n=} cannot be less than 0.")
    if n == 0: return [] # base case
    item_id: int = self.get_unique_random_item_identifier(selected_item_identifiers)
    selected_item_identifiers.append(item_id)
    return [item_id] + self.get_multiple_unique_random_item_identifiers(n-1, selected_item_identifiers) # recursive call
  
  def encounter_structure(self) -> None:
    """Generates the items for a structure being accessed."""
    item_count: int = generate_structure_item_count()
    away_storage_id: Optional[int] = self.away_storage
    if away_storage_id == None: raise TypeError(f"{self.away_storage=} cannot be `None` when encountering a structure.")
    item_identifiers: Queue[int] = Queue(self.get_multiple_unique_random_item_identifiers(item_count))
    identical_condition = nothing()
    while not item_identifiers.empty():
      item_id: int = item_identifiers.get()
      self.insert_stored(StorageItem, [away_storage_id, item_id, 1], identical_condition, StorageAttrName.STORAGE_ITEMS)
  
  def finish_structure_encounter(self) -> None:
    """Deletes items in the structure after it has been accessed."""
    away_storage_id: Optional[int] = self.away_storage
    if away_storage_id == None: raise TypeError(f"{self.away_storage=} cannot be `None` when finishing a structure encounter.")
    item_in_selected_storage: Callable[[int, StorageItem], bool] = lambda _, storage_item: storage_item.storage_id == away_storage_id
    selected_storage_items: dict[int, StorageItem] = filter_dictionary(self.storage_items, item_in_selected_storage)
    storage_item_identifiers: Queue[int] = Queue(list(selected_storage_items.keys()))
    while not storage_item_identifiers.empty():
      storage_item_identifier: int = storage_item_identifiers.get()
      self.delete_stored(StorageItem, storage_item_identifier, StorageAttrName.STORAGE_ITEMS)

  def is_all_fighting_enemies_dead(self) -> bool:
    fighting_enemies: list[FightingEnemy] = list(self.fighting_enemies.values())
    if len(fighting_enemies) == 0: return True
    for fighting_enemy in fighting_enemies:
      fighting_enemy_health: float = fighting_enemy.health
      if fighting_enemy_health > 0: return False
    return True

EOF
main.py

from app import App

def main() -> None:
  app = App()
  app.run()
  
if __name__ == "__main__": main()

EOF
