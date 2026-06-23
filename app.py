from data_access.loader import ucitaj_skup_podataka
from search.search_engine import Pretrazivac


class SocialNetworkApp:

    def __init__(self):
        self.graf = None
        self.pretrazivac = None

    def ucitaj_skup_podataka(self, putanja_do_skupa):
        self.graf = ucitaj_skup_podataka(putanja_do_skupa)
        self.pretrazivac = Pretrazivac(self.graf)

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
        pass

    def dodaj_pracenje(self, id_pratioca, id_pracenog):
        pass

    def pronadji_istoriju_interakcija(self, id_korisnika):
        pass

    def automatski_dovrsi(self, prefiks, ogranicenje=5):
        pass

    def preporuci_korisnike(self, id_korisnika, alfa, ogranicenje=10):
        pass

    def pronadji_nivoe_konekcija(self, id_korisnika, maksimalni_nivo):
        pass

    def predlozi_slicna_imena(self, korisnicko_ime, ogranicenje=5):
        pass

    def dodaj_korisnika(self, id_korisnika, korisnicko_ime, biografija):
        pass
