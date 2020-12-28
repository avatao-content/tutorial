import sqlite3, contextlib
from os.path import exists, join
from crypto import PasswordHasher

def setup_db(filename):
    try:
        connection = sqlite3.connect(filename)
        cur = connection.cursor()
        cur.execute('''CREATE TABLE users
                       (
                          userid INTEGER PRIMARY KEY,
                          username TEXT NOT NULL,
                          nickname TEXT NOT NULL,
                          passwordhash TEXT NOT NULL
                       )
                    ''')
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        return str(e)

DBFILE = join('/home/user/', '.users_db.db')

if not exists(DBFILE):
    setup_db(DBFILE)


def check_username_exists(username):
    with contextlib.closing( sqlite3.connect(DBFILE) ) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", [username])
        if len(cursor.fetchall()) > 0:
            return True
        return False


def add_new_user(username, password):
    with contextlib.closing( sqlite3.connect( DBFILE ) ) as con:
        if check_username_exists(username):
            return False
        else:
            with con as cur:
                cur.execute("INSERT INTO users(username, nickname, passwordhash) VALUES (?, ?, ?)", [username, username.lower(), PasswordHasher.hash(password)])
            return True

def check_login_credentials(username, password):
    with contextlib.closing( sqlite3.connect( DBFILE ) ) as con:
        if check_username_exists(username):
            cursor = con.cursor()
            cursor.execute("SELECT passwordhash FROM users WHERE username = ?", [username])
            pwdigest = cursor.fetchone()[0]
            return PasswordHasher.verify(password, pwdigest)
        return False

def set_nickname(username, nickname):
    with contextlib.closing( sqlite3.connect( DBFILE ) ) as con:
        cursor = con.cursor()
        cursor.execute("UPDATE users SET nickname = ? WHERE username = ?", [nickname, username])

def get_nickname(username):
    with contextlib.closing( sqlite3.connect( DBFILE ) ) as con:
        cursor = con.cursor()
        cursor.execute("SELECT nickname FROM users WHERE username = ?", [username])
        nickname = cursor.fetchone()
        return nickname[0]
