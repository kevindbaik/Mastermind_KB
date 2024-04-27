import sqlite3

class Manager():
  def __init__(self):
    self.path = 'db/game.db'

  def add_score(self, name: str, score: int, difficulty: int) -> None:
    con = sqlite3.connect(self.path)
    cur = con.cursor()
    cur.execute("INSERT INTO local_leaderboard (name, score, difficulty) VALUES (?, ?, ?)", (name, score, difficulty))
    con.commit()
    con.close()
