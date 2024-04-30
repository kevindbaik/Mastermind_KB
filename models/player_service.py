import requests

class PlayerService:
  def __init__(self):
    self.session = requests.Session()

  def create_player(self, name, email, password):
    url = 'http://localhost:5000/api/player'
    headers = {'Content-Type': 'application/json'}
    data = {
        'name': name,
        'email': email,
        'password': password
    }
    response = self.session.post(url, json=data, headers=headers)
    return response.json()


  def login_player(self, email, password):
    url = 'http://localhost:5000/api/player/login'
    headers = {'Content-Type': 'application/json'}
    data = {
        'email': email,
        'password': password
    }
    response = self.session.post(url, json=data, headers=headers)
    return response.json()

  def create_game(self, difficulty):
    url='http://localhost:5000/api/start_game'
    headers = {'Content-Type': 'application/json'}
    data = {
      'difficulty': difficulty
    }
    response = self.session.post(url, json=data, headers=headers)
    return response.json()

  def fetch_hint(self, game_id):
    url=f"http://localhost:5000/api/game/{game_id}/hint"
    response = self.session.post(url)
    return response.json()

  def fetch_make_guess(self, game_id, user_answer):
    url=f"http://localhost:5000/api/game/{game_id}/guess"
    headers = {'Content-Type': 'application/json'}
    data = {
      "guess": user_answer
    }
    response = self.session.post(url, json=data, headers=headers)
    return response.json()

  def fetch_user_games_active(self, player_id):
    url=f"http://localhost:5000/api/player/{player_id}/games/ongoing"
    response = self.session.get(url)
    return response.json()

  def fetch_user_games_ended(self, player_id):
    url=f"http://localhost:5000/api/player/{player_id}/games/ended"
    response = self.session.get(url)
    return response.json()
