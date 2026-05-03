# Raport: folosirea unui tool de AI în testarea software

**Tool folosit:** Claude (Anthropic), versiune Opus 4.7
**Acces:** https://claude.ai
**Data:** aprilie 2026
**Context:** generare automată de teste unitare pentru clasa
`StringSearcher` și comparație cu suita proprie de teste construită pe
baza strategiilor formale din suportul de curs.

---

## 1. Prompt folosit pentru generarea automată

```
Am o clasă Python `StringSearcher` cu o metodă publică `search_character(
n, text, c, repeat_option)` care:
- validează n în [1, 20] (altfel întoarce status='INVALID_N'),
- validează text de lungime exact n (altfel 'INVALID_TEXT'),
- validează c de lungime 1 (altfel 'INVALID_CHAR'),
- caută prima poziție 1-based a lui c în text,
- returnează un dict cu status, position (-1 dacă nu e găsit), message,
  continue_search (True dacă repeat_option ∈ {'y','Y'}).

Generează o suită de teste unitare cu unittest care să acopere
funcționalitatea. Nu îți cer să urmezi vreo strategie anume — vreau să
văd ce ar genera AI-ul "din instinct".
```

## 2. Rezultatul răspunsului AI (rezumat)

Suita autogenerată conținea aproximativ **15 teste**, organizate astfel:

- 4 teste pe „happy path" (găsește pe prima/ultima/mijloc poziție +
  repeat_option = 'y')
- 3 teste pe validare n (negativ, zero, peste limită)
- 2 teste pe validare text (None, lungime greșită)
- 2 teste pe validare c (None, lungime > 1)
- 2 teste pe „not found" (caracter inexistent)
- 1 test pe repeat_option = 'N' (uppercase)
- 1 test parametrizat cu mai multe combinații

## 3. Comparația cu suita proprie

| Criteriu | Suită proprie (manuală) | Suită AI (Claude) |
|---|---|---|
| Număr teste | **55** | ~15 |
| Strategie urmată explicit | Equivalence Partitioning, BVA, Statement, Branch, Condition, Independent Circuits, Mutation Killers | nicio strategie formală |
| Acoperire instrucțiune | **100%** | ~95% |
| Acoperire ramură | **100%** | ~85% |
| Mutation score (mutmut) | **75%** | ~50% (estimat – Claude rulat pe aceeași clasă fără teste killer) |
| Trasabilitate la specificație | da (clasele C_111..C_3 etichetate) | parțială |
| Boundary values explicite (n=0, 1, 20, 21) | da, atomic | n=0 și n>20 acoperite, dar n=1 și n=20 amestecate |
| Verificare cheie 'position' pe ramurile invalide | **da** (omoară mutant #8) | **nu** |
| Verificare conținut mesaj la found=True | **da** (omoară mutant #72) | **nu** |
| Lizibilitate / nume teste | metodice (test_C111_*, test_circuit_a_*) | descriptive dar non-sistematice |

## 4. Diferențe cheie

**Ce a făcut bine AI-ul:**
- A acoperit rapid „happy path"-ul și principalele cazuri invalide.
- A scris teste citibile și folosește `assertEqual`/`assertIsNone`
  corect.
- A folosit `setUp` pentru a inițializa `searcher`.
- Util ca **punct de plecare** sau **schelet** pentru o suită mai
  riguroasă.

**Ce nu a făcut AI-ul:**
- Nu a urmat o **strategie formală** — testele sunt "intuitive", nu
  derivate din clase de echivalență sau din analiza grafului CFG.
- A omis **valori de frontieră** (de ex. testarea explicită a lui
  `n = 1` separată de `n = 20`).
- Nu a derivat tests din complexitatea ciclomatică — a omis
  circuite independente.
- Nu a făcut **mutation testing** și nu a anticipat tipurile de mutanți
  ce ar putea supraviețui (ex. modificările pe câmpurile `message`).
- Nu a etichetat testele cu trasabilitate la cerință.

## 5. Concluzie

AI-ul (Claude) este un **multiplicator de productivitate**, nu un
înlocuitor pentru gândirea sistematică în testare. Suita autogenerată
în câteva secunde acoperă rapid cazurile evidente, dar:

1. nu garantează acoperire completă pe niciun criteriu formal;
2. ratează exact tipul de aserțiuni necesare pentru a omorî mutanți
   subtili (cheia `'position'` modificată, mesajul setat la `None`);
3. nu poate înlocui aplicarea sistematică a strategiilor din curs.

**Strategie recomandată:** folosirea AI-ului ca să genereze rapid
scheletul (15 teste de bază în 30 de secunde), apoi extinderea **manuală
ghidată de strategii** până se atinge:
- 100% statement & branch coverage,
- un scor de mutație acceptabil (≥ 70%),
- trasabilitate explicită cerință → test.

În proiectul nostru, suita finală de **55 de teste** cu coverage 100%
și mutation score 75% nu ar fi fost obținută doar cu ieșirea AI-ului —
ea reflectă aplicarea metodologiilor din `Functional Testing.pdf` și
`Structural Testing.pdf`.

---

## 6. Referințe

[1] OpenAI, *ChatGPT*, https://chatgpt.com — alternativă AI evaluată
inițial, neutilizată în final, accesat aprilie 2026.

[2] Anthropic, *Claude (Opus 4.7)*, https://claude.ai, data generării
suitei comparative: aprilie 2026.

[3] Documentația oficială `mutmut`,
https://mutmut.readthedocs.io, accesat 19 aprilie 2026.
