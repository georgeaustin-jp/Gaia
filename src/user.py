class User:
  def __init__(self, user_information: list, loaded: bool = True) -> None:
    self.name: str = user_information[0]
    self.pass_hash: str = user_information[1]
    self.character_quantity: int = user_information[2]
    self.world_quantity: int = user_information[3]
    self.loaded = loaded

  def to_raw_data(self) -> list:
    return [self.name, self.pass_hash, self.character_quantity, self.world_quantity]