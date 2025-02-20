from lib.model.database import Database

class Organisatie:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def create_organisatie(self, naam, organisatie_type, website, beschrijving, contactpersoon, email, telefoonnummer, overige_details):
        self.cursor.execute("""
            INSERT INTO organisaties (naam, organisatie_type, website, beschrijving, contactpersoon, email, telefoonnummer, overige_details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (naam, organisatie_type, website, beschrijving, contactpersoon, email, telefoonnummer, overige_details))
        self.conn.commit()
        return True
