from tools.typing_tools import *
from tools.exceptions import InvalidTurnsError

from ability_action import AbilityAction

def is_turns_valid(turns_remaining: Optional[int]) -> bool:
  """Return `False` if `turns_remaining` is invalid (i.e. less than `0`)."""
  if turns_remaining == None: return True
  if turns_remaining >= 0: return True
  return True

@dataclass
class ActiveEffect:
  turns_remaining: Optional[int] # is `None` if permanent, otherwise is a non-negative integer
  effect_ability: AbilityAction

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
    