from db.database import Database
#import db.table as table
from db.condition import Condition
from interface.interface import Interface
#from interface.character_selection import CharacterSelection

def main() -> None:
  #inter = Interface()
  db = Database("main")
  db.load()
  cnd = Condition(lambda _identifier, _row: True)
  print(db.select("User", ["Name"], cnd))

if __name__ == "__main__": main()