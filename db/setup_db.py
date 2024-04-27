import sqlite3

con = sqlite3.connect('db/game.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS scoreboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score integer NOT NULL,
            difficulty integer NOT NULL
            )''')

cur.execute('''INSERT INTO scoreboard (name, score, difficulty) VALUES
    ('Roslansky', 1700, 3),
    ('Hagrid', 1550, 3),
    ('Kyle', 1000, 3),
    ('Sue', 500, 3),
    ('Sydney', 1500, 2),
    ('Ian', 1400, 2),
    ('Kass', 1300, 2),
    ('Nick', 500, 2),
    ('Rishi', 1200, 1),
    ('Justin', 950, 1),
    ('Teddy', 700, 1),
    ('Taryn', 300, 1)
''')
con.commit()

con.close()
