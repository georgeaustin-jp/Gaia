from tools.typing_tools import *
from tools.constants import TableName

from database.table import Table
from database.condition import Condition
from database.file_handler import FileHandler
from database.database_main_data import DatabaseMainData
from database.config_data import ConfigData

class Database:
  def __init__(self, name: str, tables: dict[str, Table] = {}, table_names: list[str] = []) -> None:
    self.name: str = name
    self.tables: dict[str, Table] = tables
    self.file_handler = FileHandler()
    self.table_names = table_names
    self.deleted_table_names: list[str] = []

    self.config_data: ConfigData = self.get_config_data()

    self.save_on_delete: bool = True

  # built-in methods

  def __del__(self) -> None:
    if self.save_on_delete:
      self.save()

  # other

  def get_config_data(self) -> ConfigData:
    return self.file_handler.get_config_data()
  
  def exists(self) -> bool:
    """Uses the `file_handler.does_data_directory_exist()` method to determine whether the database has already been created in memory or not."""
    if self.file_handler.does_data_directory_exist(): return True
    return False
  
  def create_main(self, table_names: list[str] = []) -> None:
    if not self.file_handler.does_data_directory_exist():
      self.file_handler.create_directory("data")
    if table_names != []: self.table_names = table_names
    main_data: DatabaseMainData = DatabaseMainData(self.table_names, self.config_data.version)
    self.file_handler.save_file("MAIN", main_data.to_dict())

  def init_tables(self, table_templates: dict[TableName, list[str]]) -> None:
    for (table_name, columns) in table_templates.items():
      self.create_table(table_name, columns)

  def load(self) -> None:
    """Fetches the database from storage, loading all tables specified in `self.table_names`. Raises a `ValueError` if `self.table_names` is empty."""
    main_data: DatabaseMainData = self.load_main_data()
    table_names: list[str] = main_data.table_names
    version: str = main_data.version
    if table_names == []: raise ValueError(f"Expected a non-empty list of table names; instead got {table_names}.")
    self.table_names = table_names
    for table_name in self.table_names:
      raw_table: dict = self.file_handler.load_file(table_name)
      self.load_table(table_name, raw_table)

  def load_table(self, table_name: str, raw_table: dict[str, Any]) -> None:
    """Fetches each table from secondary storage."""
    column_names: list = raw_table["column_names"] 

    table = Table(table_name, column_names)

    identifier_name: str = column_names[0] # identifier name will always be the first element in the column_names list
    identifier: int = 0
    rows: list[Any] = raw_table["rows"]
    for row in rows: # stores each value in the table
      identifier = row[identifier_name]
      table.insert_with_identifier(row, identifier)
    self.tables[table_name] = table

  def load_main_data(self) -> DatabaseMainData:
    if self.file_handler.does_data_directory_exist():
      raw_main_data: dict[str, Any] = self.file_handler.load_file("MAIN")
      main_data: DatabaseMainData = DatabaseMainData(raw_main_data["table_names"], raw_main_data["version"])
    else: raise Exception(f"`data` directory doesn't exist.")
    return main_data

  def save(self) -> None:
    self.save_main_data()
    for table_name in self.table_names:
      self.save_table(table_name)
    for deleted_table_name in self.deleted_table_names:
      self.file_handler.delete_file(deleted_table_name)

  def save_main_data(self) -> None:
    main_data: DatabaseMainData = DatabaseMainData(self.table_names, self.config_data.version)
    if main_data.table_names == []:
      main_data = self.load_main_data()
    self.file_handler.save_file("MAIN", main_data.to_dict())

  def save_table(self, table_name: str) -> None:
    table: Table = self.find_table(table_name)
    file: dict = table.to_file()
    self.file_handler.save_file(table_name, file)

  def is_version_updated(self) -> bool:
    main_data: DatabaseMainData = self.load_main_data()
    if main_data.version != self.config_data.version: return True
    return False
  
  def is_identifier_in_table(self, identifier: int, table_name: str) -> bool:
    return self.find_table(table_name).has_key(identifier)

  # SQL queries

  def find_table(self, table_name: str) -> Table:
    try:
      table: Table = self.tables[table_name]
    except:
      raise NameError(f"Table {table_name} does not exist.")
    return table

  def select(self, table_name: str, columns: list[str], condition: Condition) -> dict[int, list[Any]]:
    return self.find_table(table_name).select(columns, condition)
  
  def update(self, table_name: str, columns_to_values: dict[str, Any], condition: Condition) -> None:
    table: Table = self.find_table(table_name)
    table.update(columns_to_values, condition)

  def delete_from(self, table_name: str, condition: Condition) -> None:
    table: Table = self.find_table(table_name)
    table.delete_from(condition)

  def insert(self, table_name: str, columns_to_values: dict[str, Any], identifier: Optional[int] = None) -> Optional[int]:
    """Inserts a new record into a specified table, returning the identifier of the newly created record."""
    table: Table = self.find_table(table_name)
    if identifier == None: return table.insert(columns_to_values)
    else: return table.insert_with_identifier(columns_to_values, identifier)

  def create_table(self, table_name: str, column_names: list[str]) -> None:
    """Initialises the given table in memory."""
    if table_name in self.table_names:
      raise BufferError(f"Table {table_name} already exists.")
    table = Table(table_name, column_names)
    self.tables[table_name] = table
    self.table_names.append(table_name)

  def delete_table(self, table_name: str) -> None:
    self.table_names = list(filter(lambda element : element != table_name, self.table_names))
    self.deleted_table_names.append(table_name)
    self.tables.pop(table_name)

  def add_column(self, table_name: str, column_name: str) -> None:
    self.find_table(table_name).add_column(column_name)

  def drop_column(self, table_name: str, column_name: str) -> None:
    self.find_table(table_name).drop_column(column_name)

  def rename_column(self, table_name: str, name: str, new_name: str) -> None:
    self.find_table(table_name).rename_column(name, new_name)

  def rename_table(self, table_name: str, new_name: str) -> None:
    table: Table = self.find_table(table_name)
    table.rename_table(new_name)
    self.tables[new_name] = self.tables.pop(table_name)