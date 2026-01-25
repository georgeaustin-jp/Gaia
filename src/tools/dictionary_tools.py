from tools.typing_tools import *

from tools.logging_tools import *

def filter_dictionary[K, V](dictionary: dict[K, V], condition: Callable[[K, V], bool]) -> dict[K, V]:
  return {key: val for key, val in dictionary.items() if condition(key,val)}

def add_if_vacant[K, V](primary_dict: dict[K, V], secondary_dict: dict[K, V]) -> dict[K, V]:
  main_keys: list[K] = list(primary_dict.keys())
  for (key, value) in secondary_dict.items():
      if not key in main_keys:
        primary_dict[key] = value
  return primary_dict

def get_sorted_identifiers(dictionary: dict[int, Any]) -> list[int]:
  return sorted(list(dictionary.keys()))

def get_next_available_identifier[T](storage_attribute: dict[int, T]) -> int:
    """Calculates the smallest, non-zero identifier not in the given storage attribute."""
    previous_id: int = -1 # defining variables
    previous_id_successor: int = 0 
    sorted_identifiers: list[int] = get_sorted_identifiers(storage_attribute)
    for current_id in sorted_identifiers:
      previous_id_successor = previous_id+1
      if current_id > previous_id_successor: # if there is a hole in the sequence (e.g. [1,2,4,5] would return 3)
        return previous_id_successor
      previous_id = current_id # sets up for next iteration
    previous_id_successor = previous_id+1
    return previous_id_successor # in the case there are no holes, then it returns the id outside of the list 