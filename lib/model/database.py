import sqlite3

class Database:
    def __init__(self, db_path):
        self.path = db_path


    def connect_db(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        return conn, cursor