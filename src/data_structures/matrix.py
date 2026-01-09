from tools.typing_tools import *
from tools.logging_tools import *
from tools.positional_tools import validate_position_on

class Matrix[T](Sized):
  """
  Items are stored at position (x,y), being accessed by calling a `Matrix` object with the position tuple.
  """
  def __init__(self, dimensions: Position) -> None:
    """
    Constructor.

    :param dimensions: In the form (x_length, y_length).
    :type dimensions: tuple[int, int]
    """
    self.dimensions = dimensions
    self.__matrix: list[list[Optional[T]]] = []
    self.init_matrix()

  # built-in methods
    
  @validate_position_on
  def __setitem__(self, position: Position, value: T) -> None:
    (x,y) = position
    self.__matrix[x][y] = value

  @validate_position_on
  def __getitem__(self, position: Position) -> Optional[T]:
    (x,y) = position
    return self.__matrix[x][y]

  def __len__(self) -> int:
    return self.dimensions[0]*self.dimensions[1]
  
  # other methods
  
  def init_matrix(self) -> None:
    """
    Requires `self.dimensions` to already be initialised.
    
    :param self: Object being called on.
    """
    (x_length, y_length) = self.dimensions
    for x in range(x_length):
      self.__matrix.append([])
      for _ in range(y_length):
        self.__matrix[x].append(None)
