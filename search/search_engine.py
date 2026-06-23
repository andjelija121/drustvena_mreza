from graph.social_graph import SocialGraph


class SearchEngine:
    """Case-insensitive pretraga pomocu inverted indeksa."""

    def __init__(self, graf: SocialGraph) -> None:
        pass

    def napravi_invertovani_indeks(self) -> None:
        pass

    def dodaj_korisnika_u_indeks(self, id_korisnika: int) -> None:
        pass

    def pretrazi_po_korisnickom_imenu(
        self, upit: str, pagerank_rezultati: dict[int, float], limit: int = 10
    ) -> list:
        pass

    def pretrazi_po_biografiji(
        self, upit: str, pagerank_rezultati: dict[int, float], limit: int = 10
    ) -> list:
        pass
