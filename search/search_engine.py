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

    def pretrazi_po_korisnickom_imenu(self, tekst_pretrage, pagerank_rezultati=None, ogranicenje=10):
        # TODO: Bice dovrseno u celini za kompletnu pretragu korisnika.
        return []

    def pretrazi_po_biografiji(self, tekst_pretrage, pagerank_rezultati=None, ogranicenje=10):
        trazene_reci = podeli_na_reci(tekst_pretrage)
        if not trazene_reci:
            return []

        pronadjeni_id_korisnika = set()
        for rec in trazene_reci:
            pronadjeni_id_korisnika.update(self.invertovani_indeks.get(rec, set()))

        rezultati = []
        for id_korisnika in pronadjeni_id_korisnika:
            korisnik = self.graf.pronadji_korisnika(id_korisnika)
            if korisnik is not None:
                rezultati.append(korisnik)

        rezultati.sort(key=lambda korisnik: korisnik.username.lower())
        return rezultati[:ogranicenje]
