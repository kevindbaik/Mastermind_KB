from models.game import Game
from typing import List

class Console:
  # ------- read methods ----------
  def read_string(self, prompt: str) -> str:
    string = input(prompt)
    return string

  def read_int(self, prompt: str, max: int) -> int:
    try:
      string = input(prompt)
      number = int(string)
      if number <= 0 or number > max:
        raise ValueError(f"that's not a valid number...")
      return number
    except:
      raise ValueError(f"that's not a valid number...")

  # ------- display methods ----------
  def display_header(self, *strings: str):
    max_length = max(len(string) for string in strings)
    print("")
    print("=" * max_length)
    for string in strings:
        print(string.center(max_length))
    print("=" * max_length)
    print("")

  def display_message(self, message: str):
    print("")
    print(message)
    print("")

  def display_hint(self, message: str):
    print(f"hint: {message}")

  def display_error(self, message: str):
    print(f"input error: {message}")

  def display_difficulty(self, name: str):
    print("")
    print("===============================")
    print(f"hello {name.lower()}! choose a difficulty: ")
    print("===============================")
    print("")
    print("1 (Easy)")
    print("2 (Medium)")
    print("3 (Hard)")
    print("")

  def display_score(self, name: str, score: int):
    print(f"congratulations {name}, you won and scored: {score}!")

  def display_welcome(self, message: str):
    lines = message.split('\n')
    max_length = max(len(line) for line in lines)
    print("+" + "-" * (max_length + 2) + "+")
    for line in lines:
        print("| " + line + " " * (max_length - len(line)) + " |")
    print("+" + "-" * (max_length + 2) + "+")

  def display_menu(self):
    print("")
    print("1 (Play Against Computer)")
    print("2 (Read Rules)")
    print("3 (Exit)")
    print("")

  def display_game(self, game: Game):
    print("=" * 50)
    print(f"difficulty: {game.difficulty}")
    print(f"hints available (type hint): {game.hints}")
    print(f"attempts remaining: {game.attempts}")
    print("")
    print("previous attempts:")
    history = game.get_history()
    self._display_feedback(history, game)
    print("=" * 50)

# ----- helper methods ------
  def _display_feedback(self, history: List[str], game: Game) -> None:
    for i in range(len(history)):
      guess = history[i]
      correct_location, correct_number = game.give_feedback(guess)
      if(correct_location == 0 and correct_number == 0):
        print(f"guess #{i+1}: {guess} - all of your numbers are incorrect!")
      else:
        print(f"guess #{i+1}: {guess} - correct locations: {correct_location}, correct numbers: {correct_number}")
