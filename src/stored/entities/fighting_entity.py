from tools.typing_tools import *
from tools.custom_exceptions import HealthSetError, UnexpectedAbilityActionError
from tools.decision_tools import *
from tools.constants import *

from stored.stored import *

from ability_action import *

# decorators and generators

type FormattableFightingEntityCallable[FightingEntityType: FightingEntity] = Callable[Concatenate[FightingEntityType, ...], Optional[str]]

def format_attribute_based_on_type(attribute: Union[str, int, float, None], rounding_accuracy: int = Constants.DEFAULT_ROUNDING_ACCURACY) -> str:
  """Eliminates the impact of floating point arithemtic errors on the length of displayed real numbers in the GUI."""
  if attribute == None: 
    return f"None"
  if type(attribute) in [str, int]:
    return f"{attribute}"
  if type(attribute) == float:
    return f"{attribute:.{rounding_accuracy}f}"
  raise TypeError(f"Tried to format {attribute=} with unknown type {type(attribute)}.")

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

def prepend_message_info[FightingEntityType: FightingEntity](attribute_tag: Union[str, int], descriptor: Optional[str] = None, units: str = "", add_brackets: bool = False, add_colon_at_end: bool = False, add_comma_at_end: bool = False, capitalise: bool = False, rounding_accuracy: int = Constants.DEFAULT_ROUNDING_ACCURACY) -> Callable[[FormattableFightingEntityCallable[FightingEntityType]], FormattableFightingEntityCallable[FightingEntityType]]:
  """
  :param attribute_tag: If of type `str`, the name of the attribute in `FightingEntityType` which will be prepended. If of type `int`, it indexes the argument will be used in prepending.
  :type attribute_tag: Union[str, int]
  """
  def decorator(func: FormattableFightingEntityCallable[FightingEntityType]) -> FormattableFightingEntityCallable[FightingEntityType]:
    def wrapper(self: FightingEntityType, *args, **kwargs) -> Optional[str]:
      attribute_str: str
      if type(attribute_tag) == int:
        attribute_str = format_attribute_based_on_type(args[attribute_tag], rounding_accuracy)
      elif type(attribute_tag) == str:
        attribute_str = format_attribute_based_on_type(getattr(self, attribute_tag), rounding_accuracy)
      info: str = format_message_info(attribute_str, descriptor, units, add_brackets, add_colon_at_end, add_comma_at_end, capitalise)
      body: Optional[str] = func(self, *args, **kwargs)
      if body == None: return None
      return f"{info} {body}"
    return wrapper
  return decorator

def append_message_info[FightingEntityType: FightingEntity](attribute_tag: Union[str, int], descriptor: Optional[str] = None, units: str = "", add_brackets: bool = False, add_colon_at_end: bool = False, add_comma_at_end: bool = False, capitalise: bool = False, rounding_accuracy: int = Constants.DEFAULT_ROUNDING_ACCURACY) -> Callable[[FormattableFightingEntityCallable[FightingEntityType]], FormattableFightingEntityCallable[FightingEntityType]]:
  """
  :param attribute_tag: If of type `str`, the name of the attribute in `FightingEntityType` which will be prepended. If of type `int`, it indexes the argument will be used in prepending.
  :type attribute_tag: Union[str, int]
  """
  def decorator(func: FormattableFightingEntityCallable[FightingEntityType]) -> FormattableFightingEntityCallable[FightingEntityType]:
    def wrapper(self: FightingEntityType, *args, **kwargs) -> Optional[str]:
      attribute_str: str
      if type(attribute_tag) == int:
        attribute_str = format_attribute_based_on_type(args[attribute_tag], rounding_accuracy)
      elif type(attribute_tag) == str:
        attribute_str = format_attribute_based_on_type(getattr(self, attribute_tag), rounding_accuracy)
      body: Optional[str] = func(self, *args, **kwargs)
      if body == None: return None
      info: str = format_message_info(attribute_str, descriptor, units, add_brackets, add_colon_at_end, add_comma_at_end, capitalise)
      return f"{body} {info}"
    return wrapper
  return decorator

# class

class FightingEntity(Stored):
  def __init__(self, name: str, health: float, max_health: float, loaded: bool = True, is_logging_enabled: bool = False, label: Optional[str] = None, include_call_stack: bool = False) -> None:
    self.name = name
    if label == None: label = self.name
    super().__init__(loaded, is_logging_enabled, label, include_call_stack)
    self.health = health
    self.max_health = max_health
    # attributes not stored in the database, but which are still important
    self.damage_resistance: float = 0
    self.is_ignited: bool = False
    self.is_pierced: bool = False
    ## parrying data
    self.is_parrying: bool = False
    self.parry_damage_threshold: Optional[float] = None
    self.parry_reflection_proportion: Optional[float] = None
    ## decision-making
    self.aggressiveness: float = 0

  # built-in methods

  def __repr__(self) -> str:
    return f"FightingEntity({self.name=}, {self.health=}, {self.max_health=})"

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.NONE

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.name, self.health, self.max_health]
  
  @staticmethod
  def instantiate(fighting_entity_data: list[Any], loaded: bool = True):
    return instantiate_fighting_entity(fighting_entity_data, loaded)
  
  # variable-setting methods

  def reset_state(self) -> None:
    self.reset_health()
    self.reset_damage_resistance()
    self.is_ignited = False
    self.is_pierced = False
    self.is_parrying = False
    self.parry_damage_threshold = None
    self.parry_reflection_proportion = None
    self.aggressiveness = 0

  ## health
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
    return f"Health set to {self.health:.{Constants.DEFAULT_ROUNDING_ACCURACY}f}HP"

  @append_message_info(0, descriptor="RAW", units="DMG", add_brackets=True)
  def take_damage(self, damage_amount: float) -> str:
    modified_damage_amount: float = damage_amount
    if not self.is_pierced or self.damage_resistance < 0:
      modified_damage_amount = self.apply_damage_resistance(damage_amount)
    if modified_damage_amount < 0: raise ValueError(f"{modified_damage_amount=} less than zero.")
    self.change_health(-1*modified_damage_amount)
    return f" Received {modified_damage_amount:.{Constants.DEFAULT_ROUNDING_ACCURACY}f}DMG"

  def heal(self, heal_amount: float) -> Optional[str]:
    if heal_amount < 0:
      raise ValueError(f"{heal_amount=} less than zero.")
    return self.change_health(heal_amount)
  
  ## damage resistance / vulnerability
  def apply_damage_resistance(self, damage_amount: float) -> float:
    new_damage_amount: float = damage_amount * (1-self.damage_resistance)
    if new_damage_amount < 0: raise ValueError(f"`{new_damage_amount=}` is less than `0` after `{self.damage_resistance=}` was applied.")
    return new_damage_amount
  
  def reset_damage_resistance(self) -> None:
    self.damage_resistance = 0

  # ability / modifier methods

  @prepend_message_info("name", add_colon_at_end=True, capitalise=True)
  def apply_ability_action(self, ability_action: AbilityAction) -> Optional[str]:
    """
    :param self: Description
    :param ability_action: Ability to be applied
    :type ability_action: AbilityAction
    :return: Resulting message from 
    :rtype: str | None
    """
    if type(ability_action) == IgniteAction: return self.ignite()
    elif type(ability_action) == DefendAction: return self.defend(ability_action.resistance)
    elif type(ability_action) == WeakenAction: return self.weaken(ability_action.vulnerability)
    elif type(ability_action) == PierceAction: return self.pierce()
    elif type(ability_action) == ParryAction: return self.engage_parry(ability_action.damage_threshold, ability_action.reflection_proportion)
    elif type(ability_action) == HealAction: return self.heal(ability_action.heal_amount)
    raise UnexpectedAbilityActionError(ability_action)

  @prepend_message_info("name", add_colon_at_end=True, capitalise=True)
  def inflict_active_effects(self) -> Optional[str]:
    if self.is_ignited: return self.deal_ignite()
    return None

  @prepend_message_info("name", add_colon_at_end=True, capitalise=True)
  def remove_ability_action(self, ability_action: AbilityAction) -> Optional[str]:
    """
    :param ability_action: The ability_action being removed. Should already be applied to the entity.
    :type ability_action: AbilityAction
    :return: The message which is to be relayed to the user. If `None`, no message is being sent.
    :rtype: Optional[str]
    """
    if type(ability_action) == IgniteAction: return self.unignite()
    elif type(ability_action) == DefendAction: return self.undefend(ability_action.resistance)
    elif type(ability_action) == WeakenAction: return self.unweaken(ability_action.vulnerability)
    elif type(ability_action) == PierceAction: return self.unpierce()
    elif type(ability_action) == ParryAction: return self.unengage_parry()
    elif type(ability_action) == HealAction: return None # no need for an "unheal"
    raise UnexpectedAbilityActionError(ability_action)

  ## ignition
  def ignite(self) -> str:
    self.is_ignited = True
    return f"Ignited"

  def deal_ignite(self) -> Optional[str]:
    ignition_damage_message: Optional[str] = self.take_damage(Constants.IGNITE_DAMAGE)
    if ignition_damage_message == None: return None
    return f"{ignition_damage_message} from being ignited"

  def unignite(self) -> str:
    self.is_ignited = False
    return f"Extinguished"
  
  ## defending
  @append_message_info(0, "RESIST", add_brackets=True, add_comma_at_end=True, rounding_accuracy=3)
  def defend(self, resistance: float) -> str:
    if resistance < 0: raise ValueError(f"{resistance=} cannot be less than `0`.")
    self.damage_resistance += resistance
    return f"Defending"

  def undefend(self, resistance: float) -> str:
    if resistance < 0: raise ValueError(f"{resistance=} cannot be less than `0`.")
    self.damage_resistance -= resistance
    return f"Defend ended"

  ## weakening
  @append_message_info(0, descriptor="VULN", add_brackets=True, add_comma_at_end=True, rounding_accuracy=3)
  def weaken(self, vulnerability: float) -> str:
    if vulnerability < 0: raise ValueError(f"{vulnerability=} cannot be less than `0`.")
    self.damage_resistance -= vulnerability
    return f"Weakened"

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
  @append_message_info(0, descriptor="RFLCT", add_brackets=True)
  @append_message_info(1, descriptor="DMG", add_brackets=True, add_comma_at_end=True)
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

  def calculate_aggressiveness_info(self, remaining_ignition_duration: Optional[int], damage_threshold: Optional[float], reflection_proportion: Optional[float]) -> tuple[float, float]:
    """
    :return: A pair of numbers, the first being the total aggressiveness and the second being the total weight of values computed.
    :rtype: tuple[float, float]
    """
    total: float = 0
    n: float = DecisionMakingConstants.HEALTH_WEIGHT+DecisionMakingConstants.IGNITED_WEIGHT+DecisionMakingConstants.DAMAGE_RESISTANCE_WEIGHT+DecisionMakingConstants.PARRY_WEIGHT
    total += self.calculate_health_aggressiveness()*DecisionMakingConstants.HEALTH_WEIGHT
    total += self.calculate_ignited_aggressiveness(remaining_ignition_duration)*DecisionMakingConstants.IGNITED_WEIGHT
    total += self.calculate_damage_resistance_aggressiveness()*DecisionMakingConstants.DAMAGE_RESISTANCE_WEIGHT
    total += self.calculate_parry_aggressiveness(damage_threshold, reflection_proportion)*DecisionMakingConstants.PARRY_WEIGHT
    return (total, n)

  def calculate_aggressiveness(self, remaining_ignition_duration: Optional[int], damage_threshold: Optional[float], reflection_proportion: Optional[float]) -> float:
    (total, n) = self.calculate_aggressiveness_info(remaining_ignition_duration, damage_threshold, reflection_proportion)
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
  
  def calculate_parry_aggressiveness(self, damage_threshold: Optional[float], reflection_proportion: Optional[float]) -> float:
    return calculate_parry_aggressiveness(damage_threshold, reflection_proportion)
  
  def calculate_aggressiveness_squared_deviation(self, offensiveness: float) -> float:
    return pow(self.aggressiveness - offensiveness, 2)

def instantiate_fighting_entity(fighting_entity_data: list[Any], loaded: bool = True) -> FightingEntity:
  name: str = fighting_entity_data[0]
  health: float = fighting_entity_data[1]
  max_health: float = fighting_entity_data[2]
  return FightingEntity(name, health, max_health, loaded)
