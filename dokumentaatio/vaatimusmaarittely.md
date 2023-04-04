# Vaatimusmäärittely

## Sovelluksen tarkoitus
Sovellus on yksinpelattava sudoku, jossa on valittavissa eri vaikeustasoja. Käyttäjä voittaa pelin, jos onnistuu täyttämään kaikki tyhjät ruudut 9x9 ruudukossa. Peliä ei voi hävitä, mutta sen voi lopettaa kesken.

## Toiminnallisuudet
### Ennen kirjautumista
- Käyttäjä voi luoda käyttäjätunnuksen
  - Käyttäjätunnuksen on oltava uniikki ja vähintään 3 merkin mittainen
  - Salasanan on oltava vähintään 4 merkin mittainen
- Käyttäjä voi kirjautua järjestelmään
  - Kirjautuminen onnistuu, jos syötetään olemassaoleva käyttäjätunnus ja sitä vastaava salasana
  - Jos käyttäjätunnus tai salasana on väärä, tai tunnusta ei ole olemassa, annetaan virheilmoitus
      
### Kirjautumisen jälkeen 
- Käyttäjä näkee tilastoja omista sudokuista
  - ratkaistujen sudokujen lukumäärä ja niihin kulunut aika
- Käyttäjä voi aloittaa uuden sudokun valitsemallaan vaikeustasolla
- Käyttäjä voi kirjautua ulos sovelluksesta
    
### Pelaaminen
- Sovellus sisältää eri vaikeustasoisia sudokuja.
- Käyttäjä voi merkata tyhjään ruudukkoon yhden tai useamman numeron
  - Useamman numeron tapauksessa ne näkyvät ruudukon yläreunassa "apunumeroina"
  - Jos ruudukossa on vain yksi numero, se näkyy suurempana keskellä ruudukkoa
- Käyttäjä voi pyyhkiä merkkaamiaan numeroita ruudukoista
- Jos kaikki ruudukot ovat täynnä ja virheitä ei havaita, peli päättyy
    
## Jatkokehitysideat
- Käyttäjä voi pyytää vihjeitä keskeneräiseen sudokuun
- Käyttäjä voi lisätä peliin sudokuja. Sovellus lukee käyttäjän lisäämät uudet sudokupelit tiedostosta.
