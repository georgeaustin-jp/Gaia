import toml
import os
import sys

from tools.typing_tools import *

# Note: added because it makes code more readable, more modular and is a different thing to the database itself.

class FileHandler:
  def __init__(self) -> None:
    pass

  @staticmethod
  def data_path() -> str:
    return os.path.join("src", "data")

  @staticmethod
  def file_path(file_name: str) -> str:
    toml_suffix: str = ".toml"
    file_name_length: int = len(file_name)
    file_name_suffix: str = file_name[file_name_length-5:]
    if file_name_suffix != toml_suffix:
      file_name = file_name + toml_suffix
    return os.path.join(FileHandler.data_path(), file_name)
  
  def does_data_directory_exist(self) -> bool:
    return os.path.isdir(self.data_path())
  
  def create_directory(self, directory_name: str) -> None:
    directory_path: str = os.path.join("src", directory_name)
    os.mkdir(directory_path)

  def save_file(self, file_name: str, data: dict[str, Any]) -> None:
    file_path: str = self.file_path(file_name)
    with open(file_path, 'w') as f:
      toml.dump(data, f)
    
  def load_file(self, file_name: str) -> dict[str, Any]:
    file_path: str = self.file_path(file_name)
    return toml.load(file_path)
  
  def delete_file(self, file_name: str) -> None:
    file_path: str = self.file_path(file_name)
    os.remove(file_path)