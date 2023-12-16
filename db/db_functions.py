import sqlite3
import os

# Initialize the database
DATABASE = 'users.db'

# Specifying the path
DB_FOLDER = '/home/jason_tang/flask_e2e_project/db'
DATABASE = os.path.join(DB_FOLDER, 'users.db')

def get_db():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            profile TEXT
            permissions TEXT DEFAULT 'basic'
        )
    ''')
    db.commit()
    return db

def update_or_create_user(user_info):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (email, name, profile) VALUES (?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET name = excluded.name, profile = excluded.profile
        ''', (user_info['email'], user_info['name'], user_info['picture']))
        db.commit()
        print("User added to database: ", user_info['email'])
    except Exception as e:
        print(e)
        db.rollback()