# Arkkitehtuurikuvaus

## Sovelluslogiikka

Sovelluksen looginen tietomalli koostuu luokista User, Sudoku ja Stats (puuttuu sovelluksesta vielä toistaiseksi),jotka kuvaavat käyttäjiä, pelattavia sudokuja sekä käyttäjien pelitietoja:

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
        status
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

