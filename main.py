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
        choice = input("Izaberite opciju: ").strip()

        if choice == "1":
            username = input("Korisnicko ime ili deo imena: ").strip()
            limit = ucitaj_pozitivan_ceo_broj("Broj rezultata [10]: ", podrazumevano=10)
            ispisi_rezultat(aplikacija.pretrazi_po_korisnickom_imenu(username, limit))

        elif choice == "2":
            query = input("Reci iz biografije: ").strip()
            limit = ucitaj_pozitivan_ceo_broj("Broj rezultata [10]: ", podrazumevano=10)
            ispisi_rezultat(aplikacija.pretrazi_po_biografiji(query, limit))

        elif choice == "3":
            limit = ucitaj_pozitivan_ceo_broj("Broj korisnika [10]: ", podrazumevano=10)
            ispisi_rezultat(aplikacija.pronadji_najuticajnije_korisnike(limit))

        elif choice == "4":
            follower_id = ucitaj_pozitivan_ceo_broj("ID korisnika koji prati: ")
            followed_id = ucitaj_pozitivan_ceo_broj("ID korisnika koji ce biti pracen: ")
            ispisi_rezultat(aplikacija.dodaj_pracenje(follower_id, followed_id))

        elif choice == "5":
            user_id = ucitaj_pozitivan_ceo_broj("ID korisnika: ")
            ispisi_rezultat(aplikacija.pronadji_istoriju_interakcija(user_id))

        elif choice == "6":
            prefix = input("Pocetak korisnickog imena: ").strip()
            limit = ucitaj_pozitivan_ceo_broj("Broj predloga [5]: ", podrazumevano=5)
            ispisi_rezultat(aplikacija.automatski_dovrsi(prefix, limit))

        elif choice == "7":
            user_id = ucitaj_pozitivan_ceo_broj("ID korisnika: ")
            alpha = ucitaj_alfu()
            limit = ucitaj_pozitivan_ceo_broj("Broj preporuka [10]: ", podrazumevano=10)
            ispisi_rezultat(aplikacija.preporuci_korisnike(user_id, alpha, limit))

        elif choice == "8":
            user_id = ucitaj_pozitivan_ceo_broj("ID pocetnog korisnika: ")
            max_level = ucitaj_pozitivan_ceo_broj("Maksimalni nivo: ")
            ispisi_rezultat(aplikacija.pronadji_nivoe_konekcija(user_id, max_level))

        elif choice == "9":
            username = input("Pogresno uneto korisnicko ime: ").strip()
            limit = ucitaj_pozitivan_ceo_broj("Broj predloga [5]: ", podrazumevano=5)
            ispisi_rezultat(aplikacija.predlozi_slicna_imena(username, limit))

        elif choice == "10":
            user_id = ucitaj_pozitivan_ceo_broj("ID novog korisnika: ")
            username = input("Korisnicko ime: ").strip()
            bio = input("Biografija: ").strip()
            ispisi_rezultat(aplikacija.dodaj_korisnika(user_id, username, bio))

        elif choice == "0":
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
