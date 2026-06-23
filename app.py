from pathlib import Path
from typing import Any

from data_access.loader import ucitaj_skup_podataka


class SocialNetworkApp:

    def __init__(self) -> None:
        self.graf = None

    def ucitaj_skup_podataka(self, putanja_do_skupa: Path) -> None:
        self.graf = ucitaj_skup_podataka(putanja_do_skupa)

    def pretrazi_po_korisnickom_imenu(self, upit: str, limit: int = 10) -> Any:
        pass

    def pretrazi_po_biografiji(self, upit: str, limit: int = 10) -> Any:
        pass

    def pronadji_najuticajnije_korisnike(self, limit: int = 10) -> Any:
        pass

    def dodaj_pracenje(self, id_pratioca: int, id_pracenog: int) -> Any:
        pass

    def pronadji_istoriju_interakcija(self, id_korisnika: int) -> Any:
        pass

    def automatski_dovrsi(self, prefiks: str, limit: int = 5) -> Any:
        pass

    def preporuci_korisnike(self, id_korisnika: int, alfa: float, limit: int = 10) -> Any:
        pass

    def pronadji_nivoe_konekcija(self, id_korisnika: int, maksimalni_nivo: int) -> Any:
        pass

    def predlozi_slicna_imena(self, korisnicko_ime: str, limit: int = 5) -> Any:
        pass

    def dodaj_korisnika(self, id_korisnika: int, korisnicko_ime: str, biografija: str) -> Any:
        pass
