from tools.typing_tools import *
from tools.logging_tools import *
from tools.constants import *
from tools.dictionary_tools import filter_dictionary, get_next_available_identifier
from tools.generation_tools import *
from tools.ability_names import *

from database.database import Database
from database.condition import Condition, everything, nothing, matching_identifiers

from stored.stored import Stored
from stored.user import User
from stored.entities.character import Character
from stored.modifiers.character_modifier import CharacterModifier
from stored.world import World

from stored.items.item import Item
from stored.items.inventory_item import InventoryItem
from stored.items.weapon import Weapon
from stored.items.equipable import Equipable
from stored.items.storage import Storage
from stored.items.storage_item import StorageItem

from stored.abilities.ability import Ability
from stored.abilities.parry_ability import ParryAbility
from stored.abilities.statistic_ability import StatisticAbility
from stored.abilities.item_ability import ItemAbility
from stored.abilities.enemy_ability import EnemyAbility

from data_structures.fighting_enemy_graph import FightingEnemyGraph
from custom_tkinter.toggleable_button import ToggleableButton
from stored.entities.enemy import Enemy
from stored.entities.fighting_enemy import FightingEnemy
from stored.modifiers.fighting_enemy_modifier import FightingEnemyModifier

from data_structures.queue import Queue

class GameData:
  def __init__(self) -> None:
    self.save_on_delete: bool = True # determines whether the current state of the database will be saved once it is deleted

    self.database = Database("game_data")

    self.users: dict[int, User] = {}
    self.active_user_id: Optional[int] = 0 # defaults as 0

    self.characters: dict[int, Character] = {}
    self.active_character_id = None
    self.character_modifiers: dict[int, CharacterModifier] = {}

    self.worlds: dict[int, World] = {}
    self.active_world_id: Optional[int] = None

    self.items: dict[int, Item] = {}
    self.inventory_items: dict[int, InventoryItem] = {}

    self.storages: dict[int, Storage] = {}
    self.storage_items: dict[int, StorageItem] = {}
    self.active_storage_id: Optional[int] = None # placeholder, TODO: set default value to `None`
    self.home_storage: Optional[int] = None
    self.away_storage: Optional[int] = None

    self.weapons: dict[int, Weapon] = {}
    self.equipables: dict[int, Equipable] = {}

    self.enemies: dict[int, Enemy] = {}
    self.fighting_enemies: dict[int, FightingEnemy] = {}
    self.fighting_enemy_graph = FightingEnemyGraph()
    self.fighting_enemy_modifiers: dict[int, FightingEnemyModifier] = {}
    self.enemy_abilities: dict[int, EnemyAbility] = {}

    self.abilities: dict[int, Ability] = {}
    self.parry_abilities: dict[int, ParryAbility] = {}
    self.statistic_abilities: dict[int, StatisticAbility] = {}

    self.item_abilities: dict[int, ItemAbility] = {}

    # Each entry contains target type as the key with a tuple as the value
    # The first element is the variable name to which the `Stored` type should be stored in within the `GameData` object
    # The next element is a boolean value denoting whether that target will be saved or loaded to the database as well
    self.save_load_targets: dict[type[Stored], Union[StorageAttrName, tuple[StorageAttrName, bool]]] = { 
      User: StorageAttrName.USERS,
      Character: StorageAttrName.CHARACTERS,
      CharacterModifier: (StorageAttrName.CHARACTER_MODIFIERS, False),

      World: StorageAttrName.WORLDS,

      Item: StorageAttrName.ITEMS,
      InventoryItem: StorageAttrName.INVENTORY_ITEMS,
      Weapon: StorageAttrName.WEAPONS,
      Equipable: StorageAttrName.EQUIPABLES,

      Storage: StorageAttrName.STORAGES,
      StorageItem: StorageAttrName.STORAGE_ITEMS,

      Enemy: StorageAttrName.ENEMIES,
      FightingEnemy: (StorageAttrName.FIGHTING_ENEMIES, False),
      FightingEnemyModifier: (StorageAttrName.FIGHTING_ENEMY_MODIFIERS, False),
      EnemyAbility: StorageAttrName.ENEMY_ABILITIES,

      Ability: StorageAttrName.ABILITIES,
      ParryAbility: StorageAttrName.PARRY_ABILITIES,
      StatisticAbility: StorageAttrName.STATISTIC_ABILITIES,
      ItemAbility: StorageAttrName.ITEM_ABILITIES,
    }

    self.table_templates: dict[TableName, list[str]] = { # comments next to templates indicate whether each has been given their own storage variables in `GameData`
      TableName.USER: ["UserID", "Name", "PasswordHash", "CharacterQuantity", "WorldQuantity"], # Y
      TableName.CHARACTER: ["CharacterID", "UserID", "Name", "Health", "MaxHealth"], # Y
      TableName.WORLD: ["WorldID", "UserID", "Name", "Seed"], # Y
      TableName.INVENTORY_ITEM: ["InventoryItemID", "CharacterID", "ItemID", "StackSize", "Equipped"], # Y
      TableName.STORAGE: ["StorageID", "WorldID", "StorageType"], # Y
      TableName.STORAGE_ITEM: ["StorageItemID", "StorageID", "ItemID", "StackSize"], # Y

      TableName.ITEM: ["ItemID", "ItemType", "Name"], # Y
      TableName.ITEM_ABILITY: ["ItemAbilityID", "ItemID", "AbilityID"], # Y
      TableName.WEAPON: ["WeaponID", "ItemID", "Damage", "UsesAmmunition", "ManaUsed", "Active"], # Y
      TableName.EQUIPABLE: ["EquipableID", "ItemID"], # Y
      TableName.ABILITY: ["AbilityID", "Text", "Type"], # Y
      TableName.PARRY_ABILITY: ["ParryAbilityID", "AbilityID", "DamageThreshold", "ReflectionProportion"], # Y
      TableName.STATISTIC_ABILITY: ["StatisticAbilityID", "AbilityID", "AbilityType", "Amount", "InitialDuration"], # Y
      TableName.ENEMY: ["EnemyID", "Name", "MaxHealth", "AttackDamage", "Intelligence", "IsBoss"], # Y
      TableName.ENEMY_ABILITY: ["EnemyAbilityID", "EnemyID", "AbilityID", "IsUsedInAttack"], # Y
    }

  # built-in methods

  def __del__(self) -> None:
    if self.save_on_delete:
      self.finish_combat_encounter()
      self.finish_structure_encounter()
      self.save()

  def __getitem__(self, storage_name: StorageAttrName) -> Any:
    return getattr(self, str(storage_name))
  
  # getter and setter methods

  @property
  def active_character_id(self) -> Optional[int]:
    return self.__active_character_id
  
  @active_character_id.setter
  def active_character_id(self, identifier: Optional[int]) -> None:
    if type(identifier) != int and identifier != None: raise TypeError(f"{identifier=} with type {type(identifier)} is not `int` or `None`.")
    self.__active_character_id = identifier

  # database and data loading methods

  def database_exists(self) -> bool:
    """Determines whether the database has already been created in memory or not by calling the \'self.database.exists()\' method."""
    return self.database.exists()

  def load_database(self) -> None:
    """Calls \'self.database.load()\'"""
    self.database.load()

  def load_game_data(self) -> None:
    """Called only once: by parent `App` after being initialised. Loads the database into memory, creating it if it doesn't already exist in storage. If the database doesn't already exist in storage, some default data is created."""
    database_exists: bool = self.database_exists()
    if not database_exists:
      self.init_database_main() # creates a database with an empty `MAIN.toml` file.
      self.load_default_data() # default data is loaded into `GameData` memory ONLY.
    existing_table_names: list[str] = self.database.load_main_data()
    self.load_database()
    self.create_tables(existing_table_names) 
    self.save()
    self.load()
    logging.debug(f"{self.characters}")
  
  def init_database_main(self, table_names: list[str] = []) -> None:
    """
    Called when no database exists in order to create a new one for use. Only creates the `MAIN.toml` file.
    
    :param table_names: The names of the tables which are to be created.
    :type table_names: list[str]
    """
    self.database.create_main(table_names)
    self.save()

  def load_default_data(self) -> None:
    """Loads data into `self` after a new database has been initialised."""
    self.users = {0: User("User", "1234", loaded=False)}
    self.items = {
      0: Item(ItemType.WEAPON, "Bronze sword", loaded=False),
      1: Item(ItemType.WEAPON, "Mace", loaded=False),
      2: Item(ItemType.WEAPON, "Dagger", loaded=False),
    }
    self.weapons = {
      0: Weapon(0, 10, loaded=False),
      1: Weapon(1, 15, loaded=False),
      2: Weapon(2, 5, loaded=False),
    }
    self.equipables = {

    }
    self.inventory_items = {
      0: InventoryItem(0, 0, 1, True, loaded=False),
      1: InventoryItem(0, 1, 1, True, loaded=False),
      2: InventoryItem(0, 2, 1, True, loaded=False),
    }
    self.enemies = {
      0: Enemy("Shep", 5, 1, 0.1, False),
      1: Enemy("Skeleton", 10, 5, 0.5, False),
    }
    self.abilities = {
      0: Ability("Small heal", AbilityTypeName.HEAL),
      1: Ability("Moderate heal", AbilityTypeName.HEAL),
      2: Ability("Significant heal", AbilityTypeName.HEAL),
    }
    self.statistic_abilities = {
      0: StatisticAbility(0, AbilityTypeName.HEAL, 10, 1),
      1: StatisticAbility(1, AbilityTypeName.HEAL, 20, 1),
      2: StatisticAbility(2, AbilityTypeName.HEAL, 30, 1),
    }


  def create_tables(self, existing_table_names: list[str]) -> None:
    for (table_name, table_columns) in self.table_templates.items():
      if not table_name in existing_table_names:
        self.database.create_table(table_name, table_columns)

  def select_from_table(self, table_name: TableName, columns: list[Any], condition: Condition) -> dict[int, list[Any]]:
    return self.database.select(table_name, columns, condition)
  
  def select_all_from_table(self, table_name: TableName) -> dict[int, list[Any]]:
    return self.select_from_table(table_name, ["*"], everything())
  
  def load_stored_from_database[StoredType: Stored](self, stored_type: Type[StoredType]) -> dict[int, StoredType]:
    entities: dict[int, StoredType] = {} # type `StoredType` is a generic which can take any type, as long as it is a subtype of `Stored`
    table_name: TableName = stored_type.get_table_name()
    raw_stored_data: dict[int, list[Any]] = self.select_all_from_table(table_name)
    for (identifier, stored_data) in raw_stored_data.items():
      stored: StoredType = cast(StoredType, stored_type.instantiate(stored_data, True))
      entities[identifier] = stored
    return entities
  
  @staticmethod
  def get_save_load_storage_options(storage_options: Union[StorageAttrName, tuple[StorageAttrName, bool]]) -> tuple[StorageAttrName, bool]:
    storage_name: StorageAttrName # can be anything, so there is no default value
    is_in_database: bool = True # defaults to true as this is the most common case
    if type(storage_options) == StorageAttrName:
      storage_name = storage_options
    elif type(storage_options) == tuple and len(storage_options) == 2:
      storage_name = storage_options[0]
      is_in_database = storage_options[1]
    else:
      raise TypeError(f"`{storage_options=}`, with `{type(storage_options)=}`, doesn't match with any expected type (`StorageAttrName`, `tuple[StorageAttrName, bool]`).")

    return (storage_name, is_in_database)

  def load(self) -> None:
    self.load_database()
    for (target, storage_options) in self.save_load_targets.items():
      (storage_name, is_in_database) = self.get_save_load_storage_options(storage_options)
      if not is_in_database: continue # skips if the target won't be saved to / loaded from the database
      setattr(self, storage_name, self.load_stored_from_database(target))

  def format_data_to_dictionary(self, table_name: TableName, raw_data: list) -> dict[str, Any]:
    formatted_data: dict[str, Any] = {}
    non_identifier_column_names: list[str] = self.database.find_table(table_name).get_non_identifier_column_names()
    for (i, column_name) in enumerate(non_identifier_column_names):
      try:
        formatted_data[column_name] = raw_data[i]
      except IndexError as e:
        raise IndexError(f"Trying to access '{raw_data=}' (`{len(raw_data)=}`) at index `{i=}` out of list range. `{table_name=}` (`Exception={e}`).")
    return formatted_data

  def update_database(self, table_name: TableName, raw_data: list[Any], condition: Condition) -> None:
    formatted_data: dict[str, Any] = self.format_data_to_dictionary(table_name, raw_data)
    self.database.update(table_name, formatted_data, condition)

  def update_database_record(self, table_name: TableName, identifier: int, raw_data: list[Any]) -> None:
    """
    Updates the fields of an existing record in the database. Only updates the database.
    
    :param table_name: The table to which the record will be updated.
    :type table_name: TableName
    :param identifier: The identifier of the record which is to be updated.
    :type identifier: int
    :param raw_data: The data which is to take the place of the existing data found in the database.
    :type raw_data: list[Any]
    """
    match_condition = Condition(lambda id, _row: id == identifier) 
    self.update_database(table_name, raw_data, match_condition)

  def insert_into_database(self, table_name: TableName, raw_data: list[Any], identifier: Optional[int] = None) -> Optional[int]:
    """Inserts a new record into a table, returning the new value's identifier afterward."""
    formatted_data: dict[str, Any] = self.format_data_to_dictionary(table_name, raw_data)
    return self.database.insert(table_name, formatted_data, identifier)
  
  def insert_into_storage[StoredType: Stored](self, storage_name: StorageAttrName, identifier: int, data: StoredType) -> None:
    """Inserts a record into the storage attribute in `self` whose name matches the one given."""
    storage: dict[int, StoredType] = getattr(self, storage_name)
    if identifier in storage: raise IndexError(f"Tried to insert {data=} with {identifier=} into {storage_name=} when the index is already being used {storage[identifier]=}.")
    storage[identifier] = data
    setattr(self, storage_name, storage)
  
  def is_stored_unique_in_table(self, table_name: TableName, identical_condition: Condition) -> bool:
    identifier_column: str = table_name + "ID"
    identical_identifiers: list[int] = list(self.select_from_table(table_name, [identifier_column], identical_condition).keys())
    if len(identical_identifiers) > 0: return False
    return True
    
  def select_from_storage[StoredType: Stored](self, storage: dict[int, StoredType], condition: Condition) -> dict[int, StoredType]:
    return {identifier: stored for identifier, stored in storage.items() if condition.evaluate(identifier, stored.get_raw_data())}

  def is_stored_unique_in_self[StoredType: Stored](self, storage_name: StorageAttrName, identical_condition: Condition) -> bool:
    storage: dict[int, StoredType] = getattr(self, storage_name)
    identical_identifiers: list[int] = list(self.select_from_storage(storage, identical_condition).keys())
    if len(identical_identifiers) > 0: return False
    return True
  
  def is_stored_unique[StoredType: Stored](self, stored_type: Type[StoredType], storage_name: StorageAttrName, identical_condition: Condition) -> bool:
    table_name: TableName = stored_type.get_table_name()
    return self.is_stored_unique_in_table(table_name, identical_condition) and self.is_stored_unique_in_self(storage_name, identical_condition) # if either are false, then the stored must not be unique

  # returns the stored's identifier and the stored which was created
  def insert_stored[StoredType: Stored](self, stored_type: Type[StoredType], stored_data: list[Any], identical_condition: Condition, storage_name: StorageAttrName) -> tuple[int, StoredType]:
    """
    Inserts a record both into the database and the appropriate storage attribute in `self`. Automatically finds the next insertion point.
    
    :param stored_type: The type of object which is being inserted.
    :type stored_type: type[StoredType]
    :param stored_data: The raw data of a single `StoredType` object. Does not include the identifier of the object.
    :type stored_data: list[Any]
    :param identical_condition: What must be true if 2 objects are identical.
    :type identical_condition: Condition
    :param storage_name: The storage attribute of `self` which the created object will be stored at.
    :type storage_name: StorageAttrName
    :return: A tuple, with the first element being the stored identifier and the second element being the newly created object.
    :rtype: tuple[int, StoredType]
    """
    table_name: TableName = stored_type.get_table_name()
    new_stored: StoredType = cast(StoredType, stored_type.instantiate(stored_data))
    if not self.is_stored_unique(stored_type, storage_name, identical_condition):
      del new_stored
      raise Exception(f"stored object (type `{stored_type}`) with data `{stored_data}` already exists in table `{table_name}`.")
    identifier: int = get_next_available_identifier(getattr(self, storage_name)) # generates its own identifier instead of relying on the database to generate it
    logging.debug(f"{identifier=}, {stored_type=}, {stored_data=}")
    self.insert_into_database(table_name, stored_data, identifier)
    self.insert_into_storage(storage_name, identifier, new_stored)
    return (identifier, new_stored)

  def insert_user(self, raw_data: list[Any]) -> int:
    identical_condition = Condition(lambda _identifier, row: row[0] == raw_data[0]) # checks if user
    (identifier, _) = self.insert_stored(User, raw_data, identical_condition, StorageAttrName.USERS)
    return identifier

  def insert_character(self, raw_data: list[Any]) -> int:
    identical_condition = Condition(lambda _identifier, row: row[1] == raw_data[1])
    (identifier, _) = self.insert_stored(Character, raw_data, identical_condition, StorageAttrName.CHARACTERS)
    return identifier

  def insert_world(self, raw_data: list[Any]) -> int:
    identical_condition = Condition(lambda _identifier, row: row[1] == raw_data[1])
    (identifier, _) = self.insert_stored(World, raw_data, identical_condition, StorageAttrName.WORLDS)
    return identifier

  def save_stored[StoredType: Stored](self, stored_type: Type[StoredType], storage_name: StorageAttrName) -> None:
    """
    Saves from one variable in the `GameData` object to `Database`. Does not insert objects into their respective variables in `self`.
    
    :param self: Object the method is called on.
    :param stored_type: The object type that is to be saved, being a subclass of `StoredType`.
    :type stored_type: Type[StoredType]
    :param storage_name: Name of the variable being saved to memory.
    :type storage_name: StorageAttrName
    """
    storage: dict[int, StoredType] = getattr(self, storage_name)
    for (identifier, stored) in storage.items():
      table_name: TableName = stored_type.get_table_name()
      raw_data: list = stored.get_raw_data()
      if stored.loaded:
        self.update_database_record(table_name, identifier, raw_data)
      else:
        self.insert_into_database(table_name, raw_data)

  def save(self) -> None:
    """Saves all targeted data stored in memory (in \'self\') to the database."""
    for (target, storage_options) in self.save_load_targets.items():
      (storage_name, is_in_database) = self.get_save_load_storage_options(storage_options)
      if not is_in_database: continue # skips if not stored in database
      self.save_stored(target, storage_name)
    self.database.save()

  def delete_stored[StoredType: Stored](self, stored_type: Type[StoredType], identifier: int, storage_name: StorageAttrName) -> None:
    """Deletes a specific value from both the appropriate storage attribute in \'self\' and the subsequent table in \'Database\'."""
    # deleting from 'self'
    updated_storage: dict[int, StoredType] = getattr(self, storage_name)
    del updated_storage[identifier]
    setattr(self, storage_name, updated_storage)
    # deleting from 'Database'
    table_name: TableName = stored_type.get_table_name()
    condition: Condition = matching_identifiers(identifier)
    self.database.delete_from(table_name, condition)

  # user methods

  def set_active_user(self, user: User) -> None:
    self.active_user = user

  def get_user_names(self) -> list:
    user_names: list = []
    for user in self.users.values():
      user_names.append(user.name) 
    return user_names
  
  # weapon methods
  
  def get_weapon_name(self, weapon_id: int) -> str:
    selected_weapon: Weapon = self.weapons[weapon_id]
    weapon_item_id: int = selected_weapon.item_id
    selected_item: Item = self.items[weapon_item_id]
    weapon_name: str = selected_item.name
    return weapon_name
  
  def get_weapon_abilities(self, weapon: Weapon) -> dict[int, Ability]:
    item_id: int = weapon.item_id
    weapon_item_abilities: dict[int, ItemAbility] = filter_dictionary(self.item_abilities, lambda _, item_ability: item_ability.item_id == item_id)
    weapon_item_abilities_ability_identifiers: list[int] = []
    for item_ability in list(weapon_item_abilities.values()):
      weapon_item_abilities_ability_identifiers.append(item_ability.ability_id)
    return filter_dictionary(self.abilities, lambda identifier, _: identifier in weapon_item_abilities_ability_identifiers)
  
  def get_weapon_parry(self, weapon: Weapon) -> ParryAbility:
    weapon_abilities: dict[int, Ability] = self.get_weapon_abilities(weapon)
    weapon_parry_abilities: dict[int, Ability] = filter_dictionary(weapon_abilities, lambda _, ability: ability.ability_type == AbilityTypeName.PARRY)
    weapon_parry_abilities_identifiers: list[int] = list(weapon_parry_abilities.keys())
    parries_dict: dict[int, ParryAbility] = filter_dictionary(self.parry_abilities, lambda _, parry_ability: parry_ability.ability_id in weapon_parry_abilities_identifiers)
    parries_list: list[ParryAbility] = list(parries_dict.values())
    if len(parries_list) != 1: raise LookupError(f"Multiple or no parry abilities found for `{weapon=}`: `{parries_dict=}`.")
    return parries_list[0]
  
  # character methods
  
  def get_active_character(self) -> Character:
    if self.active_character_id == None:
      raise AttributeError(f"Trying to access \'self.active_character_id\' when no active character has been selected (\'self.active_character_id\'=\'None\')")
    active_character: Character = self.characters[self.active_character_id]
    return active_character
  
  def get_character_name(self) -> str:
   return self.get_active_character().name
  
  # enemy and fighting_enemy methods
  
  def get_fighting_enemy_id_at(self, position: Position) -> Optional[int]:
    fighting_enemy_id: Optional[int] = self.fighting_enemy_graph.get_fighting_enemy_id(position)
    if fighting_enemy_id == None: return None
    return fighting_enemy_id
  
  def get_fighting_enemy_at(self, position: Position) -> Optional[FightingEnemy]:
    fighting_enemy_id: Optional[int] = self.get_fighting_enemy_id_at(position)
    if fighting_enemy_id == None: return None
    fighting_enemy: FightingEnemy = self.fighting_enemies[fighting_enemy_id]
    return fighting_enemy
  
  def set_fighting_enemy_at(self, position: Position, fighting_enemy_id: int) -> None:
    self.fighting_enemy_graph.set_fighting_enemy_id(position, fighting_enemy_id)

  def get_fighting_enemy_name(self, fighting_enemy_id: Optional[int]) -> str:
    if fighting_enemy_id == None: return ""
    fighting_enemy: Optional[FightingEnemy] = self.fighting_enemies[fighting_enemy_id]
    if fighting_enemy == None: return ""
    return fighting_enemy.name
  
  def get_fighting_enemy_health(self, fighting_enemy_id: Optional[int]) -> Optional[float]:
    if fighting_enemy_id == None: return None
    fighting_enemy: Optional[FightingEnemy] = self.fighting_enemies[fighting_enemy_id]
    if fighting_enemy == None: return None
    return fighting_enemy.health
  
  def get_fighting_enemy_max_health(self, fighting_enemy_id: Optional[int]) -> Optional[float]:
    if fighting_enemy_id == None: return None
    fighting_enemy: FightingEnemy = self.fighting_enemies[fighting_enemy_id]
    return fighting_enemy.max_health
  
  def get_enemy_attack_ability(self, enemy_id: int) -> Optional[tuple[int, Ability]]:
    """Assumes enemy has only one ability used in an attack."""
    enemy_attack_abilities_dict: dict[int, EnemyAbility] = filter_dictionary(self.enemy_abilities, lambda _, enemy_ability: enemy_ability.enemy_id == enemy_id and enemy_ability.is_used_in_attack)

    if len(enemy_attack_abilities_dict) == 0: return None
    if len(enemy_attack_abilities_dict) > 1: raise BufferError(f"{enemy_attack_abilities_dict=}; expected a dictionary of length `1`.")

    enemy_attack_ability: EnemyAbility = list(enemy_attack_abilities_dict.values())[0]
    ability_id: int = enemy_attack_ability.ability_id
    ability: Ability = self.abilities[ability_id]
    return (ability_id, ability)
  
  def get_enemy_heal_ability(self, enemy_id: int) -> Optional[tuple[int, Ability]]:
    """Gets the enemy's healing ability."""
    heal_abilities_dict: dict[int, StatisticAbility] = filter_dictionary(self.statistic_abilities, lambda _, statistic_ability: statistic_ability.ability_type == AbilityTypeName.HEAL)
    heal_ability_identifiers: list[int] = list(heal_abilities_dict.keys())
    enemy_heal_abilities_dict: dict[int, EnemyAbility] = filter_dictionary(self.enemy_abilities, lambda _, enemy_ability: enemy_ability.enemy_id == enemy_id and enemy_ability.ability_id in heal_ability_identifiers)

    if len(enemy_heal_abilities_dict) == 0: return None
    if len(enemy_heal_abilities_dict) > 1: raise BufferError(f"{enemy_heal_abilities_dict=}; expected a dictionary of length `1`.")

    enemy_heal_ability: EnemyAbility = list(enemy_heal_abilities_dict.values())[0]
    ability_id: int = enemy_heal_ability.ability_id
    ability: Ability = self.abilities[ability_id]
    return (ability_id, ability)
  
  # inventory and inventory item methods

  def get_character_inventory_items(self, character_id: Optional[int] = None) -> dict[int, InventoryItem]:
    if character_id == None: character_id = self.active_character_id
    filter_expression: Callable[[int, InventoryItem], bool] = lambda _, inv_item: inv_item.character_id == character_id
    return filter_dictionary(self.inventory_items, filter_expression)
  
  def set_inventory_item_equipped(self, inventory_item_id: int, being_equipped: bool) -> None:
    """Equips or unequips an inventory item depending on the \'being_equipped\' parameter."""
    self.inventory_items[inventory_item_id].equipped = being_equipped

  def toggle_inventory_item_equipped(self, toggleable_button: ToggleableButton, inventory_item_id: int) -> None:
    being_equipped: bool = bool(toggleable_button.is_toggled)
    self.set_inventory_item_equipped(inventory_item_id, being_equipped)
    logging.debug(f"\'self.inventory_items\'=`{self.inventory_items}`")
  
  def get_relevant_storage_items(self, storage_id: int) -> dict[int, StorageItem]:
    filter_expression: Callable[[int, StorageItem], bool] = lambda _, storage_item: storage_item.storage_id == storage_id
    return filter_dictionary(self.storage_items, filter_expression)
  
  def move_inventory_item_to_storage(self, inventory_item_id: int, storage_id: int) -> None:
    # get inventory item data
    inventory_item: InventoryItem = self.inventory_items[inventory_item_id]
    item_id: int = inventory_item.item_id
    stack_size: int = inventory_item.stack_size
    # TODO: handle what happens if the item is equipped such that it doesn't throw an error
    if inventory_item.equipped: raise Exception("Moving inventory items while they are equipped is not yet implemented")
    raw_storage_item_data: list[Any] = [storage_id, item_id, stack_size]
    
    same_item: Callable[[int, StorageItem], bool] = lambda _, storage_item: storage_id == storage_item.storage_id and item_id == storage_item.item_id
    matching_items: dict[int, StorageItem] = filter_dictionary(self.storage_items, same_item)
    matching_items_quantity: int = len(matching_items)
    logging.debug(f"| BEFORE MOVE (inv->store): \'matching_items_quantity\'=`{matching_items_quantity}`")

    if matching_items_quantity == 0: # if there are no items of the same type (in the target storage)
      identical_condition = Condition(lambda _identifier, _row: False) # there must be no matching items for this block to execute, so there is no need for a functional identical condition
      self.insert_stored(StorageItem, raw_storage_item_data, identical_condition, StorageAttrName.STORAGE_ITEMS)
    elif matching_items_quantity == 1: # if there is one instance of same-type items (in the target storage)
      matched_item_id: int = list(matching_items.keys())[0] # there will always be an item at index 0
      matched_item: StorageItem = list(matching_items.values())[0] 
      new_stack_size: int = stack_size + matched_item.stack_size # update stack size
      raw_storage_item_data[2] = new_stack_size
      self.update_database_record(StorageItem.get_table_name(), matched_item_id, raw_storage_item_data)
      self.storage_items[matched_item_id].stack_size = new_stack_size
    else: # erroneous case where there are 2 or more matches
      raise Exception(f"\'matching_items_quantity\'=`{matching_items_quantity}` greater than \'1\' (\'matching_items\'=`{matching_items}`)")
    
    self.delete_stored(InventoryItem, inventory_item_id, StorageAttrName.INVENTORY_ITEMS)
    logging.debug(f"| AFTER MOVE (inv->store): \'matching_items_quantity\'=`{matching_items_quantity}`")

  def move_storage_item_to_inventory(self, storage_item_id: int) -> None:
    character_id: int = unpack_optional(self.active_character_id) # 'unpack_optional' should never throw an exception here
    storage_item: StorageItem = self.storage_items[storage_item_id]
    item_id: int = storage_item.item_id
    stack_size: int = storage_item.stack_size
    equipped: bool = False # items should only equip when the player requests to
    raw_inventory_item_data: list[Any] = [character_id, item_id, stack_size, equipped]

    same_item: Callable[[int, InventoryItem], bool] = lambda _,inv_item: character_id == inv_item.character_id and item_id == inv_item.item_id
    matching_items: dict[int, InventoryItem] = filter_dictionary(self.inventory_items, same_item)
    matching_items_quantity: int = len(matching_items)
    logging.debug(f"| BEFORE MOVE (store->inv): \'matching_items_quantity\'=`{matching_items_quantity}`")

    if matching_items_quantity == 0: # if there are no items of the same type in the target storage
      identical_condition = Condition(lambda _identifier, _row: False) # there must be no matching items for this block to execute, so there is no need for a functional identical condition
      self.insert_stored(InventoryItem, raw_inventory_item_data, identical_condition, StorageAttrName.INVENTORY_ITEMS)
    elif matching_items_quantity == 1: # if there is one instance of items of the same type in the target storage
      matched_item_id: int = list(matching_items.keys())[0]
      matched_item: InventoryItem = list(matching_items.values())[0] # there will always be an item at index 0
      new_stack_size: int = stack_size + matched_item.stack_size
      raw_inventory_item_data[2] = new_stack_size
      self.update_database_record(InventoryItem.get_table_name(), matched_item_id, raw_inventory_item_data)
      self.inventory_items[matched_item_id].stack_size = new_stack_size
    else: # erroneous case where there are 2 or more matches
      raise Exception(f"\'matching_items_quantity\'=`{matching_items_quantity}` greater than \'1\' (\'matching_items\'=`{matching_items}`)")
    
    self.delete_stored(StorageItem, storage_item_id, StorageAttrName.STORAGE_ITEMS)
    logging.debug(f"| AFTER MOVE (store->inv): \'matching_items_quantity\'=`{matching_items_quantity}`")

  def is_storage_at_home(self) -> Optional[bool]:
    """Determines whether the storage is a \"Home\" storage or not."""
    storage_id: Optional[int] = self.active_storage_id
    if storage_id == None: return None
    logging.debug(f"{storage_id=}")
    storage_type: StorageType = self.storages[storage_id].storage_type
    if storage_type == StorageType.HOME: return True
    elif storage_type == StorageType.CHEST: return False
    else: raise ValueError(f"Unknown \'storage_type\'=`{storage_type}`")

  def get_inventory_item_name(self, inventory_item_id: int) -> str:
    selected_inventory_item: InventoryItem = self.inventory_items[inventory_item_id]
    selected_item_id: int = selected_inventory_item.item_id
    selected_item: Item = self.items[selected_item_id]
    return selected_item.name
  
  # methods for encountering enemies
  
  def get_random_enemy_identifier(self, get_boss: bool) -> int:
    matching_enemy_type: Callable[[int, Enemy], bool] = lambda _, enemy: enemy.is_boss == get_boss
    enemies: dict[int, Enemy] = filter_dictionary(self.enemies, matching_enemy_type)
    return select_random_identifier(enemies)
  
  def get_multiple_random_enemy_identifiers(self, n: int, get_boss: bool) -> list[int]:
    if n < 0: raise ValueError(f"{n=} cannot be less than 0.")
    if n > 1 and get_boss: raise Exception(f"Cannot get more than {n=} bosses.")
    if n == 0: return [] # base case
    enemy_id: int = self.get_random_enemy_identifier(get_boss)
    return [enemy_id] + self.get_multiple_random_enemy_identifiers(n-1, get_boss) # recursive call
  
  def add_fighting_enemy_to_grid_at_random_position(self, fighting_enemy_id: int) -> None:
    position: Position = get_random_position(self.fighting_enemy_graph.dimensions)
    if self.get_fighting_enemy_at(position) != None:
      return self.add_fighting_enemy_to_grid_at_random_position(fighting_enemy_id) # recursive call
    return self.set_fighting_enemy_at(position, fighting_enemy_id)
  
  def generate_fighting_enemies(self) -> None:
    enemy_count: int = generate_enemy_count()
    is_boss: bool = is_boss_encounter()
    enemy_identifiers: Queue[int] = Queue(self.get_multiple_random_enemy_identifiers(enemy_count, is_boss))
    while not enemy_identifiers.empty():
      enemy_id: int = enemy_identifiers.get()
      enemy: Enemy = self.enemies[enemy_id]
      # initialisation
      fighting_enemy = FightingEnemy(enemy_id, enemy.name, enemy.max_health, enemy.max_health, enemy.attack_damage, enemy.intelligence)
      self.set_fighting_enemy_abilities(fighting_enemy)
      # inserting into storage
      fighting_enemy_id: int = get_next_available_identifier(self.fighting_enemies)
      self.insert_into_storage(StorageAttrName.FIGHTING_ENEMIES, fighting_enemy_id, fighting_enemy)
      self.add_fighting_enemy_to_grid_at_random_position(fighting_enemy_id)

  def set_fighting_enemy_abilities(self, fighting_enemy: FightingEnemy) -> None:
    """Sets the attack and heal abilities for a given fighting enemy. Having no attack ability means the enemy has only a standard attack. Having no heal ability means the enemy cannot heal."""
    enemy_id: int = fighting_enemy.enemy_id
    # attack ability
    attack_data: Optional[tuple[int, Ability]] = self.get_enemy_attack_ability(enemy_id)
    if attack_data == None: attack_ability_id = None
    else: (attack_ability_id, _) = attack_data
    # heal ability
    heal_data: Optional[tuple[int, Ability]] = self.get_enemy_heal_ability(enemy_id)
    if heal_data == None: heal_ability_id = None
    else: (heal_ability_id, _) = heal_data

    fighting_enemy.set_action_identifiers(attack_ability_id, heal_ability_id)
  
  def finish_combat_encounter(self) -> None:
    for i in range(len(self.fighting_enemy_graph)):
      p: Position = self.fighting_enemy_graph.length_to_point(i)
      fighting_enemy_id: Optional[int] = self.fighting_enemy_graph[p]
      if fighting_enemy_id == None: continue
      del self.fighting_enemies[fighting_enemy_id]
    self.fighting_enemy_graph.clear_graph()
  
  # methods for handling the generation / deletion of structure items
  
  def get_random_item_identifier(self) -> int:
    return select_random_identifier(self.items)
  
  def get_unique_random_item_identifier(self, selected_item_identifiers: list[int] = []) -> int:
    item_id: int = self.get_random_item_identifier()
    if item_id in selected_item_identifiers:
      return self.get_unique_random_item_identifier(selected_item_identifiers)
    return item_id
  
  def get_multiple_unique_random_item_identifiers(self, n: int, selected_item_identifiers: list[int] = []) -> list[int]:
    if n < 0: raise ValueError(f"{n=} cannot be less than 0.")
    if n == 0: return [] # base case
    item_id: int = self.get_unique_random_item_identifier(selected_item_identifiers)
    selected_item_identifiers.append(item_id)
    return [item_id] + self.get_multiple_unique_random_item_identifiers(n-1, selected_item_identifiers) # recursive call
  
  def encounter_structure(self) -> None:
    """Generates the items for a structure being accessed."""
    item_count: int = generate_structure_item_count()
    away_storage_id: Optional[int] = self.away_storage
    if away_storage_id == None: raise TypeError(f"{self.away_storage=} cannot be `None` when encountering a structure.")
    item_identifiers: Queue[int] = Queue(self.get_multiple_unique_random_item_identifiers(item_count))
    identical_condition = nothing()
    while not item_identifiers.empty():
      item_id: int = item_identifiers.get()
      self.insert_stored(StorageItem, [away_storage_id, item_id, 1], identical_condition, StorageAttrName.STORAGE_ITEMS)
  
  def finish_structure_encounter(self) -> None:
    """Deletes items in the structure after it has been accessed."""
    away_storage_id: Optional[int] = self.away_storage
    if away_storage_id == None: raise TypeError(f"{self.away_storage=} cannot be `None` when finishing a structure encounter.")
    item_in_selected_storage: Callable[[int, StorageItem], bool] = lambda _, storage_item: storage_item.storage_id == away_storage_id
    selected_storage_items: dict[int, StorageItem] = filter_dictionary(self.storage_items, item_in_selected_storage)
    storage_item_identifiers: Queue[int] = Queue(list(selected_storage_items.keys()))
    while not storage_item_identifiers.empty():
      storage_item_identifier: int = storage_item_identifiers.get()
      self.delete_stored(StorageItem, storage_item_identifier, StorageAttrName.STORAGE_ITEMS)

  def is_all_fighting_enemies_dead(self) -> bool:
    fighting_enemies: list[FightingEnemy] = list(self.fighting_enemies.values())
    if len(fighting_enemies) == 0: return True
    for fighting_enemy in fighting_enemies:
      fighting_enemy_health: float = fighting_enemy.health
      if fighting_enemy_health > 0: return False
    return True