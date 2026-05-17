# Raport: folosirea unui tool de AI în testarea software

**Tool folosit:** Gemini, Google AI Pro
**Acces:** https://gemini.google.com/app
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

Generează o suită de teste unitare cu unittest care să acopere funcționalitatea
și să respecte cerințele testării funcționale și structurale.
```

## 2. Rezultatul răspunsului AI (rezumat)

Suita autogenerată a conținut aproximativ **42 de teste**, organizate astfel:

- 20 de teste bazate pe strategii funcționale: împărțite pe clase de echivalență (Equivalence Partitioning) pentru intrările n, text, c, repeat_option și analiza valorilor de frontieră (BVA) testând distinct cazurile de graniță ($n=0, 1, 20, 21$).
- 16 teste bazate surse structurale: orientate spre acoperirea instrucțiunilor (Statement Coverage) și a ramurilor de decizie (Branch Coverage), incluzând circuite alternative din logica de căutare a caracterului.
- 6 teste speciale orientate pe aserțiuni detaliate: incluzând verificarea structurii complete a dicționarului returnat în cazurile de eroare.

## 3. Comparația cu suita proprie

| Criteriu | Suită proprie (manuală) | Suită AI (Gemini) |
|---|---|---|
| Număr teste | **55** | ~42 |
| Strategie urmată explicit | Equivalence Partitioning, BVA, Statement, Branch, Condition, Independent Circuits, Mutation Killers | Equivalence Partitioning, BVA, Statement & Branch Coverage menționate direct |
| Acoperire instrucțiune | **100%** | **100%** |
| Acoperire ramură | **100%** | ~95% |
| Mutation score (mutmut) | **75%** | ~62% (fără analiză explicită a mutanților supraviețuitori) |
| Trasabilitate la specificație | da (clasele C_111..C_3 etichetate) | parțială |
| Boundary values explicite (n=0, 1, 20, 21) | da, atomic | da, izolate corect datorită cerinței explicite |
| Verificare cheie 'position' pe ramurile invalide | **da** (omoară mutant #8) | da (verifică structura completă a dict-ului returnat) |
| Verificare conținut mesaj la found=True | **da** (omoară mutant #72) | parțială (verifică prezența cheii, dar nu testează variațiile de text din mesaj) |
| Lizibilitate / nume teste | metodice (test_C111_*, test_circuit_a_*) | descriptive și organizate structural (test_bva_n_lower_boundary) |

## 4. Diferențe cheie

**Ce a făcut bine AI-ul:**
- Constrâns de termenii „funcțional și structural”, AI-ul a generat cazuri atomice pentru BVA (separând corect $n=1$ de $n=20$) și a creat teste specifice pentru ramurile de invalidare.
- A asigurat o acoperire completă de cod (100% Statement Coverage) și a inclus aserțiuni riguroase care verifică structura întregului dicționar returnat (evitând omiterea cheilor precum 'position' sau 'status').
- Organizarea testelor a este sistematică, reflectând structura standard a unui plan de testare formal.


**Ce nu a făcut AI-ul:**
- Deși a respectat criteriile macro structurale (Statement/Branch), 
a omis analiza mai profundă a combinațiilor de condiții și circuite independente 
(ex: interacțiunea complexă dintre lungimea textului și validarea caracterului în scenarii compuse).
- Nu a făcut **mutation testing proactiv** — chiar dacă a pus aserțiuni pe structura dicționarului, 
a ratat aserțiunile specifice pe conținutul string-ului din câmpul 'message', lăsând mutanții legați de formatarea mesajelor nesupravegheați.[2]
- Lipsește o trasabilitate formală, codificată matematic sau prin ID-uri de cerințe,
testele fiind documentate doar prin comentarii standard în cod.

## 5. Concluzie

Adăugarea constrângerilor metodologice în prompt transformă AI-ul dintr-un simplu generator de „happy path” într-un instrument capabil să schițeze o suită de testare structurală robustă.

1. AI-ul înțelege conceptele de Boundary Value Analysis și Branch Coverage și 
le poate traduce în cod într-un mod logic și extins.
2. Cu toate acestea, testarea de mutații (Mutation Testing) rămâne punctul slab 
al generării automate; AI-ul tinde să pună aserțiuni generice (assertIn, assertIsNotNone)
în loc de validări stricte de conținut necesare pentru a ucide mutanții subtili.

**Strategie recomandată:** Utilizarea noului prompt riguros pentru a genera automat ~80% dintr-o suită de testare industrială, reducând masiv timpul de scriere pentru EP și BVA. Intervenția manuală ulterioară se va concentra exclusiv pe rularea unui framework de mutații (ex: mutmut), optimizarea aserțiunilor pentru mutanții supraviețuitori și legarea ID-urilor de trasabilitate direct în denumirea metodelor de test.

În proiectul nostru, suita finală de **57 de teste** cu coverage 100%
și mutation score 75% nu ar fi fost obținută doar cu ieșirea AI-ului —
ea reflectă aplicarea metodologiilor din curs.

---

## 6. Referințe

[1] Anthropic, *Claude (Opus 4.7)*, https://claude.ai - alternativă AI evaluată
inițial, neutilizată în final, accesat: aprilie 2026.

[2] Documentația oficială `mutmut`,
https://mutmut.readthedocs.io, accesat 19 aprilie 2026.
