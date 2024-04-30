from models.game import Game
from typing import List

class Console:
  # ------- read methods ----------
  def read_string(self, prompt: str) -> str:
    string = input(prompt)
    if string == 'return':
      return 'return'
    return string

  def read_int(self, prompt: str, max: int) -> int:
    try:
      string = input(prompt)
      number = int(string)
      if number <= 0 or number > max:
        raise ValueError(f"Please enter valid number")
      return number
    except:
      raise ValueError(f"Please enter valid number")

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
    print(f"Hint: {message}")

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

  def display_win(self, name: str, score: int):
    print(f"Congratulations {name}, you won!")
    print(f"Final Score: {score}")

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
    print("3 (View Leaderboard)")
    print("4 (View Rules)")
    print("5 (Exit Game)")
    print("")

  def display_game(self, game: Game):
    print("=" * 50)
    print("Return to Menu (type return)")
    print(f"Difficulty: {game.difficulty}")
    print(f"Hints Available (type hint): {game.hints}")
    print(f"Attempts Remaining: {game.attempts}")
    print("")
    print("Previous Attempts:")
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
    if(len(games) == 0):
      print("")
      print(f"You do not have any active games")
      print("")
      return
    print("Please choose a game to continue:")
    print("")
    for i, game in enumerate(games):
      print(f"{i + 1} (Game ID: {game['id']}, Difficulty: {game['difficulty']}, Attempts: {game['attempts']}, Hints: {game['hints']})")
    print("")

  def display_old_games(self, games):
    print("=" * 50)
    if(len(games) == 0):
      print("")
      print(f"You do not have any finished games")
      print("")
      return
    print(f"Your Previous Results:")
    print("")
    for i, game in enumerate(games):
      result = "Won" if game['win'] else "Lost"
      print(f"{i + 1}. Game ID: {game['id']}, Game Answer: {game['answer']}, Difficulty: {game['difficulty']}, Final Score: {game['score']}, Game Result: {result}")
    print("")

  def display_local_scores(self, local_scores):
    for i,score in enumerate(local_scores):
      print(f"#{i+1} {score[0]}, Score: {score[1]}, Difficulty: {score[2]}")

  def display_rules(self):
    print("=" * 50)
    print("Rules for Mastermind:")
    print("1) At the start of the game, the computer will randomly select a number combination that consists of:")
    print("     - a 4 (5 on hard) digit number")
    print("     - a range of 0-7 (0-9 on medium/hard) for each number.")
    print("2) A player will have 10 attempts to guess the number combinations.")
    print("3) At the end of each guess, computer will provide one of the following response as feedback:")
    print("     - The player had guess a correct number")
    print("     - The player had guessed a correct number and its correct location")
    print("     - The players guess was incorrect")
    print("4) If the player guesses the combination correctly, they will receive a score calculated based on:")
    print("     - remaining attempts")
    print("     - remaining hints")
    print("     - difficulty")
    print("5) You may leave at any point during the game by typing 'return'")
    print("")

  def _display_feedback(self, history: List[str], game: Game) -> None:
    for i in range(len(history)):
      guess = history[i]
      correct_location, correct_number = game.give_feedback(guess)
      if(correct_location == 0 and correct_number == 0):
        print(f"Guess #{i+1}: {guess} - All of your numbers are incorrect!")
      else:
        print(f"Guess #{i+1}: {guess} - Correct Locations: {correct_location}, Correct Numbers: {correct_number}")
