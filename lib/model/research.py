from lib.model.database import Database


class Research:
    def __init__(self):
        database = Database("../../databases/database.db")
        self.conn, self.cursor = database.connect_db()

    def get_max_id(self):
        max_id = self.cursor.execute("SELECT MAX(id) FROM onderzoeken").fetchone()
        return max_id

    def get_research_by_id(self, research_id:int):
        result = self.cursor.execute("SELECT * FROM onderzoeken WHERE id = ?", research_id).fetchone()
        return result

    def create_research(self, research_item:object):


        # Accept dictionary like
        # {
        #     'organisatie_id': int,
        #     'titel': str,
        #     'beschikbaar': bool,
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
        research_item['beschikbaar'] = True  # maybe let organisation choose

        # Filter optional fields
        try:
            research_item['locatie']
        except KeyError:
            research_item['locatie'] = None

        try:
            research_item['beloning']
        except KeyError:
            research_item['beloning'] = None

        # Filter onderzoek_type
        if research_item['onderzoek_type'] not in ['ONLINE', 'OP LOCATIE', 'TELEFONISCH']:
            return False

        new_research_id = self.get_max_id()

        self.cursor.execute(
            "INSERT into onderzoeken ("
            "onderzoek_id, organisatie_id, titel, beschikbaar, "
            "datum_vanaf, datum_tot, onderzoek_type, locatie, met_beloning, "
            "beloning, leeftijd_vanaf, leeftijd_tot, status"
            ") "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                new_research_id,
                research_item['organisatie_id'], research_item['titel'], research_item['beschikbaar'],
                research_item['datum_vanaf'], research_item['datum_tot'], research_item['onderzoek_type'],
                research_item['locatie'], research_item['met_beloning'], research_item['beloning'],
                research_item['leeftijd_vanaf'], research_item['leeftijd_tot'], research_item['status']
            ),
        )
        self.conn.commit()

        # TODO: create beperking_onderzoek instances
        # for item in research_item['beperingen']

        return new_research_id
