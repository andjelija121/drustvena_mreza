from algorithms.pagerank import (
    izracunaj_pagerank,
    pronadji_najbolje_korisnike,
)
from data_access.loader import ucitaj_skup_podataka
from models.user import User
from recommendations.recommender import Recommender
from search.search_engine import Pretrazivac
from structures.trie import Trie


class SocialNetworkApp:

    def __init__(self):
        self.graf = None
        self.pretrazivac = None
        self.recommender = None
        self.trie = Trie()

    def ucitaj_skup_podataka(self, putanja_do_skupa):
        self.graf = ucitaj_skup_podataka(putanja_do_skupa)
        self.graf.pagerank = izracunaj_pagerank(self.graf)
        self.pretrazivac = Pretrazivac(self.graf)
        self.recommender = Recommender(self.graf)
        self.trie = Trie()
        for korisnik in self.graf.korisnici_po_id.values():
            self.trie.dodaj(korisnik.username, korisnik.id)

    def _osvezi_pagerank(self):
        if self.graf is None:
            return

        self.graf.pagerank = izracunaj_pagerank(
            self.graf,
            pocetni_rezultati=self.graf.pagerank,
        )

    def pretrazi_po_korisnickom_imenu(self, tekst_pretrage, ogranicenje=10):
        if self.pretrazivac is None or self.graf is None:
            return []

        return self.pretrazivac.pretrazi_po_korisnickom_imenu(
            tekst_pretrage,
            self.graf.pagerank,
            ogranicenje,
        )

    def pretrazi_po_biografiji(self, tekst_pretrage, ogranicenje=10):
        if self.pretrazivac is None:
            return []

        return self.pretrazivac.pretrazi_po_biografiji(
            tekst_pretrage,
            self.graf.pagerank,
            ogranicenje,
        )

    def pronadji_najuticajnije_korisnike(self, ogranicenje=10):
        if self.graf is None:
            return []

        najbolji = pronadji_najbolje_korisnike(
            self.graf.pagerank,
            ogranicenje,
        )
        return [
            (self.graf.pronadji_korisnika(id_korisnika), rezultat)
            for id_korisnika, rezultat in najbolji
        ]

    def dodaj_pracenje(self, id_pratioca, id_pracenog):
        if self.graf is None:
            return False

        uspesno = self.graf.dodaj_pracenje(id_pratioca, id_pracenog)
        if uspesno:
            self._osvezi_pagerank()
        return uspesno

    def pronadji_istoriju_interakcija(self, id_korisnika):
        if self.graf is None:
            return None

        return self.graf.pronadji_istoriju_interakcija(id_korisnika)

    def automatski_dovrsi(self, prefiks, ogranicenje=5):
        if self.graf is None:
            return []

        return self.trie.automatski_dovrsi(
            prefiks,
            self.graf.pagerank,
            ogranicenje,
        )

    def preporuci_korisnike(self, id_korisnika, alfa, ogranicenje=10):
        if self.recommender is None:
            return []

        return self.recommender.preporuci(
            id_korisnika,
            alfa,
            ogranicenje,
        )

    def pronadji_nivoe_konekcija(self, id_korisnika, maksimalni_nivo):
        pass

    def predlozi_slicna_imena(self, korisnicko_ime, ogranicenje=5):
        pass

    def dodaj_korisnika(self, id_korisnika, korisnicko_ime, biografija):
        if self.graf is None or self.pretrazivac is None:
            return False

        korisnicko_ime = korisnicko_ime.strip()
        if (
            not korisnicko_ime
            or self.graf.korisnik_postoji(id_korisnika)
            or self.graf.pronadji_korisnika_po_imenu(korisnicko_ime) is not None
        ):
            return False

        korisnik = User(id_korisnika, korisnicko_ime, biografija)
        self.graf.dodaj_korisnika(korisnik)
        self.pretrazivac.dodaj_korisnika_u_indeks(id_korisnika)
        self.trie.dodaj(korisnicko_ime, id_korisnika)
        self._osvezi_pagerank()
        return True
