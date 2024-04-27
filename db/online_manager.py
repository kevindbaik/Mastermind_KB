import sqlite3
import json
import os.path
from models.game import Game

class OnlineManager():
  def __init__(self, path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    self.path = os.path.join(BASE_DIR, "online_game.db")
    directory = os.path.dirname(self.path)
    if not os.path.exists(directory):
      os.makedirs(directory)

  def get_player_id(self, name: str, email: str) -> int:
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      cur.execute("SELECT id FROM players WHERE name = ? AND email = ?", (name, email))
      player = cur.fetchone()
      if player:
        return player[0]
      else:
        cur.execute("INSERT INTO players (name, email) VALUES (?, ?)", (name, email))
        con.commit()
        player_id = cur.lastrowid
        return player_id
    except sqlite3.Error as err:
      print(f"Database error: {err}")
    finally:
      con.close()

  def get_game(self, game_id):
    try:
      con = sqlite3.connect(self.path)
      cur = con.cursor()
      cur.execute("SELECT * FROM games WHERE id = ?", (game_id,))
      game = cur.fetchone()
      if game:
        print("FFFFFF" ,game)
        return Game(id=game[0], player_id=game[1], difficulty=game[2], answer=game[3], attempts=game[4], history=json.loads(game[5]), hints=game[6], win=game[7], game_over=game[8])
      return None
    except sqlite3.Error as err:
      print(f"Database error: {err}")


  def save_game_to_db(self, game: Game):
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
      print(f"Database error: {err}")
    finally:
      con.close()
