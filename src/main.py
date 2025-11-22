from db.database import Database
#import db.table as table
#import db.condition as condition
from interface.interface import Interface
#from interface.character_selection import CharacterSelection

def main() -> None:
  #inter = Interface()
  db = Database("main")
  db.load()
  db.delete_table("First")
  db.create_table("User", ["UserID", "Name", "PasswordHash", "CharacterQuantity", "WorldQuantity"])
  db.insert("User", {"Name": "Jeremiah", "PasswordHash": "1234", "WorldQuantity": 0})
  db.save()

if __name__ == "__main__": main()