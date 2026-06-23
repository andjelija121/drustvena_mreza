class SocialGraph:

    def __init__(self):
        self.korisnici_po_id = {}
        self.korisnici_po_username = {}
        self.prati = {}
        self.pratioci = {}
        self.izlazni_stepen = {}
        self.blokirao = {}
        self.blokiran_od = {}
        self.pagerank = {}
        self.istorija = []
        self.sledeci_redni_broj_dogadjaja = 1

    def dodaj_korisnika(self, korisnik):
        self.korisnici_po_id[korisnik.id] = korisnik
        self.korisnici_po_username[korisnik.username.lower()] = korisnik
        self.prati.setdefault(korisnik.id, set())
        self.pratioci.setdefault(korisnik.id, set())
        self.izlazni_stepen.setdefault(korisnik.id, 0)
        self.blokirao.setdefault(korisnik.id, set())
        self.blokiran_od.setdefault(korisnik.id, set())

    def dodaj_pracenje(self, id_pratioca, id_pracenog, evidentiraj=True):
        if id_pratioca not in self.korisnici_po_id or id_pracenog not in self.korisnici_po_id:
            return False

        if id_pratioca == id_pracenog:
            return False

        if self.postoji_blokiranje(id_pratioca, id_pracenog):
            return False

        if id_pracenog in self.prati.setdefault(id_pratioca, set()):
            return False

        self.prati[id_pratioca].add(id_pracenog)
        self.pratioci.setdefault(id_pracenog, set()).add(id_pratioca)
        self.izlazni_stepen[id_pratioca] = len(self.prati[id_pratioca])

        if evidentiraj:
            self.istorija.append(
                {
                    "redni_broj": self.sledeci_redni_broj_dogadjaja,
                    "tip": "pracenje",
                    "id_pratioca": id_pratioca,
                    "id_pracenog": id_pracenog,
                }
            )
            self.sledeci_redni_broj_dogadjaja += 1

        return True

    def dodaj_blokiranje(self, id_blokera, id_blokiranog):
        if id_blokera not in self.korisnici_po_id or id_blokiranog not in self.korisnici_po_id:
            return

        self.blokirao.setdefault(id_blokera, set()).add(id_blokiranog)
        self.blokiran_od.setdefault(id_blokiranog, set()).add(id_blokera)

    def korisnik_postoji(self, id_korisnika):
        return id_korisnika in self.korisnici_po_id

    def pronadji_korisnika(self, id_korisnika):
        return self.korisnici_po_id.get(id_korisnika)

    def pronadji_korisnika_po_imenu(self, korisnicko_ime):
        return self.korisnici_po_username.get(korisnicko_ime.lower())

    def pronadji_pracene(self, id_korisnika):
        return self.prati.get(id_korisnika, set())

    def pronadji_pratioce(self, id_korisnika):
        return self.pratioci.get(id_korisnika, set())

    def pronadji_izlazni_stepen(self, id_korisnika):
        return self.izlazni_stepen.get(id_korisnika, 0)

    def postoji_blokiranje(self, id_prvog_korisnika, id_drugog_korisnika):
        return (
            id_drugog_korisnika in self.blokirao.get(id_prvog_korisnika, set())
            or id_prvog_korisnika in self.blokirao.get(id_drugog_korisnika, set())
        )

    def prikazi_informacije_o_korisniku(self, id_korisnika):
        korisnik = self.pronadji_korisnika(id_korisnika)
        if korisnik is None:
            return None

        return {
            "id": korisnik.id,
            "username": korisnik.username,
            "bio": korisnik.bio,
            "broj_pracenih": len(self.pronadji_pracene(id_korisnika)),
            "broj_pratilaca": len(self.pronadji_pratioce(id_korisnika)),
            "broj_blokiranih": len(self.blokirao.get(id_korisnika, set())),
            "broj_korisnika_koji_su_ga_blokirali": len(self.blokiran_od.get(id_korisnika, set())),
        }

    def pronadji_istoriju_interakcija(self, id_korisnika):
        if not self.korisnik_postoji(id_korisnika):
            return None

        dogadjaji = []
        for dogadjaj in self.istorija:
            id_pratioca = dogadjaj["id_pratioca"]
            id_pracenog = dogadjaj["id_pracenog"]

            if id_korisnika == id_pratioca:
                drugi_korisnik = self.pronadji_korisnika(id_pracenog)
                smer = "zapratio"
            elif id_korisnika == id_pracenog:
                drugi_korisnik = self.pronadji_korisnika(id_pratioca)
                smer = "zapratio_njega"
            else:
                continue

            dogadjaji.append(
                {
                    **dogadjaj,
                    "smer": smer,
                    "drugi_korisnik_id": drugi_korisnik.id,
                    "drugi_korisnik_username": drugi_korisnik.username,
                }
            )

        return dogadjaji

    def bfs_nivoi(self, pocetni_id, maksimalni_nivo):
        # TODO: Bice implementirano u celini za BFS.
        return {}
