from models.game import Game
from models.player import Player
from .console import Console
from db.local_manager import LocalManager
from models.player_service import PlayerService
from typing import Dict

class Controller:
  def __init__(self):
    self.console = Console()
    self.local_manager = LocalManager()
    self.player_service = PlayerService()
    self.player = None

  def run(self, player_session=False):
    self.console.display_welcome("Welcome to Mastermind!")

    self.console.display_menu()
    while True:
      try:
        menu_choice = self.console.read_int("I choose: ", 5)
        break
      except ValueError as err:
        self.console.display_error(err)

    match menu_choice:
      case 1:
        self.local_game(player_session)
      case 2:
        self.online_game(player_session)
      case 3:
        self.view_scores(player_session)
      case 4:
        self.view_rules(player_session)
      case 5:
        exit()

  # ------- menu methods --------
  def local_game(self, player_session):
    self.console.display_message("Hello! What is your name?")
    while True:
        try:
            name = self.console.read_string("My Name: ")
            self.player = Player(name)
            break
        except ValueError as err:
            self.console.display_error(err)
    self.start_local_game(name, player_session)


  def online_game(self, player_session):
    if player_session:
      self.display_online_menu(player_session)
    else:
      self.console.display_choices("Register", "Log In", "Return To Main Menu")
      while True:
        try:
          choice = self.console.read_int("I choose: ", 3)
          break
        except ValueError as err:
          self.console.display_error(err)
      match choice:
        case 1:
          player_session = self.handle_signup()
        case 2:
          player_session = self.handle_login()
        case 3:
          self.run()
      self.display_online_menu(player_session)

  def view_scores(self, player_session):
    self.console.display_choices("Local Leaderboard", "Online Leaderboard", "Return To Menu")
    while True:
      try:
        choice = self.console.read_int("I choose: ", 3)
        break
      except ValueError as err:
        self.console.display_error(err)
    match choice:
      case 1:
        local_scores = self.local_manager.get_all_high_scores()
        self.console.display_local_scores(local_scores)
        self.return_menu(player_session)
      case 2:
        self.handle_online_scores()
        self.return_menu(player_session)
      case 3:
        self.run()

  def view_rules(self, player_session):
    self.console.display_rules()
    self.return_menu(player_session)

  # ------ LOCAL main helpers ---------
  def start_local_game(self, name, player_session):
    local_game = None
    self.console.display_difficulty()
    while True:
      try:
          difficulty = self.console.read_int("My Choice: ", 3)
          local_game = Game(difficulty)
          break
      except ValueError as err:
          self.console.display_error(err)
      except ConnectionError as err:
        self.console.display_error(err)
        if input("Try reconnecting? (y/n): ").upper() != "Y":
          return
    ## game starts
    self.console.display_game(local_game)
    while not local_game.game_over:
      if local_game.attempts == 0:
        local_game.end_game_lose()
        break
    # validates user input
      while True:
        try:
          user_answer = self.console.read_string("My Guess: ")
          if user_answer.lower() == "hint":
            self.console.display_hint(local_game.give_hint())
          else:
            local_game.validate_user_answer(user_answer)
            break
        except (ValueError, Exception) as err:
          self.console.display_error(err)

      game_won = local_game.check_answer(user_answer)
      if game_won:
        local_game.end_game_win()
        break
      else:
        local_game.decrement_attempt()
        local_game.store_history(user_answer)
        self.console.display_game(local_game)
    ## game over
    if local_game.win:
      score = local_game.calculate_score()
      self.console.display_win(self.player.name, score)
      self.local_manager.add_score(self.player.name, score, local_game.difficulty)
      self.play_again(name, player_session)
    else:
      self.console.display_message(f"Sorry {self.player.name}, the code was: {local_game.answer}")
      self.play_again(name, player_session)

  # ------ ONLINE main helpers --------
  def display_online_menu(self, player_session):
    self.console.display_choices("Play New Game", "Resume Games", "View Game Results", "Return To Main Menu")
    while True:
      try:
        game_choice = self.console.read_int("I choose: ", 4)
        break
      except ValueError as err:
        self.console.display_error(err)
    match game_choice:
      case 1:
        self.start_online_game(player_session)
      case 2:
        self.continue_game(player_session)
      case 3:
        self.display_history(player_session)
      case 4:
        self.run(player_session=player_session)

  def start_online_game(self, player_session):
    self.console.display_difficulty()
    while True:
      try:
        difficulty = self.console.read_int("I choose: ", 3)
        break
      except ValueError as err:
        self.console.display_error(err)
    online_game = self.handle_create_game(difficulty)
    self.play_online_game(online_game, player_session)

  def continue_game(self, player_session):
    online_game = self.handle_get_game_in_progress(player_session)
    self.play_online_game(online_game, player_session)

  def display_history(self, player_session):
    response = self.player_service.fetch_user_games_ended(player_session['id']) #{'success' : [ dict(game), dict(game), ...]}
    if 'success' in response:
      data = response['success']
      self.console.display_old_games(data)
      self.return_online_menu(player_session)
    else:
      self.console.display_error(response['error'])

  def play_online_game(self, online_game, player_session):
    self.console.display_game(online_game)
    while not online_game.game_over:
      while True:
        user_answer = self.console.read_string("My Guess: ")
        self.check_return(user_answer, player_session=player_session)
        if user_answer.lower() == "hint":
          self.handle_hint_request(online_game)
        else:
          self.handle_make_guess(online_game, user_answer, player_session)
          if online_game.game_over is True:
            break
    # game is over
    self.display_game_over(player_session)

  def display_game_over(self, player_session):
    self.console.display_choices("Play again?", "Return to Menu", "Exit Game")
    while True:
      try:
        choice = self.console.read_int("I choose: ", 3)
        break
      except ValueError as err:
        self.console.display_error(err)
    match choice:
      case 1:
        self.start_online_game(player_session)
      case 2:
        self.display_online_menu(player_session)
      case 3:
        exit()

  # ----- handle api -------
  def handle_signup(self):
    while True:
      name = self.console.read_string("Enter Your Name: ")
      email = self.console.read_string("Enter Your Email: ")
      password = self.console.read_string("Enter Your Password: ")
      response = self.player_service.create_player(name, email, password)
      if 'success' in response: #{'success': {'player_id':int,  'name': str, 'email': str}}
        player_session = response['success']
        self.console.display_message(f"Welcome To Online Mastermind {name}!")
        return player_session
      else:
        self.console.display_error(response['error'])

  def handle_login(self):
    while True:
      email = self.console.read_string("Enter Your Email: ")
      password = self.console.read_string("Enter Your Password: ")
      response = self.player_service.login_player(email, password)
      if 'success' in response:
        player_session = response['success']
        self.console.display_message(f"Welcome Back {player_session['name']}!")
        return player_session
      else:
        self.console.display_error(response['error'])

  def handle_create_game(self, difficulty: int) -> Game:
    response = self.player_service.create_game(difficulty)
    if 'success' in response:
      data = response['success']
      online_game = Game(difficulty=data['difficulty'], answer=data['answer'], player_id=data['player_id'], id=data['game_id'])
      return online_game
    else:
      self.console.display_error(response['error'])

  def handle_get_game_in_progress(self, player_session: Dict) -> Game:
    response = self.player_service.fetch_user_games_active(player_session['id'])
    if 'success' in response: #{'success' : [ dict(game), dict(game), ...]}
      data = response['success']
      self.console.display_resume_games(data)
      if len(data) == 0:
        self.return_online_menu(player_session)
      while True:
        try:
          game_choice = self.console.read_int("I choose: ", len(data))
          break
        except ValueError as err:
          self.console.display_error(err)
      game = data[game_choice - 1]
      online_game = Game(difficulty=game['difficulty'],answer=game['answer'],attempts=game['attempts'], history=game['history'], hints=game['hints'],player_id=game['player_id'],id=game['id'])
      return online_game
    else:
      self.console.display_error(response['error'])

  def handle_make_guess(self, online_game, user_answer, player_session):
    response = self.player_service.fetch_make_guess(online_game.id, user_answer)
    if 'success' in response: #{'success': { 'attempts': int, 'history:' : List[str] }}
      data = response['success']
      online_game.attempts = data['attempts']
      online_game.history = data['history']
      self.console.display_game(online_game)
    elif 'game_over' in response: #{'game_over': {'result': bool, 'score : int}}
      data = response['game_over']
      if data['result'] is True:
        self.console.display_win(player_session['name'], data['score'])
        online_game.game_over = True
      else:
        self.console.display_message(f"Nice try {player_session['name']}! The code was: {online_game.answer}")
        online_game.game_over = True
    else:
      self.console.display_error(response['error'])

  def handle_hint_request(self, online_game):
    response = self.player_service.fetch_hint(online_game.id)
    if 'success' in response: #{'success': { 'hint': str, 'hints_left' : str}}
      data = response['success']
      online_game.attempts -= 1
      self.console.display_hint(data['hint'])
    else:
      self.console.display_error(response['error'])

  def handle_online_scores(self):
    response = self.player_service.fetch_online_scores()
    if 'success' in response:
      online_scores = response['success']
      for i,score in enumerate(online_scores):
        print(f"#{i+1} {score['name']}, Score: {score['score']}, Difficulty: {score['difficulty']}")
    else:
      self.console.display_error(response['error'])

  # ---- small helpers -----
  def return_menu(self, player_session):
    input = self.console.read_string("Enter any key to return to menu: ")
    if input is not None:
      self.run(player_session)

  def return_online_menu(self, player_session):
    input = self.console.read_string("Enter any key to return to menu: ")
    if input is not None:
      self.display_online_menu(player_session)

  def check_return(self, input, player_session=False):
    if input == 'return':
      self.run(player_session=player_session)
    else:
      return True

  def play_again(self, name, player_session):
    self.console.display_choices("Play Again", "Return to Main Menu")
    while True:
      try:
        choice = self.console.read_int("I choose: ", 2)
      except ValueError as err:
        self.console.display_error(err)
      match choice:
        case 1:
          self.start_local_game(name, player_session)
        case 2:
          self.run(player_session=player_session)
