from lib.model.database import Database

class Organisation:
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

    def validate_credentials(self, email, password):
        result = self.cursor.execute("SELECT email FROM organisaties WHERE wachtwoord = ? AND email = ?", (password, email)).fetchone()
        return bool(result)

    def get_organisation_by_email(self, email):
        result = self.cursor.execute("SELECT * FROM organisaties WHERE email = ?", (email,)).fetchone()
        return dict(result)
