# Ohjelmistotekniikka

Tämä repositorio sisältää sekä **laskarit** että *harjoitustyön* kurssia Ohjelmistotekniikka varten.

## Harjoitustyö: sudoku
### Uusin release
[release viikko 5](https://github.com/jnnhan/ot-sudoku/releases/tag/viikko5)

### Dokumentaatio
[vaatimusmaarittely](https://github.com/jnnhan/ot-sudoku/blob/main/dokumentaatio/vaatimusmaarittely.md)

[tuntikirjanpito](https://github.com/jnnhan/ot-sudoku/blob/main/dokumentaatio/tuntikirjanpito.md)

[changelog](https://github.com/jnnhan/ot-sudoku/blob/main/dokumentaatio/changelog.md)

[arkkitehtuuri](https://github.com/jnnhan/ot-sudoku/blob/main/dokumentaatio/arkkitehtuuri.md)


## Huomioita
Sovellus on tehty ja testattu käyttäen python-versiota `3.8` sekä poetry-versiota `1.4.1`. Erityisesti vanhempien poetry-versioiden kanssa voi tulla ongelmia.
 
### Asennus
1. Kloonaa repositorio ja asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Suorita alustustoimenpiteet (tietokannan ja sudokujen haku) komennoilla:

```bash
poetry run invoke init
```

### Aloitus
Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

### Testaus

Sovelluksen testit käynnistyvät komennolla:

```bash
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin voi luoda komennolla:

```bash
poetry run invoke coverage-report
```

Raportti löytyy sovelluksen juurihakemistosta *htmlcov*-hakemistosta. Graafinen raportti löytyy tiedostosta *index.html*



## Sudokujen lisäys sovellukseen
_src_-hakemistossa on kolme tekstitiedostoa eri tasoisille sudokuille: _easy.txt_, _medium.txt_ ja _hard.txt_. Uuden sudokun voi lisätä tiedostoon syöttämällä järjestyksessä ja allekkain kaikki sudokun yhdeksän riviä. Kymmenes rivi aloitetaan pisteellä, jonka jälkeen kirjoitetaan sudokun nimi. Seuraava sudoku syötetään suoraan edellisen perään.
Esimerkki:

```bash
100020058
960100007
028640000
000000000
005002013
007390006
032800000
700400862
800000405
.medium
```

Uudet sudokut luetaan ja tallennetaan tietokantaan komennolla
```bash
poetry run invoke read-sudokus
