# Proiect TSS — T1: Testare unitară în Python 

**Materia:** Testarea Sistemelor Software
**Tema:** T1 — Testare unitară în Python
**Clasă testată:** `StringSearcher`
**Framework:** `unittest` 

---

## 1. Algoritmul testat — clasa `StringSearcher`?

Clasa implementează **căutarea unui caracter într-un șir de cel mult 20
de caractere**. Algoritmul reproduce exemplul folosit în
suportul de curs (Functional Testing & Structural Testing), tocmai pentru
a putea aplica metodologiile prezentate la curs.

### Specificația funcțională (din enunț)

> Pentru un întreg `n` aflat între 1 și 20, se introduce un șir `text` de
> exact `n` caractere, apoi un caracter `c` care este căutat în `text`.
> Programul returnează prima poziție pe care apare `c` (1-based) sau un
> mesaj indicând că nu a fost găsit. Utilizatorul poate continua
> căutarea (`'y'`/`'Y'`) sau poate opri (`'n'`/`'N'`).

### Pre-condiții

| Parametru | Restricție |
|---|---|
| `n` | întreg, `1 ≤ n ≤ 20` |
| `text` | string de lungime exact `n` |
| `c` | caracter (string de lungime 1) |
| `repeat_option` | `'y'`, `'Y'`, `'n'` sau `'N'` |

### Post-condiție

Metoda `search_character(n, text, c, repeat_option)` întoarce un
**dicționar** cu cheile:

| Cheie | Tip | Semnificație |
|---|---|---|
| `status` | string | `'OK'`, `'INVALID_N'`, `'INVALID_TEXT'`, sau `'INVALID_CHAR'` |
| `position` | int | poziția 1-based unde apare `c`, sau `-1` dacă lipsește |
| `message` | string | mesaj descriptiv pentru utilizator |
| `continue_search` | bool | `True` dacă utilizatorul vrea să continue |

### Ce se întâmplă pas cu pas în algoritm

```
search_character(n, text, c, repeat_option)
│
├─ 1) Validare n
│     dacă n < 1 SAU n > 20 → returnează INVALID_N (oprește)
│
├─ 2) Validare text
│     dacă text e None SAU len(text) ≠ n → returnează INVALID_TEXT
│
├─ 3) Validare c
│     dacă c e None SAU len(c) ≠ 1 → returnează INVALID_CHAR
│
├─ 4) Inițializare: found = False, position = -1, i = 0
│
├─ 5) Bucla de căutare: cât timp (NOT found) AND (i < n)
│     │
│     ├─ dacă text[i] == c:
│     │     found = True
│     │     position = i + 1   ← indexare 1-based, ca în curs
│     └─ i = i + 1
│
├─ 6) Construire mesaj
│     dacă found  → "character X appears at position P"
│     altfel       → "character X does not appear in string"
│
├─ 7) Decizie continuare
│     continue_search = (repeat_option == 'y' OR repeat_option == 'Y')
│
└─ returnează dict cu toate cele 4 câmpuri
```

### De ce această clasă pentru T1?

1. Are **toate tipurile de structuri** necesare pentru ilustrarea
   strategiilor: validări multiple (decizii cu `OR`), buclă cu condiție
   compusă (`AND`), `if/else`, decizie cu `OR` la final.
2. Reproduce exact algoritmul folosit la curs, deci testele noastre sunt
   direct comparabile cu exemplele din slide-uri.
3. Este destul de simplă pentru a fi prezentată în 5 minute, dar destul
   de bogată pentru a permite aplicarea celor 6 strategii cerute.

---

## 2. Strategiile de testare aplicate

În total, pentru predarea 1/3 am implementat **44 de teste**, organizate
pe 6 fișiere — câte unul pentru fiecare strategie din curs.

| # | Strategie | Tip | Fișier | Teste |
|---|---|---|---|---|
| 1 | Equivalence Partitioning | Funcțional | `test_01_equivalence_partitioning.py` | 6 |
| 2 | Boundary Value Analysis | Funcțional | `test_02_boundary_value_analysis.py` | 12 |
| 3 | Statement Coverage | Structural | `test_03_statement_coverage.py` | 3 |
| 4 | Branch / Decision Coverage | Structural | `test_04_branch_coverage.py` | 8 |
| 5 | Condition Coverage | Structural | `test_05_condition_coverage.py` | 10 |
| 6 | Independent Circuits | Structural | `test_06_independent_circuits.py` | 5 |

### 2.1. Equivalence Partitioning (`test_01`)

**Idee:** împărțim domeniul de intrare în clase de echivalență — toate
valorile dintr-o clasă sunt tratate identic de program, deci e suficient
să testăm un singur reprezentant din fiecare clasă.

**Cum am identificat clasele (urmând metodologia din curs):**

*Pe domeniul de intrare:*
- Pentru `n`:
  - `N_1 = {n | 1 ≤ n ≤ 20}` (valid)
  - `N_2 = {n | n < 1}` (invalid — prea mic)
  - `N_3 = {n | n > 20}` (invalid — prea mare)
- Pentru `repeat_option` (binar):
  - `S_1 = {'y'}`
  - `S_2 = {'n'}`

*Pe domeniul de ieșire — caracterul `c` în raport cu `text`:*
- `C_1(text) = {c | c apare în text}`
- `C_2(text) = {c | c nu apare în text}`

**Combinând**, obținem **6 clase globale**:

| Clasă | n | c apare în text? | repeat |
|---|---|---|---|
| `C_111` | valid | da | `'y'` |
| `C_112` | valid | da | `'n'` |
| `C_121` | valid | nu | `'y'` |
| `C_122` | valid | nu | `'n'` |
| `C_2`   | < 1 | — | — |
| `C_3`   | > 20 | — | — |

→ **6 reprezentanți = 6 teste** (vezi `test_01_equivalence_partitioning.py`).

### 2.2. Boundary Value Analysis (`test_02`)

**Idee:** valorile de pe frontiera claselor sunt o sursă majoră de
erori, așa că le testăm separat pe lângă reprezentanții generici.

**Frontiere identificate:**
- pentru `n`: valorile **0, 1, 20, 21**
- pentru `c`: poziția pe care apare în `text` — **prima** sau **ultima**

**Distribuția testelor (urmărind exact tabelul din suportul de curs):**

| Clasă | Subcazuri | #teste |
|---|---|---|
| `C_111` | (1,'a','a','y') + (20, str20, 'a','y') + (20, str20, 'u','y') | 3 |
| `C_112` | identic dar cu `'n'` | 3 |
| `C_121` | (1,'a','b','y') + (20, str20, 'z','y') | 2 |
| `C_122` | identic dar cu `'n'` | 2 |
| `C_2`   | n = 0 | 1 |
| `C_3`   | n = 21 | 1 |

→ **Total: 12 teste** (vezi `test_02_boundary_value_analysis.py`).

### 2.3. Statement Coverage (`test_03`)

**Idee:** fiecare instrucțiune din metoda `search_character` trebuie
executată cel puțin o dată.

Două teste atent alese acoperă tot codul principal:
1. Test pe drumul `valid + found + continue` (acoperă instrucțiunile din
   ramura `if found:` și din continuare cu `'y'`)
2. Test pe drumul `valid + not_found + stop` (acoperă ramura `else:` și
   oprirea cu `'n'`)

Plus un al treilea test pentru ramura de validare `n` invalidă.

→ **3 teste** (vezi `test_03_statement_coverage.py`).

### 2.4. Branch / Decision Coverage (`test_04`)

**Idee:** fiecare decizie (ramificație) din cod trebuie să ia atât
valoarea `True`, cât și valoarea `False`.

În metoda `search_character` am identificat **7 decizii**:

| # | Decizie | Locație |
|---|---|---|
| 1 | `n < 1 OR n > 20` | validare n |
| 2 | `text is None OR len(text) ≠ n` | validare text |
| 3 | `c is None OR len(c) ≠ 1` | validare c |
| 4 | `(not found) AND (i < n)` | bucla de căutare |
| 5 | `text[i] == c` | match caracter |
| 6 | `if found` | construire mesaj |
| 7 | `repeat == 'y' OR repeat == 'Y'` | decizia de continuare |

Pentru fiecare decizie, câte un test pentru ramura `True` și unul pentru
ramura `False` → **8 teste** (multe acoperă mai multe ramuri simultan,
deci nu avem nevoie de 14).

(vezi `test_04_branch_coverage.py`)

### 2.5. Condition Coverage (`test_05`)

**Idee:** când o decizie e compusă (`OR`/`AND`), vrem ca **fiecare
condiție individuală** din decizie să ia atât `True`, cât și `False`.
Asta merge mai departe decât branch coverage.

**Exemplu concret:** decizia `n < 1 OR n > 20` are două condiții
individuale: `n < 1` și `n > 20`. Pentru branch coverage e suficient să
intri pe ambele ramuri, dar pentru condition coverage trebuie ca:
- `n < 1` să fie testat atât `True` cât și `False`
- `n > 20` să fie testat atât `True` cât și `False`

Condițiile individuale identificate:
- `n < 1`, `n > 20`
- `not found`, `i < n`
- `text[i] == c`
- `repeat == 'y'`, `repeat == 'Y'`

→ **10 teste** (vezi `test_05_condition_coverage.py`).

### 2.6. Independent Circuits (`test_06`)

**Idee:** folosim **complexitatea ciclomatică McCabe** pentru a
determina numărul minim de drumuri independente prin graful de control,
suficient pentru a acoperi toate ramurile.

**Formula McCabe** (pentru o singură subrutină):

```
V(G) = e - n + 2
```

unde `e` = numărul de muchii, `n` = numărul de noduri din CFG.

Pentru metoda `search_character`, calculul dă:

```
V(G) = 14 - 11 + 2 = 5
```

Deci avem nevoie de cel puțin **5 circuite independente** = **5 teste
de bază**. Acestea sunt:

| # | Circuit | Caz testat |
|---|---|---|
| a | start → INVALID_N → end | `n` invalid |
| b | start → text invalid → end | `text` lungime greșită |
| c | start → c invalid → end | `c` invalid |
| d | start → buclă → found → continue → end | match + continuă |
| e | start → buclă → not found → stop → end | nu găsește + oprește |

→ **5 teste** (vezi `test_06_independent_circuits.py`).

---

## 3. Sumar — de ce 44 de teste, nu mai puține?

Strategiile **nu sunt redundante** — fiecare prinde alt tip de defect:
- *Equivalence partitioning* prinde defecte legate de **comportamentul
  pe categorii de date**
- *Boundary value* prinde defecte la **±1** și pe limite
- *Statement* / *branch* / *condition* / *circuits* prind defecte
  **structurale** (instrucțiuni neexecutate, ramuri ratate, decizii
  parțial testate)

Fiecare strategie e ilustrată pe **fișierul ei** dedicat, cu comentarii
care explică maparea explicit la metodologia din suportul de curs.

---

## 4. Cum se rulează testele

Nu e nevoie de instalări — se folosește doar modulul `unittest` din
biblioteca standard Python.

### Toate testele
```bash
python -m unittest discover -s tests -v
```

### Doar o anumită strategie
```bash
python -m unittest tests.test_01_equivalence_partitioning -v
python -m unittest tests.test_02_boundary_value_analysis -v
# etc.
```

### Rezultatul așteptat
```
Ran 44 tests in 0.002s

OK
```

---

## 5. Structura proiectului

```
tss_project/
├── README.md                         # acest fișier
├── string_searcher.py                # clasa testată
└── tests/
    ├── __init__.py
    ├── test_01_equivalence_partitioning.py  ( 6 teste)
    ├── test_02_boundary_value_analysis.py   (12 teste)
    ├── test_03_statement_coverage.py        ( 3 teste)
    ├── test_04_branch_coverage.py           ( 8 teste)
    ├── test_05_condition_coverage.py        (10 teste)
    └── test_06_independent_circuits.py      ( 5 teste)
                                       ─────────────────
                                              44 teste
```

---

## 6. Ce urmează (predările 2/3 și 3/3)

Pentru următoarele etape vor fi adăugate:
- **Mutation testing** cu `mutmut` și teste suplimentare pentru a omorî
  2 mutanți neechivalenți (cerință explicită din enunț)
- **Raport coverage** detaliat (HTML) cu `coverage.py`
- **Diagrama CFG** completă cu draw.io
- **Raport tool AI** — comparația suită proprie vs. teste autogenerate

---

## 7. Referințe

[1] Beizer, Boris, *Software Testing Techniques*, Van Nostrand Reinhold,
ediția a 2-a, 1990.

[2] McCabe, Thomas J., *A Complexity Measure*, IEEE Transactions on
Software Engineering, vol. SE-2, nr. 4, 1976, pp. 308–320.

[3] Myers, Glenford J.; Sandler, Corey; Badgett, Tom, *The Art of
Software Testing*, Wiley, ediția a 3-a, 2011.

[4] Documentația oficială Python `unittest`,
https://docs.python.org/3/library/unittest.html, accesat 19 aprilie 2026.

[5] Wikipedia, *Cyclomatic complexity*,
https://en.wikipedia.org/wiki/Cyclomatic_complexity, accesat 19 aprilie
2026.
