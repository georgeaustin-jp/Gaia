import logging

logging.basicConfig(level=logging.INFO)

from typing import Any

from sys import argv
from os import listdir
from os.path import isfile, join, isdir
from functools import reduce
import toml
import re

# counting data

type FileCount = int
type FullCountData = tuple[FileCount, FileCountData]

type FileCountData = tuple[LineCount, WordCount, CharCount]
type LineCount = int
type WordCount = int
type CharCount = int

def get_file_counts(contents: list[str]) -> FileCountData:
  return (get_file_line_count(contents), get_file_word_count(contents), get_file_char_count(contents))

def add_file_count_data(x: FileCountData, y: FileCountData) -> FileCountData:
  return (x[0] + y[0], x[1] + y[1], x[2] + y[2])

def add_full_count_data(x: FullCountData, y: FullCountData) -> FullCountData:
  return (x[0] + y[0], add_file_count_data(x[1], y[1]))

def get_file_line_count(contents: list[str]) -> LineCount:
  return len(contents)

def get_file_word_count(contents: list[str]) -> WordCount:
  word_count: int = 0
  for line in contents:
    words = re.findall(r'\b\w+\b', line)
    word_count += len(words)
  return word_count

def get_file_char_count(contents: list[str]) -> CharCount:
  char_count: int = 0
  for line in contents:
    char_count += len(line)
  return char_count

# getting the data from the files
## config
def get_config_data(config_file_path: str = "collection_to_text_config.toml") -> dict[str, Any]:
  if not isfile(config_file_path): raise Exception()
  with open(config_file_path, "r") as f:
    config_data: dict[str, Any] = toml.load(f)
  return config_data

## main data
def is_valid_directory_or_file(directory_path: str, expression: str) -> bool:
  directory_name: str = directory_path.split("\\")[-1]
  if re.fullmatch(expression, directory_name) != None: return False
  return True

def get_all_data(directory_path: str, expression: str) -> tuple[list[str], FullCountData]:
  if not is_valid_directory_or_file(directory_path, expression): return ([], (0,(0,0,0)))
  (directories, files) = get_directory_data(directory_path)
  (file_list_data, full_count_data) = get_file_list_data(directory_path, files)
  complete_directory_data: list[str] = []
  for directory in directories:
    path = join(directory_path, directory)
    (directory_data, directory_full_count_data) = get_all_data(path, expression)
    complete_directory_data += directory_data
    full_count_data = add_full_count_data(full_count_data, directory_full_count_data)
  file_list_data = complete_directory_data + file_list_data
  return (file_list_data, full_count_data)

def get_directory_data(directory_path: str) -> tuple[list[str], list[str]]:
  directories: list[str] = sorted([f for f in listdir(directory_path) if isdir(join(directory_path, f))])
  files: list[str] = sorted([f for f in listdir(directory_path) if isfile(join(directory_path, f))])
  return (directories, files)

def get_file_list_data(directory_path: str, file_names: list[str]) -> tuple[list[str], FullCountData]:
  file_list_data: list[str] = []
  file_count: FileCount = 0
  file_count_data: FileCountData = (0,0,0)
  for file_name in file_names:
    (file_text, file_counts) = get_file_text(directory_path, file_name)
    file_list_data += file_text
    file_count_data = add_file_count_data(file_count_data, file_counts)
    file_count += 1
  return (file_list_data, (file_count, file_count_data))

def get_file_text(directory_path: str, file_name: str) -> tuple[list[str], FileCountData]:
  file_path: str = join(directory_path, file_name)
  with open(file_path, "r") as f:
    contents: list[str] = f.readlines()
  display_file_path_list: list[str] = file_path.split("\\")[1:]
  display_file_path: str = reduce(lambda acc,s: f"{acc}/{s}", display_file_path_list)
  return ([f"\n\n# > FILE - '{display_file_path}'\n"] + contents, get_file_counts(contents))

# storing data

def write_result(all_data: list[str], file_name: str) -> None:
  with open(file_name, "w") as f:
    f.writelines(all_data)

def write_full_count_data(full_count_data: FullCountData, directory_name: str) -> None:
  (file_count, file_count_data) = full_count_data
  (line_count, word_count, char_count) = file_count_data
  file_data: dict[str, Any] = {directory_name: {"file_count": file_count, "line_count": line_count, "word_count": word_count, "char_count": char_count}}
  file_name = join(f"{directory_name}_count_data.toml")
  with open(file_name, 'w') as f:
    toml.dump(file_data, f)

def create_config() -> None:
  config_file_name: str = "collection_to_text_config.toml"
  config_data: dict[str, Any] = {
    "path_name": "/", # starting directory
    "save_file_name": "output.md", # name of the output file
    "ignore": "__pycache__|data", # regex which ignores all files and directories that match
  }
  with open(config_file_name, "w") as f:
    toml.dump(config_data, f)

def write_file_structure(file_structure: str) -> None:
  with open("file_structure.txt", "w") as f:
    f.write(file_structure)

# file structure

def get_file_structure(directory_path: str, expression: str, prefix: str = "") -> str:
  current_directory: str = directory_path.split("\\")[-1]
  (directories, file_names) = get_directory_data(directory_path)
  result: str = f"{prefix}{current_directory}"
  next_layer_prefix: str = f"{prefix}| "
  for next_layer_directory in directories:
    if not is_valid_directory_or_file(next_layer_directory, expression): continue
    next_layer_directory_path = join(directory_path, next_layer_directory)
    next_layer_structure: str = get_file_structure(next_layer_directory_path, expression, next_layer_prefix)
    result += f"\n{next_layer_structure}"
  for file_name in file_names:
    result += f"\n{next_layer_prefix}{file_name}"
  return result

def main(*args) -> None:
  try:
    config_data: dict[str, Any] = get_config_data()
  except:
    create_config()
    logging.warning(f"`collection_to_text_config.toml` file not found. Please check and edit the one which was automatically created.")
    return
  path_name: str = config_data["path_name"]
  save_file_name: str = config_data["save_file_name"]
  ignore_expression: str = config_data["ignore"]
  (all_data, full_count_data) = get_all_data(path_name, ignore_expression)
  file_structure: str = get_file_structure(path_name, ignore_expression)
  write_result(all_data, save_file_name)
  write_full_count_data(full_count_data, path_name)
  write_file_structure(file_structure)

if __name__ == "__main__":
  main(*argv)
