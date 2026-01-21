import toml
import os
import pathlib
import re

from tools.typing_tools import *
from tools.custom_exceptions import PathError

from database.config_data import ConfigData

class FileHandler:
  def __init__(self, ) -> None:
    self.__current_path: str = self.get_current_path()

  def get_current_path(self) -> str:
    full_path: pathlib.Path = pathlib.Path().resolve()
    full_path_str: str = str(full_path)
    (_, current_path) = os.path.split(full_path_str)
    return current_path

  def data_path(self) -> str:
    if re.match(r'Gaia(-[0-9]+\.[0-9]+\.[0-9]+(-(alpha|beta))?)?', self.__current_path):
      return os.path.join("data")
    raise PathError(self.__current_path)
  
  # directory methods
  
  def does_data_directory_exist(self) -> bool: return os.path.isdir(self.data_path())
  
  def create_directory(self, directory_name: str) -> None:
    directory_path: str = os.path.join(directory_name)
    os.mkdir(directory_path)

  # file methods

  def toml_file_path(self, file_name: str, in_data_directory: bool = True) -> str:
    toml_suffix: str = "toml"
    file_name_suffix: str = file_name.split(".")[-1]
    if file_name_suffix != toml_suffix:
      file_name = file_name + f".{toml_suffix}"
    if in_data_directory:
      return os.path.join(self.data_path(), file_name)
    return os.path.join(file_name)

  def save_file(self, file_name: str, data: dict[str, Any]) -> None:
    file_path: str = self.toml_file_path(file_name)
    with open(file_path, 'w') as f:
      toml.dump(data, f)
    
  def load_file(self, file_name: str, in_data_directory: bool = True) -> dict[str, Any]:
    file_path: str = self.toml_file_path(file_name, in_data_directory)
    return toml.load(file_path)
  
  def delete_file(self, file_name: str) -> None:
    file_path: str = self.toml_file_path(file_name)
    os.remove(file_path)

  # config methods

  def get_config_data(self) -> ConfigData:
    pyproject_raw_data: dict[str, Any] = self.load_file("pyproject.toml", False)
    project_raw_data: dict[str, Any] = pyproject_raw_data["project"]
    return ConfigData(version=project_raw_data["version"])
