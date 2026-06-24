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


def ucitaj_neprazan_tekst(prompt: str) -> str:
    while True:
        vrednost = input(prompt).strip()
        if vrednost:
            return vrednost
        print("Unos ne sme biti prazan.")


def formatiraj_korisnika(korisnik: Any, pagerank: float | None = None) -> str:
    osnovno = f"{korisnik.username} (ID: {korisnik.id})"
    if pagerank is not None:
        osnovno += f" | PageRank: {pagerank:.8f}"
    return osnovno


def ispisi_korisnike(
    korisnici: list,
    aplikacija: SocialNetworkApp,
    prikazi_biografiju: bool = False,
) -> None:
    if not korisnici:
        print("Nema rezultata za zadati upit.")
        return

    for pozicija, korisnik in enumerate(korisnici, start=1):
        pagerank = aplikacija.graf.pagerank.get(korisnik.id, 0.0)
        print(f"{pozicija}. {formatiraj_korisnika(korisnik, pagerank)}")
        if prikazi_biografiju:
            print(f"   Bio: {korisnik.bio}")


def ispisi_najuticajnije(rezultati: list) -> None:
    if not rezultati:
        print("Nema korisnika za prikaz.")
        return

    for pozicija, (korisnik, pagerank) in enumerate(rezultati, start=1):
        print(f"{pozicija}. {formatiraj_korisnika(korisnik, pagerank)}")


def ispisi_tekstualne_predloge(
    predlozi: list[str],
    aplikacija: SocialNetworkApp,
) -> None:
    if not predlozi:
        print("Nema odgovarajucih predloga.")
        return

    for pozicija, korisnicko_ime in enumerate(predlozi, start=1):
        korisnik = aplikacija.graf.pronadji_korisnika_po_imenu(korisnicko_ime)
        pagerank = (
            aplikacija.graf.pagerank.get(korisnik.id, 0.0)
            if korisnik is not None
            else 0.0
        )
        print(f"{pozicija}. {korisnicko_ime} | PageRank: {pagerank:.8f}")


def ispisi_nivoe_konekcija(
    nivoi: dict[str, list],
    aplikacija: SocialNetworkApp,
) -> None:
    if not nivoi:
        print("Nema dostiznih korisnika do zadatog nivoa.")
        return

    for naziv_nivoa, korisnici in nivoi.items():
        print(f"\n{naziv_nivoa}:")
        for korisnik in korisnici:
            pagerank = aplikacija.graf.pagerank.get(korisnik.id, 0.0)
            print(f"  - {formatiraj_korisnika(korisnik, pagerank)}")


def ispisi_istoriju_interakcija(istorija: list[dict] | None) -> None:
    if istorija is None:
        print("Korisnik sa unetim ID-jem ne postoji.")
        return

    if not istorija:
        print("Korisnik nema evidentiranih interakcija.")
        return

    for dogadjaj in istorija:
        redni_broj = dogadjaj["redni_broj"]
        drugi_id = dogadjaj["drugi_korisnik_id"]
        drugi_username = dogadjaj["drugi_korisnik_username"]

        if dogadjaj["smer"] == "zapratio":
            print(
                f"{redni_broj}. Zapratio/la korisnika "
                f"{drugi_username} (ID: {drugi_id})."
            )
        else:
            print(
                f"{redni_broj}. Korisnik {drugi_username} "
                f"(ID: {drugi_id}) ga/ju je zapratio."
            )


def ispisi_preporuke(preporuke: list) -> None:
    if not preporuke:
        print("Nema preporuka za ovog korisnika.")
        return

    for pozicija, (korisnik, rezultat, ppr, jaccard) in enumerate(
        preporuke,
        start=1,
    ):
        print(
            f"{pozicija}. {korisnik.username} (ID: {korisnik.id}) | "
            f"rezultat={rezultat:.6f}, PPR={ppr:.6f}, "
            f"Jaccard={jaccard:.6f}"
        )


def pokreni_meni(aplikacija: SocialNetworkApp) -> None:
    while True:
        ispisi_meni()
        izbor = input("Izaberite opciju: ").strip()

        if izbor == "1":
            tekst_pretrage = ucitaj_neprazan_tekst("Korisnicko ime: ")
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj rezultata [10]: ", podrazumevano=10)
            ispisi_korisnike(
                aplikacija.pretrazi_po_korisnickom_imenu(tekst_pretrage, ogranicenje),
                aplikacija,
            )

        elif izbor == "2":
            tekst_pretrage = ucitaj_neprazan_tekst("Reci iz biografije: ")
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj rezultata [10]: ", podrazumevano=10)
            ispisi_korisnike(
                aplikacija.pretrazi_po_biografiji(tekst_pretrage, ogranicenje),
                aplikacija,
                prikazi_biografiju=True,
            )

        elif izbor == "3":
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj korisnika [10]: ", podrazumevano=10)
            ispisi_najuticajnije(
                aplikacija.pronadji_najuticajnije_korisnike(ogranicenje)
            )

        elif izbor == "4":
            id_pratioca = ucitaj_pozitivan_ceo_broj("ID korisnika koji prati: ")
            id_pracenog = ucitaj_pozitivan_ceo_broj("ID korisnika koji ce biti pracen: ")
            greska = aplikacija.validiraj_pracenje(id_pratioca, id_pracenog)
            if greska is not None:
                print(f"Veza nije dodata: {greska}")
            elif aplikacija.dodaj_pracenje(id_pratioca, id_pracenog):
                print(f"Veza od {id_pratioca} do {id_pracenog} je uspesno dodata.")
            else:
                print("Veza nije dodata zbog neocekivane greske.")

        elif izbor == "5":
            id_korisnika = ucitaj_pozitivan_ceo_broj("ID korisnika: ")
            ispisi_istoriju_interakcija(
                aplikacija.pronadji_istoriju_interakcija(id_korisnika)
            )

        elif izbor == "6":
            prefiks = ucitaj_neprazan_tekst("Pocetak korisnickog imena: ")
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj predloga [5]: ", podrazumevano=5)
            ispisi_tekstualne_predloge(
                aplikacija.automatski_dovrsi(prefiks, ogranicenje),
                aplikacija,
            )

        elif izbor == "7":
            id_korisnika = ucitaj_pozitivan_ceo_broj("ID korisnika: ")
            alfa = ucitaj_alfu()
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj preporuka [10]: ", podrazumevano=10)
            if not aplikacija.graf.korisnik_postoji(id_korisnika):
                print(f"Korisnik sa ID-jem {id_korisnika} ne postoji.")
            else:
                ispisi_preporuke(
                    aplikacija.preporuci_korisnike(
                        id_korisnika,
                        alfa,
                        ogranicenje,
                    )
                )

        elif izbor == "8":
            id_korisnika = ucitaj_pozitivan_ceo_broj("ID pocetnog korisnika: ")
            maksimalni_nivo = ucitaj_pozitivan_ceo_broj("Maksimalni nivo: ")
            if not aplikacija.graf.korisnik_postoji(id_korisnika):
                print(f"Korisnik sa ID-jem {id_korisnika} ne postoji.")
            else:
                ispisi_nivoe_konekcija(
                    aplikacija.pronadji_nivoe_konekcija(
                        id_korisnika,
                        maksimalni_nivo,
                    ),
                    aplikacija,
                )

        elif izbor == "9":
            korisnicko_ime = ucitaj_neprazan_tekst(
                "Pogresno uneto korisnicko ime: "
            )
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj predloga [5]: ", podrazumevano=5)
            if aplikacija.graf.pronadji_korisnika_po_imenu(korisnicko_ime):
                print("Uneto korisnicko ime vec postoji; predlog nije potreban.")
            else:
                ispisi_tekstualne_predloge(
                    aplikacija.predlozi_slicna_imena(
                        korisnicko_ime,
                        ogranicenje,
                    ),
                    aplikacija,
                )

        elif izbor == "10":
            id_korisnika = ucitaj_pozitivan_ceo_broj("ID novog korisnika: ")
            korisnicko_ime = ucitaj_neprazan_tekst("Korisnicko ime: ")
            biografija = input("Biografija: ").strip()
            greska = aplikacija.validiraj_novog_korisnika(
                id_korisnika,
                korisnicko_ime,
            )
            if greska is not None:
                print(f"Korisnik nije dodat: {greska}")
            elif aplikacija.dodaj_korisnika(id_korisnika, korisnicko_ime, biografija):
                print(f"Korisnik {korisnicko_ime} je uspesno dodat.")
            else:
                print("Korisnik nije dodat zbog neocekivane greske.")

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
    try:
        glavna()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram je prekinut. Dovidjenja!")
