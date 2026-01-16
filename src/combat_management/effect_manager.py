from tools.typing_tools import *
from tools.ability_names import AbilityTypeName
from tools.constants import ItemType
from tools.dictionary_tools import filter_dictionary

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
      effects = self.fighting_enemy_effects[fighting_enemy_id]
    is_ignite_ability: Callable[[ActiveEffect], bool] = lambda effect: effect.effect_ability.get_ability_type_name() == AbilityTypeName.IGNITE
    ignition_effects: list[ActiveEffect] = list(filter(lambda effect: is_ignite_ability(effect), effects))
    if len(ignition_effects) == 0: return None
    elif len(ignition_effects) == 1:
      ignition_duration: Optional[int] = ignition_effects[0].turns_remaining
      if ignition_duration == None: raise ValueError(f"{ignition_effects[0]=} has {ignition_duration=}, which cannot be `None`.")
      return ignition_duration
    raise BufferError(f"Multiple ignition effects found: {ignition_effects=}.") # TODO: edit effect application to make it impossible to have multiple ignitions applied at once 