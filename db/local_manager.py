import sqlite3
import os.path

class LocalManager():
  def __init__(self):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    self.path = os.path.join(BASE_DIR, "local_game.db")
    directory = os.path.dirname(self.path)
    if not os.path.exists(directory):
      os.makedirs(directory)

  def add_score(self, name: str, score: int, difficulty: int) -> None:
    con = sqlite3.connect(self.path)
    cur = con.cursor()
    cur.execute("INSERT INTO local_leaderboard (name, score, difficulty) VALUES (?, ?, ?)", (name, score, difficulty))
    con.commit()
    con.close()

  def get_all_high_scores(self):
    con = sqlite3.connect(self.path)
    cur = con.cursor()
    cur.execute("SELECT name, score, difficulty FROM local_leaderboard ORDER BY score DESC LIMIT 10")
    all_scores = cur.fetchall()
    con.close()
    return all_scores
