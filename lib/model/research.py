from pathlib import Path

from lib.model.database import Database
from lib.model.disabilities import Disabilities
from lib.model.enlistments import Enlistment


class Research:
    def __init__(self):
        database = Database('./databases/database.db')
        self.conn, self.cursor = database.connect_db()

    def get_research_by_id(self, research_id:int):
        result = self.cursor.execute("SELECT * FROM onderzoeken WHERE onderzoek_id=?", (research_id,)).fetchone()
        return result

    def get_organisation_by_id(self, research_id:int):
        result = self.cursor.execute("SELECT organisatie_id FROM onderzoeken WHERE onderzoek_id = ?", (research_id,)).fetchone()
        return result

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

        return new_research_id

    def get_all_research_ids_by_organisation_id(self, organisation_id):
        self.cursor.execute("SELECT onderzoek_id FROM onderzoeken WHERE organisatie_id = ?", (organisation_id,))
        rows = self.cursor.fetchall()
        return rows


    def get_all_available_research_items(self, age: int, disability_ids: list):
        available_research = self.cursor.execute("SELECT * FROM onderzoeken WHERE status = ? AND beschikbaar = ?"
                                                 "AND ? BETWEEN leeftijd_vanaf AND leeftijd_tot",
                            ('GOEDGEKEURD', True, age)).fetchall()


        relevant_research = []

        # Filter disabilities
        for research in available_research:
            # Check if any of the expert disabilities is in the research disabilities
            is_relevant = False
            research_disability_ids = self.get_disability_ids(research['onderzoek_id'])
            for dis_id in disability_ids:
                if dis_id in research_disability_ids:
                    is_relevant = True
                    break

            if is_relevant:
                relevant_research.append(research)

        return relevant_research


    def get_all_research_items_for_admins(self):
        self.cursor.execute("SELECT * FROM onderzoeken JOIN organisaties USING(organisatie_id)")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]


    def format_research_item(self, research_item) -> dict:
        """ Adds organisatie_naam to research_item and converts it to dict """
        research_item = dict(research_item)

        organisation_id = research_item['organisatie_id']
        organisation_name = self.cursor.execute("SELECT naam FROM organisaties WHERE organisatie_id = ?", (organisation_id,))
        organisation_name = organisation_name.fetchone()['naam']

        research_item['organisatie_naam'] = organisation_name

        return research_item

    def edit_research(self, research, research_id):
        try:
            research['beloning']
        except KeyError:
            if research['met_beloning'] == 1:
                return {"error": "Field <beloning> missing"}
            else:
                research['beloning'] = None

        try:
            research['beschrijving']
        except KeyError:
                research['beschrijving'] = None

        self.cursor.execute('UPDATE onderzoeken '
                            'SET titel = ?, beschikbaar = ?, beschrijving = ?, datum_vanaf = ?, '
                            'datum_tot = ?, beloning = ?, met_beloning = ? WHERE onderzoek_id = ?',
                            (research['titel'], research['beschikbaar'], research['beschrijving'],
                             research['datum_vanaf'], research['datum_tot'], research['beloning'],
                             research['met_beloning'], research_id))
        self.conn.commit()
        return True

    def status_update(self, status, onderzoek_id, admin_id):
        self.cursor.execute("UPDATE onderzoeken SET status = ?, beheerder_id = ? WHERE onderzoek_id = ?", (status, admin_id, onderzoek_id))
        self.conn.commit()
        return True, "Status gewijzigd!"

    def get_organisation_id(self, research_id):
        self.cursor.execute("SELECT organisatie_id FROM onderzoeken WHERE onderzoek_id = ?", (research_id,))
        return self.cursor.fetchone()['organisatie_id']

    def get_all_information(self, research_id):
        research_item = dict(self.get_research_by_id(research_id))

        # Add disabilities
        research_disabilities = self.cursor.execute("""
                        SELECT beperking FROM beperkingen
                        WHERE beperking_id IN (SELECT beperking_id FROM beperking_onderzoek WHERE onderzoek_id = ?)
                    """, (research_id,)).fetchall()

        research_disabilities = [dict(disability)['beperking'] for disability in research_disabilities]

        research_item['beperkingen'] = research_disabilities

        # Add enlistments
        enlistment_model = Enlistment()
        enlistments = enlistment_model.get_enlistments_for_organisation(research_id)

        research_item['inschrijvingen'] = enlistments

        return research_item

    def get_disability_ids(self, research_id):
        id_list = self.cursor.execute("""
            SELECT beperking_id FROM beperking_onderzoek WHERE onderzoek_id = ?
        """, (research_id,)).fetchall()
        return [dis_id['beperking_id'] for dis_id in id_list]