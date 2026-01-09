from tools.typing_tools import *
from tools.exceptions import StackError

class Stack[T](Sized):
  def __init__(self) -> None:
    self.__stack: list[T] = []

  # built-in methods

  def __len__(self) -> int:
    return len(self.__stack)
  
  def __repr__(self) -> str:
    return f"{self.__stack}"
  
  # stack operations
  
  def is_empty(self) -> bool:
    return len(self) == 0

  def pop(self) -> T:
    if self.is_empty(): raise StackError(f"Tried to pop value from empty stack.")
    return self.__stack.pop()
  
  def peek(self) -> Optional[T]:
    if self.is_empty(): return None
    return self.__stack[-1]
  
  def push(self, value: T) -> None:
    self.__stack.append(value)