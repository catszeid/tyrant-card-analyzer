from sqlite3 import Connection, connect

def connect_db(file: str) -> Connection:
    con = connect(file)
    return con

def build_tyrant_db(db, script: str):
    conn = connect(db)
    cursor = conn.cursor()

    with open(script, 'r') as f:
        sql_script = f.read()

    cursor.executescript(sql_script)

    conn.commit()
    conn.close()