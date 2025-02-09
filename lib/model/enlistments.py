from lib.model.database import Database

class Enlistment:
    def __init__(self):
        database = Database("./databases/database.db")
        self.conn, self.cursor = database.connect_db()

    def create_enlistment(self, research_id:int, expert_id:int) -> int:
        # Create new enlistment
        self.cursor.execute(
            """
            INSERT INTO inschrijvingen 
            (deskundige_id, onderzoek_id, status) 
            VALUES (?,?,?)
            """,
            (expert_id, research_id, "NIEUW")
        )
        new_enlistment_id = self.cursor.lastrowid

        self.conn.commit()

        return new_enlistment_id

    def get_enlistment_by_id(self, enlistment_id:int):
        enlistment = self.cursor.execute("SELECT * FROM inschrijvingen WHERE inschrijving_id = ?", (enlistment_id,)).fetchone()
        return enlistment
