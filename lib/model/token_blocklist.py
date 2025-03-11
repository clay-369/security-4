from lib.model.database import Database

class TokenBlocklist:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def check_jti_in_blocklist(self, jti):
        result = self.cursor.execute('SELECT * FROM token_blocklist WHERE jti = ?', (jti,)).fetchone()
        if result is not None:
            return True
        return False

    def add_token(self, jti):
        self.cursor.execute('INSERT INTO token_blocklist (jti) VALUES (?)', (jti,))
        self.conn.commit()
        return True