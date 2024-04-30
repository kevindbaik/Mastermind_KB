import sqlite3
import os.path
import json

def setup_online_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "online_game.db")
    db_directory = os.path.dirname(db_path)
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS players")
    cur.execute("DROP TABLE IF EXISTS games")
    cur.execute("DROP TABLE IF EXISTS online_leaderboard")

    #
    cur.execute('''
        CREATE TABLE players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
    cur.execute('''
        CREATE TABLE games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            difficulty INTEGER,
            answer TEXT,
            attempts INTEGER,
            history TEXT,
            hints INTEGER,
            win BOOLEAN,
            game_over BOOLEAN,
            score INTEGER,
            FOREIGN KEY (player_id) REFERENCES players (id)
        )''')
    cur.execute('''
        CREATE TABLE online_leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            difficulty INTEGER NOT NULL
        )''')

    # seeders
    one_list = ['1111', '2222', '1234', '1111', '1111', '1111', '2222', '2222', '4444']
    one_string = json.dumps(one_list)
    two_list = ['1111']
    two_string = json.dumps(two_list)
    cur.execute("INSERT INTO players (name, email, password) VALUES (?, ?, ?)",
                ("Demo User", "demouser@demo.com", "demouser"))
    cur.execute("INSERT INTO games (player_id, difficulty, answer, attempts, history, hints, win, game_over, score) VALUES (1, 3, '1234', 1, ?, 2, TRUE, TRUE, 300)", (one_string,))
    cur.execute("INSERT INTO games (player_id, difficulty, answer, attempts, history, hints, win, game_over, score) VALUES (1, 2, '5678', 9, ?, 1, FALSE, FALSE, 0)", (two_string,))

    scores = [
        ("Frodo", 1600, 3),
        ("Sam", 1599, 3),
        ("Merry", 900, 2),
        ("Pippin", 500, 2),
        ("Harry", 1200, 2),
        ("Hermione", 1700, 3),
        ("Ron", 100, 1),
        ("Luna", 600, 1),
        ("Malfoy", 200, 1),
        ("Voldemort", 1000, 1)
    ]
    cur.executemany("INSERT INTO online_leaderboard (name, score, difficulty) VALUES (?, ?, ?)", scores)
    con.commit()
    con.close()

if __name__ == '__main__':
    setup_online_db()
