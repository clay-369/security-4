from lib.model.database import Database

class Users:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def login(self, email, password):
        user = self.cursor.execute('SELECT * FROM deskundigen WHERE email = ?', (email,)).fetchone()
        if user is not None and password == user[2]:
            return 'user', True
        else:
            admin = self.cursor.execute('SELECT * FROM beheerders WHERE email = ?', (email,)).fetchone()
            if admin is not None and password == admin[4]:
                return 'admin', True