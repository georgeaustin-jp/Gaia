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