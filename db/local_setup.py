import sqlite3
import os.path

def setup_local_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "local_game.db")
    db_directory = os.path.dirname(db_path)
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS local_leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score integer NOT NULL,
                difficulty integer NOT NULL
                )''')
    scores = [
        ('Roslansky', 1700, 3),
        ('Keisha', 1550, 3),
        ('Kyle', 1000, 3),
        ('Yi', 500, 3),
        ('Sue', 100, 3),
        ('Sydney', 1500, 2),
        ('Ian', 1400, 2),
        ('Kass', 1300, 2),
        ('Lan', 500, 2),
        ('Huynh', 200, 2),
        ('Rishi', 1200, 1),
        ('Justin', 950, 1),
        ('Teddy', 700, 1),
        ('Taryn', 300, 1),
        ('JB', 100, 1)]

    cur.executemany("INSERT INTO local_leaderboard (name, score, difficulty) VALUES (?, ?, ?)", scores)

    con.commit()
    con.close()

if __name__ == '__main__':
    setup_local_db()
