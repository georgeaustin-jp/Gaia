from tools.typing_tools import *

class EntityType:
  """
  Abstract base class for representing which type of fighting entity another entity is addressing. Subclasses of `CharacterType`, `EnemyType`, and `EmptyType`.
  """
  @staticmethod
  def __eq__(this, that) -> bool:
    if type(this) == type(that): return True
    return False
  
@dataclass
class CharacterType(EntityType):
  def __repr__(self) -> str: return "Character"

@dataclass
class EnemyType(EntityType):
  """
  :param identifier: Unique identifier of the fighting enemy it references.
  :type identifier: int
  :param position: Location of the enemy on the grid.
  :type position: Position
  """
  identifier: int
  position: Position

  def __repr__(self) -> str: return f"Enemy (at {self.position})"

@dataclass
class EmptyType(EntityType):
  """
  :param position: Location of the empty tile on the grid.
  :type position: Position
  """
  position: Position

  def __repr__(self) -> str: return f"Empty tile (at {self.position})"