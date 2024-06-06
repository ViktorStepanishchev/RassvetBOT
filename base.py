import sqlite3

db = sqlite3.connect("anketa.db")
cursor = db.cursor()
def create_db():
    cursor.execute("""CREATE TABLE IF NOT EXISTS data_users(
        id TEXT,
        name TEXT,
        occupation TEXT,
        education TEXT,
        about TEXT,
        photo TEXT,
        username TEXT
        )""")
    db.commit()

def add_user(user_id: int, data, username) -> None:
    name = data.get('name')
    occupation = data.get('occupation')
    education = data.get('education')
    about = data.get('about')
    photo = data.get('photo')
    cursor.execute("INSERT INTO data_users VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, name, occupation, education, about, photo, username))
    db.commit()

def update_user(user_id: int, data) -> None:
    name = data.get('name')
    occupation = data.get('occupation')
    education = data.get('education')
    about = data.get('about')
    photo = data.get('photo')
    cursor.execute("""UPDATE data_users SET name = ?, occupation = ?, education = ?, about = ?, photo = ? WHERE id = (?)""", (name, occupation, education, about, photo, user_id))
    db.commit()