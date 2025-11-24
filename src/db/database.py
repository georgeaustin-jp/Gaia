from db.table import Table
from db.condition import Condition
from db.file_handler import FileHandler

class Database:
  def __init__(self, name: str, tables: dict[str, Table] = {}) -> None:
    self.name: str = name
    self.tables: dict[str, Table] = tables
    self.file_handler = FileHandler()
    self.table_names: list = []
    self.deleted_table_names: list = []
  
  def exists(self) -> bool:
    main_data = self.load_main_data()
    if main_data == []:
      return False
    return True

  # fetches the database from storage
  def load(self) -> None:
    self.table_names = self.load_main_data()
    for table_name in self.table_names:
      raw_table: dict = self.file_handler.load_file(table_name)
      self.load_table(table_name, raw_table)

  # fetches each table from secondary storage
  def load_table(self, table_name: str, raw_table: dict) -> None:
    column_names: list = raw_table["column_names"] 

    table = Table(table_name, column_names)

    identifier_name: str = column_names[0] # identifier name will always be the first element in the column_names list
    identifier: int = 0
    rows: list = raw_table["rows"]
    for row in rows: # stores each value in the table
      identifier = row[identifier_name]
      table.insert_with_identifier(row, identifier)
    self.tables[table_name] = table

  def load_main_data(self) -> list:
    try:
      main_data: list = self.file_handler.load_file("MAIN")["tables"]
    except:
      main_data = list(self.tables.keys())
    return main_data

  def save(self) -> None:
    self.save_main_data()
    for table_name in self.table_names:
      self.save_table(table_name)
    for deleted_table_name in self.deleted_table_names:
      self.file_handler.delete_file(deleted_table_name)

  def save_main_data(self) -> None:
    main_data: dict = {"tables": self.table_names}
    self.file_handler.save_file("MAIN", main_data)

  def save_table(self, table_name: str) -> None:
    table: Table = self.find_table(table_name)
    file: dict = table.to_file()
    self.file_handler.save_file(table_name, file)

  def find_table(self, table_name: str) -> Table:
    try:
      table: Table = self.tables[table_name]
    except:
      raise Exception(f"Table `{table_name}` does not exist.")
    return table

  # SELECT columns FROM table WHERE condition ORDER BY order
  def select(self, table_name: str, columns: list[str], condition: Condition) -> dict[int, list]:
    return self.find_table(table_name).select(columns, condition)
  
  #update
  def update(self, table_name: str, columns_to_values, condition: Condition) -> None:
    table: Table = self.find_table(table_name)
    table.update(columns_to_values, condition)

  #delete_from
  def delete_from(self, table_name: str, condition: Condition) -> None:
    table: Table = self.find_table(table_name)
    table.delete_from(condition)

  #insert
  def insert(self, table_name: str, fields) -> None:
    self.find_table(table_name).insert(fields)

  def create_table(self, table_name: str, column_names: list[str]) -> None:
    if table_name in self.table_names:
      raise Exception(f"Table `{table_name}` already exists.")
    table: Table = Table(table_name, column_names)
    self.tables[table_name] = table
    self.table_names.append(table_name)

  def delete_table(self, table_name: str) -> None:
    self.table_names = list(filter(lambda element : element != table_name, self.table_names))
    self.deleted_table_names.append(table_name)
    self.tables.pop(table_name)

  #add_column
  def add_column(self, table_name: str, column_name: str) -> None:
    self.find_table(table_name).add_column(column_name)

  #drop_column
  def drop_column(self, table_name: str, column_name: str) -> None:
    self.find_table(table_name).drop_column(column_name)

  #rename_column
  def rename_column(self, table_name: str, name: str, new_name: str) -> None:
    self.find_table(table_name).rename_column(name, new_name)

  #rename_table
  def rename_table(self, table_name: str, new_name: str) -> None:
    table: Table = self.find_table(table_name)
    table.rename_table(new_name)
    self.tables[new_name] = self.tables.pop(table_name)