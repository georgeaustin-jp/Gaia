from tools.typing_tools import *
from tools.dictionary_tools import *
from tools.logging_tools import *

from database.condition import Condition, get_condition_inverse

from tools.custom_exceptions import InsertAtExistingIdentifierError

class Table(Loggable):
  def __init__(self, name: str, column_names: list[str], is_logging_enabled: bool = False, tag: Optional[str] = None, include_call_stack: bool = False) -> None:
    self.name: str = name
    if tag == None: tag = self.name
    super().__init__(is_logging_enabled, tag, include_call_stack)
    self.column_names: list[str] = column_names
    self.rows: dict[int, list[Any]] = {}

  # built-in methods

  def __repr__(self) -> str:
    formatted_table: str = ""
    formatted_table += f"Table: name=`{self.name}`"
    formatted_table += f"\ncolumn_names=`{self.column_names}`"
    formatted_table += "\nrows = {"
    for (identifier, row) in self.rows.items():
      formatted_table += f"\n\t{identifier}: [{row[0]}"
      if len(row) > 1:
        for field in row[1:]:
          formatted_table += f",\t{field}"
        formatted_table += "],"
    formatted_table += "\n}"
    return formatted_table
  
  def __getitem__(self, identifier: int) -> list[Any]:
    return self.rows[identifier]
  
  def __setitem__(self, identifier: int, value: list[Any]) -> None:
    self.rows[identifier] = value
  
  def __contains__(self, value: Union[int, list[Any]]) -> bool:
    return value in self.rows
  
  def has_key(self, key: int) -> bool:
    return key in self.rows

  # basic getter and setter methods

  @property
  def identifiers(self) -> list[int]:
    return sorted(list(self.rows.keys()))

  def get_identifier_name(self) -> str:
    return self.column_names[0]  # identifier name will always be the first element in the column_names list
  
  def get_non_identifier_column_names(self) -> list[str]:
    if len(self.column_names) == 1:
      return []
    return self.column_names[1:]

  def to_file(self) -> dict[str, Any]:
    file: dict[str, Any] = {}

    file["column_names"] = self.column_names

    rows: list[dict[str, Any]] = []
    identifier_name: str = self.get_identifier_name()
    remaining_columns: list[str] = []
    file_row: dict[str, Any] = {}
    for (identifier, table_row) in self.rows.items():
      file_row[identifier_name] = identifier # sets the first value to be the identifier
      remaining_columns = self.get_non_identifier_column_names() # goes through every column except the identifier
      for (i, column_name) in enumerate(remaining_columns):
        file_row[column_name] = table_row[i]
      rows.append(file_row.copy()) # a copy is used, as if it were not, then all of the rows would be stored with the same data as the most recently saved one

    file["rows"] = rows
    return file

  # SELECT columns FROM rows WHERE condition ORDER BY order
  def select(self, columns: list[str], condition: Condition) -> dict[int, list[Any]]:
    non_identifier_column_names: list[str] = self.get_non_identifier_column_names()
    if columns[0] == "*":
      columns = non_identifier_column_names
    selected_column_indexes: list[int] = []
    for (i, column_name) in enumerate(non_identifier_column_names):
      if column_name in columns:
        selected_column_indexes.append(i)

    selected_rows: dict[int, Any] = filter_dictionary(self.rows, condition)
    for (identifier, row) in selected_rows.items():
      filtered_row = []
      for i in selected_column_indexes:
        filtered_row.append(row[i])
      selected_rows[identifier] = filtered_row

    return selected_rows
  
  def update(self, columns_to_values: dict[str, Any], condition: Condition) -> None:
    rows_to_update: dict[int, list[Any]] = filter_dictionary(self.rows, condition)
    identifiers_to_update: list[int] = list(rows_to_update.keys())
    column_name: str = ""
    updated_rows: dict[int, list[Any]] = {}
    non_identifier_column_names: list[str] = self.get_non_identifier_column_names()
    for identifier in identifiers_to_update:
      fields_to_update = rows_to_update[identifier]
      for (i, column_name) in enumerate(non_identifier_column_names):
        try:
          column_value = columns_to_values[column_name]
        except:
          continue
        fields_to_update[i] = column_value
      updated_rows[identifier] = fields_to_update
    for identifier in updated_rows:
      self[identifier] = updated_rows[identifier]

  def delete_from(self, condition: Condition) -> None:
    """Deletes all values from the table where the condition statement evaluates to `True`."""
    condition_inverse: Condition = get_condition_inverse(condition)
    undeleted_rows: dict[int, list[Any]] = filter_dictionary(self.rows, condition_inverse)
    self.rows = undeleted_rows
  
  def format_raw_row(self, raw_row: dict[str, Any]) -> list[Any]:
    """Turns a dictionary of the form `column: field` to an array of fields in order *without* the identifier"""
    formatted_row: list[Any] = []
    non_identifier_column_names: list[str] = self.get_non_identifier_column_names()
    for column_name in non_identifier_column_names:
      try:
        value = raw_row[column_name]
      except:
        value = None
      formatted_row.append(value)
    return formatted_row
  
  def insert_with_identifier(self, raw_row: dict[str, Any], identifier: int) -> None:
    """Inserts a new record at a given identifier. Raises an error if the identifier has already been assigned."""
    existing_identifiers: list[int] = list(self.rows.keys())
    if identifier in existing_identifiers: raise InsertAtExistingIdentifierError(identifier, self.name)
    self[identifier] = self.format_raw_row(raw_row)

  #insert
  def insert(self, raw_row: dict[str, Any]) -> int:
    identifier: int = get_next_available_identifier(self.rows)
    self.insert_with_identifier(raw_row, identifier)
    return identifier
  
  def get_next_available_identifier(self) -> int:
    """Calculates the smallest, non-zero identifier not in the table."""
    previous_id: int = -1 # defining variables
    previous_id_successor: int = 0 
    for current_id in self.identifiers:
      previous_id_successor = previous_id+1
      if current_id > previous_id_successor: # if there is a hole in the sequence (e.g. [1,2,4,5] would return 3)
        return previous_id_successor
      previous_id = current_id # sets up for next iteration
    previous_id_successor = previous_id+1
    return previous_id_successor # in the case there are no holes, then it returns the id outside of the list 

  #add_column
  def add_column(self, name: str) -> None:
    if name in self.column_names:
      raise Exception(f"Column `{name}` already exists.")
    self.column_names.append(name)
    for identifier in self.rows.keys():
      self[identifier].append(None)

  #drop_column
  def drop_column(self, name: str) -> None:
    if not (name in self.column_names):
      raise Exception(f"Cannot remove column `{name}` which does not exist.")
    non_identifier_column_names: list[str] = self.get_non_identifier_column_names()
    new_column_names: list[str] = []
    dropped_index: int = -1
    for (i, column_name) in enumerate(non_identifier_column_names):
      if column_name == name:
        dropped_index = i
      else:
        new_column_names.append(column_name)
    
    self.column_names = new_column_names
    
    for (identifier, row) in self.rows.items():
      new_row = []
      for (i, field) in enumerate(row):
        if i != dropped_index:
          new_row.append(field)
      self[identifier] = new_row

  #rename_column
  def rename_column(self, name: str, new_name: str) -> None:
    for (i, column_name) in enumerate(self.column_names):
      if column_name == name:
        self.column_names[i] = new_name

  #rename_table
  def rename_table(self, new_name) -> None:
    self.name = new_name