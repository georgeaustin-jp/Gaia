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