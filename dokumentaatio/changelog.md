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

## Viikko 5

- Valmiin sudokun tarkistus toimii oikein
- Pelitiedot tallennetaan stats-tauluun
- Hiottu UI-luokan pelinäkymää: lisätty painike yksittäisen sudokuruudukon tyhjäykselle, ja paranneltu muiden painikkeiden asettelua. Sudokuruudukon visuaalisen ilmeen parannusta
- Luotu testejä, joilla varmistetaan SudokuRepository-luokan toimivuus. Luotu myös testejä SudokuService-luokalle
- Otettu käyttöön pylint-työkalu koodin laadun parantamiseksi

## Viikko 6

- Lisätty docstring-kommentteja
- Hiottu graafista käyttöliittymää, paranneltu asetteluja ja värejä
- Lisätty virheentarkistuksia ja virheviestejä käyttäjutunnuksen rekisteröintiin ja uusien sudokujen lukuun
- Siirretty sudokut sisältävät tekstitiedostot data-hakemistoon
- Lisätty käyttöohje


## Viikko 7

- Lisätty loput docstring-kommentit
- Sovelluksen luokkien testaus viety loppuun
- Lisätty sudokunvalintasivulle mahdollisuus siirtyä eri sivujen välillä
- Lisätty toiminnallisuus sudokujen lisäykseen käyttöliittymän kautta ja poistettu tekstitiedostojen kautta tapahtuva sudokujen lisäys ja luku
- Lisätty toiminnallisuus sudokujen poistamiseksi käyttöliittymän kautta
- Lisätty tarkistuksia käyttäjäsyötteisiin
- Eriytetty raskas sovelluslogiikkaluokka kahteen erilliseen SudokuService- ja UserService-luokkaan
- Lisätty dokumentaatio sovelluksen testauksesta
- Lisätty käyttöjärjestelmätarkistus sovelluksen käynnistyksen yhteyteen, jotta sovellus toimii myös Windowsilla