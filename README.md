# Drustvena mreza - ASP Projekat 2

Python konzolna aplikacija koja simulira deo drustvene mreze. Ucitava korisnike,
follow veze i blokiranja, pa omogucava pretragu, rangiranje, preporuke i obilazak
grafa.

Program na pocetku trazi da se izabere skup podataka: `small`, `medium` ili `full`.

## Ulazni fajlovi

Za svaku velicinu skupa u folderu `dataset/` se nalaze:

- `users.txt` - `id|username|bio`
- `connections.txt` - `from_id|to_id`
- `blocked.txt` - `blocker_id|blocked_id`

Fajlovi se ucitavaju u memoriju pri pokretanju programa. Novi korisnici i nove
veze koje se dodaju tokom rada ne upisuju se nazad u fajlove, vec vaze samo dok
program radi.

## Sta je uradjeno

- Pretraga po korisnickom imenu i po recima iz biografije, case insensitive
- Inverted index za pretragu biografija
- PageRank, damping `0.85`, epsilon `1e-6`
- Ponovno racunanje PageRank-a posle dodavanja korisnika ili veze
- Prikaz top korisnika preko heap-a
- Dodavanje nove follow veze uz proveru da korisnici postoje, da veza ne postoji
  vec i da nema blokiranja
- Istorija dodatih veza, hronoloski
- Autocomplete korisnickih imena preko prefiksnog stabla, sortirano po PageRank-u
- Hibridne preporuke: `alpha * PPR + (1 - alpha) * Jaccard`
- BFS po nivoima konekcije od izabranog korisnika
- "Did you mean" preko Levenshtein rastojanja
- Blokirani korisnici se ne prikazuju u preporukama
- Ako izmedju dva korisnika postoji blokiranje, ne moze da se doda follow veza
- Dodavanje novog korisnika u graf, indekse i prefiksno stablo

## Strukture koje su koriscene

- Graf - hash mape za korisnike, izlazne veze, ulazne veze i blokiranja
- Inverted index za reci iz biografija
- Prefiksno stablo za autocomplete
- Heap za top liste
- BFS - `deque` i skup posecenih
- Jaccard slicnost za poredjenje biografija
- Levenshtein distanca za slicna korisnicka imena

## Provera unosa

Program proverava da su brojevi validni, da je `alpha` izmedju 0 i 1 i da tekstualni
unos nije prazan. Kada nesto ne moze da se uradi, ispisuje se razlog, na primer:
korisnik ne postoji, ID ili username je zauzet, veza vec postoji, korisnik pokusava
da zaprati samog sebe ili postoji blokiranje.

Rezultati pretrage, autocomplete-a, BFS-a i top liste prikazuju ID, username i
PageRank. Kod preporuka se vidi i ukupni skor, PPR i Jaccard deo.

## Merenje vremena

Merenje je uradjeno 05.07.2026. na Windows-u. Vremena zavise od racunara i od toga
sta jos radi u pozadini.

Full skup ima 81.306 korisnika, 1.768.135 follow veza i 1.626 blokiranja.

| Operacija | Vreme |
| --- | ---: |
| Ucitavanje fajlova i formiranje grafa | 4.649 s |
| Pocetno racunanje PageRank-a | 228.536 s |
| Formiranje inverted index-a | 2.127 s |
| Formiranje prefiksnog stabla | 6.401 s |
| Ukupno pocetno formiranje struktura | 241.713 s |
| Top 10 po PageRank-u | 0.029 s |
| Pretraga biografije | 0.001 s |
| BFS do nivoa 3 | 0.104 s |
| Autocomplete | 0.006 s |
| "Did you mean" | 3.490 s |
| Hibridne preporuke | 123.693 s |

PageRank i preporuke su najsporiji deo. Preporuke ponovo racunaju PPR za izabranog
korisnika, sto znaci da opet prolaze kroz veliki graf. Ostale opcije rade nad vec
formiranim strukturama, pa su dosta brze.

Na `medium` skupu je pocetno ucitavanje i formiranje struktura trajalo oko `4.893 s`,
a nakon toga su opcije radile interaktivno.

## Struktura projekta

- `algoritmi/` - PageRank i personalizovani PageRank
- `podaci/` - ucitavanje fajlova
- `graph/` - graf
- `modeli/` - klasa korisnika
- `preporuke/` - hibridne preporuke
- `pretraga/` - pretraga i inverted index
- `strukture/` - prefiksno stablo
- `pomocno/` - obrada teksta i Levenshtein
- `app.py` - povezuje sve delove
- `main.py` - meni
