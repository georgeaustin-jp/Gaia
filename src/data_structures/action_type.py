from tools.typing_tools import *

from ability_action import *
from data_structures.queue import Queue

@dataclass
class ActionType:
  """
  Which action an instance of `CombatAction` will use on its target, alongside any relevant information which comes with that.

  Abstract base class, with subclasses of `Attack`, `Parry` and `Heal`.
  """
  quantity: float

@dataclass
class Attack(ActionType):
  """
  Docstring for Attack

  :param quantity: Amount of base damage the attack does.
  :type quantity: float
  """
  effects: Queue[AbilityAction] = Queue()

  def add_ability(self, ability: AbilityAction) -> None:
    self.effects.put(ability)

  def get_next_ability(self) -> AbilityAction:
    return self.effects.get()

@dataclass
class Parry(ActionType):
  """
  Docstring for Parry

  :param quantity: Threshold of damage recieved before the sender starts taking damage.
  :type quantity: float
  :param reflect_proportion: The percentage of damage blocked by the parry which will be reflected at the attacker.
  :type reflect_proportion: float
  """
  reflect_proportion: float

@dataclass
class Heal(ActionType):
  """
  Docstring for Heal

  :param quantity:
  :type quantity: float
  """
  ...
