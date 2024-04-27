import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from flask import Flask, request, jsonify
from models.game import Game
from models.player import Player
from db.online_manager import OnlineManager

app = Flask(__name__)
online_manager = OnlineManager()

@app.route('/api/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    difficulty = data.get('difficulty')
    name = data.get('name')
    email = data.get('email')

    player_id = online_manager.get_player_id(name, email)
    try:
      game = Game(difficulty, player_id=player_id)
    except ValueError as err:
      return jsonify({'error': str(err)}), 400

    game_id = online_manager.save_game_to_db(game)
    return jsonify({ 'message': 'Game started successfully', 'game_id': game_id, 'player_id': player_id })

@app.route('/api/game/<int:game_id>', methods=['GET'])
def get_status(game_id):
  game = online_manager.get_game(game_id)

  if not game:
    return jsonify({ 'message': 'Game not found'}), 404

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

  game = online_manager.get_game(game_id)
  if not game:
    return jsonify({'error': 'Game not found'}), 404
  if game.game_over:
    return jsonify({'message': 'Game has already ended'}), 200

  try:
    game.validate_user_answer(guess)
  except ValueError as err:
    return jsonify({'error': str(err)}), 400

  if game.check_answer(guess):
    game.end_game_win()
  else:
    game.decrement_attempt()
    if game.attempts == 0:
      game.end_game_lose()
    game.store_history(guess)
    feedback = game.give_feedback(guess)

  online_manager.update_game(game_id, game)
  game_status = {
      'attempts_left': game.attempts,
      'feedback': feedback,
      'history': game.get_history()
  }
  return jsonify(game_status)


if __name__ == "__main__":
  app.run(debug=True)
