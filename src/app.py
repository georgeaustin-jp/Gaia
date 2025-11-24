from db.database import Database
from interface.interface import Interface

class App:
  def __init__(self) -> None:
    self.database = Database("main")
    self.interface = Interface()

  def load_database(self) -> None:
    if not self.database.exists():
      return
    self.database.load()

  def run(self) -> None:
    self.interface.run()