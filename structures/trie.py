class TrieNode:
    def __init__(self) -> None:
        pass


class Trie:
    """Prefiksno stablo za autocomplete korisnickih imena."""

    def __init__(self) -> None:
        pass

    def dodaj(self, korisnicko_ime: str, id_korisnika: int) -> None:
        pass

    def automatski_dovrsi(
        self, prefiks: str, pagerank_rezultati: dict[int, float], limit: int = 5
    ) -> list:
        pass

    def _sakupi_reci(self, cvor: TrieNode, prefiks: str, rezultati: list) -> None:
        pass
