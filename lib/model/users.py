from lib.model.database import Database
from hashlib import sha256

class Users:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def login(self, email, password):
        self.cursor.execute('SELECT * FROM deskundingen WHERE email = ?', (email,))
        user = self.cursor.fetchone()
        if user and password == user['password']:
                return 'user', True
        else:
            self.cursor.execute('SELECT * FROM beheerders WHERE email = ?', (email,))
            admin = self.cursor.fetchone()
            if admin and password == user['password']:
                    return 'admin', True