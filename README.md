# Ohjelmistotekniikka

Tämä repositorio sisältää sekä **laskarit** että *harjoitustyön* kurssia Ohjelmistotekniikka varten.

## Harjoitustyö: sudoku
### Dokumentaatio
[vaatimusmaarittely](https://github.com/jnnhan/ot-sudoku/blob/main/dokumentaatio/vaatimusmaarittely.md)

[tuntikirjanpito](https://github.com/jnnhan/ot-sudoku/blob/main/dokumentaatio/tuntikirjanpito.md)

[changelog](https://github.com/jnnhan/ot-sudoku/blob/main/dokumentaatio/changelog.md)


## Huomioita
Sovellus on tehty ja testattu käyttäen python-versiota `3.8` sekä poetry-versiota `1.4.1`. Erityisesti vanhempien poetry-versioiden kanssa voi tulla ongelmia.
 
### Asennus
1. Kloonaa repositorio ja asenna riippuvuudet komennolla:

```bash
poetry install
```

2. Suorita alustustoimenpiteet (mm. tietokannan luonti) komennolla:

```bash
poetry run invoke init
```

3. Käynnistä sovellus komennolla:

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

