# Arkkitehtuurikuvaus

## Sovelluslogiikka

Sovelluksen looginen tietomalli koostuu luokista User, Sudoku ja Stats,jotka kuvaavat käyttäjiä, pelattavia sudokuja sekä käyttäjien pelitietoja:

```mermaid
classDiagram
    Sudoku "0..*" --> "0..*" Stats
    Stats "1" --> "1" User
    Sudoku "*" --> "*" User

    class User{
        username
        password
    }
    class Sudoku{
        name
        puzzle
        level
    }
    class Stats{
        user_id
        sudoku_id
        playtime
    }
```

Luokka _UserService_ vastaa sovelluksen käyttäjätietoihin liittyvistä toiminnallisista kokonaisuuksista. Sen metodeja ovat mm.:

- `login(username, password)`
- `create_user(username, password)`
- `get_playtime(user_id, sudoku_id)`

Luokka _SudokuService_ vastaa sovelluksen sudokuihin liittyvistä toiminnallisista kokonaisuuksista. Sen metodeja ovat mm.:

- `check_sudoku(sudoku)`
- `check_new_sudoku_input(sudoku)`
- `get_sudokus(level)`
- `numbers_to_puzzle(sudoku)`


_UserService_ pääsee käsiksi käyttäjäolioihin luokan UserRepository kautta. Se vastaa käyttäjätietojen käsittelystä ja tallennuksesta tietokantaan. Luokka hyödyntää myös luokkaa _SudokuService_ tallentaakseen käyttäjän tiettyä sudokua koskevia pelitietoja.

_SudokuService_ pääsee käsiksi sudokuolioihin luokan SudokuRepository kautta. Se vastaa sudokujen käsittelystä ja tallennuksesta tietokantaan.

Luokka/pakkauskaavio:

![Pakkausrakenne ja luokat](./kuvat/pakkauskaavio.png)

## Tietojen tallennus

Sovelluksen luokat `UserRepository` ja `SudokuRepository` vastaavat tietojen tallennuksesta SQLite-tietokantaan. Sovelluksen asennuksen ja alustuksen jälkeen tietokannassa on valmiiksi sudokuja eri vaikeustasoilla. Käyttäjä voi syöttää uusia sudokuja käyttöliittymän kautta, ja ne tallennetaan tietokantaan. 

### Tiedostot

Sovellus tallettaa tietokantojen sisällön .sqlite-tiedostoon, jonka nimi on määritelty konfiguraatiotiedostossa [.env](https://github.com/jnnhan/ot-sudoku/blob/main/.env).

Käyttäjät tallennetaan SQLite-tietokannan tauluun  `users`, sudokut tauluun `sudokus` ja pelitiedot tauluun `stats`. Nämä taulut alustetaan tiedostossa [init_database.py](https://github.com/jnnhan/ot-sudoku/blob/main/src/init_database.py).

## Toiminnallisuudet sekvenssikaaviona

### Uuden käyttäjän luonti

Sovelluksen käynnistymisen jälkeen klikataan _'Create a new user'_-painiketta, ja syötetään ilmestyviin kenttiin uusi käyttäjänimi ja oikeellinen salasana. Lopuksi klikataan 'Register'-painiketta, jonka jälkeen uudella käyttäjätunnuksella voi kirjautua sisään.

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant UserService
    participant UserRepository
    participant kotikissa
    User->>UI: click "Register" button
    UI->>UserService: create_user("kotikissa", "kissa123")
    UserService->>UserRepository: find_user("kotikissa")
    UserRepository-->>UserService: None
    UserService->>UserService: generate_password_hash("kissa123)
    UserService-->>UserService: hash_value
    UserService->>kotikissa: User("kotikissa", "kissa123")
    UserService->>UserRepository: create_user(kotikissa, hash_value)
    UserRepository-->>UserService: user
    UserService-->>UI: user
    UI->>UI: show_login_view()
```

Tapahtumakäsittelijä kutsuu sovelluslogiikan, eli `UserService`:n, metodia `create_user`, jolle annetaan parametriksi uusi käyttäjätunnus ja salasana. Sovelluslogiikka selvittää  `UserRepository`-luokan metodin `find_user` avulla onko annettu käyttäjätunnus jo olemassa. Jos ei, sovelluslogiikka luo `User`-olion annetuilla parametreilla, ja merkkijonomuotoinen salasana hashataan `werkzeug`-kirjaston metodin `generate_password_hash` avulla. Käyttäjänimi ja sitä vastaava salattu salasana tallennetaan tietokantaan kutsumalla `UserRepository`-luokan metodia `create_user`. Tämän jälkeen käyttöliittymä vaihtaa näkymäksi sisäänkirjautumisnäkymän, eli `LoginView`:n.

### Sisäänkirjautuminen

Sovelluksen kirjautumisnäkymän kenttiin syötetään olemassaoleva käyttäjätunnus ja sitä vastaava salasana, ja klikataan _'Login'_-painiketta. 

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant UserService
    participant UserRepository
    User->>UI: click "Login" button
    UI->>UserService: login("kotikissa", "kissa123")
    UserService->>UserRepository: find_user("kotikissa")
    UserRepository-->>UserService: user
    UserService->>UserRepository: get_password("kotikissa")
    UserRepository-->>UserService: hash_password
    UserService-->>UI: user
    UI->>UI: show_main_view()
```

Tapahtumakäsittelijä reagoi painikkeen painamiseen ja kutsuu sovelluslogiikan `UserService` metodia `login`, joka saa parametrikseen käyttäjän syöttämän käyttäjätunnuksen ja salasanan. Sovelluslogiikka selvittää `UserRepository`:n avulla ensin onko käyttäjätunnusta vastaava käyttäjä olemassa. Jos on, tarkistetaan seuraavaksi vastaako käyttäjän syöttämä salasana tietokantaan talletettua hash-salasanaa. Jos kaikki täsmää, käyttöliittymä vaihtaa näkymäksi `MainView`:n, eli sovelluksen päänäkymän, jonka kautta sudokupelin vaikeustason voi valita.

### Sudokun pelaaminen

Käyttäjä valitsee pelattavan sudokun klikkaamalla sen nimeä. Käyttäjä syöttää kenttiin oikeat numerot ja pelin pelattuaan painaa _'Return'_-painiketta.

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant SudokuService
    participant UserService
    participant SudokuRepository
    participant UserRepository
    User->>UI: click button with sudoku's name
    UI->>UI: show_game_view()
    UI->>UI: fill the sudoku correctly
    UI->> SudokuService: check_sudoku(puzzle)
    SudokuService-->>UI: True
    UI->>UserService: save_status()
    UserService->>UserRepository: get_user_id(user.username)
    UserRepository-->>UserService: user_id
    UserService->>SudokuService: get_sudoku_id(sudoku)
    SudokuService-->>UserService: sudoku_id
    UserService->>SudokuRepository: save_status(user_id, sudoku_id)
    SudokuRepository-->>UserService: 
    UserService-->>UI: 
    User->>UI: click the "Return" button
    UI->>SudokuService: get_current_sudoku()
    SudokuService-->>UI: sudoku
    UI->>SudokuService: remove_current_sudoku()
    UI->>UI: show_sudoku_select(sudoku.level)
```

Tapahtumäkäsittelijä näyttää pelinäkymän ja tarkistaa jokaisen uuden syötetyn numeron jälkeen onko ruudukko täynnä. Jos on, kutsutaan sovelluslogiikan `SudokuService` metodia `check_sudoku`, joka tarkistaa ovatko syötetyt numerot oikein. Jos ovat, kutsutaan seuraavaksi sovelluslogiikan käyttäjätoiminnallisuuksista vastaavaa metodia `save_status`, joka tallentaa `SudokuRepository`:n kautta tietokantaan tiedon pelaajan ratkaisemasta sudokusta. Käyttäjän klikattua _'Return'_-painiketta kutsutaan sovelluslogiikan metodia `get_current_sudoku`, jonka avulla saadaan tietoon juuri pelatun sudokun vaikeustaso. Tämä vaikeustaso annetaan parametrina käyttöliittymän näkymäluokalle `SudokuSelectView`.

### Sudokun lisääminen

Käyttäjä painaa sovelluksen päänäkymässä '_Add sudoku_'-painiketta, jonka jälkeen näytetään näkymä sudokujen lisäämiseksi. Käyttäjä syöttää uuden sudokun tiedot ja painaa '_Submit_'-painiketta.

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant SudokuService
    participant SudokuRepository
    participant sudoku
    User->>UI: input info for new sudoku
    UI->>SudokuService: save_sudoku("easy sudoku", 1, "0123...008")
    SudokuService->>sudoku: Sudoku("easy sudoku", "0123...008", 1)
    SudokuService->>SudokuService: numbers_to_matrix(sudoku)
    SudokuService-->>SudokuService: sudoku_matrix
    SudokuService->>SudokuService: check_sudoku(sudoku_matrix)
    SudokuService-->>SudokuService: True
    SudokuService->>SudokuRepository: create_sudoku(sudoku)
    SudokuRepository-->>SudokuService: 
    SudokuService-->>UI: 
    UI->>UI: show_add_sudoku_view()
```

Tapahtumakäsittelijä näyttää sudokunluontinäkymän. Käyttäjän painettua _'Submit'_-painiketta kutsutaan sovelluslogiikan sudokutoiminnallisuuksista vastaavan luokkan `SudokuService` metodia `save_sudoku`. Sovelluslogiikka luo annetuilla parametreilla `Sudoku`-olion ja kutsuu omaa metodiaan `numbers_to_matrix` luodakseen annetuista numeroista sudokumatriisin. Sudokumatriisi annetaan parametrina metodille `check_sudoku`, joka tarkistaa, että annettu sudoku on mahdollista ratkaista. Jos näin on, kutsutaan `SudokuRepository`-luokan metodia `create_sudoku`, joka tallentaa annetun sudokun tietokantaan.

### Sudokun poistaminen

Käyttäjä painaa sudokunvalintanäkymässä painiketta _'Delete sudokus'_. Jokaisen suokun alle ilmestyy pieni ruutu, ja käyttäjä valitsee niiden avulla poistettavat sudokut. Lopuksi painetaan _'Confirm'_-painiketta.

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant SudokuService
    participant SudokuRepository
    User->>UI: click "Confirm" button
    UI->>SudokuService: delete_sudokus(["outosudoku"])
    SudokuService->>SudokuRepository: get_sudoku_ids("outosudoku")
    SudokuRepository-->>SudokuService: sudoku_id
    SudokuService->>SudokuRepository: delete_sudokus_from_db(sudoku_id)
    SudokuRepository-->>SudokuService: 
    SudokuService-->>UI: 
    UI->>UI: show_select_view()
```

Tapahtumakäsittelijä kutsuu sovelluslogiikan `SudokuService`-luokan metodia `delete_sudokus`, joka saa parametrinaan poistettavien sudokujen nimet. Metodi kutsuu `SudokuRepository`-luokan metodia `get_sudoku_ids` ja hakee sudokujen id-numerot, joiden perusteella sudokut poistetaan tietokannasta. Poiston jälkeen tapahtumakäsittelijä näyttää sudokunvalintanäkymän nykyisen tilan.

### Muut toiminnallisuudet

Muut sovelluksen toiminnallisuudet seuraavat samaa periaatetta. Käyttäjän valintojen mukaan käyttöliittymän tapahtumakäsittelijä kutsuu sovelluslogiikan metodia, josta tapahtumasta riippuen kutsutaan `SudokuRepository`:n tai `UserRepository`:n metodeita.
