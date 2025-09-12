from sqlite3 import Connection, connect
import os

def connect_db(file: str) -> Connection:
    con = connect(file)
    return con

def build_tyrant_db(db, script: str, data: dict):
    exists = db in os.listdir(os.path.join(os.getcwd(), 'data'))
    conn = connect(db)
    cursor = conn.cursor()

    if not exists:
        with open(script, 'r') as f:
            sql_script = f.read()

        cursor.executescript(sql_script)

        conn.commit()

        card_insert = "INSERT INTO card(id, name, attack, health, cost, rarity, card_set, type, fusion_level, upgrade_id) VALUES (?,?,?,?,?,?,?,?,?,?)"
        for key in data:
            cursor.execute(card_insert, (data[key]['id'], data[key]['name'], data[key]['attack'], data[key]['health'], data[key]['cost'], data[key]['rarity'], data[key]['set'], data[key]['type'], data[key]['fusion_level'], data[key]['upgrade_id']))

        conn.commit()
    else:
        card_update = "UPDATE card SET id = ?, name = ?, attack = ?, health = ?, cost =?, rarity = ?, card_set=?, type=?, fusion_level=?, upgrade_id=? WHERE id =?"
        for key in data:
            cursor.execute(card_update, (data[key]['id'], data[key]['name'], data[key]['attack'], data[key]['health'], data[key]['cost'], data[key]['rarity'], data[key]['set'], data[key]['type'], data[key]['fusion_level'], data[key]['upgrade_id'], data[key]['upgrade_id']))
    conn.close()