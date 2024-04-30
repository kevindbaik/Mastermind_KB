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
        raise ValueError(f"Please enter valid number...")
      return number
    except:
      raise ValueError(f"That's not a valid number...")

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


  def display_hint(self, message: str):
    print(f"hint: {message}")

  def display_error(self, message: str):
    print("-" * 50)
    print(f"Error: {message}")
    print("-" * 50)

  def display_difficulty(self):
    print("")
    print("=" * 50)
    print(f"Choose your difficulty: ")
    print("=" * 50)
    print("")
    print("1 (Easy)")
    print("2 (Medium)")
    print("3 (Hard)")
    print("")

  def display_score(self, name: str, score: int):
    print(f"congratulations {name}, you won!")
    print(f"total score: {score}")

  def display_welcome(self, message: str):
    lines = message.split('\n')
    max_length = max(len(line) for line in lines)
    print("+" + "-" * (max_length + 2) + "+")
    for line in lines:
        print("| " + line + " " * (max_length - len(line)) + " |")
    print("+" + "-" * (max_length + 2) + "+")

  def display_menu(self):
    print("")
    print("1 (Play Local)")
    print("2 (Play Online)")
    print("3 (View High Scores)")
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

  def display_choices(self, *strings):
    print("=" * 50)
    print("Please select an option:")
    print("")
    for i, option in enumerate(strings):
      print(f"{i + 1} ({option})")
    print("")

  def display_resume_games(self, games):
    print("=" * 50)
    print("Please choose a game to continue:")
    print("")
    for i, game in enumerate(games):
      print(f"{i + 1} (Game ID: {game['id']}, Difficulty: {game['difficulty']}, Attempts: {game['attempts']}, Hints: {game['hints']})")
    print("")
# ----- helper methods ------
  def _display_feedback(self, history: List[str], game: Game) -> None:
    for i in range(len(history)):
      guess = history[i]
      correct_location, correct_number = game.give_feedback(guess)
      if(correct_location == 0 and correct_number == 0):
        print(f"guess #{i+1}: {guess} - all of your numbers are incorrect!")
      else:
        print(f"guess #{i+1}: {guess} - correct locations: {correct_location}, correct numbers: {correct_number}")
