import logging

from tools.typing_tools import *

from ability_action import AbilityAction
from data_structures.action_type import *
from data_structures.entity_type import *

from stored.entities.fighting_entity import FightingEntity

def only_for_attacks(func):
  def wrapper(self, *args, **kwargs):
    if type(self.action_type) != Attack: raise TypeError(f"Cannot apply method to `{type(self.action_type)=}` not of type `Attack`.")
    return func(self, *args, **kwargs)
  return wrapper

class CombatAction:
  """
  Represents a single action taken in combat. All methods handle attacks on individual entities.

  :param sender_type: The entity who made the action.
  :type sender_type: EntityType
  :param target_type: The entity who will receive the action.
  :type target_type: EntityType
  :param action_type: What action is being carried out.
  :type action_type: ActionType
  """
  def __init__(self, sender_type: EntityType, target_type: Optional[EntityType], action_type: ActionType) -> None:
    self.sender_type = sender_type
    self.target_type = target_type
    self.action_type = action_type

  # built-in methods

  def __repr__(self) -> str:
    return f"ACTION {self.action_type}\n  [ {self.sender_type} -> {self.target_type} ]"

  def __call__(self, sender: FightingEntity, target: Optional[FightingEntity]) -> None:
    type_of_action: Type[ActionType] = type(self.action_type)
    if type_of_action == Attack: self.attack_fighting_entity(sender, target)
    elif type_of_action == Parry: pass # parrying is handled in `CombatManager`
    elif type_of_action == Heal: self.heal_fighting_entity(sender, target)
    else:
      raise TypeError(f"Action type `{type_of_action}` does not match with any known action types (\'Attack\', \'Parry\', \'Heal\')")
    
  # abilities and modifiers

  @only_for_attacks
  def add_ability_to_attack(self, ability: AbilityAction) -> None:
    if type(self.action_type) != Attack: raise TypeError(f"Cannot add abilities to `{type(self.action_type)=}`. Must be of type `Attack`.")
    return self.action_type.add_ability(ability)
  
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

  def attack_fighting_entity(self, sender: FightingEntity, target: Optional[FightingEntity]) -> None:
    if type(self.action_type) != Attack:
      raise TypeError(f"Expected type `Attack` for `type(self.action_type)`; got `{type(self.action_type)=}` instead.")
    if target == None:
      logging.info("target=\'None\'")
      return
    damage: float = self.action_type.quantity
    if target.is_parrying:
      parry_damage_threshold: Optional[float] = target.parry_damage_threshold
      parry_reflection_proportion: Optional[float] = target.parry_reflection_proportion
      if parry_damage_threshold == None or parry_reflection_proportion == None:
        raise ValueError(f"One of {parry_damage_threshold=} and/or {parry_reflection_proportion=} is `None`; both should be defined.")
      (damage, reflected_damage) = ParryAction.parry_damage(damage, parry_damage_threshold, parry_reflection_proportion)
      sender.take_damage(reflected_damage)
    target.take_damage(damage)

  def heal_fighting_entity(self, sender: FightingEntity, target: Optional[FightingEntity]) -> None:
    if type(self.action_type) != Heal:
      raise TypeError(f"Expected type `Heal` for `type(self.action_type)`. Got `{type(self.action_type)=}` instead.")
    if target == None:
      logging.info("target=`None`")
      return
    healing: float = self.action_type.quantity
    target.heal(healing)