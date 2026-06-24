import heapq


class TrieNode:
    def __init__(self) -> None:
        self.deca: dict[str, TrieNode] = {}
        self.kraj_reci = False
        self.korisnicko_ime: str | None = None
        self.id_korisnika: int | None = None


class Trie:
    def __init__(self) -> None:
        self.koren = TrieNode()

    def dodaj(self, korisnicko_ime: str, id_korisnika: int) -> None:
        korisnicko_ime = korisnicko_ime.strip()
        if not korisnicko_ime:
            return

        cvor = self.koren
        for znak in korisnicko_ime.casefold():
            if znak not in cvor.deca:
                cvor.deca[znak] = TrieNode()
            cvor = cvor.deca[znak]

        cvor.kraj_reci = True
        cvor.korisnicko_ime = korisnicko_ime
        cvor.id_korisnika = id_korisnika

    def automatski_dovrsi(
        self, prefiks: str, pagerank_rezultati: dict[int, float], limit: int = 5
    ) -> list[str]:
        prefiks = prefiks.strip()
        if not prefiks or limit <= 0:
            return []

        cvor = self.koren
        normalizovan_prefiks = prefiks.casefold()
        for znak in normalizovan_prefiks:
            cvor = cvor.deca.get(znak)
            if cvor is None:
                return []

        zavrseci: list[tuple[str, int]] = []
        self._sakupi_reci(cvor, normalizovan_prefiks, zavrseci)

        rangirani = (
            (
                pagerank_rezultati.get(id_korisnika, 0.0),
                -id_korisnika,
                korisnicko_ime,
            )
            for korisnicko_ime, id_korisnika in zavrseci
        )
        najbolji = heapq.nlargest(limit, rangirani)
        return [
            korisnicko_ime
            for _pagerank, _negativan_id, korisnicko_ime in najbolji
        ]

    def _sakupi_reci(
        self,
        cvor: TrieNode,
        prefiks: str,
        rezultati: list[tuple[str, int]],
    ) -> None:
        if (
            cvor.kraj_reci
            and cvor.korisnicko_ime is not None
            and cvor.id_korisnika is not None
        ):
            rezultati.append((cvor.korisnicko_ime, cvor.id_korisnika))

        for znak, dete in cvor.deca.items():
            self._sakupi_reci(dete, prefiks + znak, rezultati)
