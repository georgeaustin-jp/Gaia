from tools.typing_tools import *

class EntityType:
  """
  Abstract base class for representing which type of fighting entity another entity is addressing. Subclasses of `CharacterType`, `EnemyType`, and `EmptyType`.
  """
  ...
  
@dataclass
class CharacterType(EntityType):
  def __repr__(self) -> str: return "Character"

@dataclass
class EnemyType(EntityType):
  identifier: int
  position: Position

  def __repr__(self) -> str: return f"Enemy (at {self.position})"

@dataclass
class EmptyType(EntityType):
  position: Position

  def __repr__(self) -> str: return f"Empty tile (at {self.position})"