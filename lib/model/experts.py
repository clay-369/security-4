from lib.model.database import Database
from lib.model.users import hash_password


class Experts:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def create_deskundige(self, expert):
        neccesary_fields = ["email", "wachtwoord", "voornaam", "achternaam", "postcode", "telefoonnummer", "geboortedatum"]
        
        # Check if the user has agreed to the terms and conditions
        if expert["akkoord"] == False:
            return False, "U moet akkoord gaan met de voorwaarden en privacy."
        
        if expert["toezichthouder"] == True:
            neccesary_fields.append("toezichthouder_naam")
            neccesary_fields.append("toezichthouder_email")
            neccesary_fields.append("toezichthouder_telefoonnummer")
        
        # Check if all neccesary fields are filled
        for field in expert:
            if field in neccesary_fields and expert[field] == "":
                return False, f"Het veld {field} is verplicht.\n"

        try:
            self.cursor.execute("""
                INSERT into deskundigen (email,wachtwoord,voornaam,achternaam,postcode,telefoonnummer,geboortedatum,
                hulpmiddelen,bijzonderheden, bijzonderheden_beschikbaarheid, introductie, voorkeur_benadering, 
                type_beperking, type_onderzoeken, toezichthouder, toezichthouder_naam, toezichthouder_email, 
                toezichthouder_telefoonnummer, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (expert["email"], hash_password(expert["wachtwoord"]), expert["voornaam"], expert["achternaam"],
                 expert["postcode"], expert["telefoonnummer"], expert["geboortedatum"], expert["hulpmiddelen"],
                 expert["bijzonderheden"], expert["bijzonderheden_beschikbaarheid"], expert["introductie"],
                 expert["voorkeur_benadering"], expert["type_beperking"], expert["type_onderzoek"],
                 expert["toezichthouder"], expert["toezichthouder_naam"], expert["toezichthouder_email"],
                 expert["toezichthouder_telefoonnummer"], "NIEUW"))
        except:
            return False, "Er is iets mis gegaan."
        finally:
            # Wijzigingen opslaan
            self.conn.commit()

        return True, "Deskundige gemaakt!"

    def get_deskundigen(self):
        self.cursor.execute("SELECT * FROM deskundigen")
        return self.cursor.fetchall()
    
    def get_single_deskundige(self, expert_id):
        print(expert_id)
        self.cursor.execute("SELECT * FROM deskundigen WHERE deskundige_id = ?", (expert_id,))
        return self.cursor.fetchone()
    
    def update_deskundige(self, expert):
        neccesary_fields = ["email", "wachtwoord", "voornaam", "achternaam", "postcode", "telefoonnummer", "geboortedatum"]
        
        if expert["toezichthouder"] == True:
            neccesary_fields.append("toezichthouder_naam")
            neccesary_fields.append("toezichthouder_email")
            neccesary_fields.append("toezichthouder_telefoonnummer")
        
        # Check if all neccesary fields are filled
        for field in expert:
            if field in neccesary_fields and expert[field] == "":
                return False, f"Het veld {field} is verplicht.\n"

        try:
            self.cursor.execute("""
                UPDATE deskundigen SET email = ?, wachtwoord = ?, voornaam = ?, achternaam = ?, postcode = ?, 
                telefoonnummer = ?, geboortedatum = ?, hulpmiddelen = ?, bijzonderheden = ?, 
                bijzonderheden_beschikbaarheid = ?, introductie = ?, voorkeur_benadering = ?, type_beperking = ?, 
                type_onderzoeken = ?, toezichthouder = ?, toezichthouder_naam = ?, toezichthouder_email = ?, 
                toezichthouder_telefoonnummer = ? WHERE deskundige_id = ?""",
                (expert["email"], expert["wachtwoord"], expert["voornaam"], expert["achternaam"],
                 expert["postcode"], expert["telefoonnummer"], expert["geboortedatum"], expert["hulpmiddelen"],
                 expert["bijzonderheden"], expert["bijzonderheden_beschikbaarheid"], expert["introductie"],
                 expert["voorkeur_benadering"], expert["type_beperking"], expert["type_onderzoek"],
                 expert["toezichthouder"], expert["toezichthouder_naam"], expert["toezichthouder_email"],
                 expert["toezichthouder_telefoonnummer"], expert["deskundige_id"]))
        except:
            return False, "Er is iets mis gegaan."
        finally:
            self.conn.commit()

        return True, "Deskundige gewijzigd!"
