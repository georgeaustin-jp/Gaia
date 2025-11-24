class User:
  def __init__(self, identifier: int, user_information: list) -> None:
    self.identifier = identifier
    self.name = user_information[0]
    self.pass_hash = user_information[1]
    self.character_quantity = user_information[2]
    self.world_quantity = user_information[3]
