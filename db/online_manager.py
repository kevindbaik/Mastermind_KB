import sqlite3
import json
import os.path
from models.game import Game
from flask import jsonify

class OnlineManager():
  def __init__(self):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    self.path = os.path.join(BASE_DIR, "online_game.db")
    directory = os.path.dirname(self.path)
    if not os.path.exists(directory):
      os.makedirs(directory)

  def save_player_to_db(self, name, password, email):
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      cur.execute("INSERT into players (name, password, email) VALUES (?, ?, ?)",
                  (name, password, email))
      con.commit()
      player_id = cur.lastrowid
      return jsonify({'message': 'User created successfully', 'player_id': player_id}), 201
    except sqlite3.IntegrityError as err:
      return jsonify({'error': 'This username or email already exists'}), 409
    except Exception as err:
      return jsonify({'error': str(err)}), 500
    finally:
      con.close()

  def get_player(self, email: str):
    try:
      con = sqlite3.connect(self.path)
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute("SELECT * FROM players WHERE email = ?", (email,))
      player = cur.fetchone()
      if player:
        return dict(player)
    except sqlite3.Error as err:
      return jsonify({'error': str(err)})
    finally:
      con.close()

  def get_game(self, game_id: int) -> Game:
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      cur.execute("SELECT * FROM games WHERE id = ?", (game_id,))
      game = cur.fetchone()
      if game:
        return Game(id=game[0], player_id=game[1], difficulty=game[2], answer=game[3], attempts=game[4], history=json.loads(game[5]), hints=game[6], win=game[7], game_over=game[8])
      else:
        return None
    except sqlite3.Error as err:
      return jsonify({'error': str(err)})
    finally:
      con.close()

  def update_game(self, game_id: int, game: Game) -> None:
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      history_json = json.dumps(game.history)
      cur.execute("UPDATE games SET attempts = ?, win = ?, game_over = ?, history = ?, hints = ? WHERE id = ?",
                        (game.attempts, game.win, game.game_over, history_json, game.hints, game_id))
      con.commit()
    except sqlite3.Error as err:
      return jsonify({'error': str(err)})
    finally:
      con.close()

  def save_game_to_db(self, game: Game) -> int:
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      history_json = json.dumps(game.history)
      cur.execute("INSERT INTO games (player_id, difficulty, answer, attempts, history, hints, win, game_over) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
      (game.player_id, game.difficulty, game.answer, game.attempts, history_json, game.hints, game.win, game.game_over))
      con.commit()
      game_id = cur.lastrowid
      return game_id
    except sqlite3.Error as err:
      return jsonify({'error': str(err)})
    finally:
      con.close()
