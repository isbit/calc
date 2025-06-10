'''
Funksjoner brukt i app.py
'''

from flask import g
from werkzeug.security import check_password_hash
import sqlite3

database = 'database.db'

def get_db():
    if not hasattr(g, "_database"):
        g._database = sqlite3.connect(database)
    return g._database

def valid_login(username, password):
    """Sjekker om brukernavn og passord er korrekt ved login"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT password FROM users WHERE name = ?", (username,))
    result = cursor.fetchone()
    if result:
        stored_password = result[0]
        return check_password_hash(stored_password, password)
    return False

def valid_user_password(password, password_retype):
    """Sjekker om passordet oppfyller krav"""
    if len(password) < 5 or password != password_retype:
        return False
    else:
        return True
    
def is_admin(username):
    """Sjekker om brukernavn er admin"""
    if username is not None:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT isadmin FROM users WHERE name = ?", (username,))
        result = cursor.fetchone()
        if result[0]:
            return True
    else:
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'} 
    # rsplit splitter fra høyre. [1] finner filtype

def calculate_percentage(answered, total):
    if total == 0:
        return 0
    return round((answered / total) * 100, 2)