from models.game import Game
from models.player import Player
from .console import Console
from db.local_manager import LocalManager
from models.player_service import PlayerService

class Controller:
  def __init__(self):
    self.console = Console()
    self.local_manager = LocalManager()
    self.player_service = PlayerService()
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
        self.play_local_game()
      case 2: # high scores
        self.play_online_game()
      case 3: # exit game
        self.view_scores()

  # ------- menu methods --------
  def play_local_game(self):
    self.console.display_header("challenge accepted!", "my names link... what's your name?")
    while True:
        try:
            name = self.console.read_string("My Name: ")
            self.player = Player(name)
            break
        except ValueError as err:
            self.console.display_error(err)
    self.console.display_difficulty()
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

  def play_online_game(self):
    self.console.display_choices("Register", "Log In")
    while True:
      try:
        login_choice = self.console.read_int("I choose: ", 2)
        break
      except ValueError as err:
        self.console.display_error(err)
    match login_choice:
      case 1:
        while True:
          name = self.console.read_string("Enter Your Name: ")
          email = self.console.read_string("Enter Your Email: ")
          password = self.console.read_string("Enter Your Password: ")
          response = self.player_service.create_player(name, email, password)
          if 'success' in response:
            player_info = response['success']
            self.console.display_message(f"Welcome To Online Mastermind {name}!")
            break
          else:
            self.console.display_error(response['error'])
      case 2:
        while True:
          email = self.console.read_string("Enter Your Email: ")
          password = self.console.read_string("Enter Your Password: ")
          response = self.player_service.login_player(email, password)
          if 'success' in response:
            player_info = response['success']
            self.console.display_message(f"Welcome Back {player_info['name']}!")
            break
          else:
            self.console.display_error(response['error'])

    self.console.display_choices("Play New Game", "Resume Ongoing Games", "View Past Game Results")
    while True:
      try:
        game_choice = self.console.read_int("I choose: ", 2)
        break
      except ValueError as err:
        self.console.display_error(err)
    match game_choice:
      case 1:
        self.console.display_difficulty()
        while True:
          try:
            difficulty = self.console.read_int("I choose: ", 3)
            break
          except ValueError as err:
            self.console.display_error(err)
        response = self.player_service.create_game(difficulty)
        if 'success' in response:
          game_data = response['success']
          online_game = Game(difficulty=game_data['difficulty'], answer=game_data['answer'], attempts=game_data['attempts'], history=game_data['history'], hints=game_data['hints'], win=game_data['win'], game_over=game_data['game_over'], player_id=game_data['player_id'], id=game_data['game_id'], score=game_data['score'])
          self.console.display_game(online_game)
          while not online_game.game_over:
            while True:
              user_answer = self.console.read_string("My Guess: ")
              if user_answer == "hint":
                response = self.player_service.fetch_hint(online_game.id)
                if 'success' in response: #{'success': { 'hint': xx, 'hints_left' : xx}}
                  data = response['success']
                  online_game.attempts -= 1
                  self.console.display_message(data['hint'])
                else:
                  self.console.display_error(response['error'])
              else:
                response = self.player_service.fetch_make_guess(online_game.id, user_answer)
                if 'success' in response: #{'success': {}}
                  data = response['success']
                  online_game.attempts = data['attempts']
                  online_game.history = data['history']
                  self.console.display_game(online_game)
                elif 'game_over' in response:
                  data = response['game_over']
                  if data['result'] is True:
                    self.console.display_score(player_info['name'], data['score'])
                    break
                  else:
                    self.console.display_message(f"nice try {player_info['name']}... my code was: {online_game.answer}")
                    break
                else:
                  self.console.display_error(response['error'])
        else:
          self.console.display_error(response['error'])
  # ------ helpers --------
  def view_scores(self):
    high_scores = self.local_manager.get_all_high_scores()
    print("Top 10 Scores:")
    for score in high_scores:
      print(f"Name: {score[0]}, Score: {score[1]}, Difficulty: {score[2]}")
