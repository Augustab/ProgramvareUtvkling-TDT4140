![Logo](https://github.com/Augustab/ProgramvareUtvkling-TDT4140/blob/master/static/images/Hotell_logo2.png?raw=true)


# Programvareutvikling - Gruppe 36

### Introduksjon

Gruppe 36 i Programvareutvikling (TDT4140) har i løpet av dette semesteret laget en nettside for hotellet "Skikkelig Fancy Hotell". Nettsiden er ment å gjøre det lettere for hotellet å ta imot bestillinger og ha oversikt over hvem som bor på hotellet, og når de bor der. Det skal være mulig å opprette en bruker, bestille/avbestille et rom og ikke minst se tilgjengelige rom. Admin skal ha mulighet til å legge til/fjerne rom, samt ha oversikt over bookinger og ansatte. Investorer og vaskehjelper vil også ha egen funksjonalitet.

#### Hva trenger du?
###### Python (Programmeringsspråket)
* [Python 3.8 Windows] - Kun hvis du bruker Windows.
* [Python 3.8 Mac] - Kun hvis du bruker Mac.

###### PyCharm (IDE)
* [JetBrains PyCharm]
Her finnes det to versjoner til hvert operativsystem: én gratis og én profesjonell versjon (anbefalt).

###### Git
* [Git Windows] - Kun hvis du bruker Windows.
* [Git Mac] - Kun hvis du bruker Mac.
	

### Installering
##### Installer Git
1. Finn og kopiér filplasseringen til ***git.exe***  i Git/cmd-mappen
2. Åpne filutforskeren og høyreklikk på *Denne PCen*>Egenskaper
3. Trykk på *Avanserte systeminstillinger* ***(til venstre***) > *Miljøvariabler*
4. Trykk på *Path* under ***Systemvariabler*** > *Rediger...*
5. Trykk ***Ny*** og lim inn filplasseringen til ***git.exe*** (steg 1)
6. Deretter trykker du OK til alt.

##### Hent prosjektet fra GitLab
1. Åpne PyCharm
2. Trykk *File* > *Close Project* (Hvis du har et prosjekt åpnet ved startup)
3. Klikk på *Get from Version Control*
4. Lim inn https://gitlab.stud.idi.ntnu.no/tdt4140-2020/36.git i URL-feltet
5. Trykk *Clone*
6. Logg inn med NTNU-brukeren for å få tilgang.

##### Lag en Interpreter
I PyCharm må du definere en *Interpreter* som skal forstå koden din. Vi skal da linke til Python 3.8 som du skal ha installert tidligere i guiden.
1. Trykk på File>Settings
2. Under *Project 36* ligger *Python Interpreter*
3. Hvis Python 3.8 ikke ligger som et alternativ i drop-down bar'en, trykker du på tannhjulet til høyre og deretter ***Add...***
4. Huk av for *New Environment*
5. Link til filplasseringen til ***python.exe*** i *Base Interpreter* (Denne ligger der du installerte Python 3.8)
6. Trykk OK

##### Oppdater prosjektet
1. Åpne terminalen (ligger nederst til venstre)
2. Skriv inn linjene nedenfor og trykk enter etter hver linje.
**Dette er for Windows! Hvis du bruker Mac blir pip > pip3 og py > python3**
```sh
pip install -r requirements.txt
py manage.py migrate
py manage.py loaddata db.json
```

Gratulerer! Du har nå installert prosjektet! 
Du kan teste hvordan applikasjonen ser ut (se "Kjøre applikasjonen" (Lokalt))
	
### Mappestruktur
Her er et diagram som viser de viktigste delene av mappestrukturen:

![Diagram](https://gitlab.stud.idi.ntnu.no/tdt4140-2020/36/-/raw/demo2/static/images/diagram.png)

**Mappen *untitled1* er root-filen.**


### Testing
I prosjektet er det flere funksjoner og elementer som er kritiske og som ***må*** fungere for at nettsiden kan brukes ordentlig. Dermed har vi laget tester som dekker det kritiske som må fungere, bl.a. booking-funksjonen. Vi har har to typer tester: manuelle tester og automatiske tester.

##### Automatisk testing
De automatiske testene dekker kodekvalitet, kompabilitet og funksjonalitet. Vi har også implementert CI i gitlab-prosjektet vårt. CI tester kompabiliteten til koden du skal til å *pushe* inn til prosjektet, og er til som en forsikring om at hele prosjektet ikke blir ødelagt av en feilbar *push*.
**For å kjøre testene vi har skrevet selv, åpner du terminalen og skriver:**
```
py manage.py test
```

##### Manuell testing
Manuelle tester gjennomfører vi fra tid til annen ved å kjøre applikasjonen og se at alt fungerer som det skal.
### Kjøre applikasjonen

##### Lokalt
Kjør koden i terminalen
```
py manage.py runserver
```
I databasen finner du flere forskjellige typer brukere som "augbi"(admin), "investor", "vaskehjelp", "booker", der alle har passord: "passord123". Gjennom disse brukerne får du testet all funksjonalitet til nettsiden. 

For å stenge ned serveren, holder du CTRL+C

**For å lage en ny administrator på den lokale nettsiden, skriver du:**
```
py manage.py createsuperuser
```
Deretter fyller du ut informasjonen som Django spør om.
##### Nettsiden
Det kan ta litt tid å starte opp serveren første gang du går inn på nettsiden.
https://skikkeligfancy-hotell.herokuapp.com/

Admin-brukeren på nettsiden heter "gruppe36" og passord "passord123". Ellers er resterende brukere identiske med den lokale versjonen.


### Verktøy

- Python 3.8 (Språk)
- PyCharm (IDE)
- Django (Framework)
- SQLite (Database)
- Bootstrap (UI)

### Systemutviklere

- Sindre Sand Wilberg (Scrum Master)
- Ingrid Renolen Borkenhagen (Utvikler)
- Jenny Heggen Thiis (Utvikler)
- August Asheim Birkeland (Utvikler)
- Jonathan Hailemariam (Utvikler)
- Mads Bråten Eliassen (Utvikler)
- Stefan Magnus Xara Brazil Fongen (Utvikler)

[//]: 

[Python 3.8 Windows]: <https://www.python.org/ftp/python/3.8.2/python-3.8.2-amd64.exe>
[Python 3.8 Mac]: <https://www.python.org/ftp/python/3.8.2/python-3.8.2-macosx10.9.pkg>
[JetBrains PyCharm]: <https://www.jetbrains.com/pycharm/download/#section=windows>
[Git Windows]: <https://git-scm.com/download/win>
[Git Mac]: <https://git-scm.com/download/mac>
