from math import exp2, tanh, pow

from tools.typing_tools import *
from tools.decision_tools import *
from tools.constants import *
from data_structures.action_type import ActionType

from data_structures.queue import Queue

from stored.entities.fighting_entity import *
from database.condition import Condition

from ability_action import *

class FightingEnemy(FightingEntity):
  def __init__(self, enemy_id: int, name: str, health: float, max_health: float, attack_damage: float, intelligence: float, loaded: bool = True) -> None:
    super().__init__(name, health, max_health, loaded)
    self.enemy_id: int = enemy_id
    self.attack_damage: float = attack_damage
    self.intelligence: float = intelligence
    self.decision_error_bound: float = get_decision_error_bound(self.intelligence)

    self.action_offensiveness_table: dict[ActionName, float] = {
      ActionName.ATTACK: 0,
      ActionName.HEAL: 0,
    }
    self.ability_id_table: dict[ActionName, Optional[int]] = {}

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
  
  # decision making methods

  def set_action_identifiers(self, attack_ability_id: int, heal_ability_id: Optional[int]) -> None:
    self.ability_id_table[ActionName.ATTACK] = attack_ability_id
    if heal_ability_id != None:
      self.ability_id_table[ActionName.HEAL] = heal_ability_id

  ## calculating action values
  def set_action_offensiveness_value(self, action_name: ActionName, offensiveness: float) -> None:
    self.action_offensiveness_table[action_name] = offensiveness

  def calculate_action_offensiveness_value(self, action_name: ActionName) -> float:
    raise NotImplementedError()
      
  ## aggressiveness calculations
  def calculate_aggressiveness(self, remaining_ignition_duration: int, is_target_parrying: bool, negative_player_total: float, player_n: int) -> float:
    (total, n) = self.calculate_aggressiveness_info(remaining_ignition_duration, is_target_parrying)
    total += negative_player_total
    n += player_n
    self.aggressiveness = total / n
    return self.aggressiveness
  
  ## choosing the action
  def choose_action_name(self) -> ActionName:
    chosen_action: Optional[tuple[ActionName, float]] = None
    if len(self.action_offensiveness_table) == 0: raise BufferError(f"{self.action_offensiveness_table=} cannot be empty when choosing the action tag.")
    for (action_name, offensiveness) in self.action_offensiveness_table.items():
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
