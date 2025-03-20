import sqlite3
from hashlib import sha256
from pathlib import Path

def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()


class WP3DatabaseGenerator:
    def __init__(self, database_file, overwrite=False, initial_data=False):
        self.database_file = Path(database_file)
        self.create_initial_data = initial_data
        self.database_overwrite = overwrite
        self.test_file_location()
        self.conn = sqlite3.connect(self.database_file)

    def generate_database(self):
        self.create_table_deskundigen()
        self.create_table_beheerders()
        self.create_table_organisaties()
        self.create_table_beperkingen()
        self.create_table_onderzoeken()
        self.create_table_beperking_deskundige()
        self.create_table_beperking_onderzoek()
        self.create_table_inschrijvingen()
        self.create_table_token_blocklist()
        if self.create_initial_data:
            self.fill_database()


    def fill_database(self):
        self.insert_beperkingen()
        self.insert_beheerders()
        self.insert_defaults_into_tables()
        self.insert_research()

    def create_table_deskundigen(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS deskundigen (
            deskundige_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            wachtwoord TEXT NOT NULL,
            voornaam TEXT NOT NULL,
            achternaam TEXT NOT NULL,
            geslacht TEXT NOT NULL,
            postcode TEXT,
            telefoonnummer TEXT,
            geboortedatum TEXT,
            hulpmiddelen TEXT,
            bijzonderheden TEXT,
            bijzonderheden_beschikbaarheid TEXT,
            introductie TEXT,
            type_onderzoeken TEXT,
            voorkeur_benadering TEXT,
            toezichthouder INTEGER NOT NULL,
            toezichthouder_naam TEXT,
            toezichthouder_email TEXT,
            toezichthouder_telefoonnummer TEXT,
            status TEXT NOT NULL,
            beheerder_id INTEGER,
            FOREIGN KEY (beheerder_id) REFERENCES beheerders(beheerder_id)
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Deskundigen table created")

    def create_table_beheerders(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS beheerders (
            beheerder_id INTEGER PRIMARY KEY AUTOINCREMENT,
            voornaam TEXT NOT NULL,
            achternaam TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            wachtwoord TEXT NOT NULL
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Beheerders table created")

    def create_table_organisaties(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS organisaties (
            organisatie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            naam TEXT NOT NULL,
            organisatie_type TEXT NOT NULL,
            website TEXT NOT NULL,
            beschrijving TEXT,
            contactpersoon TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL ,
            telefoonnummer TEXT NOT NULL,
            overige_details TEXT,
            wachtwoord TEXT NOT NULL
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Organisaties table created")

    def create_table_beperkingen(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS beperkingen (
            beperking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_beperking TEXT NOT NULL,
            beperking TEXT NOT NULL
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Beperkingen table created")

    def create_table_beperking_deskundige(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS beperking_deskundige (
            beperking_deskundige_id INTEGER PRIMARY KEY AUTOINCREMENT,
            beperking_id INTEGER NOT NULL,
            deskundige_id INTEGER NOT NULL,
            FOREIGN KEY (beperking_id) REFERENCES beperkingen(beperking_id),
            FOREIGN KEY (deskundige_id) REFERENCES deskundigen(deskundige_id)
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Beperking-deskundige table created")

    def create_table_beperking_onderzoek(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS beperking_onderzoek (
            beperking_onderzoek_id INTEGER PRIMARY KEY AUTOINCREMENT,
            beperking_id INTEGER NOT NULL,
            onderzoek_id INTEGER NOT NULL,
            FOREIGN KEY (beperking_id) REFERENCES beperkingen(beperking_id),
            FOREIGN KEY (onderzoek_id) REFERENCES onderzoeken(onderzoek_id)
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Beperking-onderzoek table created")

    def create_table_onderzoeken(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS onderzoeken (
            onderzoek_id INTEGER PRIMARY KEY AUTOINCREMENT,
            organisatie_id INTEGER NOT NULL,
            beschrijving TEXT NOT NULL,
            titel TEXT NOT NULL,
            aanmaak_datum TEXT DEFAULT CURRENT_TIMESTAMP,
            beschikbaar INTEGER NOT NULL,
            datum_vanaf TEXT NOT NULL,
            datum_tot TEXT NOT NULL,
            onderzoek_type TEXT NOT NULL,
            locatie TEXT,
            met_beloning INTEGER NOT NULL,
            beloning TEXT,
            leeftijd_vanaf INTEGER,
            leeftijd_tot INTEGER,
            status TEXT NOT NULL,
            beheerder_id INTEGER,
            FOREIGN KEY (beheerder_id) REFERENCES beheerders(beheerder_id),
            FOREIGN KEY (organisatie_id) REFERENCES organisaties(organisatie_id)
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Onderzoeken table created")

    def create_table_inschrijvingen(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS inschrijvingen (
            inschrijving_id INTEGER PRIMARY KEY AUTOINCREMENT,
            deskundige_id INTEGER NOT NULL,
            onderzoek_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            beheerder_id INTEGER,
            FOREIGN KEY (deskundige_id) REFERENCES deskundigen(deskundige_id),
            FOREIGN KEY (onderzoek_id) REFERENCES onderzoeken(onderzoek_id),
            FOREIGN KEY (beheerder_id) REFERENCES beheerders(beheerder_id)
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Beperkingen table created")

    def create_table_token_blocklist(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS token_blocklist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jti TEXT NOT NULL,
            created_date TEXT DEFAULT current_timestamp
            );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Token Blocklist table created")


    def insert_beperkingen(self):
        beperkingen = [
            # Auditieve beperkingen
            ("auditief", "doof"),
            ("auditief", "slechthorend"),
            ("auditief en visueel", "doofblind"),
            # Visuele beperkingen
            ("visueel", "blind"),
            ("visueel", "slechtziend"),
            ("visueel", "kleurenblind"),
            # Motorische / lichamelijke beperkingen
            ("motorisch of lichamelijk", "amputatie of mismaaktheid"),
            ("motorisch of lichamelijk", "artritus"),
            ("motorisch of lichamelijk", "fibromyalgie"),
            ("motorisch of lichamelijk", "reuma"),
            ("motorisch of lichamelijk", "verminderde handvaardigheid"),
            ("motorisch of lichamelijk", "spierdystrofie"),
            ("motorisch of lichamelijk", "rsi"),
            ("motorisch of lichamelijk", "tremor of spasmen"),
            ("motorisch of lichamelijk", "quadriplegie of tetraplegie"),
            # Cognitieve / neurologische beperkingen
            ("cognitief of neurologisch", "adhd"),
            ("cognitief of neurologisch", "autisme"),
            ("cognitief of neurologisch", "dyslexie"),
            ("cognitief of neurologisch", "dyscalculie"),
            ("cognitief of neurologisch", "leerstoornis"),
            ("cognitief of neurologisch", "geheugen beperking"),
            ("cognitief of neurologisch", "mulltiple sclerose"),
            ("cognitief of neurologisch", "epilepsie"),
            ("cognitief of neurologisch", "migraine")
        ]
        insert_statement = "INSERT INTO beperkingen (type_beperking, beperking) VALUES (?, ?)"
        self.__execute_many_transaction_statement(insert_statement, beperkingen)
        print("✅ Filled beperkingen table")

    def insert_beheerders(self):
        beheerders = [
            ("Gerry", "van Kruiningen", "krugw@hr.nl", hash_password("geheim"))
        ]
        insert_statement = "INSERT INTO beheerders (voornaam, achternaam, email, wachtwoord) VALUES (?, ?, ?, ?)"
        self.__execute_many_transaction_statement(insert_statement, beheerders)
        print("✅ Filled default admin account")


    def insert_defaults_into_tables(self):
        insert_statement_organisation = ("""INSERT INTO organisaties
            (naam, organisatie_type, website, beschrijving, contactpersoon, email, telefoonnummer, overige_details, wachtwoord)
            VALUES (?,?, ?, ?, ?, ?, ?, ?, ?)""")
        values_organisation = ('Stichting accessibility', 'non-profit', 'www.google.com', 'Mijn beschrijving', 'peter', 'peter@email.com', '06', 'Details', hash_password('ABC'))
        self.__execute_transaction_statement(insert_statement_organisation, values_organisation)
        print("✅ Filled default organisation account")

    def insert_research(self):
        # Create default research item:
        research_item = {
            'titel': 'Onderzoek naar doofheid van mensen',
            'beschikbaar': True,
            'beschrijving': 'Wij zoeken 20 mensen die doof zijn voor een onderzoek naar het gehoor.',
            'datum_vanaf': '01-01-2025',
            'datum_tot': '01-08-2025',
            'onderzoek_type': 'OP LOCATIE',
            'locatie': 'Rotterdam',
            'met_beloning': True,
            'beloning': 'Bol.com cadeaukaart van 20 euro.',
            'leeftijd_vanaf': 18,
            'leeftijd_tot': 80,
            'status': 'NIEUW'
        }
        organisation_id = 1

        # Create new research
        insert_statement = """
            INSERT INTO onderzoeken 
            (
                organisatie_id, titel, beschrijving, beschikbaar, datum_vanaf, datum_tot, onderzoek_type, locatie, 
                met_beloning, beloning, leeftijd_vanaf, leeftijd_tot, status
            ) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """

        values = (
                organisation_id, research_item['titel'], research_item['beschrijving'], research_item['beschikbaar'],
                research_item['datum_vanaf'], research_item['datum_tot'], research_item['onderzoek_type'],
                research_item['locatie'], research_item['met_beloning'], research_item['beloning'],
                research_item['leeftijd_vanaf'], research_item['leeftijd_tot'], research_item['status']
            )

        self.__execute_transaction_statement(insert_statement, values)
        print("✅ Filled research")

        disability_research_couple = [
            (1, 1), # Doof
            (2, 1), # Slechthorend
            (3, 1)  # Doofblind
        ]
        insert_statement_dis = "INSERT INTO beperking_onderzoek (beperking_id, onderzoek_id) VALUES (?,?)"
        self.__execute_many_transaction_statement(insert_statement_dis, disability_research_couple)
        print("✅ Filled disability with research")




    # Transacties zijn duur, dat wil zeggen, ze kosten veel tijd en CPU kracht. Als je veel insert doet
    # bundel je ze in één transactie, of je gebruikt de SQLite executemany methode.
    def __execute_many_transaction_statement(
        self, create_statement, list_of_parameters=()
    ):
        c = self.conn.cursor()
        c.executemany(create_statement, list_of_parameters)
        self.conn.commit()

    def __execute_transaction_statement(self, create_statement, parameters=()):
        c = self.conn.cursor()
        c.execute(create_statement, parameters)
        self.conn.commit()

    def test_file_location(self):
        if not self.database_file.parent.exists():
            raise ValueError(
                f"Database file location {self.database_file.parent} does not exist"
            )
        if self.database_file.exists():
            if not self.database_overwrite:
                raise ValueError(
                    f"Database file {self.database_file} already exists, set overwrite=True to overwrite"
                )
            else:
                # Unlink verwijdert een bestand
                self.database_file.unlink()
                print("✅ Database already exists, deleted")
        if not self.database_file.exists():
            try:
                self.database_file.touch()
                print("✅ New database setup")
            except Exception as e:
                raise ValueError(
                    f"Could not create database file {self.database_file} due to error {e}"
                )





if __name__ == "__main__":
    my_path = Path(__file__).parent.resolve()
    project_root = my_path.parent.parent
    # Deze slashes komen uit de "Path" module. Dit is een module die je kan gebruiken
    # om paden te maken. Dit is handig omdat je dan niet zelf hoeft te kijken of je
    # een / (mac) of een \ (windows) moet gebruiken.
    database_path = project_root / "databases" / "database.db"
    database_generator = WP3DatabaseGenerator(
        database_path, overwrite=True, initial_data=True
    )
    database_generator.generate_database()
