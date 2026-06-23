from pathlib import Path
from typing import Any

from app import SocialNetworkApp


DATASET_ROOT = Path(__file__).resolve().parent / "dataset"


def ispisi_meni() -> None:
    print("\n" + "=" * 55)
    print("                 DRUSTVENA MREZA")
    print("=" * 55)
    print(" 1. Pretraga korisnika po korisnickom imenu")
    print(" 2. Pretraga korisnika po recima iz biografije")
    print(" 3. Prikaz najuticajnijih korisnika")
    print(" 4. Dodavanje nove follow veze")
    print(" 5. Prikaz istorije interakcija korisnika")
    print(" 6. Autocomplete korisnickog imena")
    print(" 7. Hibridne preporuke korisnika")
    print(" 8. BFS - prikaz nivoa konekcija")
    print(" 9. Did you mean - predlog slicnih imena")
    print("10. Dodavanje novog korisnika")
    print(" 0. Izlazak iz programa")
    print("-" * 55)


def izaberi_skup_podataka() -> str:
    available = {"1": "small", "2": "medium", "3": "full"}

    while True:
        print("Izaberite skup podataka:")
        print("1. Small  (preporucen za razvoj)")
        print("2. Medium (preporucen za demonstraciju)")
        print("3. Full   (provera performansi)")
        choice = input("Izbor: ").strip()

        if choice in available:
            return available[choice]

        print("Neispravan izbor. Pokusajte ponovo.\n")


def ucitaj_pozitivan_ceo_broj(prompt: str, podrazumevano: int | None = None) -> int:
    while True:
        raw_value = input(prompt).strip()
        if not raw_value and podrazumevano is not None:
            return podrazumevano

        try:
            value = int(raw_value)
            if value > 0:
                return value
        except ValueError:
            pass

        print("Unesite ceo broj veci od nule.")


def ucitaj_alfu() -> float:
    while True:
        raw_value = input("Alpha [0-1, podrazumevano 0.5]: ").strip()
        if not raw_value:
            return 0.5

        try:
            alpha = float(raw_value)
            if 0.0 <= alpha <= 1.0:
                return alpha
        except ValueError:
            pass

        print("Alpha mora biti broj izmedju 0 i 1.")


def ispisi_rezultat(result: Any) -> None:
    if result is None:
        print("Funkcionalnost jos nije implementirana.")
        return

    if isinstance(result, dict):
        if not result:
            print("Nema rezultata.")
            return
        for key, value in result.items():
            print(f"{key}: {value}")
        return

    if isinstance(result, (list, tuple, set)):
        if not result:
            print("Nema rezultata.")
            return
        for item in result:
            print(item)
        return

    print(result)


def pokreni_meni(aplikacija: SocialNetworkApp) -> None:
    while True:
        ispisi_meni()
        izbor = input("Izaberite opciju: ").strip()

        if izbor == "1":
            tekst_pretrage = input("Korisnicko ime: ").strip()
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj rezultata [10]: ", podrazumevano=10)
            ispisi_rezultat(aplikacija.pretrazi_po_korisnickom_imenu(tekst_pretrage, ogranicenje))

        elif izbor == "2":
            tekst_pretrage = input("Reci iz biografije: ").strip()
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj rezultata [10]: ", podrazumevano=10)
            ispisi_rezultat(aplikacija.pretrazi_po_biografiji(tekst_pretrage, ogranicenje))

        elif izbor == "3":
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj korisnika [10]: ", podrazumevano=10)
            ispisi_rezultat(aplikacija.pronadji_najuticajnije_korisnike(ogranicenje))

        elif izbor == "4":
            id_pratioca = ucitaj_pozitivan_ceo_broj("ID korisnika koji prati: ")
            id_pracenog = ucitaj_pozitivan_ceo_broj("ID korisnika koji ce biti pracen: ")
            ispisi_rezultat(aplikacija.dodaj_pracenje(id_pratioca, id_pracenog))

        elif izbor == "5":
            id_korisnika = ucitaj_pozitivan_ceo_broj("ID korisnika: ")
            ispisi_rezultat(aplikacija.pronadji_istoriju_interakcija(id_korisnika))

        elif izbor == "6":
            prefiks = input("Pocetak korisnickog imena: ").strip()
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj predloga [5]: ", podrazumevano=5)
            ispisi_rezultat(aplikacija.automatski_dovrsi(prefiks, ogranicenje))

        elif izbor == "7":
            id_korisnika = ucitaj_pozitivan_ceo_broj("ID korisnika: ")
            alfa = ucitaj_alfu()
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj preporuka [10]: ", podrazumevano=10)
            ispisi_rezultat(aplikacija.preporuci_korisnike(id_korisnika, alfa, ogranicenje))

        elif izbor == "8":
            id_korisnika = ucitaj_pozitivan_ceo_broj("ID pocetnog korisnika: ")
            maksimalni_nivo = ucitaj_pozitivan_ceo_broj("Maksimalni nivo: ")
            ispisi_rezultat(aplikacija.pronadji_nivoe_konekcija(id_korisnika, maksimalni_nivo))

        elif izbor == "9":
            korisnicko_ime = input("Pogresno uneto korisnicko ime: ").strip()
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj predloga [5]: ", podrazumevano=5)
            ispisi_rezultat(aplikacija.predlozi_slicna_imena(korisnicko_ime, ogranicenje))

        elif izbor == "10":
            id_korisnika = ucitaj_pozitivan_ceo_broj("ID novog korisnika: ")
            korisnicko_ime = input("Korisnicko ime: ").strip()
            biografija = input("Biografija: ").strip()
            ispisi_rezultat(aplikacija.dodaj_korisnika(id_korisnika, korisnicko_ime, biografija))

        elif izbor == "0":
            print("Dovidjenja!")
            break

        else:
            print("Neispravna opcija. Pokusajte ponovo.")


def glavna() -> None:
    dataset_size = izaberi_skup_podataka()
    dataset_path = DATASET_ROOT / dataset_size

    aplikacija = SocialNetworkApp()
    aplikacija.ucitaj_skup_podataka(dataset_path)
    pokreni_meni(aplikacija)


if __name__ == "__main__":
    glavna()
