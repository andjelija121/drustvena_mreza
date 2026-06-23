class User:
    """Model korisnika drustvene mreze."""

    def __init__(self, id_korisnika: int, korisnicko_ime: str, biografija: str) -> None:
        from utils.text_processing import podeli_na_reci

        self.id = id_korisnika
        self.username = korisnicko_ime
        self.bio = biografija
        self.bio_words = podeli_na_reci(biografija)

    def to_dict(self) -> dict:
        """Vraca obican dict koji se lako moze sacuvati ili prikazati."""
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio,
            "bio_words": self.bio_words,
        }

    def __repr__(self) -> str:
        return f"User(id={self.id}, username='{self.username}')"
