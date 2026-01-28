from tools.typing_tools import *
from tools.constants import BaseDatabaseStrEnum
from tools.custom_exceptions import *

# enums

class AbilityTypeName(BaseDatabaseStrEnum):
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

def get_ability_type_name_qualifier(ability_type_name: AbilityTypeName) -> str:
  message: str = ""
  match ability_type_name:
    case AbilityTypeName.PARRY: message = "Pa"
    case AbilityTypeName.WEAKEN: message = "Wk"
    case AbilityTypeName.DEFEND: message = "Df"
    case AbilityTypeName.HEAL: message = "He"
    case AbilityTypeName.IGNITE: message = "Ig"
    case AbilityTypeName.PIERCE: message = "Pr"
    case _: raise UnexpectedAbilityTypeNameError(ability_type_name)
  return message