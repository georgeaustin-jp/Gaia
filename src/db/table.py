from db.condition import Condition

class Table:
  def __init__(self, name: str, column_names: list[str]) -> None:
    self.name: str = name
    self.column_names: list[str] = column_names
    self.rows: dict[int, list] = {}

  def get_identifier_name(self) -> str:
    return self.column_names[0]  # identifier name will always be the first element in the column_names list
  
  def get_non_identifier_column_names(self) -> list:
    if len(self.column_names) == 1:
      return []
    return self.column_names[1:]
  
  @staticmethod
  def filter_dictionary(dictionary: dict, condition: Condition) -> dict:
    return {key: val for key, val in dictionary.items() if condition.evaluate(key,val)}

  def to_file(self) -> dict:
    file: dict = {}

    file["column_names"] = self.column_names

    rows: list = []
    identifier_name: str = self.get_identifier_name()
    remaining_columns: list = []
    file_row: dict = {}
    for (identifier, table_row) in self.rows.items():
      file_row[identifier_name] = identifier # sets the first value to be the identifier
      remaining_columns = self.get_non_identifier_column_names() # goes through every column except the identifier
      for (i, column_name) in enumerate(remaining_columns):
        file_row[column_name] = table_row[i]
      rows.append(file_row.copy()) # a copy is used, as if it were not, then all of the rows would be stored with the same data as the most recently saved one

    file["rows"] = rows
    return file

  # SELECT columns FROM rows WHERE condition ORDER BY order
  def select(self, columns: list[str], condition: Condition) -> dict[int, list]:
    selected_column_indexes: list = []
    non_identifier_column_names: list = self.get_non_identifier_column_names()
    for (i, column_name) in enumerate(non_identifier_column_names):
      if column_name in columns:
        selected_column_indexes.append(i)

    selected_rows: dict = self.filter_dictionary(self.rows, condition)
    for (identifier, row) in selected_rows.items():
      filtered_row = []
      print(identifier, row)
      for i in selected_column_indexes:
        filtered_row.append(row[i])
      selected_rows[identifier] = filtered_row

    return selected_rows
  
  #update
  def update(self, columns_to_values: dict, condition: Condition) -> None:
    rows_to_update: dict = self.filter_dictionary(self.rows, condition)
    identifiers_to_update: list = list(rows_to_update.keys())
    column_name: str = ""
    updated_rows: dict = {}
    non_identifier_column_names: list = self.get_non_identifier_column_names()
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
      self.rows[identifier] = updated_rows[identifier]

  #delete_from
  def delete_from(self, condition: Condition) -> None:
    undeleted_rows: dict = self.filter_dictionary(self.rows, condition)
    self.rows = undeleted_rows

  def get_next_available_identifier(self) -> int:
    previous_key: int = -1
    previous_key_successor: int = 0 # defining variables
    for current_key in self.rows.keys():
      previous_key_successor = previous_key+1
      if current_key != previous_key_successor: # if there is a hole in the sequence (e.g. [1,2,4,5] would return 3)
        return previous_key_successor
      previous_key = current_key # sets up for next iteration
    previous_key_successor = previous_key+1
    return previous_key_successor # in the case there are no holes, then it returns the key outside of the list 
  
  # Turns a dictionary of the form `column: field` to an array of fields in order *without* the identifier
  def format_raw_row(self, raw_row: dict) -> list:
    formatted_row: list = []
    non_identifier_column_names: list = self.get_non_identifier_column_names()
    for column_name in non_identifier_column_names:
      try:
        value = raw_row[column_name]
      except:
        value = None
      formatted_row.append(value)
    return formatted_row
  
  #TODO: make more secure 
  def insert_with_identifier(self, raw_row: dict, identifier: int) -> None:
    self.rows[identifier] = self.format_raw_row(raw_row)

  #insert
  def insert(self, raw_row: dict) -> None:
    identifier: int = self.get_next_available_identifier()
    self.insert_with_identifier(raw_row, identifier)

  #add_column
  def add_column(self, name: str) -> None:
    if name in self.column_names:
      raise Exception(f"Column `{name}` already exists.")
    self.column_names.append(name)
    for identifier in self.rows.keys():
      self.rows[identifier].append(None)

  #drop_column
  def drop_column(self, name: str) -> None:
    if not (name in self.column_names):
      raise Exception(f"Cannot remove column `{name}` which does not exist.")
    non_identifier_column_names: list = self.get_non_identifier_column_names()
    new_column_names: list = []
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
      self.rows[identifier] = new_row

  #rename_column
  def rename_column(self, name: str, new_name: str) -> None:
    for (i, column_name) in enumerate(self.column_names):
      if column_name == name:
        self.column_names[i] = new_name

  #rename_table
  def rename_table(self, new_name) -> None:
    self.name = new_name