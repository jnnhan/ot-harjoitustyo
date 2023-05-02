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

Luokka SudokuService vastaa sovelluksen toiminnallisista kokonaisuuksista. Sen metodeja ovat mm.:

- `login(username, password)`
- `create_user(username, password)`
- `read_sudokus(file_path, level)`
- `check_sudoku_win(sudoku)`
- `get_sudokus(level)`
- `numbers_to_puzzle(sudoku)`

_SudokuService_ pääsee käsiksi käyttäjä- ja sudokuolioihin luokkien UserRepository ja SudokuRepository kautta. Ne vastaavat käyttäjätietojen, sudokujen ja pelitilastojen käsittelystä ja tallennuksesta tietokantaan.

Luokka/pakkauskaavio:

![Pakkausrakenne ja luokat](./kuvat/pakkauskaavio.png)

## Tietojen tallennus

Sovelluksen luokat `UserRepository` ja `SudokuRepository` vastaavat tietojen tallennuksesta SQLite-tietokantaan. SudokuRepository lukee pelattavat sudokutiedostot txt-tiedostosta.

### Tiedostot

Sovellus tallettaa tietokantojen sisällön .sqlite-tiedostoon, jonka nimi on määritelty konfiguraatiotiedostossa [.env](https://github.com/jnnhan/ot-sudoku/blob/main/.env). Kyseisessä tiedostossa on määritelty myös tiedostot, joihin uudet sudokut lisätään ja joista ne luetaan. Sudokujen luku tapahtuu tiedoston [read_sudokus.py](https://github.com/jnnhan/ot-sudoku/blob/main/src/read_sudokus.py) kautta.

Sudokut ovat tekstitiedostoissa seuraavanlaisessa formaatissa:

```
759620004
016040000
000005900
601004000
000713046
080062090
000208009
300000650
198056070
.easy3
```

Ensin on syötetty järjestyksessä ja allekkain sudokun 9 riviä. Luvut 0 merkitsevät tyhjiä ruutuja. Kymmenes rivi aloitetaan pisteellä, jonka jälkeen on kirjoitettu sudokun nimi. Sudokujen nimiet ovat uniikkeja.

Käyttäjät tallennetaan SQLite-tietokannan tauluun  `users`, sudokut tauluun `sudokus` ja pelitiedot tauluun `stats`. Nämä taulut alustetaan tiedostossa [init_database.py](https://github.com/jnnhan/ot-sudoku/blob/main/src/init_database.py).

## Toiminnallisuudet sekvenssikaaviona

### Uuden käyttäjän luonti

Sovelluksen käynnistymisen jälkeen klikataan _'Create new username'_-painiketta, ja syötetään ilmestyviin kenttiin uusi käyttäjänimi ja oikeellinen salasana. Lopuksi klikataan 'Register'-painiketta, jonka jälkeen uudella käyttäjätunnuksella voi kirjautua sisään.

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant SudokuService
    participant UserRepository
    participant kotikissa
    User->>UI: click "Register" button
    UI->>SudokuService: create_user("kotikissa", "kissa123")
    SudokuService->>UserRepository: find_user("kotikissa")
    UserRepository-->>SudokuService: None
    SudokuService->>kotikissa: User("kotikissa", "kissa123")
    SudokuService->>UserRepository: create_user(kotikissa)
    UserRepository-->>SudokuService: user
    SudokuService-->>UI: user
    UI->>UI: show_login_view()
```

Tapahtumakäsittelijä kutsuu sovelluslogiikan, eli `SudokuService`:n, metodia `create_user`, jolle annetaan parametriksi uusi käyttäjätunnus ja salasana. Sovelluslogiikka selvittää  `UserRepository`-luokan metodin `find_user` avulla onko annettu käyttäjätunnus jo olemassa. Jos ei, sovelluslogiikka luo `User`-olion annetuilla parametreilla, ja se tallennetaan tietokantaan kutsumalla `UserRepository`-luokan metodia `create_user`. Kyseisessä metodissa merkkijonomuotoinen salasana hashataan `werkzeug`-kirjaston metodin `generate_password_hash` avulla. Tämän jälkeen käyttöliittymä vaihtaa näkymäksi sisäänkirjautumisnäkymän, eli `LoginView`:n.

### Sisäänkirjautuminen

Sovelluksen kirjautumisnäkymän kenttiin syötetään olemassaoleva käyttäjätunnus ja sitä vastaava salasana, ja klikataan _'Login'_-painiketta. 

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant SudokuService
    participant UserRepository
    User->>UI: click "Login" button
    UI->>SudokuService: login("kotikissa", "kissa123")
    SudokuService->>UserRepository: find_user("kotikissa")
    UserRepository-->>SudokuService: user
    SudokuService->>UserRepository: get_password("kotikissa")
    UserRepository-->>SudokuService: hash_password
    SudokuService-->>UI: user
    UI->>UI: show_main_view()
```

Tapahtumakäsittelijä reagoi painikkeen painamiseen ja kutsuu sovelluslogiikan `SudokuService` metodia `login`, joka saa parametrikseen käyttäjän syöttämän käyttäjätunnuksen ja salasanan. Sovelluslogiikka selvittää `UserRepository`:n avulla ensin onko käyttäjätunnusta vastaava käyttäjä olemassa. Jos on, tarkistetaan seuraavaksi vastaako käyttäjän syöttämä salasana tietokantaan talletettua hash-salasanaa. Jos kaikki täsmää, käyttöliittymä vaihtaa näkymäksi `MainView`:n, eli sovelluksen päänäkymän, jonka kautta sudokupelin vaikeustason voi valita.

### Sudokun pelaaminen

Käyttäjä valitsee pelattavan sudokun klikkaamalla sen nimeä. Käyttäjä syöttää kenttiin oikeat numerot ja pelin pelattuaan painaa _'Return'_-painiketta.

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant SudokuService
    participant SudokuRepository
    participant UserRepository
    User->>UI: click button with sudoku's name
    UI->>UI: show_game_view()
    UI->>UI: fill the sudoku correctly
    UI->> SudokuService: check_sudoku_win(sudoku)
    SudokuService-->>UI: True
    UI->>SudokuService: save_status()
    SudokuService->>UserRepository: get_user_id(user.username)
    UserRepository-->>SudokuService: user_id
    SudokuService->>SudokuRepository: get_sudoku_id(sudoku.name)
    SudokuRepository-->>SudokuService: sudoku_id
    SudokuService->>SudokuRepository: save_status(user_id, sudoku_id)
    SudokuRepository-->>SudokuService: 
    SudokuService-->>UI: 
    User->>UI: click the "Return" button
    UI->>SudokuService: get_current_sudoku()
    SudokuService-->>UI: sudoku
    UI->>SudokuService: remove_current_sudoku()
    UI->>UI: show_sudoku_select(sudoku.level)
```

Tapahtumäkäsittelijä näyttää pelinäkymän ja tarkistaa jokaisen uuden syötetyn numeron jälkeen onko ruudukko täynnä. Jos on, kutsutaan sovelluslogiikan `SudokuService` metodia `check_sudoku_win`, joka tarkistaa ovatko syötetyt numerot oikein. Jos ovat, kutsutaan seuraavaksi sovelluslogiikan metodia `save_status`, joka tallentaa `SudokuRepository`:n kautta tietokantaan tiedon pelaajan ratkaisemasta sudokusta. Käyttäjän klikattua _'Return'_-painiketta kutsutaan sovelluslogiikan metodia `get_current_sudoku`, jonka avulla saadaan tietoon juuri pelatun sudokun vaikeustaso. Tämä vaikeustaso annetaan parametrina käyttöliittymän näkymäluokalle `SudokuSelectView`.

### Muut toiminnallisuudet

Muut sovelluksen toiminnallisuudet seuraavat samaa periaatetta. Käyttäjän valintojen mukaan käyttöliittymän tapahtumakäsittelijä kutsuu sovelluslogiikan metodia, josta tapahtumasta riippuen kutsutaan `SudokuRepository`:n tai `UserRepository`:n metodeita.
