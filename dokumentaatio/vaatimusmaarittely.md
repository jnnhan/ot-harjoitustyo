# Vaatimusmäärittely

## Sovelluksen tarkoitus
Sovellus on yksinpelattava sudoku, jossa on valittavissa eri vaikeustasoja. Käyttäjä voittaa pelin, jos onnistuu täyttämään kaikki tyhjät ruudut 9x9 ruudukossa. Peliä ei voi hävitä, mutta sen voi lopettaa kesken.

## Toiminnallisuudet

### Tehty:
#### Ennen kirjautumista
- Käyttäjä voi luoda käyttäjätunnuksen
  - Käyttäjätunnuksen on oltava uniikki ja vähintään 3 merkin mittainen
  - Salasanan on oltava vähintään 4 merkin mittainen
- Käyttäjä voi kirjautua järjestelmään
  - Kirjautuminen onnistuu, jos syötetään olemassaoleva käyttäjätunnus ja sitä vastaava salasana
  - Jos käyttäjätunnus tai salasana on väärä, tai tunnusta ei ole olemassa, annetaan virheilmoitus

#### Kirjautumisen jälkeen
- Käyttäjä voi aloittaa uuden sudokun valitsemallaan vaikeustasolla
- Käyttäjä voi kirjautua ulos sovelluksesta
- Käyttäjä voi lisätä omia sudokuja sovellukseen muokkaamalla tekstitiedostoa
- Käyttäjä näkee tilastoja omista sudokuista
  - ratkaistujen sudokujen lukumäärä

#### Pelaaminen
- Sovellus sisältää eri vaikeustasoisia sudokuja.
- Käyttäjä voi merkata tyhjään ruudukkoon yhden tai useamman numeron
  - Useamman numeron tapauksessa ne näkyvät ruudukon yläreunassa "apunumeroina"
  - Jos ruudukossa on vain yksi numero, se näkyy suurempana keskellä ruudukkoa
- Käyttäjä voi pyyhkiä merkkaamiaan numeroita ruudukoista tai tyhjentää koko pelin
- Jos kaikki ruudukot ovat täynnä ja virheitä ei havaita, peli päättyy
      
### Tekeillä:
### Kirjautumisen jälkeen 
- Jos tietyntasoisia sudokuja on useampi kuin neljä, näytä loput sudokut seuraavalla sivulla
    
    
## Jatkokehitysideat
- Käyttäjä voi pyytää vihjeitä keskeneräiseen sudokuun
- Uusia sudokuja voi lisätä suoraan sovelluksen kautta, jolloin tämän toiminnallisuuden käyttöliittymä on parempi
