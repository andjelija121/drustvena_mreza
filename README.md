# Drustvena mreza - ASP Projekat 2

Konzolna Python aplikacija koja ucitava usmereni graf drustvene mreze i
omogucava pretragu, rangiranje, preporuke i obilazak korisnika.

## Pokretanje

Potreban je Python 3.10 ili noviji. Projekat ne koristi spoljne biblioteke.

Iz korenskog direktorijuma projekta pokrenuti:

```powershell
python main.py
```

Nakon pokretanja bira se jedan od skupova:

1. `small` - razvoj i brzo testiranje
2. `medium` - demonstracija interaktivnog rada
3. `full` - provera performansi

## Ulazni fajlovi

Za svaku velicinu skupa direktorijum `dataset/` sadrzi:

- `users.txt` u formatu `id|username|bio`
- `connections.txt` u formatu `from_id|to_id`
- `blocked.txt` u formatu `blocker_id|blocked_id`

Pri pokretanju se fajlovi ucitavaju u memoriju i formiraju se potrebne
strukture podataka. Nove veze i korisnici vaze tokom trenutnog pokretanja
programa. Specifikacija ne zahteva cuvanje izmena nazad u ulazne fajlove.

## Implementirane funkcionalnosti

1. Pretraga korisnika po korisnickom imenu, bez obzira na velicinu slova
2. Pretraga po recima iz biografije pomocu inverted index strukture
3. Iterativni PageRank sa damping faktorom `0.85` i `epsilon = 1e-6`
4. Prikaz najuticajnijih korisnika pomocu heap strukture
5. Dodavanje nove follow veze uz proveru korisnika, duplikata i blokiranja
6. Hronoloska istorija novih follow veza dodatih tokom rada programa
7. Trie autocomplete rangiran prema PageRank vrednosti
8. Hibridne preporuke: `alpha * PPR + (1 - alpha) * Jaccard`
9. BFS prikaz korisnika po nivoima konekcije
10. "Did you mean" predlozi pomocu Levenshtein udaljenosti
11. Filtriranje blokiranih korisnika u vezama i preporukama
12. Dodavanje novog korisnika u graf, hash mape, indekse i Trie
13. Ponovno racunanje PageRank-a nakon dodavanja veze ili korisnika

## Strukture i algoritmi

- Graf: skupovi izlaznih i ulaznih veza i mapa izlaznih stepena
- Brz pristup korisnicima: hash mape po ID-u i korisnickom imenu
- Pretraga biografija: inverted index
- Autocomplete: sopstvena implementacija Trie strukture
- Rangiranje: PageRank, Personalized PageRank i heap
- Obilazak grafa: BFS uz `deque` i skup posecenih cvorova
- Slicnost biografija: Jaccard slicnost skupova reci
- Slicna imena: Levenshtein edit distance

## Validacija i poruke

Meni proverava da su brojcani unosi pozitivni celi brojevi, da je `alpha`
izmedju 0 i 1 i da tekstualni upiti nisu prazni. Pri dodavanju veze ili
korisnika prikazuje se konkretan razlog neuspeha, na primer nepostojeci ID,
zauzet ID ili username, postojeca veza, pokusaj pracenja samog sebe ili
blokiranje.

Rezultati pretrage, autocomplete-a, BFS-a i top liste prikazuju ID,
korisnicko ime i PageRank vrednost. Preporuke dodatno prikazuju kombinovani
skor, PPR i Jaccard komponentu.

## Primeri za demonstraciju

Na `small` skupu mogu se koristiti:

- pretraga korisnickog imena: `gui`
- pretraga biografije: `guildwars`
- autocomplete prefiks: `mar`
- BFS pocetni korisnik: ID `1`, maksimalni nivo `3`
- preporuke: ID `1`, `alpha = 0.5`

Za odbranu je preporuceno iste opcije demonstrirati na `medium` skupu.

## Testiranje

Specifikacija ne zahteva biblioteku za automatsko testiranje niti poseban
`tests/` direktorijum. Izvrsena je funkcionalna smoke provera na `small`
skupu koja obuhvata ucitavanje, pretragu, top korisnike, BFS, preporuke,
dodavanje korisnika, azuriranje indeksa i ponovno racunanje PageRank-a.

Na `medium` skupu provereni su ucitavanje, PageRank, top lista, pretraga
biografije i BFS. Pocetno ucitavanje cele aplikacije trajalo je oko `4.26 s`
i aplikacija je nakon toga radila interaktivno.

## Merenje full skupa

Merenje je izvrseno 24.06.2026. na Windows okruzenju sa Python verzijom
3.12.13. Vremena zavise od procesora, memorije i trenutnog opterecenja
racunara.

Full skup sadrzi:

- 81.306 korisnika
- 1.768.135 follow veza

Izmerena vremena:

| Operacija | Vreme |
| --- | ---: |
| Ucitavanje tekstualnih fajlova i formiranje grafa | 4.194 s |
| Pocetno racunanje PageRank-a | 70.473 s |
| Formiranje inverted index-a | 0.661 s |
| Formiranje Trie strukture | 1.548 s |
| Ukupno pocetno formiranje svih struktura | 76.876 s |
| Top 10 PageRank korisnika | 0.005 s |
| Pretraga biografije | 0.003 s |
| BFS do nivoa 3 | 0.033 s |
| Autocomplete | 0.002 s |
| "Did you mean" | 1.281 s |
| Hibridne preporuke | 41.874 s |

Najskuplje operacije su globalni PageRank i hibridne preporuke, zato sto
PPR u preporukama ponovo iterativno prolazi kroz veliki graf. Ucitavanje,
pretraga, top lista, autocomplete i BFS koriste unapred formirane strukture
i znatno su brzi.

## Organizacija projekta

- `algorithms/` - PageRank i Personalized PageRank
- `data_access/` - ucitavanje skupova podataka
- `graph/` - model usmerenog grafa
- `models/` - korisnicki model
- `recommendations/` - hibridne preporuke
- `search/` - pretraga i inverted index
- `structures/` - Trie
- `utils/` - obrada teksta i slicna imena
- `app.py` - povezivanje algoritama i struktura
- `main.py` - tekstualni korisnicki interfejs
