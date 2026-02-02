from typing import Any
import logging

logging.basicConfig(level=logging.INFO)

def main() -> None:
  """
  Example: enemy with a name, current health, maximum health and indicator of life. Stored with 4 elements.

  Data types:
    * name - string
    * health - float
    * max_health - float
    * is_alive - bool

  Data for this enemy:
    * name = foo
    * health = 5
    * max_health = 10
    * is_alive = True
  """

  # with a list
  enemy_row_list: list[Any] = ["Foo", 5, 10, True] # no way of denoting fixed-length lists, or lists with specific data types for individual elements
  logging.info(f"Before change: {enemy_row_list=}")
  enemy_row_list[3] = -1 # setting `is_alive` to an invalid value
  logging.info(f"After change: {enemy_row_list=}")

  # with a tuple
  enemy_row_tuple: tuple[str, float, float, bool] = ("Foo", 5, 10, True) # allows you to denote a fixed-length data structure, as well as the expected data types of each element
  logging.info(f"Using tuple: {enemy_row_tuple=}")
  try:
    enemy_row_tuple[3] = False # however, tuples cannot be edited # type: ignore
  except Exception as error:
    logging.info(f"{error=}")

if __name__ == "__main__": main()