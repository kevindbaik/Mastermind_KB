import sqlite3
import json
import os.path

class OnlineManager():
  def __init__(self, path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    self.path = os.path.join(BASE_DIR, "online_game.db")
    directory = os.path.dirname(self.path)
    if not os.path.exists(directory):
      os.makedirs(directory)

  def get_player_id(self, name, email):
    con = None
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
    except Exception as ex:
      print(f"An error has occured: {ex}")
    finally:
      if con:
        con.close()

  def save_game_to_db(self, game):
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
