import sqlite3

con = sqlite3.connect('local_game.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS local_leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score integer NOT NULL,
            difficulty integer NOT NULL
            )''')

cur.execute('''INSERT INTO local_leaderboard (name, score, difficulty) VALUES
    ('Roslansky', 1700, 3),
    ('Hagrid', 1550, 3),
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
    ('JB', 100, 1)
''')
con.commit()

con.close()
