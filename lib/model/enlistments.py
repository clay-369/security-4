from lib.model.database import Database

class Enlistment:
    def __init__(self):
        database = Database("./databases/database.db")
        self.conn, self.cursor = database.connect_db()

    def create_enlistment(self, research_id:int, expert_id:int) -> int:
        # Create new enlistment
        result = self.cursor.execute(
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
        self.cursor.execute("SELECT * FROM inschrijvingen WHERE inschrijving_id = ?", (enlistment_id,))
        return dict(self.cursor.fetchone())

    def get_formatted_enlistments_by_expert(self, expert_id, search_words):
        """ Gets enlistments with corresponding research title, then converts Rows to dict """
        result = self.cursor.execute(
            """
            SELECT 
            inschrijvingen.*, onderzoeken.titel
            FROM inschrijvingen
            JOIN onderzoeken USING(onderzoek_id)
            WHERE deskundige_id = ?
            AND (onderzoeken.titel LIKE ? OR onderzoeken.beschrijving LIKE ?)
            """,
            (expert_id, f"%{search_words}%", f"%{search_words}%")
        ).fetchall()

        all_enlistments = [dict(row) for row in result]

        return all_enlistments

    def delete_enlistment(self, expert_id:int, research_id:int):
        deleted_item = self.cursor.execute(
            """
            DELETE FROM inschrijvingen
            WHERE deskundige_id = ? AND onderzoek_id = ?
            """,
            (expert_id, research_id)
        )
        self.conn.commit()
        return dict(deleted_item)

    def get_enlistments_by_expert(self, expert_id:int):
        self.cursor.execute("SELECT * FROM inschrijvingen WHERE deskundige_id = ?", (expert_id,))
        return self.cursor.fetchall()

    def get_enlistments_details(self):
        self.cursor.execute("SELECT * FROM ((inschrijvingen "
                            "INNER JOIN onderzoeken ON onderzoeken.onderzoek_id = inschrijvingen.onderzoek_id)"
                            "INNER JOIN deskundigen ON deskundigen.deskundige_id = inschrijvingen.deskundige_id);")
        return self.cursor.fetchall()

    def status_update(self, status, enlistment_id, admin_id):
        self.cursor.execute("UPDATE inschrijvingen SET status = ?, beheerder_id = ? WHERE inschrijving_id = ?", (status, admin_id, enlistment_id))
        self.conn.commit()
        return True, "Status gewijzigd!"
