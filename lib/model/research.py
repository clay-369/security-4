from lib.model.database import Database

class Research:
    def __init__(self):
        database = Database("../../databases/database.db")
        self.conn, self.cursor = database.connect_db()

    def create_research(self, research_item):
        research_item['status'] = 'NIEUW'
        research_item['beschikbaar'] = True

        # Filter optional fields
        try: research_item['locatie']
        except KeyError: research_item['locatie'] = None

        try: research_item['beloning']
        except KeyError: research_item['beloning'] = None

        # Filter onderzoek_type in ['ONLINE', 'OP LOCATIE', 'TELEFONISCH']
        if not research_item['onderzoek_type'] in ['ONLINE', 'OP LOCATIE', 'TELEFONISCH']:
            return False

        self.cursor.execute(
            "INSERT into onderzoeken ("
                "organisatie_id, titel, beschikbaar, "
                "datum_vanaf, datum_tot, onderzoek_type, locatie, met_beloning, "
                "beloning, leeftijd_vanaf, leeftijd_tot, status"
            ") "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                research_item['organisatie_id'], research_item['titel'], research_item['beschikbaar'],
                research_item['datum_vanaf'], research_item['datum_tot'], research_item['onderzoek_type'],
                research_item['locatie'], research_item['met_beloning'], research_item['beloning'],
                research_item['leeftijd_vanaf'], research_item['leeftijd_tot'], research_item['status']
             ),
        )
        self.conn.commit()

        return True
