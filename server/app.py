import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from flask import Flask, request, jsonify
from models.game import Game
from models.player import Player
from db.online_manager import OnlineManager

app = Flask(__name__)
online_manager = OnlineManager('db/online_game.db')

@app.route('/api/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    difficulty = data.get('difficulty')
    name = data.get('name')
    email = data.get('email')
    player_id = online_manager.get_player_id(name, email)

    game = Game(difficulty, player_id=player_id)
    game_id = online_manager.save_game_to_db(game)
    return jsonify({ 'message': 'Game started successfully', 'game_id': game_id, 'player_id': player_id })

@app.route('/api/game_status/<int:game_id>')
def get_game_status(game_id):
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

if __name__ == "__main__":
  app.run(debug=True)
