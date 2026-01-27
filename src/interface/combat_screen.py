import tkinter as tk

from tools.logging_tools import *

from tools.typing_tools import *
from tools.dictionary_tools import filter_dictionary
from tools.custom_exceptions import *
from tools.constants import *
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
from stored.items.inventory_item import InventoryItem

from stored.abilities.item_ability import ItemAbility
from stored.abilities.ability import Ability
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
  """Decorator that allows for the text in the info box to be edited."""
  def wrapper(self, info: Optional[str] = None, *args, **kwargs) -> ReturnType:
    self.info_box["state"] = tk.NORMAL
    result: ReturnType = func(self, info, *args, **kwargs)
    self.info_box["state"] = tk.DISABLED
    return result
  return wrapper

class CombatScreen(AbstractScreen):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
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

    self.__parry_used: bool = False

    self.end_combat_command: Callable[[ScreenName], None] = kwargs["end_combat"]

    super().__init__(root, parent, game_data, **kwargs)

  # getter and setter methods

  @property
  def is_parry_used(self) -> bool:
    return self.__parry_used
  
  @is_parry_used.setter
  def is_parry_used(self, is_parry_used: bool) -> None:
    """Sets the state of the parry button for all weapon interfaces."""
    self.__parry_used = is_parry_used
    for weapon_interface in self.weapon_interfaces:
      weapon_interface.is_parry_used = is_parry_used

  # weapon label operations
  
  def init_weapon_interfaces(self, weapon_grid: tk.Frame, placement_options: dict[str, Any] = {}, **kwargs) -> None:
    weapon_interfaces: list[WeaponInterface] = []
    for i in range(Constants.MAX_EQUIPPED_WEAPONS):
      weapon_interface = create_weapon_interface(self.root, parent=weapon_grid, position=(i,0), placement_options=placement_options, label=f"{i}", **kwargs)
      weapon_interfaces.append(weapon_interface)
    self.weapon_interfaces = weapon_interfaces
  
  def load_weapon_label_names(self) -> None:
    weapon_names: list[str] = self.game_data.get_equipped_weapon_names()
    for (i, weapon_name) in enumerate(weapon_names):
      self.weapon_interfaces[i].weapon_name = weapon_name

  def load_weapon_interface_at(self, index: int) -> None:
    weapon_interface: WeaponInterface = self.weapon_interfaces[index]
    if index >= len(self.game_data.equipped_weapon_identifiers):
      weapon_interface.load()
      return None
    weapon_identifier: int = self.game_data.equipped_weapon_identifiers[index]
    equipped_weapon_names: list[str] = self.game_data.get_equipped_weapon_names()
    weapon_name: Optional[str] = equipped_weapon_names[index]
    weapon: Weapon = self.game_data.weapons[weapon_identifier]
    attack_damage: float = weapon.damage
    # getting parry data
    weapon_parry: Optional[ParryAbility] = self.game_data.get_weapon_parry(weapon)
    parry_damage_threshold: Optional[float] = None # values if no parry is found
    parry_reflection_proportion: Optional[float] = None
    if weapon_parry != None:
      parry_damage_threshold = weapon_parry.damage_threshold
      parry_reflection_proportion = weapon_parry.reflection_proportion
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
      raise ValueError(f"{self.equipped_inventory_equipable_identifiers=} should have maximum length {Constants.MAX_EQUIPPED_EQUIPABLES}; instead has length of {len(self.equipped_inventory_equipable_identifiers)}.")
    
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
    self.set_all_weapon_interfaces_button_attributes(attribute, value, include_attack, include_parry)
    
    (enemy_interface_widgets_width, enemy_interface_widgets_height) = self.enemy_interface_widgets.dimensions
    for x in range(enemy_interface_widgets_width):
      for y in range(enemy_interface_widgets_height):
        enemy_interface: Optional[EnemyInterfaceWidgets] = self.enemy_interface_widgets[(x,y)]
        if enemy_interface == None: continue
        enemy_button: ToggleableButton = enemy_interface[0]
        enemy_button[attribute] = value

    self.health_potion_button[attribute] = value

    if include_confirm: self.confirmation_button[attribute] = value

  def set_all_weapon_interfaces_button_attributes(self, attribute: str, value: Any, include_attack: bool = True, include_parry: bool = True) -> None:
    if not (include_attack or include_parry): return None # skips the weapon interfaces if neither `include_attack` nor `include_parry` is active
    for i in range(len(self.weapon_interfaces)):
      self.set_weapon_interface_button_attribute_at(i, attribute, value, include_attack, include_parry)

  def set_weapon_interface_button_attribute_at(self, i: int, attribute: str, value: Any, include_attack: bool = True, include_parry: bool = True) -> None:
    """Assumes at least one of `include_attack` or `include_parry` is `True`."""
    if include_attack:
      self.set_attack_button_attribute(i, attribute, value)
    if include_parry:
      self.set_parry_button_attribute(i, attribute, value)

  def set_user_buttons_toggled(self, is_toggled: ToggleState, include_attack: bool = True, include_parry: bool = True) -> None:
    self.set_user_buttons_attributes("is_toggled", is_toggled, include_attack, include_parry, include_confirm=False)

  def reset_toggleable_user_buttons_toggled(self) -> None:
    self.set_user_buttons_toggled(ToggleState.OFF)

  def set_user_buttons_state(self, state: str, include_attack: bool = True, include_parry: bool = True, include_confirm: bool = True) -> None:
    self.set_user_buttons_attributes("state", state, include_attack, include_parry, include_confirm)

  def enable_user_buttons(self, include_attack: bool = True, include_parry: bool = False, include_confirm: bool = True) -> None:
    self.set_user_buttons_state(tk.NORMAL, include_attack, include_parry, include_confirm)

  def disable_user_buttons(self, include_attack: bool = True, include_parry: bool = True, include_confirm: bool = True) -> None:
    self.set_user_buttons_state(tk.DISABLED, include_attack, include_parry, include_confirm)

  # weapon buttons
  def set_weapon_button_attribute(self, weapon_index: int, button_type: WeaponUIComponentName, attribute: str, value: Any) -> None:
    if button_type not in [WeaponUIComponentName.ATTACK, WeaponUIComponentName.PARRY]: raise TypeError(f"`button_type`=`{button_type}` not one of `{WeaponUIComponentName.ATTACK}`, `{WeaponUIComponentName.PARRY}`.")
    weapon_interface: WeaponInterface = self.weapon_interfaces[weapon_index]
    selected_button: ToggleableButton = weapon_interface[button_type]
    selected_button[attribute] = value

  def set_attack_button_attribute(self, weapon_index: int, attribute: str, value: Any) -> None:
    weapon_interface: WeaponInterface = self.weapon_interfaces[weapon_index]
    if attribute == "state" and value == tk.NORMAL and not weapon_interface.has_attack: return None
    self.set_weapon_button_attribute(weapon_index, WeaponUIComponentName.ATTACK, attribute, value)

  def set_parry_button_attribute(self, weapon_index: int, attribute: str, value: Any) -> None:
    weapon_interface: WeaponInterface = self.weapon_interfaces[weapon_index]
    if attribute == "state" and value == tk.NORMAL and not weapon_interface.has_parry: return None
    self.set_weapon_button_attribute(weapon_index, WeaponUIComponentName.PARRY, attribute, value)

  def enable_attack_button(self, weapon_index: int) -> None:
    self.set_attack_button_attribute(weapon_index, "state", tk.NORMAL)

  def disable_attack_button(self, weapon_index: int) -> None:
    self.set_attack_button_attribute(weapon_index, "state", tk.DISABLED)

  def disable_parry_button(self, weapon_index: int) -> None:
    self.set_parry_button_attribute(weapon_index, "state", tk.DISABLED)

  def reset_weapon_states(self) -> None:
    for i in range(Constants.MAX_EQUIPPED_WEAPONS):
      try:
        weapon_id: Optional[int] = self.game_data.equipped_weapon_identifiers[i]
      except:
        weapon_id = None
      if weapon_id != None:
        self.weapon_interfaces[i].is_weapon_used = False
    self.is_parry_used = False

  def find_active_weapon_index(self) -> Optional[int]:
    for i in range(Constants.MAX_EQUIPPED_WEAPONS):
      weapon_interface: WeaponInterface = self.weapon_interfaces[i]
      if weapon_interface.is_attack_toggled ^ weapon_interface.is_parry_toggled: # XOR operation. If neither buttons are toggled, the weapon cannot be active, but if they are both toggled, then an invalid move is being made.
        return i
    return None
      
  # character labels

  def set_health_label(self, health: float) -> None:
    if health < 0:
      raise ValueError(f"Cannot set `displayed_health` to be less than zero ({health=} < 0)")
    display: str = f"{health:.{Constants.INTERFACE_ROUNDING_ACCURACY}f}HP"
    self.displayed_health.set(display)

  def update_health_label(self) -> None:
    character_health: float = self.game_data.get_active_character().health
    self.set_health_label(character_health)

  def set_damage_resistance_label(self, damage_resistance: float) -> None:
    display: str = f"{damage_resistance*100:.{Constants.INTERFACE_ROUNDING_ACCURACY}f}%"
    self.displayed_damage_resistance.set(display)

  def update_damage_resistance_label(self) -> None:
    character_damage_resistance: float = self.game_data.get_active_character().damage_resistance
    self.set_damage_resistance_label(character_damage_resistance)

  def wait_until_confirmed(self) -> None:
    if self.is_quitting: return None
    self.wait_variable(self.is_confirm_pressed)
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
      self.weapon_interfaces[weapon_index].is_weapon_used = True
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
  
  def is_one_attack_button_toggled(self) -> ComparisonFlag:
    count: int = 0
    for weapon_interface in self.weapon_interfaces:
      if weapon_interface.is_attack_toggled:
        count += 1
      if count > 1: return ComparisonFlag.GREATER
    if count == 0: return ComparisonFlag.LESS
    return ComparisonFlag.EQUAL
  
  def is_no_attack_buttons_toggled(self) -> bool:
    for weapon_interface in self.weapon_interfaces:
      if weapon_interface.is_attack_toggled: return False
    return True
  
  def is_one_parry_button_toggled(self) -> ComparisonFlag:
    count: int = 0
    for weapon_interface in self.weapon_interfaces:
      if weapon_interface.is_parry_toggled:
        count += 1
      if count > 1: return ComparisonFlag.GREATER
    if count == 0: return ComparisonFlag.LESS
    return ComparisonFlag.EQUAL
  
  def is_no_parry_buttons_toggled(self) -> bool:
    for weapon_interface in self.weapon_interfaces:
      if weapon_interface.is_parry_toggled: return False
    return True
  
  def is_health_potion_button_toggled(self) -> bool:
    return bool(self.health_potion_button.is_toggled)

  def get_action_type(self) -> ActionType:
    action: ActionType
    using_health_potion: bool = self.is_health_potion_button_toggled()
    using_weapons: bool = not self.is_no_weapon_buttons_toggled()
    
    using_one_attack: ComparisonFlag = self.is_one_attack_button_toggled()
    if using_one_attack == ComparisonFlag.GREATER:
      raise TooManyAttackButtonsSelectedError()
    is_attacking: bool = using_one_attack == ComparisonFlag.EQUAL
    
    using_one_parry: ComparisonFlag = self.is_one_parry_button_toggled()
    if using_one_parry == ComparisonFlag.GREATER:
      raise TooManyParryButtonsSelectedError()
    is_parrying: bool = using_one_parry == ComparisonFlag.EQUAL

    targeting_one_enemy_comparison: ComparisonFlag = self.is_one_enemy_button_toggled()
    if targeting_one_enemy_comparison == ComparisonFlag.GREATER: raise TooManyEnemiesSelectedError() # only 0 or 1 enemies can be selected
    targeting_no_enemies: bool = targeting_one_enemy_comparison == ComparisonFlag.LESS # to check if targeting 1 enemy, use `not targeting_no_enemies`, as 2 or more enemies cannot be selected

    if not (using_health_potion or using_weapons) and targeting_no_enemies and not using_weapons: # character can never select no buttons for an action
      raise NoButtonsSelectedError() 
    elif using_health_potion and targeting_no_enemies and not using_weapons: # handles using the health potion
      action = Heal(Constants.HEALTH_POTION_AMOUNT)
    elif using_health_potion: # health potion button can't be toggled from this point
      raise TooManyButtonsSelectedError(f"\'health_potion_button\' is toggled when other buttons are as well") 
    elif is_parrying and not is_attacking and targeting_no_enemies: # handles character parries
      parry_data: Optional[tuple[float, float]] = self.get_selected_weapon_parry_data()
      if parry_data == None: raise NoParryError(parry_data)
      (damage_threshold, reflection_proportion) = parry_data
      action = Parry(damage_threshold, reflection_proportion)
      self.is_parry_used = True
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
  
  def get_selected_weapon_attack_damage(self) -> float:
    weapon_buttons_selected: int = 0 # if weapon_interface.is_attack_toggled: return False
    for (i, weapon_interface) in enumerate(self.weapon_interfaces):
      is_attack_toggled: ToggleState = weapon_interface.is_attack_toggled
      if is_attack_toggled:
        weapon_buttons_selected += 1
        selected_weapon_identifier_index = i
      if weapon_buttons_selected > 1:
        raise TooManyWeaponButtonsSelectedError(i)
    weapon_identifier: Optional[int] = self.game_data.equipped_weapon_identifiers[selected_weapon_identifier_index]
    if weapon_identifier == None: raise TypeError(f"{weapon_identifier=} should never be `None`.")
    return self.game_data.weapons[weapon_identifier].damage
  
  def get_selected_weapon_parry_data(self) -> Optional[tuple[float, float]]:
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
    weapon_identifier: Optional[int] = self.game_data.equipped_weapon_identifiers[selected_weapon_identifier_index]
    if weapon_identifier == None: raise TypeError("\'weapon_identifier\' can never be \'None\'")
    weapon: Weapon = self.game_data.weapons[weapon_identifier]
    parry_ability: Optional[ParryAbility] = self.game_data.get_weapon_parry(weapon)
    if parry_ability == None: return None
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

      heal_ability_id: Optional[int] = None # set default value
      if fighting_enemy_id != None:
        enemy_interface_widgets[1].config(bg=Constants.ENEMY_ATTACK_LABEL_COLOUR)
        enemy_interface_widgets[2].config(bg=Constants.ENEMY_HEAL_LABEL_COLOUR)

        fighting_enemy = unpack_optional(self.game_data.get_fighting_enemy_at(position))

        fighting_enemy_name: str = self.game_data.get_fighting_enemy_name(fighting_enemy_id)
        fighting_enemy_heath: Optional[float] = self.game_data.get_fighting_enemy_health(fighting_enemy_id)
        fighting_enemy_max_heath: Optional[float] = self.game_data.get_fighting_enemy_max_health(fighting_enemy_id)

        button_display = f"{fighting_enemy_name}"
        if fighting_enemy_heath != None and fighting_enemy_max_heath != None:
          button_display += f"\n{fighting_enemy_heath:.{Constants.INTERFACE_ROUNDING_ACCURACY}f}/{fighting_enemy_max_heath:.{Constants.INTERFACE_ROUNDING_ACCURACY}f}HP"

        damage_str = format(fighting_enemy.attack_damage)

        heal_ability_id = cast(Optional[int], fighting_enemy.ability_id_table.get(ActionName.HEAL))

      if heal_ability_id != None:
        heal_ability: Ability = self.game_data.abilities[heal_ability_id]
        heal_ability_action: HealAction = cast(HealAction, self.game_data.get_ability_action(heal_ability_id, heal_ability))
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
    self.game_data.load_active_character_equipped_weapon_identifiers()
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

    self.create_quit()