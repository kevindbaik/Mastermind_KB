from models.game import Game
from models.player import Player
from .console import Console

class Controller:
  def __init__(self):
    self.console = Console()
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
        print(err)

    match menu_choice:
      case 1: # play game
        self.handle_case_one()
      case 2: # read rules
        pass
      case 3: # exit game
        pass

  # ------- helpers --------
  def handle_case_one(self):
    self.console.display_header("challenge accepted!", "my names link... what's your name?")
    while True:
        try:
            name = self.console.read_string("My Name: ")
            self.player = Player(name)
            break
        except ValueError as err:
            print(err)
    self.console.display_difficulty(name)
    while True:
        try:
            difficulty = self.console.read_int("My Choice: ", 3)
            self.console.display_header("ok...give me one second...", "creating my secret code...")
            self.game = Game(difficulty)
            break
        except (ValueError, ConnectionError) as err:
            print(err)
            if isinstance(err, ConnectionError):
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
            self.game.give_hint()
          else:
            self.game.validate_user_answer(user_answer)
            break
        except ValueError as err:
          print(err)

      game_won = self.game.check_answer(user_answer)
      if game_won:
        self.game._end_game_win()
        break
      else:
        self.game.decrement_attempt()
        self.game.store_history(user_answer)
        self.console.display_game(self.game)

    ## game over
    if self.game.win:
       print("congrats you won!")
    else:
       print("you lose try again!")
