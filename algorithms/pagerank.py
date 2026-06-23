from graph.social_graph import SocialGraph


def izracunaj_pagerank(
    graf: SocialGraph,
    faktor_prigusenja: float = 0.85,
    epsilon: float = 1e-6,
    pocetni_rezultati: dict[int, float] | None = None,
) -> dict[int, float]:
    pass


def izracunaj_personalizovani_pagerank(
    graf: SocialGraph,
    pocetni_id_korisnika: int,
    faktor_prigusenja: float = 0.85,
    epsilon: float = 1e-6,
) -> dict[int, float]:
    pass


def pronadji_najbolje_korisnike(
    pagerank_rezultati: dict[int, float], limit: int = 10
) -> list[tuple[int, float]]:
    pass
