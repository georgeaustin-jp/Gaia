from random import randint

# Abstract base class
class Entity:
  def __init__(self, max_health):
    self.max_health = max_health
    self.health = self.max_health

  def move(self, target): pass
  def select_move(self): pass
  def change_health(self, amount): pass
  def display_stats(self): pass
  def is_dead(self): pass

class Player(Entity):
  def __init__(self):
    super().__init__(100)

  def move(self, target):
    move_n = self.select_move()
    match move_n:
      case 1:
        target.change_health(-10)
        print("Player used \"Attack\"")
      case 2:
        self.change_health(10)
        print("Player used \"Heal\"")

  def select_move(self):
    raw_move_n = input("Select move:\n 1: Attack (10 DMG)\n 2: Heal (10 HP)\n > ")
    move_n = int(raw_move_n)
    return move_n
  
  def change_health(self, amount):
    self.health += amount
    if self.health > self.max_health: self.health = self.max_health

  def display_stats(self):
    print(f"Player: {self.health}/{self.max_health} HP")

  def is_dead(self):
    if self.health <= 0: return True
    return False

class Enemy(Entity):
  def __init__(self):
    super().__init__(50)

  def move(self, target):
    move_n = self.select_move()
    match move_n:
      case 1:
        target.change_health(-5)
        print("Enemy used \"Attack\"")
      case 2:
        self.change_health(5)
        print("Enemy used \"Heal\"")

  def select_move(self):
    move_n = randint(1,2)
    return move_n
  
  def change_health(self, amount):
    self.health += amount
    if self.health > self.max_health: self.health = self.max_health

  def display_stats(self):
    print(f"Enemy: {self.health}/{self.max_health} HP")

  def is_dead(self):
    if self.health <= 0: return True
    return False
  
def is_fighting(player: Player, enemy: Enemy):
  if player.is_dead() or enemy.is_dead(): return False
  return True

# PROGRAM STARTS HERE
def main():
  player: Player = Player()
  enemy: Enemy = Enemy()

  winner: str = ""
  fighting: bool = True

  while fighting:
    player.display_stats()
    enemy.display_stats()
    # player turn
    player.move(enemy)
    fighting = is_fighting(player, enemy)
    if not fighting: continue
    # enemy turn
    enemy.move(player)
    fighting = is_fighting(player, enemy)
    if not fighting: continue

  winner = "Player" if enemy.is_dead() else "Enemy"
  print(f"Game end. Winner: {winner}.")

if __name__ == "__main__":
  main()