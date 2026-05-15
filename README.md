# Proiect TSS — T1: Testare unitară în Python

**Materia:** Testarea Sistemelor Software
**Tema aleasă:** T1 — Testare unitară în Python
**Clasă testată:** `StringSearcher`

### Echipa
- Copilău Andrei
- Florea Mihai-Alexandru
- Piele Stefan-Vladut
- Filote Toma-Andrei

---

## 1. Configurația folosită

| Componentă | Versiune |
|---|---|
| Sistem de operare | Ubuntu 24.04 |
| Python | 3.12 |
| Framework testare unitară | `unittest` (standard library) |
| Tool acoperire cod | `coverage.py` 7.x |
| Tool mutation testing | `mutmut` 3.5.0 |
| Mașină virtuală | da - Oracle VM VirtualBox |

Instalare dependențe:

```bash
pip install coverage mutmut --break-system-packages
```

## Link-ul către videoclip:
https://youtu.be/hdYZ5AIYF4I

---

## 2. Structura proiectului

```
tss_project/
├── string_searcher.py            # clasa testată
├── tests/
│   ├── test_01_equivalence_partitioning.py
│   ├── test_02_boundary_value_analysis.py
│   ├── test_03_statement_coverage.py
│   ├── test_04_branch_coverage.py
│   ├── test_05_condition_coverage.py
│   ├── test_06_independent_circuits.py
│   ├── test_07_auxiliary.py
│   └── test_08_mutation_killers.py
├── docs/
│   ├── cfg.mermaid               # graf de flux de control 
│   ├── coverage_html/            # raport coverage HTML
│   ├── mutmut_results.txt        # raport mutație
│   └── ai_report.md              # raport folosire tool AI [7]
├── setup.cfg                     # config mutmut
└── README.md                     # acest fișier
```

---

## 3. Algoritmul testat — `StringSearcher`

Algoritmul reproduce și extinde exemplul folosit ca fir roșu în suportul de
curs: pentru un întreg `n` între 1 și 20, se introduce un șir `text` de
exact `n` caractere, apoi un caracter `c` care este căutat în `text`.
Programul returnează prima poziție pe care apare `c` (indexare 1-based)
sau un mesaj indicând că nu a fost găsit. Utilizatorul poate continua
căutarea (`'y'`/`'Y'`) sau opri (`'n'`/`'N'`).

### Specificație (pre/post-condiții)

**Pre-condiții:**
- `n` întreg, `1 ≤ n ≤ 20`
- `text` de lungime exact `n`
- `c` caracter (string de lungime 1)
- `repeat_option ∈ {'y', 'Y', 'n', 'N'}`

**Post-condiții:** dicționar cu cheile `status`, `position`, `message`,
`continue_search`.

### Diagramă CFG (graf de flux de control)

Graful de flux de control reproduce exact cel din suportul de curs, cu **16 noduri** și **22 arce**:

```
Noduri: 1-3, 4, 5, 6, 7, 8, 9-13, 14, 15, 16, 17, 18, 19-20, 21-23, 24, 25
```

```mermaid
flowchart TD
    %% Validare N - Bucla do-while de la inceput
    1_3((1-3)) --> 4{4}
    4 -- "n < 1 || n > 20" --> 1_3
    4 -- "False" --> 5[5]

    %% Citire caractere - Bucla for i < n
    5 --> 6{6}
    6 -- "True" --> 7[7]
    7 --> 6
    6 -- "False" --> 8[8]

    %% Initializare cautare
    8 --> 9_13((9-13))

    %% Bucla de cautare - for !found && i < n
    9_13 --> 14{14}
    14 -- "True (!found && i < n)" --> 15{15}

    %% Decizia if a[i] == c
    15 -- "True (a[i] == c)" --> 16[16]
    15 -- "False" --> 14
    16 --> 14

    %% Decizie afisare dupa bucla
    14 -- "False (Loop Exit)" --> 17{17}
    17 -- "True (found)" --> 18[18]
    17 -- "False" --> 19_20((19-20))

    %% Pregatire repetare
    18 --> 21_23((21-23))
    19_20 --> 21_23
    21_23 --> 24{24}

    %% Decizie finala - repeat?
    24 -- "True ('y' || 'Y')" --> 9_13
    24 -- "False" --> 25([25: END])

    %% Stiluri
    classDef decision fill:#fff4e6,stroke:#d97706,stroke-width:2px;
    classDef action fill:#e6f4ff,stroke:#1d4ed8,stroke-width:2px;
    classDef terminal fill:#f3e8ff,stroke:#7e22ce,stroke-width:2px;
    classDef groupNode fill:#fff,stroke:#333,stroke-width:2px;

    class 4,6,14,15,17,24 decision;
    class 5,7,8,16,18 action;
    class 25 terminal;
    class 1_3,9_13,19_20,21_23 groupNode;


Complexitatea ciclomatică McCabe:
```
V(G) = e - n + 1 = 22 - 16 + 1 = 7  (graf complet conectat)[2]
```

Vezi `docs/cfg.mermaid` (vizualizabil pe https://mermaid.live sau direct
în GitHub).

---

## 4. Strategii de testare aplicate

În total: **57 de teste**, organizate în 8 fișiere, fiecare ilustrând o
strategie distinctă din suportul de curs.

### 4.1. (Funcțional) Equivalence Partitioning — `test_01`

**Idee:** împărțim domeniul de intrare în clase de echivalență — toate
valorile dintr-o clasă sunt tratate identic de program, deci e suficient
să testăm un singur reprezentant din fiecare clasă.[3]

**Cum am identificat clasele:**

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

→ **6 reprezentanți = 6 teste**

### 4.2. (Funcțional) Boundary Value Analysis — `test_02`

**Idee:** valorile de pe frontiera claselor sunt o sursă majoră de
erori, așa că le testăm separat pe lângă reprezentanții generici.[3]

**Frontiere identificate:**
- pentru `n`: valorile **0, 1, 20, 21**
- pentru `c`: poziția pe care apare în `text` — **prima** sau **ultima**

**Distribuția testelor:**

| Clasă | Subcazuri | #teste |
|---|---|---|
| `C_111` | (1,'a','a','y') + (20, str20, 'a','y') + (20, str20, 'u','y') | 3 |
| `C_112` | identic dar cu `'n'` | 3 |
| `C_121` | (1,'a','b','y') + (20, str20, 'z','y') | 2 |
| `C_122` | identic dar cu `'n'` | 2 |
| `C_2`   | n = 0 | 1 |
| `C_3`   | n = 21 | 1 |

→ **Total: 12 teste**

### 4.3. (Structural) Statement Coverage — `test_03`

**Idee:** fiecare instrucțiune din metoda `search_character` trebuie
executată cel puțin o dată.[1]

Două teste atent alese acoperă tot codul principal:
1. Test pe drumul `valid + found + continue` (acoperă instrucțiunile din
   ramura `if found:` și din continuare cu `'y'`)
2. Test pe drumul `valid + not_found + stop` (acoperă ramura `else:` și
   oprirea cu `'n'`)

Plus un al treilea test pentru ramura de validare `n` invalidă.

→ **3 teste**

### 4.4. (Structural) Decision/Branch Coverage — `test_04`

Conform CFG-ului, deciziile sunt:
1. `while (n<1 || n>20)` — nod 4
2. `for (i=0; i<n; i++)` — nod 6
3. `for (i=0; !found && i<n; i++)` — nod 14
4. `if (a[i] == c)` — nod 15
5. `if (found)` — nod 17
6. `while ((response=='y') || (response=='Y'))` — nod 24

Plus deciziile Python-specifice pentru validare text și char.
→**8 teste.**

### 4.5. (Structural) Condition Coverage — `test_05`

**Idee:** când o decizie e compusă (`OR`/`AND`), vrem ca **fiecare
condiție individuală** din decizie să ia atât `True`, cât și `False`.
Asta merge mai departe decât branch coverage.[1]

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

→ **10 teste**

### 4.6. (Structural) Independent Circuits — `test_06`

Complexitatea ciclomatică McCabe conform cursului:
`V(G) = e − n + 1 = 22 − 16 + 1 = 7` (graf complet conectat).

Setul de bază conține **7 circuite independente**:

| # | Circuit | Caz testat |
|---|---|---|
| a | 1..3, 4, 5, 6, 8, 9..13, 14, 17, 18, 21..23, 24, 25, 1..3 | traseu complet, found=True |
| b | 1..3, 4, 5, 6, 8, 9..13, 14, 17, 19..20, 21..23, 24, 25, 1..3 | traseu complet, found=False |
| c | 1..3, 4, 1..3 | bucla do-while validare n |
| d | 6, 7, 6 | bucla for citire caractere |
| e | 14, 15, 14 | bucla căutare: a[i]!=c |
| f | 14, 15, 16, 14 | bucla căutare: a[i]==c |
| g | 9..13, 14, 17, 18, 21..23, 24, 9..13 | bucla repeat search |

→**7 teste.**

### 4.7. Teste auxiliare — `test_07`

Pentru `validate_n`, `get_history`, `clear_history`. 
→**6 teste.**

### 4.8. Mutation killers — `test_08` (vezi secțiunea 6)

→**5 teste** suplimentare pentru a omorî 2 mutanți neechivalenți.

---

## 5. Rezultate coverage

Comanda:
```bash
coverage run --source=. --omit="tests/*,mutants/*,*setup*" --branch -m unittest discover -s tests
coverage report -m
```

| Modul | Stmts | Miss | Branch | BrPart | Cover |
|---|---|---|---|---|---|
| `string_searcher.py` | 35 | 0 | 14 | 0 | **100%** |

Raportul HTML detaliat este în `docs/coverage_html/index.html`.[5]

---

## 6. Mutation testing

Tool: **mutmut 3.5.0**. Comandă: `mutmut run`.[6]

### Raport utilizare **unittest**
Alegerea unittest (standard library Python) a fost dictată de necesitatea unei structuri riguroase și a unei compatibilități native, fără dependențe externe pentru execuția de bază. Avantajele au fost:
- Este inclus în biblioteca standard Python, nefiind necesară instalarea prin pip
- Utilizează clase de test (TestCase), facilitând organizarea testelor pe strategii de testare
- Permite gruparea testelor în suite, lucru esențial pentru cele 44 de teste implementate

**Cum funcționează:**
Scanează fișierele de test, instanțiază clasele derivate din unittest.TestCase și execută fiecare metodă care începe cu prefixul test_. Acesta izolează fiecare caz de testare, asigurându-se că succesul sau eșecul unuia nu influențează restul suitei.[4]

### Raport utilizare **mutmut**
Mutmut a fost ales pentru simplitatea sa și capacitatea de a genera mutanți realiști în codul Python. Avantajele au fost:
- Generează automat mutanți (modificări de operatori, valori, condiții) fără intervenție manuală.
- Funcționează perfect cu unittest și raportează direct care teste au eșuat ("omorât mutanții").
- Permite re-rularea doar pentru mutanții care au supraviețuit ("suspicious mutants").

**Cum funcționează:**
Mutmut funcționează prin injectarea unor erori controlate (mutanți) direct în codul sursă, pentru a evalua eficiența suitei de teste existente. Procesul începe prin crearea unei copii modificate a codului, urmată de rularea automată a testelor unitare; dacă cel puțin un test eșuează, mutantul este considerat „omorât” (killed), validând astfel capacitatea testelor de a detecta defecte, însă dacă toate testele trec, mutantul „supraviețuiește” (survived), semnalând o breșă în acoperirea logică a suitei de testare.[6]

### 6.1. Rezultat inițial (cu primele 52 de teste)

| Categorie | Număr |
|---|---|
| Mutanți generați | 101 |
| Omorâți (killed) | 71 |
| Supraviețuitori (survived) | 29 |
| Timeout | 1 |

Scor inițial: **71/100 ≈ 71%**.

### 6.2. Mutanți aleși pentru omorât

Cerința din temă: *"teste suplimentare pentru a omorî 2 dintre mutanții
neechivalenți rămași în viață"*.

#### Mutant #8 — schimbă cheia `'position'` în `'XXpositionXX'` pe ramura `INVALID_N`

```diff
-            'position': -1,
+            'XXpositionXX': -1,
```

**De ce supraviețuiește:** testele de equivalence/BVA pentru `INVALID_N`
verifică doar `status`, nu accesează cheia `position` din răspuns.

**Test killer adăugat:**
```python
def test_kill_mutant_8_invalid_n_response_has_position_key(self):
    result = self.searcher.search_character(0, '', 'a', 'n')
    self.assertIn('position', result)
    self.assertEqual(result['position'], -1)
```

#### Mutant #72 — înlocuiește mesajul de "found" cu `None`

```diff
-        message = f'character {c} appears at position {position}'
+        message = None
```

**De ce supraviețuiește:** testele existente verifică doar `position`
când caracterul este găsit, nu și conținutul mesajului.

**Test killer adăugat:**
```python
def test_kill_mutant_72_found_message_contains_position(self):
    result = self.searcher.search_character(5, 'abcde', 'd', 'n')
    self.assertIsNotNone(result['message'])
    self.assertIn('position', result['message'].lower())
    self.assertIn('4', result['message'])
```

### 6.3. Rezultat după teste suplimentare

| Categorie | Înainte | După |
|---|---|---|
| Omorâți | 68 | **75** |
| Supraviețuitori | 32 | **25** |
| Timeout | 1 | 1 |

Scor: **75/100 = 75%** (+7 mutanți omorâți, inclusiv #8 și #72 țintiți
explicit + alți 5 omorâți colateral de aceleași aserțiuni).

### 6.4. Mutanți rămași — analiză

Mutanții rămași în viață sunt în mare parte:
- **echivalenți semantic**: ex. înlocuirea unui f-string cu un string
  literal care conține aceeași informație într-un context unde nu este
  testat;
- **modificări de mesaje** la care testele nu se uită (ex. textul
  exact al mesajului de validare INVALID_TEXT/INVALID_CHAR);
- **mutații pe constante string** care nu afectează ramurile testate.

Aceștia ar putea fi omorâți cu aserțiuni mai stricte pe câmpurile
`message`, dar consider scorul de 75% suficient pentru ilustrarea
cerinței.

---

## 7. Rulare

### Toate testele
```bash
python3 -m unittest discover -s tests -v
```

### Doar o categorie
```bash
python3 -m unittest tests.test_01_equivalence_partitioning -v
```

### Coverage
```bash
coverage run --source=. --omit="tests/*,mutants/*,*setup*" --branch -m unittest discover -s tests
coverage report -m
coverage html -d docs/coverage_html
```

### Mutation testing
```bash
mutmut run
mutmut results
mutmut show <id_mutant>
```

---

## 8. Referințe

[1] Beizer, Boris, *Software Testing Techniques*, Van Nostrand Reinhold,
ediția a 2-a, 1990.

[2] McCabe, Thomas J., *A Complexity Measure*, IEEE Transactions on
Software Engineering, vol. SE-2, nr. 4, 1976, pp. 308–320.

[3] Myers, Glenford J.; Sandler, Corey; Badgett, Tom, *The Art of
Software Testing*, Wiley, ediția a 3-a, 2011.

[4] Documentația oficială Python `unittest`,
https://docs.python.org/3/library/unittest.html, accesat 19 aprilie 2026.

[5] Documentația oficială `coverage.py`,
https://coverage.readthedocs.io, accesat 19 aprilie 2026.

[6] Documentația oficială `mutmut`,
https://mutmut.readthedocs.io, accesat 19 aprilie 2026.

[7] Anthropic, Claude (Opus 4.7), https://claude.ai, data generării: aprilie 2026.