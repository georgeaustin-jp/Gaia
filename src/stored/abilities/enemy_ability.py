from tools.typing_tools import Any

from database.condition import Condition
from stored.stored import Stored, TableName

class EnemyAbility(Stored):
  def __init__(self, enemy_id: int, ability_id: int, is_used_in_attack: bool, loaded: bool = True) -> None: # "EnemyID", "AbilityID", "IsUsedInAttack"
    super().__init__(loaded)
    self.enemy_id = enemy_id
    self.ability_id = ability_id
    self.is_used_in_attack = is_used_in_attack

  # `Stored` methods

  @staticmethod
  def get_table_name() -> TableName: return TableName.ENEMY_ABILITY

  def get_raw_data(self) -> list[Any]:
    return [self.enemy_id, self.ability_id, self.is_used_in_attack]

  @staticmethod
  def instantiate(data: list[Any], loaded: bool = True):
    return instantiate_enemy_ability(data, loaded)
  
  @staticmethod
  def identical_condition(enemy_ability_row: list[Any]) -> Condition:
    return Condition(lambda _, row: False)

def instantiate_enemy_ability(enemy_ability_data: list[Any] = [], loaded: bool = True) -> EnemyAbility:
  enemy_id: int = enemy_ability_data[0]
  ability_id: int = enemy_ability_data[1]
  is_used_in_attack: bool = enemy_ability_data[1]
  return EnemyAbility(enemy_id, ability_id, is_used_in_attack, loaded)