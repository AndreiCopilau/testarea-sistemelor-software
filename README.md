# Proiect TSS — T1: Testare unitară în Python

**Materia:** Testarea Sistemelor Software
**Tema aleasă:** T1 — Testare unitară în Python
**Clasă testată:** `StringSearcher`

---

## 1. Configurația folosită + componența echipei

| Componentă | Versiune |
|---|---|
| Sistem de operare | Ubuntu 24.04 |
| Python | 3.12 |
| Framework testare unitară | `unittest` (standard library) |
| Tool acoperire cod | `coverage.py` 7.x |
| Tool mutation testing | `mutmut` 3.5.0 |
| Mașină virtuală | nu (rulare directă) |

Instalare dependințe:

```bash
pip install coverage mutmut --break-system-packages
```

### Echipa
- Copilău Andrei
- Florea Mihai-Alexandru
- Piele Stefan-Vladut
- Filote Toma-Andrei

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
│   ├── cfg.mermaid               # graf de flux de control (corect)
│   ├── coverage_html/            # raport coverage HTML
│   ├── mutmut_results.txt        # raport mutație
│   └── ai_report.md              # raport folosire tool AI
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

Graful de flux de control reproduce exact cel din suportul de curs
(pagina 5), cu **16 noduri** și **22 arce**:

```
Noduri: 1-3, 4, 5, 6, 7, 8, 9-13, 14, 15, 16, 17, 18, 19-20, 21-23, 24, 25
```

Complexitatea ciclomatică McCabe (pagina 14):
```
V(G) = e - n + 1 = 22 - 16 + 1 = 7  (graf complet conectat)
```

Vezi `docs/cfg.mermaid` (vizualizabil pe https://mermaid.live sau direct
în GitHub).

---

## 4. Strategii de testare aplicate

În total: **57 de teste**, organizate în 8 fișiere, fiecare ilustrând o
strategie distinctă din suportul de curs.

### 4.1. (Funcțional) Equivalence Partitioning — `test_01`

Domeniul de intrare al lui `n` se descompune în trei clase:
`N_1 = {1..20}`, `N_2 = {n | n < 1}`, `N_3 = {n | n > 20}`. Opțiunea de
continuare are două clase: `S_1 = {'y'}`, `S_2 = {'n'}`. Domeniul de
ieșire dă două clase pentru caracter: `C_1(x) = {c | c ∈ x}`,
`C_2(x) = {c | c ∉ x}`. Combinând se obțin 6 clase globale:
`C_111`, `C_112`, `C_121`, `C_122`, `C_2`, `C_3`. Câte un reprezentant
din fiecare clasă → **6 teste**.

### 4.2. (Funcțional) Boundary Value Analysis — `test_02`

Pe lângă reprezentanții din clasele de echivalență, se aleg valorile
de frontieră: `n ∈ {0, 1, 20, 21}`, iar pentru `c` se testează poziția
1 și poziția `n` în `text`. Conform metodologiei din suportul de curs,
rezultă **12 teste**.

### 4.3. (Structural) Statement Coverage — `test_03`

Conform CFG-ului din suportul de curs (pagina 5-6), nodurile grafului sunt:
`1-3, 4, 5, 6, 7, 8, 9-13, 14, 15, 16, 17, 18, 19-20, 21-23, 24, 25`.

Două teste atent alese acoperă toate instrucțiunile (nodurile) grafului,
plus un al treilea pentru ramura de validare `n` invalidă (nod 4 → True).
**3 teste.**

### 4.4. (Structural) Decision/Branch Coverage — `test_04`

Conform CFG-ului (pagina 8), deciziile sunt:
1. `while (n<1 || n>20)` — nod 4
2. `for (i=0; i<n; i++)` — nod 6
3. `for (i=0; !found && i<n; i++)` — nod 14
4. `if (a[i] == c)` — nod 15
5. `if (found)` — nod 17
6. `while ((response=='y') || (response=='Y'))` — nod 24

Plus deciziile Python-specifice pentru validare text și char.
**8 teste.**

### 4.5. (Structural) Condition Coverage — `test_05`

Conform tabelului din curs (pagina 9), condițiile individuale sunt:
`n < 1`, `n > 20`, `i < n`, `found`, `a[i] == c`, `response == 'y'`,
`response == 'Y'`. Fiecare ia atât True cât și False. **10 teste.**

### 4.6. (Structural) Independent Circuits — `test_06`

Complexitatea ciclomatică McCabe conform cursului (pagina 14):
`V(G) = e − n + 1 = 22 − 16 + 1 = 7` (graf complet conectat).

Setul de bază conține **7 circuite independente** (pagina 14):

| # | Circuit | Caz testat |
|---|---|---|
| a | 1..3, 4, 5, 6, 8, 9..13, 14, 17, 18, 21..23, 24, 25, 1..3 | traseu complet, found=True |
| b | 1..3, 4, 5, 6, 8, 9..13, 14, 17, 19..20, 21..23, 24, 25, 1..3 | traseu complet, found=False |
| c | 1..3, 4, 1..3 | bucla do-while validare n |
| d | 6, 7, 6 | bucla for citire caractere |
| e | 14, 15, 14 | bucla căutare: a[i]!=c |
| f | 14, 15, 16, 14 | bucla căutare: a[i]==c |
| g | 9..13, 14, 17, 18, 21..23, 24, 9..13 | bucla repeat search |

**7 teste.**

### 4.7. Teste auxiliare — `test_07`

Pentru `validate_n`, `get_history`, `clear_history`. **6 teste.**

### 4.8. Mutation killers — `test_08` (vezi secțiunea 6)

**5 teste** suplimentare pentru a omorî 2 mutanți neechivalenți.

---

## 5. Rezultate coverage

Comanda:
```bash
coverage run --source=. --omit="tests/*,mutants/*,*setup*" --branch \
    -m unittest discover -s tests
coverage report -m
```

| Modul | Stmts | Miss | Branch | BrPart | Cover |
|---|---|---|---|---|---|
| `string_searcher.py` | 35 | 0 | 14 | 0 | **100%** |

Raportul HTML detaliat este în `docs/coverage_html/index.html`.

---

## 6. Mutation testing

Tool: **mutmut 3.5.0**. Comandă: `mutmut run`.

### 6.1. Rezultat inițial (cu primele 50 de teste)

| Categorie | Număr |
|---|---|
| Mutanți generați | 101 |
| Omorâți (killed) | 68 |
| Supraviețuitori (survived) | 32 |
| Timeout | 1 |

Scor inițial: **68/100 ≈ 68%**.

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
explicit + alte 5 omorâți colateral de aceleași aserțiuni).

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
python -m unittest discover -s tests -v
```

### Doar o categorie
```bash
python -m unittest tests.test_01_equivalence_partitioning -v
```

### Coverage
```bash
coverage run --source=. --omit="tests/*,mutants/*,*setup*" --branch \
    -m unittest discover -s tests
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

[4] Ostrand, Thomas J.; Balcer, Marc J., *The Category-Partition Method
for Specifying and Generating Functional Tests*, Communications of the
ACM, vol. 31, nr. 6, 1988, pp. 676–686.
