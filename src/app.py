from db.condition import Condition
from db.database import Database
from interface.interface import Interface
from game_data import GameData

class App:
  def __init__(self) -> None:
    self.game_data = GameData()

    self.dynamic_table_templates: dict[str, list] = {
      "User": ["UserID", "Name", "PasswordHash", "CharacterQuantity", "WorldQuantity"],
      "Character": ["CharacterID", "UserID", "Name", "Health", "MaxHealth"],
      "ItemAbility": ["ItemAbilityID", "ItemID", "AbilityID"],
      "CharacterModifier": ["CharacterModifierID", "CharacterID", "AbilityID", "RemainingTurns"],
      "World": ["WorldID", "UserID", "Name", "Seed"]
    }
    self.static_table_templates: dict[str, list] = {
      "Item": ["ItemID", "ItemType", "Name"],
      "Weapon": ["WeaponID", "ItemID", "Damage", "UsesAmmunition", "ManaUsed"],
      "AmmunitionBox": ["AmmunitionBoxID", "ItemID", "Damage"],
      "Equipable": ["EquipableID", "ItemID"],
      "Consumable": ["ConsumableID", "ItemID"],
      "Ability": ["AbilityID", "Text", "Type"],
      "StatisticAbility": ["StatisticAbilityID", "AbilityID", "AffectedStatistic", "Amount"],
      "EffectAbility": ["EffectAbilityID", "AbilityID", "Effect"],
    }

    self.load_game_data()

    users: list = list(self.game_data.users.values())
    self.interface = Interface(users=users, quit_command=self.quit_command)

  def load_game_data(self) -> None:
    if not self.game_data.database_exists():
      self.create_database()
    self.game_data.load()

  def create_database(self) -> None:
    self.game_data.database.create_main()
    self.create_static_tables()
    self.create_dynamic_tables()
    self.save()

  def create_static_tables(self) -> None:
    for (table_name, table_columns) in self.static_table_templates.items():
      self.game_data.database.create_table(table_name, table_columns)

  def create_dynamic_tables(self) -> None:
    for (table_name, table_columns) in self.dynamic_table_templates.items():
      self.game_data.database.create_table(table_name, table_columns)

  def save(self) -> None:
    self.game_data.database.save()

  def set_up(self) -> None:
    pass

  def run(self) -> None:
    users: list = list(self.game_data.users.values())
    self.interface.run(users)

  def quit_command(self) -> None:
    self.save()
    quit(1)