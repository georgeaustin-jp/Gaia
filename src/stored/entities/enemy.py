from tools.typing_tools import *

from stored.stored import *

class Enemy(Stored):
  def __init__(self, name: str, max_health: float, attack_damage: float, intelligence: float, is_boss: bool, loaded: bool = True) -> None:
    super().__init__(loaded)
    self.name = name
    self.max_health = max_health
    self.attack_damage = attack_damage
    self.intelligence = intelligence
    self.is_boss = is_boss

  @staticmethod
  def get_table_name() -> TableName: return TableName.ENEMY

  def get_raw_data(self) -> list[Any]:
    return super().get_raw_data() + [self.name, self.max_health, self.attack_damage, self.intelligence, self.is_boss]
  
  @staticmethod
  def instantiate(enemy_data: list[Any], loaded: bool = True):
    return instantiate_enemy(enemy_data, loaded)

def instantiate_enemy(enemy_data: list[Any], loaded: bool = True) -> Enemy:
  name: str = enemy_data[0]
  max_health: float = enemy_data[1]
  attack_damage: float = enemy_data[2]
  intelligence: float = enemy_data[3]
  is_boss: bool = enemy_data[4]
  return Enemy(name, max_health, attack_damage, intelligence, is_boss, loaded)