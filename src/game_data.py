from db.database import Database
from db.condition import Condition
from user import User

class GameData:
  def __init__(self) -> None:
    self.database = Database("game_data")
    self.users: dict[int, User] = {}
    self.active_user: User
    self.every = Condition(lambda _identifier, _row: True)

  def database_exists(self) -> bool:
    return self.database.exists()

  def load_database(self) -> None:
    self.database.load()

  def select_from_database(self, table_name: str, columns: list, condition: Condition) -> dict:
    return self.database.select(table_name, columns, condition)
  
  def select_all_from_database(self, table_name: str) -> dict:
    return self.select_from_database(table_name, ["*"], self.every)

  def load_users(self) -> None:
    raw_user_data = self.select_all_from_database("User")
    for (identifier, user_information) in raw_user_data.items():
      user = User(user_information)
      self.users[identifier] = user

  def load(self) -> None:
    self.load_database()
    self.load_users()

  def format_data_to_dictionary(self, table_name: str, raw_data: list) -> dict:
    formatted_data: dict = {}
    non_identifier_column_names: list = self.database.find_table(table_name).get_non_identifier_column_names()
    for (i, column_name) in enumerate(non_identifier_column_names):
      formatted_data[column_name] = raw_data[i]
    return formatted_data

  def update_database(self, table_name: str, raw_data: list, condition: Condition) -> None:
    formatted_data: dict = self.format_data_to_dictionary(table_name, raw_data)
    self.database.update(table_name, formatted_data, condition)

  def update_record(self, table_name: str, identifier: int, raw_data: list) -> None:
    match_condition = Condition(lambda id, _row: id == identifier) 
    self.update_database(table_name, raw_data, match_condition)

  def insert_into_database(self, table_name: str, raw_data: list) -> None:
    formatted_data: dict = self.format_data_to_dictionary(table_name, raw_data)
    self.database.insert(table_name, formatted_data)

  def insert_user(self, raw_data: list) -> None:
    new_user = User(raw_data, True)
    self.insert_into_database("User", raw_data)
    find_user_id = Condition(lambda _identifier, row: row[0] == new_user.name)
    identifiers: list = list(self.select_from_database("User", ["UserID"], find_user_id).keys())
    if len(identifiers) > 1:
      raise Exception(f"User with name `{new_user.name}` already exists")
    identifier: int = identifiers[0]
    self.users[identifier] = new_user

  def save_users(self) -> None:
    for (identifier, user) in self.users.items():
      user_table_name: str = "User"
      user_raw_data: list = user.to_raw_data()
      if user.loaded:
        self.update_record(user_table_name, identifier, user_raw_data)
      else:
        self.insert_into_database(user_table_name, user_raw_data)

  def save_database(self) -> None:
    self.save_users()
    self.database.save()

  def set_active_user(self, user: User) -> None:
    self.active_user = user

  def get_user_names(self) -> list:
    user_names: list = []
    for user in self.users.values():
      user_names.append(user.name) 
    return user_names