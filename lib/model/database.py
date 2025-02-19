import sqlite3

# L.C. (2023, 31 December). Build a To-Do List App Using Python Flask, Jinja2, and SQL. hashnode. Geraadpleegd op 5 Februari 2025 van https://lovelacecoding.hashnode.dev/build-a-to-do-list-app-using-python-flask-jinja2-and-sql
class Database:
    def __init__(self, db_path):
        # Locatie van het database bestand
        self.path = db_path


    def connect_db(self):
        # Maak verbinding met het database bestand
        conn = sqlite3.connect(self.path)
        # Geef het resultaat in een dictionary in plaats van een lijst
        conn.row_factory = sqlite3.Row
        # Maak een cursor object waarmee je SQL statements kan uitvoeren
        cursor = conn.cursor()
        return conn, cursor