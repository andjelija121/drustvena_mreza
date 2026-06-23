import heapq

from utils.text_processing import podeli_na_reci


class Pretrazivac:

    def __init__(self, graf):
        self.graf = graf
        self.invertovani_indeks = {}
        self.napravi_invertovani_indeks()

    def napravi_invertovani_indeks(self):
        self.invertovani_indeks = {}

        for id_korisnika in self.graf.korisnici_po_id:
            self.dodaj_korisnika_u_indeks(id_korisnika)

    def dodaj_korisnika_u_indeks(self, id_korisnika):
        korisnik = self.graf.pronadji_korisnika(id_korisnika)
        if korisnik is None:
            return

        for rec in korisnik.bio_words:
            self.invertovani_indeks.setdefault(rec, set()).add(id_korisnika)

    def izracunaj_relevantnost_korisnickog_imena(self, korisnik, tekst_pretrage):
        korisnicko_ime = korisnik.username.lower()
        tekst_pretrage = tekst_pretrage.lower().strip()

        if tekst_pretrage and korisnicko_ime == tekst_pretrage:
            return 10
        if tekst_pretrage and korisnicko_ime.startswith(tekst_pretrage):
            return 7
        if tekst_pretrage and tekst_pretrage in korisnicko_ime:
            return 5
        return 0

    def izracunaj_relevantnost_biografije(self, korisnik, trazene_reci):
        reci_biografije = set(korisnik.bio_words)
        broj_poklapanja = 0

        for rec in trazene_reci:
            if rec in reci_biografije:
                broj_poklapanja += 1

        return broj_poklapanja * 2

    def pretrazi_po_korisnickom_imenu(self, tekst_pretrage, pagerank_rezultati=None, ogranicenje=10):
        tekst_pretrage = tekst_pretrage.lower().strip()
        if not tekst_pretrage:
            return []

        if pagerank_rezultati is None:
            pagerank_rezultati = {}

        rangirani_kandidati = []
        for id_korisnika, korisnik in self.graf.korisnici_po_id.items():
            relevantnost = self.izracunaj_relevantnost_korisnickog_imena(
                korisnik,
                tekst_pretrage,
            )
            if relevantnost == 0:
                continue

            pagerank = pagerank_rezultati.get(id_korisnika, 0)
            rangirani_kandidati.append((relevantnost, pagerank, -id_korisnika, korisnik))

        najbolji = heapq.nlargest(ogranicenje, rangirani_kandidati)
        return [korisnik for relevantnost, pagerank, negativan_id, korisnik in najbolji]

    def pretrazi_po_biografiji(self, tekst_pretrage, pagerank_rezultati=None, ogranicenje=10):
        trazene_reci = podeli_na_reci(tekst_pretrage)
        if not trazene_reci:
            return []

        pronadjeni_id_korisnika = set()
        for rec in trazene_reci:
            pronadjeni_id_korisnika.update(self.invertovani_indeks.get(rec, set()))

        rangirani_kandidati = []
        if pagerank_rezultati is None:
            pagerank_rezultati = {}

        for id_korisnika in pronadjeni_id_korisnika:
            korisnik = self.graf.pronadji_korisnika(id_korisnika)
            if korisnik is not None:
                relevantnost = self.izracunaj_relevantnost_biografije(
                    korisnik,
                    trazene_reci,
                )
                pagerank = pagerank_rezultati.get(id_korisnika, 0)
                rangirani_kandidati.append((relevantnost, pagerank, -id_korisnika, korisnik))

        najbolji = heapq.nlargest(ogranicenje, rangirani_kandidati)
        return [korisnik for relevantnost, pagerank, negativan_id, korisnik in najbolji]
