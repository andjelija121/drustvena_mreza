from pomocno.obrada_teksta import podeli_na_reci


class Korisnik:
    def __init__(self, id_korisnika, korisnicko_ime, biografija):
        self.id = id_korisnika
        self.username = korisnicko_ime
        self.bio = biografija
        self.bio_words = podeli_na_reci(biografija)
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio,
            "bio_words": self.bio_words,
        }

    def __repr__(self):
        return f"Korisnik(id={self.id}, username='{self.username}')"
