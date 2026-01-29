from tools.typing_tools import *
from tools.custom_exceptions import InvalidTurnsError
from tools.logging_tools import *

from ability_action import *

def is_turns_valid(turns_remaining: Optional[int]) -> bool:
  """Return `False` if `turns_remaining` is invalid (i.e. less than `0`)."""
  if turns_remaining == None: return True
  if turns_remaining >= 0: return True
  return True

@dataclass
class ActiveEffect:
  """
  :param turns_remaining: `None` if permanent, otherwise is a non-negative integer.
  :type turns_remaining: Optional[int]
  :param effect_ability: The ability which is being applied.
  :type effect_ability: AbilityAction
  """
  turns_remaining: Optional[int]
  effect_ability: AbilityAction

  # built-in methods

  def __eq__(self, other) -> bool:
    return isinstance(other, ActiveEffect) and self.effect_ability == other.effect_ability

  # other

  def is_no_turns_remaining(self) -> bool:
    if self.turns_remaining == 0: return True
    return False
  
  def is_permanent(self) -> bool:
    if self.turns_remaining == None: return True
    return False

  def decrement_remaining_turns(self) -> None:
    if self.turns_remaining == None: raise ValueError(f"Cannot decrement `self.turns_remaining` when it is `None`.")
    decremented_turns_remaining: int = self.turns_remaining - 1
    if not is_turns_valid(decremented_turns_remaining): raise InvalidTurnsError(decremented_turns_remaining)
    self.turns_remaining = decremented_turns_remaining
