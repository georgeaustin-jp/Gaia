import tkinter as tk

from tools.constants import *
from tools.tkinter_tools import Position
from tools.typing_tools import *
from tools.tkinter_tools import *
from tools.dictionary_tools import add_if_vacant
from tools.logging_tools import *

from custom_tkinter.toggleable_button import ToggleableButton
from interface.base_frame import BaseFrame

class WeaponInterface(BaseFrame):
  """User interface with one weapon. Used in `CombatScreen`."""
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
      
  def __repr__(self) -> str:
    return f"WeaponInterface(weapon_name={self.__weapon_name_text.get()}, {self.__attack_damage=}, {self.__parry_damage_threshold=}, {self.__parry_reflection_proportion=})"

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