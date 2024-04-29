import sqlite3
import os

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
    cur.execute('''CREATE TABLE online_leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score integer NOT NULL,
            difficulty integer NOT NULL
            )''')

    con.commit()
    con.close()

if __name__ == '__main__':
    setup_online_db()
