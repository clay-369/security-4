from lib.model.database import Database
from lib.model.disabilities import Disabilities
from lib.model.users import hash_password
import re
from datetime import datetime, date

class Experts:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()


    def create_deskundige(self, deskundige):
        neccesary_fields = ["email", "wachtwoord", "voornaam", "achternaam", "postcode", "telefoonnummer", "geboortedatum", "introductie", "voorkeur_benadering", "type_beperking"]

        if deskundige["voorkeur_benadering"] == "":
            return False, "U moet een voorkeur benadering selecteren."

        if len(deskundige["introductie"]) < 10:
            return False, "Vertel wat meer in je introductie."
        
        # Check if the user has agreed to the terms and conditions
        if deskundige["akkoord"] == False:
            return False, "U moet akkoord gaan met de voorwaarden en privacy."
        
        if deskundige["toezichthouder"] == True:
            neccesary_fields.append("toezichthouder_naam")
            neccesary_fields.append("toezichthouder_email")
            neccesary_fields.append("toezichthouder_telefoonnummer")

            if deskundige["toezichthouder_naam"] == "":
                return False, "U moet een naam invullen voor de toezichthouder omdat u toezichthouder heeft geselecteerd."

            if deskundige["toezichthouder_email"] == "":
                return False, "U moet een e-mailadres invullen voor de toezichthouder omdat u toezichthouder heeft geselecteerd."

            if deskundige["toezichthouder_telefoonnummer"] == "":
                return False, "U moet een telefoonnummer invullen voor de toezichthouder omdat u toezichthouder heeft geselecteerd."


        # Check if the email is valid
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', deskundige["email"])
        if not valid:
            return False, "U moet een geldig e-mailadres invullen."

        # Check if the phone number is valid
        valid = re.match(r'^[0-9]{10}$', deskundige["telefoonnummer"])
        if not valid:
            return False, "U moet een geldig telefoonnummer invullen."

        # Check if the postcode is valid
        valid = re.match(r'^[1-9][0-9]{3} ?[A-Z]{2}$', deskundige["postcode"])
        if not valid:
            return False, "U moet een geldige postcode invullen."

          # Temporary solution to check if there are "onderzoeken"
        if deskundige["type_onderzoek"] == "":
            return False, "U moet een type onderzoek selecteren."

        # Check if all neccesary fields are filled
        for field in deskundige:
            if field in neccesary_fields and deskundige[field] == "":
                return False, f"Het veld {field} is verplicht.\n"


        # Check if the email is already in use
        existing_email = self.cursor.execute("SELECT email FROM deskundigen WHERE email = ?", (deskundige["email"],)).fetchone()
        if existing_email:
            return False, "Dit emailadres is al geregistreerd."

        # Create expert
        self.cursor.execute("INSERT into deskundigen (email,wachtwoord,voornaam,achternaam,postcode,geslacht,telefoonnummer,geboortedatum,hulpmiddelen,bijzonderheden, bijzonderheden_beschikbaarheid, introductie, voorkeur_benadering, type_onderzoeken, toezichthouder, toezichthouder_naam, toezichthouder_email, toezichthouder_telefoonnummer, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (deskundige["email"], hash_password(deskundige["wachtwoord"]), deskundige["voornaam"], deskundige["achternaam"], deskundige["postcode"], deskundige["geslacht"], deskundige["telefoonnummer"], deskundige["geboortedatum"], deskundige["hulpmiddelen"], deskundige["bijzonderheden"], deskundige["bijzonderheden_beschikbaarheid"], deskundige["introductie"], deskundige["voorkeur_benadering"], deskundige["type_onderzoek"], deskundige["toezichthouder"], deskundige["toezichthouder_naam"], deskundige["toezichthouder_email"], deskundige["toezichthouder_telefoonnummer"], "NIEUW"))

        new_expert_id = self.cursor.lastrowid

        # Create link with disabilities
        for disability_id in deskundige['beperkingen']:
            self.cursor.execute(
                """
                INSERT INTO beperking_deskundige 
                (beperking_id, deskundige_id)
                VALUES (?,?)
                """,
                (disability_id, new_expert_id)
            )

        # Wijzigingen opslaan
        self.conn.commit()
        return True, "Deskundige gemaakt!"

    def get_experts(self):
        self.cursor.execute("SELECT * FROM deskundigen")
        return self.cursor.fetchall()
    
    def get_single_expert(self, expert_id):
        self.cursor.execute("SELECT * FROM deskundigen WHERE deskundige_id = ?", (expert_id,))
        return dict(self.cursor.fetchone())
    
    def update_expert(self, expert, expert_id):
        neccesary_fields = ["email", "voornaam", "achternaam", "postcode", "telefoonnummer", "geboortedatum", "introductie", "voorkeur_benadering", "type_beperking"]

        if expert["voorkeur_benadering"] == "":
            return False, "U moet een voorkeur benadering selecteren."

        if len(expert["introductie"]) < 10:
            return False, "Vertel wat meer in je introductie."
        
        if expert["toezichthouder"] == True:
            neccesary_fields.append("toezichthouder_naam")
            neccesary_fields.append("toezichthouder_email")
            neccesary_fields.append("toezichthouder_telefoonnummer")

            if expert["toezichthouder_naam"] == "":
                return False, "U moet een naam invullen voor de toezichthouder omdat u toezichthouder heeft geselecteerd."

            if expert["toezichthouder_email"] == "":
                return False, "U moet een e-mailadres invullen voor de toezichthouder omdat u toezichthouder heeft geselecteerd."

            if expert["toezichthouder_telefoonnummer"] == "":
                return False, "U moet een telefoonnummer invullen voor de toezichthouder omdat u toezichthouder heeft geselecteerd."

        else:
            expert["toezichthouder_naam"] = ""
            expert["toezichthouder_email"] = ""
            expert["toezichthouder_telefoonnummer"] = ""


        # Check if the email is valid
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', expert["email"])
        if not valid:
            return False, "U moet een geldig e-mailadres invullen."

        # Check if the phone number is valid
        valid = re.match(r'^[0-9]{10}$', expert["telefoonnummer"])
        if not valid:
            return False, "U moet een geldig telefoonnummer invullen."

        # Check if the postcode is valid
        valid = re.match(r'^[1-9][0-9]{3} ?[A-Z]{2}$', expert["postcode"])
        if not valid:
            return False, "U moet een geldige postcode invullen."

        # Temporary solution to check if there are "onderzoeken"
        if expert["type_onderzoek"] == "":
            return False, "U moet een type onderzoek selecteren."

        # Check if all neccesary fields are filled
        for field in expert:
            if field in neccesary_fields and expert[field] == "":
                return False, f"Het veld {field} is verplicht.\n"

        # Delete current disabilities
        self.cursor.execute("DELETE FROM beperking_deskundige WHERE deskundige_id = ?", (expert_id,))

        # Create edited disabilities
        for disability_id in expert['beperkingen']:
            self.cursor.execute(
                """
                INSERT INTO beperking_deskundige 
                (beperking_id, deskundige_id)
                VALUES (?,?)
                """,
                (disability_id, expert_id)
            )

        self.cursor.execute("""
            UPDATE deskundigen SET email = ?, voornaam = ?, achternaam = ?, postcode = ?, 
            telefoonnummer = ?, geboortedatum = ?, hulpmiddelen = ?, bijzonderheden = ?, 
            bijzonderheden_beschikbaarheid = ?, introductie = ?, voorkeur_benadering = ?, 
            type_onderzoeken = ?, toezichthouder = ?, toezichthouder_naam = ?, toezichthouder_email = ?, 
            toezichthouder_telefoonnummer = ? WHERE deskundige_id = ?""",
            (expert["email"], expert["voornaam"], expert["achternaam"],
            expert["postcode"], expert["telefoonnummer"], expert["geboortedatum"], expert["hulpmiddelen"],
            expert["bijzonderheden"], expert["bijzonderheden_beschikbaarheid"], expert["introductie"],
            expert["voorkeur_benadering"], expert["type_onderzoek"],
            expert["toezichthouder"], expert["toezichthouder_naam"], expert["toezichthouder_email"],
            expert["toezichthouder_telefoonnummer"], expert_id))

        if expert['wachtwoord']:
            self.cursor.execute("""
                UPDATE deskundigen SET wachtwoord = ? WHERE deskundige_id = ?""",
                (hash_password(expert["wachtwoord"]), expert_id))

        self.conn.commit()
        return True, "Deskundige gewijzigd!"

    def status_update(self, status, expert_id, admin_id):
        self.cursor.execute("UPDATE deskundigen SET status = ?, beheerder_id = ?  WHERE deskundige_id = ?", (status, admin_id, expert_id))
        self.conn.commit()
        return True, "Status gewijzigd!"

    def get_expert_by_email(self, email):
        self.cursor.execute("SELECT * FROM deskundigen WHERE email = ?", (email,))
        return self.cursor.fetchone()


    def validate_credentials(self, email, password):
        password = hash_password(password)
        result = self.cursor.execute("SELECT email FROM deskundigen WHERE wachtwoord = ? AND email = ?", (password, email)).fetchone()
        return bool(result)

    def get_disabilities(self, expert_id):
        rows = self.cursor.execute("SELECT beperking_id FROM beperking_deskundige WHERE deskundige_id = ?", (expert_id,)).fetchall()
        return [dict(row)['beperking_id'] for row in rows]

    def calculate_age(self, date_of_birth:str) -> int:
        today = date.today()
        covert_date = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        difference = (today - covert_date).days
        age = int(difference / 365)
        return age
