import networkx as nx

from tools.typing_tools import *
from tools.constants import Constants
from tools.logging_tools import *
from tools.positional_tools import *

class FightingEnemyGraph(Sized):
  """
  Stores instances of `FightingEnemy` in an undirected graph data structure.
  """
  def __init__(self) -> None:
    self.dimensions: Position = (Constants.GRID_WIDTH, Constants.GRID_HEIGHT)
    self.__graph: nx.Graph[Position] = nx.grid_graph(dim=self.dimensions) # TODO: put stuff about Graphs in my documentation
    self.init_storage()
    self.add_edges()

  # built-in methods

  @validate_position_on
  def __call__(self, position: Position) -> Optional[int]:
    return self.get_fighting_enemy_id(position)
  
  @validate_position_on
  def __setitem__(self, position: Position, value: Optional[int]) -> None:
    self.set_fighting_enemy_id(position, value)

  @validate_position_on
  def __getitem__(self, position: Position) -> Optional[int]:
    return self.get_fighting_enemy_id(position)
  
  def __len__(self) -> int:
    return self.dimensions[0]*self.dimensions[1]
  
  def __iter__(self):
    self.l: int = 0
    return self
  
  def __next__(self) -> Optional[int]:
    if self.l >= len(self): raise StopIteration
    p: Position = self.length_to_point(self.l)
    self.l += 1
    return self.get_fighting_enemy_id(p)
  
  # other methods

  def length_to_point(self, length: int) -> Position:
    x: int = length % self.dimensions[1]
    y: int = length // self.dimensions[0]
    return (x,y)

  def apply_to_all(self, function: Callable[..., None], **kwargs) -> None:
    """
    Applies a given function, taking inputs of the node position with the kwargs, to every node of the graph.
    
    :param function: Takes an input of `position: Position` first, taking `**kwargs` afterward.
    :type function: Callable[..., None]
    """
    node_count: int = len(self)
    for i in range(node_count):
      position = self.length_to_point(i)
      function(position=position, **kwargs)

  def init_storage(self) -> None:
    node_count: int = len(self)
    for i in range(node_count):
      position = self.length_to_point(i)
      self.__graph.add_node(position, fighting_enemy_id=None)

  @validate_position_on
  def set_fighting_enemy_id(self, position: Position, fighting_enemy_id: Optional[int]) -> None:
    self.__graph.nodes[position]["fighting_enemy_id"] = fighting_enemy_id

  @validate_position_on
  def get_fighting_enemy_id(self, position: Position) -> Optional[int]:
    return self.__graph.nodes[position]["fighting_enemy_id"]
  
  @validate_position_on
  def is_fighting_enemy_at(self, position: Position) -> bool:
    if self.get_fighting_enemy_id(position) == None: return False
    return True
  
  @validate_position_on
  def add_fighting_enemy_id(self, position: Position, fighting_enemy_id: int) -> None:
    if self.is_fighting_enemy_at(position):
      raise MemoryError(f"Attempting to add fighting enemy (id=`{fighting_enemy_id}`) at position `{position}` when there is already an enemy there")
    self.set_fighting_enemy_id(position, fighting_enemy_id)
  
  @validate_position_on
  def clear_fighting_enemy_id(self, position: Position) -> None:
    self.set_fighting_enemy_id(position, None)

  def clear_graph(self) -> None:
    self.apply_to_all(self.clear_fighting_enemy_id)

  def add_edges(self) -> None:
    node_count: int = len(self)
    for l1 in range(node_count-1):
      p1 = self.length_to_point(l1)
      for l2 in range(l1+1, node_count):
        p2 = self.length_to_point(l2)
        distance: float = calculate_distance(p1, p2)
        self.__graph.add_edge(p1, p2, distance=distance)