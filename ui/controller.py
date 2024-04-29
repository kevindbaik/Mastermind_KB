from models.game import Game
from models.player import Player
from .console import Console
from db.local_manager import LocalManager

class Controller:
  def __init__(self):
    self.console = Console()
    self.local_manager = LocalManager()
    self.player = None
    self.game = None

  def run(self):
    self.console.display_welcome("Welcome to Mastermind!")

    self.console.display_menu()
    while True:
      try:
        menu_choice = self.console.read_int("I choose: ", 3)
        break
      except ValueError as err:
        self.console.display_error(err)

    match menu_choice:
      case 1: # play game
        self.play_game()
      case 2: # high scores
        pass
      case 3: # exit game
        self.view_scores()

  # ------- helpers --------
  def play_game(self):
    self.console.display_header("challenge accepted!", "my names link... what's your name?")
    while True:
        try:
            name = self.console.read_string("My Name: ")
            self.player = Player(name)
            break
        except ValueError as err:
            self.console.display_error(err)
    self.console.display_difficulty(name)
    while True:
        try:
            difficulty = self.console.read_int("My Choice: ", 3)
            self.console.display_header("ok...give me one second...", "creating my secret code...")
            self.game = Game(difficulty)
            break
        except ValueError as err:
            self.console.display_error(err)
        except ConnectionError as err:
           self.console.display_error(err)
           if input("do you want me to retry connecting? (y/n): ").upper() != "Y":
            return
    ## game starts
    self.console.display_game(self.game)
    while not self.game.game_over:
      if self.game.attempts == 0:
        self.game.end_game_lose()
        break
    # validates user input
      while True:
        try:
          user_answer = self.console.read_string("My Guess: ")
          if user_answer == "hint":
            self.console.display_hint(self.game.give_hint())
          else:
            self.game.validate_user_answer(user_answer)
            break
        except (ValueError, Exception) as err:
          self.console.display_error(err)

      game_won = self.game.check_answer(user_answer)
      if game_won:
        self.game.end_game_win()
        break
      else:
        self.game.decrement_attempt()
        self.game.store_history(user_answer)
        self.console.display_game(self.game)

    ## game over
    if self.game.win:
      score = self.game.calculate_score()
      self.console.display_score(self.player.name, self.game.score)
      self.local_manager.add_score(self.player.name, self.game.score, self.game.difficulty)
    else:
      self.console.display_message(f"nice try {self.player.name}... my code was: {self.game.answer}")

  def view_scores(self):
    high_scores = self.local_manager.get_all_high_scores()
    print("Top 10 Scores:")
    for score in high_scores:
      print(f"Name: {score[0]}, Score: {score[1]}, Difficulty: {score[2]}")
