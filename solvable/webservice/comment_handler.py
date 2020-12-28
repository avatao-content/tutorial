import sqlite3, contextlib
from os.path import exists, join

def setup_db(filename):
    try:
        connection = sqlite3.connect(filename)
        cur = connection.cursor()
        cur.execute('''CREATE TABLE comments
                       (
                          name TEXT,
                          comment TEXT,
                          filename TEXT
                       )
                    ''')
        connection.commit()
        connection.close()
    except Exception as e:
        pass

DBFILE = join('/home/user/', '.comments_db.db')

if not exists(DBFILE):
    setup_db(DBFILE)

def add_new_comment(to_insert):
    with contextlib.closing( sqlite3.connect( DBFILE ) ) as con:
        with con as cur:
            cur.execute("INSERT INTO comments VALUES (?,?,?)", (to_insert[0], to_insert[1], to_insert[2]) )


def get_all_comments():
    with contextlib.closing( sqlite3.connect( DBFILE ) ) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM comments")
        rows = cur.fetchall()
    return reversed(rows)
