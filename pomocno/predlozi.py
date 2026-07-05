import heapq


def _levenshtein_udaljenost(prvi_tekst, drugi_tekst):
    if len(prvi_tekst) < len(drugi_tekst):
        prvi_tekst, drugi_tekst = drugi_tekst, prvi_tekst

    prethodni_red = list(range(len(drugi_tekst) + 1))

    for indeks_prvog, prvi_znak in enumerate(prvi_tekst, start=1):
        trenutni_red = [indeks_prvog]

        for indeks_drugog, drugi_znak in enumerate(drugi_tekst, start=1):
            cena_zamene = 0 if prvi_znak == drugi_znak else 1
            trenutni_red.append(
                min(
                    trenutni_red[-1] + 1,
                    prethodni_red[indeks_drugog] + 1,
                    prethodni_red[indeks_drugog - 1] + cena_zamene,
                )
            )

        prethodni_red = trenutni_red

    return prethodni_red[-1]


def predlozi_slicna_imena(
    korisnicko_ime,
    postojeca_imena,
    limit=5,
    pagerank_po_imenu=None,
):
    korisnicko_ime = korisnicko_ime.strip()
    if not korisnicko_ime or limit <= 0:
        return []

    normalizovano_trazeno_ime = korisnicko_ime.lower()
    pagerank_po_imenu = pagerank_po_imenu or {}
    normalizovan_pagerank = {
        ime.lower(): rezultat
        for ime, rezultat in pagerank_po_imenu.items()
    }

    jedinstvena_imena = {}
    for postojece_ime in postojeca_imena:
        ocisceno_ime = postojece_ime.strip()
        if ocisceno_ime:
            jedinstvena_imena.setdefault(ocisceno_ime.lower(), ocisceno_ime)

    if normalizovano_trazeno_ime in jedinstvena_imena:
        return []

    rangirani_kandidati = (
        (
            _levenshtein_udaljenost(
                normalizovano_trazeno_ime,
                normalizovano_postojece_ime,
            ),
            -normalizovan_pagerank.get(normalizovano_postojece_ime, 0.0),
            normalizovano_postojece_ime,
            postojece_ime,
        )
        for normalizovano_postojece_ime, postojece_ime
        in jedinstvena_imena.items()
    )

    najbolji = heapq.nsmallest(limit, rangirani_kandidati)
    return [
        postojece_ime
        for _udaljenost, _negativan_pagerank, _normalizovano_ime, postojece_ime
        in najbolji
    ]
