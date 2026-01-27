from tools.typing_tools import *
from tools.custom_exceptions import *
from tools.logging_tools import * # required for `Loggable`

class Queue[QueueType](Sized, Loggable):
  def __init__(self, queue: list[QueueType] = [], is_logging_enabled: bool = False, label: Optional[str] = None) -> None:
    self.__queue: list[QueueType]
    if queue == []: self.__queue = [].copy()
    else: self.__queue = queue.copy()
    super().__init__(is_logging_enabled, label)

  # built-in methods

  def __len__(self) -> int:
    return len(self.__queue)
  
  def __repr__(self) -> str:
    return f"{self.__queue}"

  # queue operations
  
  def empty(self) -> bool:
    return len(self) == 0

  def get(self) -> QueueType:
    if self.empty(): raise QueueError(f"Tried to pop value from empty queue.")
    return self.__queue.pop(0)
  
  def peek(self) -> Optional[QueueType]:
    if self.empty(): return None
    return self.__queue[0]

  def put(self, value: QueueType) -> None:
    return self.__queue.append(value)