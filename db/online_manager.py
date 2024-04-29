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

  def save_player_to_db(self, name, email, password):
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      cur.execute("INSERT into players (name, email, password) VALUES (?, ?, ?)",
                  (name, email.lower(), password))
      con.commit()
      player_id = cur.lastrowid
      return {'player_id': player_id, 'name': name, 'email': email }, 201
    except sqlite3.IntegrityError as err:
      return {'error': 'This username or email already exists'}, 409
    except Exception as err:
      return {'error': str(err)}, 500
    finally:
      con.close()

  def get_player(self, email: str):
    try:
      con = sqlite3.connect(self.path)
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute("SELECT id, name, email, password FROM players WHERE email = ?", (email.lower(),))
      player = cur.fetchone()
      if player:
        player_dict = dict(player)
        check_password = player_dict.pop('password')
        return player_dict, check_password, 200
      else:
        return {'error': 'User email does not exist in database'}, None, 404
    except sqlite3.Error as err:
      return {'error': str(err)}, 500
    finally:
      con.close()

  def save_game_to_db(self, game: Game) -> int:
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      history_json = json.dumps(game.history) #converts my list to a json string
      cur.execute("INSERT INTO games (player_id, difficulty, answer, attempts, history, hints, win, game_over, score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
      (game.player_id, game.difficulty, game.answer, game.attempts, history_json, game.hints, game.win, game.game_over, game.score))
      con.commit()

      game_id = cur.lastrowid
      game_dict = {
      'game_id': game_id,
      'player_id': game.player_id,
      'difficulty': game.difficulty,
      'answer': game.answer,
      'attempts': game.attempts,
      'history': game.history,
      'hints': game.hints,
      'win': game.win,
      'game_over': game.game_over,
      'score': game.score
      }
      return game_dict, 200
    except sqlite3.Error as err:
      return {'error': str(err)}, 500
    finally:
      con.close()

  def get_player_games(self, player_id, game_over):
    try:
      con = sqlite3.connect(self.path)
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute(f"SELECT * FROM games WHERE player_id = ? AND game_over = {game_over}", (player_id,))
      games = cur.fetchall()
      games_list = []
      for game in games:
          game_dict = dict(game)
          if game_dict['history']:
              game_dict['history'] = json.loads(game_dict['history']) #converts json string back to py list
          if not game_over:
            del game_dict['answer']
          games_list.append(game_dict)
      return games_list
    except sqlite3.Error as err:
      return {'error': str(err)}
    finally:
      con.close()

  def get_game(self, game_id: int) -> Game:
    try:
      con = sqlite3.connect(self.path)
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute('''
          SELECT games.*, players.name AS player_name
          FROM games
          JOIN players ON games.player_id = players.id
          WHERE games.id = ?
      ''', (game_id,))
      result = cur.fetchone()
      if result:
        game = Game(id=result[0], player_id=result[1], difficulty=result[2], answer=result[3], attempts=result[4], history=json.loads(result[5]), hints=result[6], win=result[7], game_over=result[8], score=0)
        player_name = result['player_name']
        return (game, player_name)
      else:
        return (None, None)
    except sqlite3.Error as err:
      return jsonify({'error': str(err)})
    finally:
      con.close()

  def get_leaderboard(self):
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      cur.execute('''SELECT name, score, difficulty FROM online_leaderboard ORDER BY score DESC LIMIT 10''')
      rows = cur.fetchall()
      leaderboard = []
      for row in rows:
        row_dict = {'name': row[0], 'score':row[1], 'difficulty': row[2]}
        leaderboard.append(row_dict)
      return leaderboard
    except sqlite3.Error as err:
      return jsonify({'error': str(err)})
    finally:
      con.close()

  def update_game(self, game_id: int, game: Game) -> None:
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      history_json = json.dumps(game.history)
      cur.execute("UPDATE games SET attempts = ?, win = ?, game_over = ?, history = ?, hints = ?, score = ? WHERE id = ?",
                        (game.attempts, game.win, game.game_over, history_json, game.hints, game.score, game_id))
      con.commit()
    except sqlite3.Error as err:
      return jsonify({'error': str(err)})
    finally:
      con.close()

  def save_score_to_game(self, game_id, score):
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      cur.execute("UPDATE game SET score = ? WHERE id = ?", (score, game_id))
      con.commit()
    except sqlite3.Error as err:
      return jsonify({'error': str(err)})
    finally:
      con.close()

  def save_score_to_leaderboard(self, name, score, difficulty):
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      cur.execute("INSERT INTO online_leaderboard (name, score, difficulty) VALUES (?, ?, ?)",
                  (name, score, difficulty))
      con.commit()
    except sqlite3.Error as err:
      return jsonify({'error' : str(err)})
    finally:
      con.close()
