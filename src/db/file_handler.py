import toml
import os

# Note: added because it makes code more readable, more modular and is a different thing to the database itself.

class FileHandler:
  def __init__(self) -> None:
    pass

  @staticmethod
  def file_path(file_name: str) -> str:
    toml_suffix: str = ".toml"
    file_name_length: int = len(file_name)
    file_name_suffix: str = file_name[file_name_length-5:]
    if file_name_suffix != toml_suffix:
      file_name = file_name + toml_suffix
    return os.path.join("src", "data", file_name)

  def save_file(self, file_name: str, data: dict) -> None:
    file_path: str = self.file_path(file_name)
    with open(file_path, 'w') as f:
      toml.dump(data, f)
    
  def load_file(self, file_name: str) -> dict:
    file_path: str = self.file_path(file_name)
    return toml.load(file_path)
  
  def delete_file(self, file_name: str) -> None:
    file_path: str = self.file_path(file_name)
    os.remove(file_path)