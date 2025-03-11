import sqlite3

from lib.model.database import Database

class Organisation:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def create_organisation(self, data):

        try:
            data['description']
        except KeyError:
            data['description'] = None

        try:
            data['details']
        except KeyError:
            data['details'] = None

        # Check if the email is already in use
        existing_email = self.cursor.execute("SELECT email FROM deskundigen WHERE email = ?",
                                             (data["email"],)).fetchone()
        if existing_email:
            return False

        self.cursor.execute(
            """
            INSERT INTO organisaties (naam, organisatie_type, website, beschrijving, contactpersoon, email, 
                telefoonnummer, overige_details, wachtwoord)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (data['name'], data['organisation_type'], data['website'], data['description'], data['contact_person'],
            data['email'], data['phone_number'], data['details'], data['password']))

        self.conn.commit()
        return self.cursor.lastrowid

    def validate_credentials(self, email, password):
        result = self.cursor.execute("SELECT email FROM organisaties WHERE wachtwoord = ? AND email = ?", (password, email)).fetchone()
        return bool(result)

    def get_organisation_by_email(self, email):
        result = self.cursor.execute("SELECT * FROM organisaties WHERE email = ?", (email,)).fetchone()
        return dict(result)

    def get_all_organisations(self):
        result = self.cursor.execute("SELECT * FROM organisaties").fetchall()
        return result
