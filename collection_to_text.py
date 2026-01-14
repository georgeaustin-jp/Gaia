import logging

logging.basicConfig(level=logging.INFO)

from sys import argv
from os import listdir
from os.path import isfile, join, isdir
from regex import match
from functools import reduce

def is_valid_directory_or_file(directory_path: str) -> bool:
  directory_name: str = directory_path.split("\\")[-1]
  if match("__pycache__", directory_name): return False
  return True

def get_all_data(directory_path: str) -> list[str]:
  if not is_valid_directory_or_file(directory_path): return []
  (directories, files) = get_directory_data(directory_path)
  file_list_data = get_file_list_data(directory_path, files)
  for directory in directories:
    path = join(directory_path, directory)
    directory_data = get_all_data(path)
    file_list_data = directory_data + file_list_data
  return file_list_data

def get_directory_data(directory_path: str) -> tuple[list[str], list[str]]:
  directories: list[str] = [f for f in listdir(directory_path) if isdir(join(directory_path, f))]
  files: list[str] = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
  return (directories, files)

def get_file_list_data(directory_path: str, file_names: list[str]) -> list[str]:
  file_list_data: list[str] = []
  for file_name in file_names:
    file_list_data += get_file_text(directory_path, file_name)
  return file_list_data

def get_file_text(directory_path: str, file_name: str) -> list[str]:
  file_path: str = join(directory_path, file_name)
  with open(file_path, "r") as f:
    contents: list[str] = f.readlines()
  display_file_path_list: list[str] = file_path.split("\\")[1:]
  display_file_path: str = reduce(lambda acc,s: f"{acc}/{s}", display_file_path_list)
  return [f"{display_file_path}\n\n"] + contents + ["\n\nEOF\n"]

def write_result(all_data: list[str], file_name: str):
  with open(file_name, "w") as f:
    f.writelines(all_data)

def main(*args) -> None:
  try: path_name: str = args[1]
  except: path_name = "."
  try: save_file_name: str = args[2]
  except: save_file_name = "output.py"
  all_data: list[str] = get_all_data(path_name)
  write_result(all_data, save_file_name)

if __name__ == "__main__":
  main(*argv)
