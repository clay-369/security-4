from lib.model.database import Database

class Disabilities:
    def __init__(self):
        database = Database("./databases/database.db")
        self.conn, self.cursor = database.connect_db()

    def get_disability_id(self, disability_name):
        disability_id = self.cursor.execute(
            """
            SELECT beperking_id
            FROM beperkingen
            WHERE beperking = ?
            """,
            (disability_name,)
        ).fetchone()['beperking_id']

        return disability_id
