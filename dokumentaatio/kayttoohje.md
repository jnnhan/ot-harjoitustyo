# Käyttöohje

Lataa sovelluksen viimeisimmän [releasen](https://github.com/jnnhan/ot-sudoku/releases) lähdekoodi (zip-tiedosto).

## Sovelluksen käynnistäminen
1. Projektin purkamisen jälkeen siirry juuri luotuun hakemistoon ja asenna riippuvuudet komennolla:
```bash
poetry install
```
2. Suorita alustustoimenpiteet (tietokantojen ja sudokujen luonti) komennolla:
```bash
poetry run invoke init
```
3. Käynnistä sovellus komennolla:
```bash
poetry run invoke start
```

## Kirjautuminen

Sovellus käynnistyy kirjautumisnäkymään:

![](.kuvat/login.png)

Kirjautuminen tapahtuu syöttämällä olemassaoleva käyttäjätunnus ja sitä vastaava salasana syötekenttiin ja painamalla "Login"-painiketta.

## Käyttäjätunnuksen luominen

Kirjautumisnäkymästä voi siirtyä uuden käyttäjätunnuksen luontiin painamalla "Create a new user"-painiketta. Avautuviin kenttiin syötetään käyttäjätunnus (vähintään 3 merkkiä) ja salasana (vähintään 4 merkkiä), ja painetaan "Register"-painiketta. 

![](.kuvat/register.png)

Jos käyttäjätunnuksen luominen onnistui, sovellus palaa kirjautumisnäkymään.

## Sudokun valinta

Sisäänkirjautumisen onnistuttua siirrytään näkymään, jossa voi valita sudokun vaikeustason:

![](.kuvat/select.png)

Vaikeustason valinnan jälkeen valitaan jokin sudokuista:

![](.kuvat/sudokuselect.png)

## Pelaaminen

Sudokun valinnan jälkeen siirrytään pelinäkymään:

![](.kuvat/play.png)

Mustia numeroita ei voi muuttaa, mutta tyhjiin ruutuihin voi syöttää numeronäppäimillä numeroita. Syöttämällä yhteen ruutuun useamman numeron voi merkitä itselleen apunumeroita, eli ruutuun mahdollisesti tulevia numeroita.

Kaikkien ruutujen ollessa täynnä ja oikein syötettyjä peli päättyy:

![](.kuvat/win.png)

Voiton jälkeen sudokun voi ratkaista uudestaan, tai palata takaisin ja valita toisen sudokun.