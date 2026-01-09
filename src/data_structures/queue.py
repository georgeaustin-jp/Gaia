from tools.typing_tools import *
from tools.exceptions import *

class Queue[T](Sized):
  def __init__(self, queue: list[T] = []) -> None:
    self.__queue: list[T] = queue

  # built-in methods

  def __len__(self) -> int:
    return len(self.__queue)
  
  def __repr__(self) -> str:
    return f"{self.__queue}"
  
  # stack operations
  
  def empty(self) -> bool:
    return len(self) == 0

  def get(self) -> T:
    if self.empty(): raise QueueError(f"Tried to pop value from empty stack.")
    return self.__queue.pop(0)
  
  def peek(self) -> Optional[T]:
    if self.empty(): return None
    return self.__queue[0]
  
  def put(self, value: T) -> None:
    self.__queue.append(value)