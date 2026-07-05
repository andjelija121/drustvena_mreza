import heapq

from algoritmi.pagerank import izracunaj_personalizovani_pagerank
from pomocno.obrada_teksta import podeli_na_reci


class Preporucivac:

    def __init__(self, graf):
        self.graf = graf

    def izracunaj_jaccard_slicnost(
        self, prva_biografija, druga_biografija
    ):
        prve_reci = set(podeli_na_reci(prva_biografija))
        druge_reci = set(podeli_na_reci(druga_biografija))
        unija = prve_reci | druge_reci

        if not unija:
            return 0.0

        return len(prve_reci & druge_reci) / len(unija)

    def preporuci(
        self, id_korisnika, alfa=0.5, limit=10
    ):
        if not 0.0 <= alfa <= 1.0:
            raise ValueError("Alfa mora biti izmedju 0 i 1.")
        if limit <= 0 or not self.graf.korisnik_postoji(id_korisnika):
            return []

        pocetni_korisnik = self.graf.pronadji_korisnika(id_korisnika)
        ppr_rezultati = izracunaj_personalizovani_pagerank(
            self.graf,
            id_korisnika,
        )

        iskljuceni = (
            {id_korisnika}
            | set(self.graf.pronadji_pracene(id_korisnika))
            | set(self.graf.blokirao.get(id_korisnika, set()))
            | set(self.graf.blokiran_od.get(id_korisnika, set()))
        )

        rangirani = []
        for id_kandidata, kandidat in self.graf.korisnici_po_id.items():
            if id_kandidata in iskljuceni:
                continue

            ppr = ppr_rezultati.get(id_kandidata, 0.0)
            jaccard = self.izracunaj_jaccard_slicnost(
                pocetni_korisnik.bio,
                kandidat.bio,
            )
            rezultat = alfa * ppr + (1.0 - alfa) * jaccard

            rangirani.append(
                (rezultat, ppr, jaccard, -id_kandidata, kandidat)
            )

        najbolji = heapq.nlargest(limit, rangirani)
        return [
            (kandidat, rezultat, ppr, jaccard)
            for rezultat, ppr, jaccard, _negativan_id, kandidat in najbolji
        ]
