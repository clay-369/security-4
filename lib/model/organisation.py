from lib.model.database import Database
from lib.model.users import hash_password

class Organisation:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def create_organisation(self, data):

        try:
            if data['description'] == '':
                data['description'] = None
        except KeyError:
            data['description'] = None

        try:
            if data['details'] == '':
                data['details'] = None
        except KeyError:
            data['details'] = None

        # Check if the email is already in use
        existing_email = self.cursor.execute("SELECT email FROM organisaties WHERE email = ?",
                                             (data["email"],)).fetchone()
        if existing_email:
            return False

        try:
            self.cursor.execute(
                """
                INSERT INTO organisaties (naam, organisatie_type, website, beschrijving, contactpersoon, email, 
                    telefoonnummer, overige_details, wachtwoord)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (data['name'], data['organisation_type'], data['website'], data['description'], data['contact_person'],
                data['email'], data['phone_number'], data['details'], hash_password(data['password'])))
        finally:
            self.conn.commit()
        return self.cursor.lastrowid

    def validate_credentials(self, email, password):
        password = hash_password(password)
        result = self.cursor.execute("SELECT email FROM organisaties WHERE wachtwoord = ? AND email = ?", (password, email)).fetchone()
        return bool(result)

    def get_organisation_by_email(self, email):
        result = self.cursor.execute("SELECT * FROM organisaties WHERE email = ?", (email,)).fetchone()
        return result

    def get_all_organisations(self):
        result = self.cursor.execute("SELECT * FROM organisaties").fetchall()
        return result

    def edit_organisation(self, organisation_id, data):
        try:
            if not data['beschrijving']:
                data['beschrijving'] = None
        except KeyError:
            data['beschrijving'] = None

        try:
            if not data['overige_details']:
                data['overige_details'] = None
        except KeyError:
            data['overige_details'] = None

        is_edited = False

        try:
            self.cursor.execute("""
                UPDATE organisaties
                SET naam =?, organisatie_type =?, website =?, beschrijving =?, contactpersoon =?, email =?, 
                telefoonnummer =?, overige_details =?, wachtwoord =? WHERE organisatie_id =?
            """, (data['naam'], data['organisatie_type'], data['website'], data['beschrijving'], data['contact_persoon'],
                  data['email'], data['telefoonnummer'], data['overige_details'], hash_password(data['wachtwoord']),
                  organisation_id)
            )
            is_edited = True
        finally:
            self.conn.commit()

        return is_edited
