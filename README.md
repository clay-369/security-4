Python versie: 3.13

Maak een virtual environment:
1) python -m venv venv
2) .\venv\Scripts\activate

Installeer packages:
pip install -r requirements.txt

Start de app met:
python app.py
En ga naar http://127.0.0.1:5000

# Website
Log in met de email "kruwg@hr.nl" en wachtwoord "geheim" om in te loggen in een beheerder account.

Je kan op ieder moment rechtsbovenin wisselen tussen donker en licht thema.

## Beheerders
### Verzoeken
Op het beheerder dashboard kom je op het scherm waarbij je verzoeken kan goed en fout keuren voor onderzoeken, 
nieuwe deskundigen en inschrijvingen op onderzoeken.

Er staat standaard een onderzoek in. Deze kan je goedkeuren.
### Beheerders
Wanneer je op de tab 'Beheerders' klikt, kom je op een overzicht
met alle beheerder accounts. Je kan hier ook nieuwe accounts aanmaken, bewerken en verwijderen.
### Organisatie
In de tab 'Organisatie' kom je op een pagina waar je nieuwe organisaties kan registreren.

## Deskundigen
### Registreren
Wanneer je op het login scherm rechtsboven op 'Registreren' klikt, kom je op de pagina waar je als 
deskundige kan registreren.
### Inloggen
Als je nu inlogt met je account krijg je een melding dat je registratie in behandeling is.

Het onderzoek die standaard in de database staat heeft als beperkingen doof, slechthorend en doofblind.
Als je een account maakt met 1 of meerdere van deze beperkingen kan je dit onderzoek terugvinden wanneer je inlogd.

Je moet nu wachten tot een beheerder het heeft goedgekeurd. (dit kan je nu zelf doen met het beheerder account)
Als deze is afgekeurd krijg je dat te zien bij de volgende keer dat je inlogt.
Als deze is goedgekeurd kan je gewoon inloggen.
### Dashboard
Wanneer er onderzoeken zijn die voldoen aan jouw opgegeven informatie, zoals jouw leeftijd en beperkingen, vind je die 
hier terug. 

Als je net de beperking doof, slechthorend of doofblind had gekozen, kan je nu het standaard onderzoek zien.

Ze moeten natuurlijk ook beschikbaar worden gezet door de organisatie en worden goedgekeurd door een beheerder. 
Wanneer je op een onderzoek klikt kan je hier voor inschrijven.
### Inschrijvingen
Onder de tab 'Inschrijvingen' vind je al jouw inschrijvingen terug. Hier zie je welke inschrijvingen 
lopend, goedgekeurd of afgekeurd zijn. Op het punt dat een onderzoek lopend of goedgekeurd is, kan je er altijd nog
voor uitschrijven. Kan krijg je ze weer te zien op het dashboard.

Je kunt op deze pagina ook zoeken naar een inschrijving. Er wordt dan gezocht op de titel en de beschrijving van de onderzoeken.
### Profiel
Onder de tab 'Profiel' vind je jouw profielgegevens terug. Hier kan je ze ook bijwerken.

## Organisaties
### Bruno
De endpoints van de organisaties zijn beschreven in Bruno in de folder 'Bruno-WP3'.
In de map 'JWT' vind je alles wat met je account te maken heeft, zoals in en uitloggen.
In de map 'Organisations' vind je alles wat een organisatie kan doen.

### JWT
#### Login /auth/login (POST)
De login is gevuld met de e-mail en wachtwoord van de standaard organisatie.
Dit is 
`{
  "email": "peter@email.com",
  "password": "ABC"
}`
Als je dit verstuurt krijg je een access en refresh token terug. Kopieër de access token.
#### Refresh Token /auth/refresh (GET)
Als je in de Auth header je refresh token stuurt, krijg je een nieuwe access token terug. 
Dit kan je doen wanneer je access token is verlopen.
#### Who Am I /auth/whoami (GET)
Als je hier je auth token verstuurt, krijg je alle informatie van jouw account terug behalve je wachtwoord.
#### Logout /auth/logout (GET)
Als je hier en access of refresh token meestuurt, worden ze niet meer bruikbaar.

### Organisations
#### Create Research /onderzoeken (POST)
Geef hier je access token mee in de Auth.
In de body wordt de json structuur verwacht die in de Docs tab staat.
`{
  "titel": String,
  "beschikbaar": Bool,
  "beschrijving": String,
  "datum_vanaf": String,
  "datum_tot": String,
  "onderzoek_type": String (OP LOCATE, TELEFONISCH, ONLINE),
  "locatie": String (Only if onderzoek_type is OP LOCATIE),
  "met_beloning": Bool,
  "beloning": String (Only if "met_beloning is true"),
  "leeftijd_vanaf": Int,
  "leeftijd_tot": Int,
  "beperkingen": [
    "blind",
    "amputatie of mismaaktheid",
    "doof"
  ] (Can be any disability that is in the database)
}`
#### Get All Research Items /onderzoeken (GET)
Geef je access token mee in de Auth.
Je krijgt hier alle onderzoeken gekoppeld aan dit account met alle informatie. Zo zie je ook alle goed- en afgekeurde inschrijvingen
en het onderzoek_id van jouw onderzoeken.
#### Get Research Item /onderzoeken/<onderzoek_id> (GET)
Vul het onderzoek_id in van één van jouw onderzoeken in de URL.
Geef je access token mee in de Auth.
Hier zie je alle informatie van één van jouw onderzoeken.
#### Edit Research /onderzoeken/<onderzoek_id> (PUT)
Vul het onderzoek_id in van één van jouw onderzoeken in de URL.
Geef je access token mee in de Auth.
Geef het aangegeven json structuur mee uit Docs in de body.
`{
 "titel": String,
 "beschikbaar": Bool,
 "beschrijving": String,
 "datum_vanaf": String,
 "datum_tot": String,
 "met_beloning": Bool,
 "beloning": String
}`
Deze velden kan je nu bewerken. Ze worden allemaal bewerkt, dus laat er geen weg.
#### Edit Organisation /organisatie (PUT)
Geef je access token mee in de Auth.
Hier kan je je organisatie account bewerken.
Geef het aangegeven json structuur uit Docs mee in de body.
`{
  "naam": String,
  "organisatie_type": String (non-profit, commercieel,
  "website": String,
  "beschrijving": String (Optioneel),
  "contact_persoon": String,
  "email": String,
  "telefoonnummer": String,
  "overige_details": String (Optioneel),
  "wachtwoord": String
}`




# Technische details
Alle nodige routes zijn beschermd met JWT.
De beheerder pagina's "Verzoeken", "Logsysteem" en "Beheerders"
en deskundige pagina's "Inschrijvingen" en "Onderzoeken"
worden in real-time ververst op updates

# Bronnen:

- Krishna, A. (2022, 1 september). How to Use Blueprints to Organize Your Flask Apps. freeCodeCamp.org. https://www.freecodecamp.org/news/how-to-use-blueprints-to-organize-flask-apps/

- JWT authentication for flask. (n.d.). YouTube. https://www.youtube.com/playlist?list=PLEt8Tae2spYmugodsDflw5U8zp1yzSPgU

- calculating age using date and string type values. (z.d.). Stack Overflow. https://stackoverflow.com/questions/76325701/calculating-age-using-date-and-string-type-values
