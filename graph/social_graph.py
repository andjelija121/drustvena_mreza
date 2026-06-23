from models.user import User


class SocialGraph:

    def __init__(self) -> None:
        self.korisnici_po_id: dict[int, User] = {}
        self.korisnici_po_username: dict[str, User] = {}
        self.prati: dict[int, set[int]] = {}
        self.pratioci: dict[int, set[int]] = {}
        self.izlazni_stepen: dict[int, int] = {}
        self.blokirao: dict[int, set[int]] = {}
        self.blokiran_od: dict[int, set[int]] = {}
        self.pagerank: dict[int, float] = {}
        self.istorija: list[tuple[int, int]] = []

    def dodaj_korisnika(self, korisnik: User) -> None:
        self.korisnici_po_id[korisnik.id] = korisnik
        self.korisnici_po_username[korisnik.username.lower()] = korisnik
        self.prati.setdefault(korisnik.id, set())
        self.pratioci.setdefault(korisnik.id, set())
        self.izlazni_stepen.setdefault(korisnik.id, 0)
        self.blokirao.setdefault(korisnik.id, set())
        self.blokiran_od.setdefault(korisnik.id, set())

    def dodaj_pracenje(self, id_pratioca: int, id_pracenog: int) -> bool:
        if id_pratioca not in self.korisnici_po_id or id_pracenog not in self.korisnici_po_id:
            return False

        if id_pratioca == id_pracenog:
            return False

        if id_pracenog in self.prati.setdefault(id_pratioca, set()):
            return False

        self.prati[id_pratioca].add(id_pracenog)
        self.pratioci.setdefault(id_pracenog, set()).add(id_pratioca)
        self.izlazni_stepen[id_pratioca] = len(self.prati[id_pratioca])
        return True

    def dodaj_blokiranje(self, id_blokera: int, id_blokiranog: int) -> None:
        if id_blokera not in self.korisnici_po_id or id_blokiranog not in self.korisnici_po_id:
            return

        self.blokirao.setdefault(id_blokera, set()).add(id_blokiranog)
        self.blokiran_od.setdefault(id_blokiranog, set()).add(id_blokera)

    def pronadji_korisnika(self, id_korisnika: int) -> User | None:
        return self.korisnici_po_id.get(id_korisnika)

    def pronadji_korisnika_po_imenu(self, korisnicko_ime: str) -> User | None:
        return self.korisnici_po_username.get(korisnicko_ime.lower())

    def pronadji_pracene(self, id_korisnika: int) -> set[int]:
        return self.prati.get(id_korisnika, set())

    def pronadji_pratioce(self, id_korisnika: int) -> set[int]:
        return self.pratioci.get(id_korisnika, set())

    def pronadji_izlazni_stepen(self, id_korisnika: int) -> int:
        return self.izlazni_stepen.get(id_korisnika, 0)

    def postoji_blokiranje(self, id_prvog_korisnika: int, id_drugog_korisnika: int) -> bool:
        return (
            id_drugog_korisnika in self.blokirao.get(id_prvog_korisnika, set())
            or id_prvog_korisnika in self.blokirao.get(id_drugog_korisnika, set())
        )

    def pronadji_istoriju_interakcija(self, id_korisnika: int) -> list:
        # TODO: Bice dovrseno u celini za istoriju interakcija.
        return []

    def bfs_nivoi(self, pocetni_id: int, maksimalni_nivo: int) -> dict[int, list[int]]:
        # TODO: Bice implementirano u celini za BFS.
        return {}
