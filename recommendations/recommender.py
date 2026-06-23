from graph.social_graph import SocialGraph


class Recommender:
    """Hibridne preporuke: alpha * PPR + (1-alpha) * slicnost."""

    def __init__(self, graf: SocialGraph) -> None:
        pass

    def izracunaj_jaccard_slicnost(
        self, prva_biografija: str, druga_biografija: str
    ) -> float:
        pass

    def preporuci(
        self, id_korisnika: int, alfa: float = 0.5, limit: int = 10
    ) -> list:
        pass
