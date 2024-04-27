import sqlite3

class LocalManager():
  def __init__(self):
    self.path = 'db/local_game.db'

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
