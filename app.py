from algorithms.pagerank import (
    izracunaj_pagerank,
    pronadji_najbolje_korisnike,
)
from data_access.loader import ucitaj_skup_podataka
from models.user import User
from recommendations.recommender import Recommender
from search.search_engine import Pretrazivac
from structures.trie import Trie
from utils.suggestions import predlozi_slicna_imena


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

        if self.validiraj_pracenje(id_pratioca, id_pracenog) is not None:
            return False

        uspesno = self.graf.dodaj_pracenje(id_pratioca, id_pracenog)
        if uspesno:
            self._osvezi_pagerank()
        return uspesno

    def validiraj_pracenje(self, id_pratioca, id_pracenog):
        if self.graf is None:
            return "Skup podataka nije ucitan."
        if not self.graf.korisnik_postoji(id_pratioca):
            return f"Korisnik koji prati (ID {id_pratioca}) ne postoji."
        if not self.graf.korisnik_postoji(id_pracenog):
            return f"Korisnik koji treba da bude pracen (ID {id_pracenog}) ne postoji."
        if id_pratioca == id_pracenog:
            return "Korisnik ne moze da prati samog sebe."
        if self.graf.postoji_blokiranje(id_pratioca, id_pracenog):
            return "Veza nije dozvoljena jer izmedju korisnika postoji blokiranje."
        if id_pracenog in self.graf.pronadji_pracene(id_pratioca):
            return "Ova veza pracenja vec postoji."
        return None

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
        if self.graf is None:
            return {}

        nivoi = self.graf.bfs_nivoi(id_korisnika, maksimalni_nivo)
        return {
            f"Nivo {nivo}": [
                self.graf.pronadji_korisnika(id_korisnika)
                for id_korisnika in korisnici
            ]
            for nivo, korisnici in nivoi.items()
        }

    def predlozi_slicna_imena(self, korisnicko_ime, ogranicenje=5):
        if self.graf is None:
            return []

        korisnici = list(self.graf.korisnici_po_id.values())
        pagerank_po_imenu = {
            korisnik.username: self.graf.pagerank.get(korisnik.id, 0.0)
            for korisnik in korisnici
        }
        return predlozi_slicna_imena(
            korisnicko_ime,
            [korisnik.username for korisnik in korisnici],
            ogranicenje,
            pagerank_po_imenu,
        )

    def dodaj_korisnika(self, id_korisnika, korisnicko_ime, biografija):
        if self.graf is None or self.pretrazivac is None:
            return False

        korisnicko_ime = korisnicko_ime.strip()
        if self.validiraj_novog_korisnika(id_korisnika, korisnicko_ime) is not None:
            return False

        korisnik = User(id_korisnika, korisnicko_ime, biografija)
        self.graf.dodaj_korisnika(korisnik)
        self.pretrazivac.dodaj_korisnika_u_indeks(id_korisnika)
        self.trie.dodaj(korisnicko_ime, id_korisnika)
        self._osvezi_pagerank()
        return True

    def validiraj_novog_korisnika(self, id_korisnika, korisnicko_ime):
        if self.graf is None:
            return "Skup podataka nije ucitan."
        if id_korisnika <= 0:
            return "ID korisnika mora biti ceo broj veci od nule."

        korisnicko_ime = korisnicko_ime.strip()
        if not korisnicko_ime:
            return "Korisnicko ime ne sme biti prazno."
        if "|" in korisnicko_ime:
            return "Korisnicko ime ne sme da sadrzi znak |."
        if self.graf.korisnik_postoji(id_korisnika):
            return f"ID {id_korisnika} je vec zauzet."
        if self.graf.pronadji_korisnika_po_imenu(korisnicko_ime) is not None:
            return f"Korisnicko ime '{korisnicko_ime}' je vec zauzeto."
        return None
