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
    url=f'http://localhost:5000/api/{game_id}/hint'
    headers = {'Content-Type': 'application/json'}
    response = self.session.post(url, headers=headers)
    return response.json()
