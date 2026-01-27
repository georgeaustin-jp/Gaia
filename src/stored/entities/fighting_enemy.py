from tools.typing_tools import *
from tools.decision_tools import *
from tools.constants import *

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
  def __init__(self, enemy_id: int, name: str, health: float, max_health: float, attack_damage: float, intelligence: float, loaded: bool = True, is_logging_enabled: bool = True, label: Optional[str] = None, include_call_stack: bool = False) -> None:
    super().__init__(name, health, max_health, loaded, is_logging_enabled, label, include_call_stack)
    self.enemy_id: int = enemy_id
    self.attack_damage: float = attack_damage
    # decision-making attributes
    ## scalar values
    self.intelligence: float = intelligence
    self.decision_error_bound: float = get_decision_error_bound(self.intelligence)
    ## tables
    self.__action_offensiveness_table: dict[ActionName, float] = {
      ActionName.ATTACK: 0.0,
      ActionName.HEAL: 0.0,
    }.copy()
    self.ability_id_table: dict[ActionName, Optional[Union[int, list[int]]]] = {}.copy()
    self.VALID_ACTION_NAMES: list[ActionName] = [ActionName.ATTACK, ActionName.HEAL].copy()

  # built-in methods

  def __repr__(self) -> str:
    return f"FightingEnemy({self.enemy_id=}, {self.name=}, {self.health=}, {self.max_health=}, {self.attack_damage=}, {self.intelligence=}, {self.__action_offensiveness_table=}, {self.ability_id_table=})"

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
    return lambda _, row: False

  # getter and setter methods

  def get_action_names(self) -> list[ActionName]:
    return list(self.__action_offensiveness_table.keys())
  
  @validate_action_name
  def set_action_offensiveness(self, action_name: ActionName, offensiveness: float) -> None:
    self.__action_offensiveness_table[action_name] = offensiveness
  
  # decision making methods

  def set_action_identifiers(self, attack_ability_ids: Optional[list[int]], heal_ability_id: Optional[int]) -> None:
    self.ability_id_table[ActionName.ATTACK] = attack_ability_ids
    if heal_ability_id == None:
      del self.__action_offensiveness_table[ActionName.HEAL]
      return None
    self.ability_id_table[ActionName.HEAL] = heal_ability_id

  ## calculating action values
  def calculate_action_offensiveness_value(self, action_name: ActionName, actions: list[AbilityAction], store_result: bool = True) -> Optional[float]:
    """
    :param action_name: The name of the action which the offensiveness is being calculated for.
    :type action_name: ActionName
    :param actions: The list of abilities associated with this action. Being empty denotes no abilities.
    :type actions: list[AbilityAction]
    :param store_result: Whether the result should be stored in `self`. Defaults to `True`.
    :type store_result: bool
    """
    offensiveness_total: float = DecisionMakingConstants.DEFAULT_ATTACK_OFFENSIVENESS if action_name == ActionName.ATTACK else DecisionMakingConstants.DEFAULT_HEAL_OFFENSIVENESS
    n: float = 1
    if actions != []: 
      for ability in actions:
        offensiveness_total += ability.calculate_offensiveness()
        n += 1
    elif action_name == ActionName.HEAL:
      return None
    average_offensiveness = offensiveness_total/n
    if store_result: self.set_action_offensiveness(action_name, average_offensiveness)
    return average_offensiveness
      
  ## aggressiveness calculations
  def generate_decision_error(self) -> float:
    return generate_decision_error(self.decision_error_bound)
  
  def clip_aggressiveness(self, aggressiveness: float) -> float:
    return clip(aggressiveness, -self.decision_error_bound, self.decision_error_bound)

  def calculate_aggressiveness(self, remaining_ignition_duration: Optional[int], damage_threshold: Optional[float], reflection_proportion: Optional[float], negative_character_value: float) -> float:
    (total, n) = self.calculate_aggressiveness_info(remaining_ignition_duration, damage_threshold, reflection_proportion)
    total += negative_character_value * DecisionMakingConstants.PLAYER_WEIGHT
    n += DecisionMakingConstants.PLAYER_WEIGHT
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
