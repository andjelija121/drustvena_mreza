import re


def normalizuj_tekst(tekst):
    tekst = tekst.lower()
    tekst = re.sub(r"[^a-z0-9\s_]", " ", tekst)
    tekst = re.sub(r"\s+", " ", tekst)
    return tekst.strip()


def podeli_na_reci(tekst):
    normalizovan_tekst = normalizuj_tekst(tekst)
    if not normalizovan_tekst:
        return []

    return normalizovan_tekst.split()
