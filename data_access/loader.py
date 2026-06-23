from pathlib import Path

from graph.social_graph import SocialGraph
from models.user import User


def ucitaj_korisnike(putanja: Path, graf: SocialGraph) -> None:
    with putanja.open("r", encoding="utf-8") as fajl:
        for linija in fajl:
            linija = linija.strip()
            if not linija:
                continue

            delovi = linija.split("|", 2)
            if len(delovi) != 3:
                continue

            id_korisnika, korisnicko_ime, biografija = delovi
            korisnik = User(int(id_korisnika), korisnicko_ime, biografija)
            graf.dodaj_korisnika(korisnik)


def ucitaj_konekcije(putanja: Path, graf: SocialGraph) -> None:
    with putanja.open("r", encoding="utf-8") as fajl:
        for linija in fajl:
            linija = linija.strip()
            if not linija:
                continue

            delovi = linija.split("|", 1)
            if len(delovi) != 2:
                continue

            id_pratioca, id_pracenog = delovi
            graf.dodaj_pracenje(int(id_pratioca), int(id_pracenog))


def ucitaj_blokiranja(putanja: Path, graf: SocialGraph) -> None:
    with putanja.open("r", encoding="utf-8") as fajl:
        for linija in fajl:
            linija = linija.strip()
            if not linija:
                continue

            delovi = linija.split("|", 1)
            if len(delovi) != 2:
                continue

            id_blokera, id_blokiranog = delovi
            graf.dodaj_blokiranje(int(id_blokera), int(id_blokiranog))


def ucitaj_skup_podataka(putanja_do_skupa: Path) -> SocialGraph:
    graf = SocialGraph()

    ucitaj_korisnike(putanja_do_skupa / "users.txt", graf)
    ucitaj_konekcije(putanja_do_skupa / "connections.txt", graf)
    ucitaj_blokiranja(putanja_do_skupa / "blocked.txt", graf)

    return graf
