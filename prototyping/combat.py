from random import randint

def main():
  player: dict = {"max_health": 100, "health": 100}
  enemy: dict = {"max_health": 50, "health": 50}

  winner: str = ""
  fighting: bool = True

  while fighting:
    display_stats(player, enemy)
    # player turn
    (player, enemy) = player_turn(player, enemy)
    (fighting, winner) = check_health_underflow(player, enemy)
    if not fighting: continue
    # enemy turn
    (player, enemy) = enemy_turn(player, enemy)
    (fighting, winner) = check_health_underflow(player, enemy)
    if not fighting: continue

  print(f"Game end. Winner: {winner}.")

# Returns (player, enemy)
def player_turn(player: dict, enemy: dict) -> tuple[dict, dict]:
  move_n = int(input("Select move:\n 1: attack\n 2: heal\n > "))
  match move_n:
    case 1:
      enemy["health"] = enemy["health"] - 10
      print("Player used \"attack\"")
    case 2:
      player["health"] = player["health"] + 10
      print("Player used \"heal\"")
  return check_health_overflow(player, enemy)

# Returns (player, enemy)
def enemy_turn(player: dict, enemy: dict) -> tuple[dict, dict]:
  move_n = randint(1,2)
  match move_n:
    case 1:
      player["health"] = player["health"] - 10
      print("Enemy used \"attack\"")
    case 2:
      enemy["health"] = enemy["health"] + 5
      print("Enemy used \"heal\"")
  return check_health_overflow(player, enemy)

# Returns (player, enemy)
def check_health_overflow(player: dict, enemy: dict) -> tuple[dict, dict]:
  if player["health"] > player["max_health"]:
    player["health"] = player["max_health"]
  if enemy["health"] > enemy["max_health"]:
    enemy["health"] = enemy["max_health"]
  return (player, enemy)

# Returns (fighting, winner)
def check_health_underflow(player: dict, enemy: dict) -> tuple[bool, str]:
  if player["health"] <= 0:
    return [False, "enemy"]
  if enemy["health"] <= 0:
    return [False, "player"]
  return [True, ""]

def display_stats(player: dict, enemy: dict) -> None:
  display_player_stats(player)
  display_enemy_stats(enemy)

def display_player_stats(player: dict) -> None:
  print(f"Player\nHealth: {player["health"]}")   

def display_enemy_stats(enemy: dict) -> None:
  print(f"Enemy\nHealth: {enemy["health"]}") 

if __name__ == "__main__":
  main()