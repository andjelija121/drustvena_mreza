import heapq


def izracunaj_pagerank(
    graf,
    faktor_prigusenja=0.85,
    epsilon=1e-6,
    pocetni_rezultati=None,
):
    if not 0.0 <= faktor_prigusenja <= 1.0:
        raise ValueError("Faktor prigusenja mora biti izmedju 0 i 1.")
    if epsilon <= 0:
        raise ValueError("Epsilon mora biti veci od nule.")

    ids = list(graf.korisnici_po_id)
    broj_korisnika = len(ids)
    if broj_korisnika == 0:
        return {}

    if pocetni_rezultati:
        rezultati = {
            id_korisnika: max(0.0, pocetni_rezultati.get(id_korisnika, 0.0))
            for id_korisnika in ids
        }
        zbir = sum(rezultati.values())
        if zbir > 0:
            rezultati = {
                id_korisnika: rezultat / zbir
                for id_korisnika, rezultat in rezultati.items()
            }
        else:
            rezultati = {id_korisnika: 1.0 / broj_korisnika for id_korisnika in ids}
    else:
        rezultati = {id_korisnika: 1.0 / broj_korisnika for id_korisnika in ids}
    osnovni_doprinos = (1.0 - faktor_prigusenja) / broj_korisnika


    for _ in range(10_000):
        dangling_masa = sum(
            rezultati[id_korisnika]
            for id_korisnika in ids
            if graf.pronadji_izlazni_stepen(id_korisnika) == 0
        )
        dangling_doprinos = (
            faktor_prigusenja * dangling_masa / broj_korisnika
        )

        novi_rezultati = {}
        for id_korisnika in ids:
            dolazni_doprinos = 0.0
            for id_pratioca in graf.pronadji_pratioce(id_korisnika):
                izlazni_stepen = graf.pronadji_izlazni_stepen(id_pratioca)
                if izlazni_stepen > 0:
                    dolazni_doprinos += (
                        rezultati[id_pratioca] / izlazni_stepen
                    )

            novi_rezultati[id_korisnika] = (
                osnovni_doprinos
                + dangling_doprinos
                + faktor_prigusenja * dolazni_doprinos
            )

        razlika = sum(
            abs(novi_rezultati[id_korisnika] - rezultati[id_korisnika])
            for id_korisnika in ids
        )
        rezultati = novi_rezultati
        if razlika < epsilon:
            break


    zbir = sum(rezultati.values())
    return {
        id_korisnika: rezultat / zbir
        for id_korisnika, rezultat in rezultati.items()
    }


def izracunaj_personalizovani_pagerank(
    graf,
    pocetni_id_korisnika,
    faktor_prigusenja=0.85,
    epsilon=1e-6,
):
    if not 0.0 <= faktor_prigusenja <= 1.0:
        raise ValueError("Faktor prigusenja mora biti izmedju 0 i 1.")
    if epsilon <= 0:
        raise ValueError("Epsilon mora biti veci od nule.")
    if not graf.korisnik_postoji(pocetni_id_korisnika):
        raise ValueError("Pocetni korisnik ne postoji.")

    ids = list(graf.korisnici_po_id)
    if not ids:
        return {}

    rezultati = {
        id_korisnika: (
            1.0 if id_korisnika == pocetni_id_korisnika else 0.0
        )
        for id_korisnika in ids
    }

    for _ in range(10_000):
        dangling_masa = sum(
            rezultati[id_korisnika]
            for id_korisnika in ids
            if graf.pronadji_izlazni_stepen(id_korisnika) == 0
        )
        novi_rezultati = {}
        for id_korisnika in ids:
            dolazni_doprinos = 0.0
            for id_pratioca in graf.pronadji_pratioce(id_korisnika):
                izlazni_stepen = graf.pronadji_izlazni_stepen(id_pratioca)
                if izlazni_stepen > 0:
                    dolazni_doprinos += (
                        rezultati[id_pratioca] / izlazni_stepen
                    )

            novi_rezultati[id_korisnika] = (
                faktor_prigusenja * dolazni_doprinos
            )

        novi_rezultati[pocetni_id_korisnika] += (
            1.0
            - faktor_prigusenja
            + faktor_prigusenja * dangling_masa
        )

        razlika = sum(
            abs(novi_rezultati[id_korisnika] - rezultati[id_korisnika])
            for id_korisnika in ids
        )
        rezultati = novi_rezultati
        if razlika < epsilon:
            break
    zbir = sum(rezultati.values())
    if zbir == 0:
        return rezultati

    return {
        id_korisnika: rezultat / zbir
        for id_korisnika, rezultat in rezultati.items()
    }


def pronadji_najbolje_korisnike(
    pagerank_rezultati,
    limit=10,
):
    if limit <= 0:
        return []
    rangirani = (
        (rezultat, -id_korisnika, id_korisnika)
        for id_korisnika, rezultat in pagerank_rezultati.items()
    )
    najbolji = heapq.nlargest(limit, rangirani)
    return [
        (id_korisnika, rezultat)
        for rezultat, _negativan_id, id_korisnika in najbolji
    ]
