from lib.model.database import Database
from lib.model.users import hash_password


class Deskundige:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def create_deskundige(self, deskundige):
        # if "email" not in deskundige:
        #     deskundige["email"] = ""
        # if "wachtwoord" not in deskundige:
        #     deskundige["wachtwoord"] = ""
        # if "voornaam" not in deskundige:
        #     deskundige["voornaam"] = ""
        # if "achternaam" not in deskundige:
        #     deskundige["achternaam"] = ""
        # if "postcode" not in deskundige:
        #     deskundige["postcode"] = ""
        # if "telefoonnummer" not in deskundige:
        #     deskundige["telefoonnummer"] = ""
        # if "geboortedatum" not in deskundige:
        #     deskundige["geboortedatum"] = ""
        # if "hulpmiddelen" not in deskundige:
        #     deskundige["hulpmiddelen"] = ""
        # if "bijzonderheden" not in deskundige:
        #     deskundige["bijzonderheden"] = ""
        print(f'deskundige: {deskundige}')

        self.cursor.execute("INSERT into deskundigen (email,wachtwoord,voornaam,achternaam,postcode,telefoonnummer,geboortedatum,hulpmiddelen,bijzonderheden, bijzonderheden_beschikbaarheid, introductie, voorkeur_benadering, type_beperking, type_onderzoeken, toezichthouder, toezichthouder_naam, toezichthouder_email, toezichthouder_telefoonnummer, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (deskundige["email"], hash_password(deskundige["wachtwoord"]), deskundige["voornaam"], deskundige["achternaam"], deskundige["postcode"], deskundige["telefoonnummer"], deskundige["geboortedatum"], deskundige["hulpmiddelen"], deskundige["bijzonderheden"], deskundige["bijzonderheden_beschikbaarheid"], deskundige["introductie"], deskundige["voorkeur_benadering"], deskundige["type_beperking"], deskundige["type_onderzoek"], deskundige["toezichthouder"], deskundige["toezichthouder_naam"], deskundige["toezichthouder_email"], deskundige["toezichthouder_telefoonnummer"], "Nieuw"))
        # Wijzigingen opslaan
        self.conn.commit()
        self.conn.close()
        return True

    def get_deskundigen(self):
        self.cursor.execute("SELECT * FROM deskundigen")
        return self.cursor.fetchall()
    
    def get_single_deskundige(self, deskundige_id):
        print(deskundige_id)
        self.cursor.execute("SELECT * FROM deskundigen WHERE deskundige_id = ?", (deskundige_id,))
        return self.cursor.fetchone()
    
    def update_deskundige(self, deskundige):
        self.cursor.execute("UPDATE deskundigen SET email = ?, wachtwoord = ?, voornaam = ?, achternaam = ?, postcode = ?, telefoonnummer = ?, geboortedatum = ?, hulpmiddelen = ?, bijzonderheden = ?, bijzonderheden_beschikbaarheid = ?, introductie = ?, voorkeur_benadering = ?, type_beperking = ?, type_onderzoeken = ?, toezichthouder = ?, toezichthouder_naam = ?, toezichthouder_email = ?, toezichthouder_telefoonnummer = ? WHERE deskundige_id = ?", (deskundige["email"], hash_password(deskundige["wachtwoord"]), deskundige["voornaam"], deskundige["achternaam"], deskundige["postcode"], deskundige["telefoonnummer"], deskundige["geboortedatum"], deskundige["hulpmiddelen"], deskundige["bijzonderheden"], deskundige["bijzonderheden_beschikbaarheid"], deskundige["introductie"], deskundige["voorkeur_benadering"], deskundige["type_beperking"], deskundige["type_onderzoek"], deskundige["toezichthouder"], deskundige["toezichthouder_naam"], deskundige["toezichthouder_email"], deskundige["toezichthouder_telefoonnummer"], deskundige["deskundige_id"]))
        self.conn.commit()
        self.conn.close()
        return True
