from lib.model.database import Database


class Deskundige:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def create_deskundige(self, deskundige):
        neccesary_fields = ["email", "wachtwoord", "voornaam", "achternaam", "postcode", "telefoonnummer", "geboortedatum"]
        
        # Check if the user has agreed to the terms and conditions
        if deskundige["akkoord"] == False:
            return False, "U moet akkoord gaan met de voorwaarden en privacy."
        
        if deskundige["toezichthouder"] == True:
            neccesary_fields.append("toezichthouder_naam")
            neccesary_fields.append("toezichthouder_email")
            neccesary_fields.append("toezichthouder_telefoonnummer")
        
        # Check if all neccesary fields are filled
        for field in deskundige:
            if field in neccesary_fields and deskundige[field] == "":
                return False, f"Het veld {field} is verplicht.\n"
        self.cursor.execute("INSERT into deskundigen (email,wachtwoord,voornaam,achternaam,postcode,telefoonnummer,geboortedatum,hulpmiddelen,bijzonderheden, bijzonderheden_beschikbaarheid, introductie, voorkeur_benadering, type_beperking, type_onderzoeken, toezichthouder, toezichthouder_naam, toezichthouder_email, toezichthouder_telefoonnummer, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (deskundige["email"], deskundige["wachtwoord"], deskundige["voornaam"], deskundige["achternaam"], deskundige["postcode"], deskundige["telefoonnummer"], deskundige["geboortedatum"], deskundige["hulpmiddelen"], deskundige["bijzonderheden"], deskundige["bijzonderheden_beschikbaarheid"], deskundige["introductie"], deskundige["voorkeur_benadering"], deskundige["type_beperking"], deskundige["type_onderzoek"], deskundige["toezichthouder"], deskundige["toezichthouder_naam"], deskundige["toezichthouder_email"], deskundige["toezichthouder_telefoonnummer"], "Nieuw"))
        
        # Wijzigingen opslaan
        self.conn.commit()
        self.conn.close()
        return True, "Deskundige gemaakt!"

    def get_deskundigen(self):
        self.cursor.execute("SELECT * FROM deskundigen")
        return self.cursor.fetchall()
    
    def get_single_deskundige(self, deskundige_id):
        print(deskundige_id)
        self.cursor.execute("SELECT * FROM deskundigen WHERE deskundige_id = ?", (deskundige_id,))
        return self.cursor.fetchone()
    
    def update_deskundige(self, deskundige):
        neccesary_fields = ["email", "wachtwoord", "voornaam", "achternaam", "postcode", "telefoonnummer", "geboortedatum"]
        
        if deskundige["toezichthouder"] == True:
            neccesary_fields.append("toezichthouder_naam")
            neccesary_fields.append("toezichthouder_email")
            neccesary_fields.append("toezichthouder_telefoonnummer")
        
        # Check if all neccesary fields are filled
        for field in deskundige:
            if field in neccesary_fields and deskundige[field] == "":
                return False, f"Het veld {field} is verplicht.\n"
        self.cursor.execute("UPDATE deskundigen SET email = ?, wachtwoord = ?, voornaam = ?, achternaam = ?, postcode = ?, telefoonnummer = ?, geboortedatum = ?, hulpmiddelen = ?, bijzonderheden = ?, bijzonderheden_beschikbaarheid = ?, introductie = ?, voorkeur_benadering = ?, type_beperking = ?, type_onderzoeken = ?, toezichthouder = ?, toezichthouder_naam = ?, toezichthouder_email = ?, toezichthouder_telefoonnummer = ? WHERE deskundige_id = ?", (deskundige["email"], deskundige["wachtwoord"], deskundige["voornaam"], deskundige["achternaam"], deskundige["postcode"], deskundige["telefoonnummer"], deskundige["geboortedatum"], deskundige["hulpmiddelen"], deskundige["bijzonderheden"], deskundige["bijzonderheden_beschikbaarheid"], deskundige["introductie"], deskundige["voorkeur_benadering"], deskundige["type_beperking"], deskundige["type_onderzoek"], deskundige["toezichthouder"], deskundige["toezichthouder_naam"], deskundige["toezichthouder_email"], deskundige["toezichthouder_telefoonnummer"], deskundige["deskundige_id"]))
        self.conn.commit()
        self.conn.close()
        return True, "Deskundige gewijzigd!"
