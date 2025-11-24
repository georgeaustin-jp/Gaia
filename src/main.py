#from db.database import Database
#import db.table as table
#from db.condition import Condition
from interface.interface import Interface
from app import App
#from interface.character_selection import CharacterSelection

def main() -> None:
  app = App()
  app.run()

if __name__ == "__main__": main()