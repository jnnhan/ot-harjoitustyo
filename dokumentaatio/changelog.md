## Viikko 3

- Käyttäjä voi luoda käyttäjätunnuksen ja kirjautua sisään
- Luotu alkeellinen sudoku grid
- Luotu UserRepository-luokka, joka vastaa käyttäjätietojen tallennuksesta tietokantaan
- Luotu SudokuService-luokka, joka vastaa sovelluslogiikasta
- Luotu käyttöliittymästä vastaava UI-luokka ja luokat sovelluksen kirjautumis- ja rekisteröitymisnäkymiä varten
- Luotu testit, joilla varmistetaan UserRepository-luokan toimivuus ja tietojen oikeellinen tallennus
- Lisätty werkzeug-kirjasto salasanojen suojaamista varten, vaikka se ei kurssin kannalta tärkeää ollutkaan

## Viikko 4

- Sudokujen luku tekstitiedostosta. Käyttäjä voi halutessaan lisätä omia sudokuja tiedostoon
- Luotu luokka Sudoku-oliolle
- Luotu SudokuRepository-luokka, joka vastaa sudokujen ja pelitietojen tallennuksesta tietokantaan
- Luotu näkymät pelin vaikeustason valinnalle sekä eri sudokujen valinta listamuodossa
- Valmiin sudokun tarkistus. Jos numerot ovat oikein, näytetään viesti onnistumisesta. Tämä ei toimi vielä täysin moitteettomasti
