from sqlite3 import Connection, connect
import os
import xml.etree.ElementTree as ET

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
        skill_insert = "INSERT INTO card_skill(owner_id, skill_id, x, y, n, c, a, trigger, card_id) VALUES (?,?,?,?,?,?,?,?,?)"
        get_skill_id = "SELECT id FROM skill WHERE ? = name_xml"
        get_trigger_id = "SELECT id FROM trigger WHERE name = ?"
        for key in data:
            owner_id = data[key]['id']
            cursor.execute(card_insert, (owner_id, data[key]['name'], data[key]['attack'], data[key]['health'], data[key]['cost'], data[key]['rarity'], data[key]['set'], data[key]['type'], data[key]['fusion_level'], data[key]['upgrade_id']))
            for skill in data[key]["skills"]:
                owner_id = int(owner_id)
                skill_name = skill.get('id', None)
                if skill_name == 'arored':
                    skill_name = 'armored'
                elif skill_name == 'Leech':
                    skill_name = 'leech'
                try:
                    skill_id = cursor.execute(get_skill_id, [skill_name]).fetchone()[0]
                except:
                    print(f"Failed to find skill in db: {skill_name}.")
                    continue
                skill_x = skill.get('x', None)
                if skill_x is not None:
                    skill_x = int(skill_x)
                skill_y = skill.get('y', None)
                if skill_y is not None:
                    skill_y = int(skill_y)
                skill_n = skill.get('n', None)
                if skill_n is not None:
                    skill_n = int(skill_n)
                skill_c = skill.get('c', None)
                if skill_c is not None:
                    skill_c = int(skill_c)
                skill_a = skill.get('a', None)
                if skill_a is not None:
                    skill_a = int(skill_a)
                skill_trigger = skill.get('trigger', None)
                if skill_trigger is not None:
                    skill_trigger = cursor.execute(get_trigger_id, [skill_trigger]).fetchone()[0]
                skill_card_id = skill.get('card_id', None)
                if skill_card_id is not None:
                    skill_card_id = int(skill_card_id)
                cursor.execute(skill_insert, (owner_id, skill_id, skill_x, skill_y, skill_n, skill_c, skill_a, skill_trigger, skill_card_id))

        conn.commit()
    else:
        card_update = "UPDATE card SET id = ?, name = ?, attack = ?, health = ?, cost =?, rarity = ?, card_set=?, type=?, fusion_level=?, upgrade_id=? WHERE id =?"
        for key in data:
            cursor.execute(card_update, (data[key]['id'], data[key]['name'], data[key]['attack'], data[key]['health'], data[key]['cost'], data[key]['rarity'], data[key]['set'], data[key]['type'], data[key]['fusion_level'], data[key]['upgrade_id'], data[key]['upgrade_id']))
    conn.close()