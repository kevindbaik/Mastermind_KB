import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from flask import Flask, request, jsonify, session
from models.game import Game
from models.player import Player
from db.online_manager import OnlineManager

app = Flask(__name__)
app.secret_key = 'alright_then_keep_your_secrets'
online_manager = OnlineManager()

@app.route('/api/player', methods=['POST'])
def create_player():
  data = request.get_json()
  name = str(data.get('name', '')).strip()
  password = str(data.get('password', '')).strip()
  email = str(data.get('email', '')).strip()

  if 'player_id' in session:
      return jsonify({'message': 'You are already logged in.'}), 200
  if not name or not password or not email:
    return jsonify({'error': 'Missing username, password, or email'}), 400
  try:
    player = Player(name=name, email=email, password=password)
  except ValueError as err:
    return jsonify({'error': str(err)}), 400

  email = email.lower()
  response, status_code = online_manager.save_player_to_db(name, email, password)
  response = response.get_json()
  if status_code == 201:
    session['player_id'] = response['player_id']
    session['email'] = email
    return jsonify({'message': 'User created successfully'}), 201
  else:
    return response, status_code

@app.route('/api/player/login', methods=['POST'])
def login_player():
  data = request.get_json()
  email = str(data.get('email', '')).strip()
  password = str(data.get('password', '')).strip()

  if not email or not password:
    return jsonify({'error': 'Missing email or password'}), 400
  if 'player_id' in session:
    return jsonify({'message': 'You are already logged in.'}), 200
  if not isinstance(email, str) or "@" not in email:
    return jsonify({'error': 'Invalid email address'})
  player = online_manager.get_player(email)
  if player is None:
      return jsonify({'error': 'User email does not exist in database'}), 404
  elif password != player['password']:
    return jsonify({'error': 'User password is incorrect'})
  else:
      session['player_id'] = player['id']
      session['email'] = email.lower()
      return jsonify({'message': 'Login successful'}), 200

@app.route('/api/player/<int:player_id>/games/ongoing', methods=['GET'])
def get_player_games_active(player_id):
  games = online_manager.get_player_games(player_id, game_over=False)
  if isinstance(games, dict) and 'error' in games:
    return jsonify(games), 500
  return jsonify({'games': games}), 200

@app.route('/api/player/<int:player_id>/games/ended', methods=['GET'])
def get_player_games_ended(player_id):
  games = online_manager.get_player_games(player_id, game_over=True)
  if isinstance(games, dict) and 'error' in games:
    return jsonify(games), 500
  return jsonify({'games': games}), 200

@app.route('/api/player/logout', methods=['GET'])
def logout_player():
  if 'player_id' in session:
      session.pop('player_id', None)
      session.pop('email', None)
      return jsonify({'message' : 'You have been logged out'}), 200
  else:
    return jsonify({'error': 'No user is currently logged in'}), 403

@app.route('/api/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    difficulty = data.get('difficulty')

    if 'player_id' not in session:
      return jsonify({'error': 'You must be logged in to play'}), 400

    try:
      game = Game(difficulty, player_id=session['player_id'])
    except ValueError as err:
      return jsonify({'error': str(err)}), 400

    game_id = online_manager.save_game_to_db(game)
    return jsonify({ 'message': 'Game started successfully', 'game_id': game_id, 'player_id': session['player_id']}), 201

@app.route('/api/game/<int:game_id>', methods=['GET'])
def get_status(game_id):
  game, player_name = online_manager.get_game(game_id)

  if not game:
    return jsonify({ 'message': 'Game not found'}), 404
  if game.game_over:
    return jsonify({'message': 'Game has already ended'}), 200
  if game.player_id != session['player_id']:
    return jsonify({'error': 'Game does not belong to user'}),403

  game_status = {
    'game_id': game_id,
    'player_id': game.player_id,
    'difficulty': game.difficulty,
    'attempts_left': game.attempts,
    'hints_left': game.hints,
    'win': game.win,
    'game_over': game.game_over,
    'history': game.history}
  return jsonify(game_status)

@app.route('/api/game/<int:game_id>/guess', methods=['POST'])
def make_guess(game_id):
  data = request.get_json()
  guess = data.get('guess')
  if not guess:
    return jsonify({'error': 'Missing guess'}), 400
  if 'player_id' not in session:
    return jsonify({'error' : 'User must be logged in'}), 400
  game, player_name = online_manager.get_game(game_id)
  if not game:
    return jsonify({'error': 'Game not found'}), 404
  if game.game_over:
    return jsonify({'message': 'Game has already ended'}), 200
  if game.player_id != session['player_id']:
    return jsonify({'error': 'Game does not belong to user'}),403

  try:
    game.validate_user_answer(guess)
  except ValueError as err:
    return jsonify({'error': str(err)}), 400

  if game.check_answer(guess):
    game.end_game_win()
    score = game.calculate_score()
    online_manager.save_score_to_game(game.id, score)
    online_manager.update_game(game_id, game)
    online_manager.save_score_to_leaderboard(player_name, game.score, game.difficulty)
    return jsonify({'message' : 'Congratulations.. You Won!'})
  else:
    game.decrement_attempt()
    if game.attempts == 0:
      game.end_game_lose()
    game.store_history(guess)
    feedback = game.give_feedback(guess)
    feedback_dict = { 'correct_locations': feedback[0], 'correct_numbers': feedback[1] }

    historical_feedback = []
    for i, guess in enumerate(game.get_history()):
      feedback = game.give_feedback(guess)
      feedback_entry = {
          'guess_number': i + 1,
          'guess': guess,
          'feedback': {
              'correct_location': feedback[0],
              'correct_number': feedback[1]
          }
      }
      historical_feedback.append(feedback_entry)
  online_manager.update_game(game_id, game)
  game_status = {
      'difficulty': game.difficulty,
      'guess': guess,
      'attempts_remaining': game.attempts,
      'feedback': feedback_dict,
      'previous_attempts': historical_feedback
  }
  return jsonify(game_status)

@app.route('/api/game/<int:game_id>/hint', methods=['POST'])
def get_hint(game_id):
  game, player_name = online_manager.get_game(game_id)
  if game is None:
    return jsonify({'error': 'Game not found'}), 404
  if game.game_over:
    return jsonify({'message': 'Game has already ended'}), 200
  if game.player_id != session['player_id']:
    return jsonify({'error': 'Game does not belong to user'}),403

  try:
    hint = game.give_hint()
    online_manager.update_game(game_id, game)
    return jsonify({'hint': hint, 'hints_left': game.hints})
  except Exception as err:
    return jsonify({'error': str(err)}), 400

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
  leaderboard = online_manager.get_leaderboard()
  return jsonify({'leaderboard': leaderboard})

if __name__ == "__main__":
  app.run(debug=True)
