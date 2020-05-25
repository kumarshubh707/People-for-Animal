import sqlite3

def connect():
    conn = sqlite3.connect("./bookshelf_database.db")
    cur = conn.cursor()
    return conn, cur


def create_db():
    conn, cur = connect()

    cur.execute("--query here--")

    data = cur.fetchall()

    conn.commit()
    conn.close()


