from lib.model.database import Database
from lib.model.disabilities import Disabilities


class Research:
    def __init__(self):
        database = Database("./databases/database.db")
        self.conn, self.cursor = database.connect_db()

    def get_research_by_id(self, research_id:int):
        result = self.cursor.execute(f"SELECT * FROM onderzoeken WHERE onderzoek_id=?", (research_id,)).fetchone()
        return dict(result)

    def create_research(self, research_item:dict, organisation_id:int):


        # Accept dictionary like
        # {
        #     'titel': str,
        #     'beschikbaar': bool,
        #     'beschrijving': str,
        #     'datum_vanaf': date,
        #     'datum_tot': date,
        #     'onderzoek_type': str,
        #     'locatie': str, (optional)
        #     'met_beloning': bool,
        #     'beloning': str, (optional)
        #     'leeftijd_vanaf': int,
        #     'leeftijd_tot': int,
        #     'beperkingen': list
        # }


        research_item['status'] = 'NIEUW'

        # Filter onderzoek_type
        if research_item['onderzoek_type'].upper() not in ['ONLINE', 'OP LOCATIE', 'TELEFONISCH']:
            return False

        # Filter optional fields
        try:
            research_item['locatie']
        except KeyError:
            if research_item['onderzoek_type'] == 'OP LOCATIE':
                return {"error": "Field <locatie> missing"}
            else:
                research_item['locatie'] = None

        try:
            research_item['beloning']
        except KeyError:
            if research_item['met_beloning'] == 1:
                return {"error": "Field <beloning> missing"}
            else:
                research_item['beloning'] = None



        # Check if disabilities exist in database
        disability_model = Disabilities()
        for disability_name in research_item['beperkingen']:
            disability_id = None
            try:
                disability_id = disability_model.get_disability_id(disability_name.lower())
            finally:
                if not disability_id:
                    return {"error": f"Disability <{disability_name}> does not exist in the database"}

        # Create new research
        self.cursor.execute(
            """
            INSERT INTO onderzoeken 
            (
                organisatie_id, titel, beschrijving, beschikbaar, datum_vanaf, datum_tot, onderzoek_type, locatie, 
                met_beloning, beloning, leeftijd_vanaf, leeftijd_tot, status
            ) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                organisation_id, research_item['titel'], research_item['beschrijving'], research_item['beschikbaar'],
                research_item['datum_vanaf'], research_item['datum_tot'], research_item['onderzoek_type'],
                research_item['locatie'], research_item['met_beloning'], research_item['beloning'],
                research_item['leeftijd_vanaf'], research_item['leeftijd_tot'], research_item['status']
            )
        )

        new_research_id = self.cursor.lastrowid

        # Create beperking_onderzoek instances
        for disability_name in research_item['beperkingen']:
            disability_id = disability_model.get_disability_id(disability_name)

            self.cursor.execute(
                """
                INSERT INTO beperking_onderzoek 
                (beperking_id, onderzoek_id)
                VALUES (?,?)
                """,
                (disability_id, new_research_id)
            )

        self.conn.commit()

        new_research_item = self.get_research_by_id(new_research_id)
        return new_research_item

    def get_all_research_items_by_organisation_id(self, organisation_id):
        self.cursor.execute("SELECT * FROM onderzoeken WHERE organisatie_id = ?", (organisation_id,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]


    def get_all_available_research_items(self):
        self.cursor.execute("SELECT * FROM onderzoeken WHERE status = ? AND beschikbaar = ?",
                            ('GOEDGEKEURD', True))
        return self.cursor.fetchall()


    def format_research_item(self, research_item) -> dict:
        """ Adds organisatie_naam to research_item and converts it to dict """
        research_item = dict(research_item)

        organisation_id = research_item['organisatie_id']
        organisation_name = self.cursor.execute("SELECT naam FROM organisaties WHERE organisatie_id = ?", (organisation_id,))
        organisation_name = organisation_name.fetchone()['naam']

        research_item['organisatie_naam'] = organisation_name

        return research_item
