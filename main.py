from pathlib import Path

from app import AplikacijaDrustveneMreze


DATASET_ROOT = Path(__file__).resolve().parent / "dataset"


def ispisi_meni():
    print("\n" + "=" * 55)
    print("                 DRUSTVENA MREZA")
    print("=" * 55)
    print(" 1. Nadji korisnika po imenu")
    print(" 2. Pretrazi biografije")
    print(" 3. Najuticajniji korisnici")
    print(" 4. Dodaj pracenje")
    print(" 5. Istorija pracenja")
    print(" 6. Dovrsi korisnicko ime")
    print(" 7. Preporuci korisnike")
    print(" 8. Prikazi nivoe konekcija")
    print(" 9. Predlozi slicno ime")
    print("10. Dodaj korisnika")
    print(" 0. Izlaz")
    print("-" * 55)


def izaberi_skup_podataka():
    available = {"1": "small", "2": "medium", "3": "full"}

    while True:
        print("Izaberite skup podataka:")
        print("1. Mali   (najbrzi za probu)")
        print("2. Srednji (dobar za prikaz rada)")
        print("3. Ceo    (za proveru brzine)")
        choice = input("Izbor: ").strip()

        if choice in available:
            return available[choice]

        print("Nema te opcije, probajte ponovo.\n")


def ucitaj_pozitivan_ceo_broj(prompt, podrazumevano=None):
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

        print("Unesite broj veci od nule.")


def ucitaj_alfu():
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

        print("Alpha mora biti izmedju 0 i 1.")


def ucitaj_neprazan_tekst(prompt):
    while True:
        vrednost = input(prompt).strip()
        if vrednost:
            return vrednost
        print("Unos ne moze biti prazan.")


def formatiraj_korisnika(korisnik, pagerank=None):
    osnovno = f"{korisnik.username} (ID: {korisnik.id})"
    if pagerank is not None:
        osnovno += f" | PageRank: {pagerank:.8f}"
    return osnovno


def ispisi_korisnike(
    korisnici,
    aplikacija,
    prikazi_biografiju=False,
):
    if not korisnici:
        print("Nista nije nadjeno za taj unos.")
        return

    for pozicija, korisnik in enumerate(korisnici, start=1):
        pagerank = aplikacija.graf.pagerank.get(korisnik.id, 0.0)
        print(f"{pozicija}. {formatiraj_korisnika(korisnik, pagerank)}")
        if prikazi_biografiju:
            print(f"   Biografija: {korisnik.bio}")


def ispisi_najuticajnije(rezultati):
    if not rezultati:
        print("Nema korisnika za prikaz.")
        return

    for pozicija, (korisnik, pagerank) in enumerate(rezultati, start=1):
        print(f"{pozicija}. {formatiraj_korisnika(korisnik, pagerank)}")


def ispisi_tekstualne_predloge(
    predlozi,
    aplikacija,
):
    if not predlozi:
        print("Nema dobrih predloga.")
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
    nivoi,
    aplikacija,
):
    if not nivoi:
        print("Nema korisnika do tog nivoa.")
        return

    for naziv_nivoa, korisnici in nivoi.items():
        print(f"\n{naziv_nivoa}:")
        for korisnik in korisnici:
            pagerank = aplikacija.graf.pagerank.get(korisnik.id, 0.0)
            print(f"  - {formatiraj_korisnika(korisnik, pagerank)}")


def ispisi_istoriju_interakcija(istorija):
    if istorija is None:
        print("Korisnik sa tim ID-jem ne postoji.")
        return

    if not istorija:
        print("Za ovog korisnika jos nema novih pracenja.")
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


def ispisi_preporuke(preporuke):
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


def pokreni_meni(aplikacija):
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
            id_pracenog = ucitaj_pozitivan_ceo_broj("ID korisnika koga prati: ")
            greska = aplikacija.validiraj_pracenje(id_pratioca, id_pracenog)
            if greska is not None:
                print(f"Veza nije dodata: {greska}")
            elif aplikacija.dodaj_pracenje(id_pratioca, id_pracenog):
                print(f"Dodato je pracenje: {id_pratioca} -> {id_pracenog}.")
            else:
                print("Veza nije dodata.")

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
            korisnicko_ime = ucitaj_neprazan_tekst("Uneto korisnicko ime: ")
            ogranicenje = ucitaj_pozitivan_ceo_broj("Broj predloga [5]: ", podrazumevano=5)
            if aplikacija.graf.pronadji_korisnika_po_imenu(korisnicko_ime):
                print("To korisnicko ime vec postoji, nema potrebe za predlogom.")
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
                print(f"Korisnik {korisnicko_ime} je dodat.")
            else:
                print("Korisnik nije dodat.")

        elif izbor == "0":
            print("Dovidjenja!")
            break

        else:
            print("Nema te opcije, probajte ponovo.")


def glavna():
    dataset_size = izaberi_skup_podataka()
    dataset_path = DATASET_ROOT / dataset_size

    aplikacija = AplikacijaDrustveneMreze()
    aplikacija.ucitaj_skup_podataka(dataset_path)
    pokreni_meni(aplikacija)


if __name__ == "__main__":
    try:
        glavna()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram je prekinut. Dovidjenja!")
