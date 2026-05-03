"""
TEST STRUCTURAL (c): Condition Coverage
=======================================

Conform suportului de curs (pagina 9), fiecare conditie individuala dintr-o
decizie compusa trebuie sa ia atat True cat si False.

Conditii individuale extrase din decizii (conform tabelului din curs):
| Decizie (nod CFG)                        | Conditii individuale          |
| while (n<1 || n>20) -- nod 4             | n < 1, n > 20                |
| for (i=0; i<n; i++) -- nod 6             | i < n                        |
| for (i=0; !found && i<n; i++) -- nod 14  | found, i < n                 |
| if (a[i] == c) -- nod 15                 | a[i] == c                    |
| if (found) -- nod 17                     | found                        |
| while (resp=='y' || resp=='Y') -- nod 24 | response=='y', response=='Y' |

Conform tabelului din curs (pagina 9):
| n=0                  | INVALID           | n<1=True                     |
| n=25                 | INVALID           | n>20=True                    |
| (1, 'a', 'A', 'y')  | poz 1, continua   | response=='y'=True           |
| (1, 'a', 'B', 'Y')  | nu apare, continua| response=='Y'=True           |
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from string_searcher import StringSearcher


class TestConditionCoverage(unittest.TestCase):
    """Acoperire la nivel de conditie individuala."""

    def setUp(self):
        self.searcher = StringSearcher()

    # === Conditia: n < 1 ===
    def test_cond_n_less_than_1_True(self):
        """n < 1 = True (n = 0)."""
        r = self.searcher.search_character(0, '', 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_N')

    def test_cond_n_less_than_1_False_and_n_greater_20_False(self):
        """n < 1 = False AND n > 20 = False (n in [1,20])."""
        r = self.searcher.search_character(5, 'abcde', 'a', 'n')
        self.assertEqual(r['status'], 'OK')

    # === Conditia: n > 20 ===
    def test_cond_n_greater_20_True(self):
        """n > 20 = True (n = 25)."""
        r = self.searcher.search_character(25, 'a' * 25, 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_N')

    # === Conditia: not found ===
    def test_cond_not_found_True_then_False(self):
        """not found ia True (la inceput), apoi False (cand gaseste)."""
        # Cazul: caracter pe pozitia 2 din 3 -> not found = True la i=0,
        # apoi devine False la i=1 dupa ce match-ul are loc
        r = self.searcher.search_character(3, 'abc', 'b', 'n')
        self.assertEqual(r['position'], 2)

    # === Conditia: i < n ===
    def test_cond_i_less_n_True_then_False(self):
        """i < n ia ambele valori - cand caracterul nu e gasit pana la final."""
        r = self.searcher.search_character(3, 'abc', 'd', 'n')
        self.assertEqual(r['position'], -1)

    # === Conditia: text[i] == c ===
    def test_cond_char_match_True(self):
        """text[i] == c = True"""
        r = self.searcher.search_character(1, 'a', 'a', 'n')
        self.assertEqual(r['position'], 1)

    def test_cond_char_match_False(self):
        """text[i] == c = False de fiecare data."""
        r = self.searcher.search_character(1, 'a', 'b', 'n')
        self.assertEqual(r['position'], -1)

    # === Conditia: repeat_option == 'y' ===
    def test_cond_repeat_lowercase_y(self):
        """== 'y' = True ; == 'Y' = False"""
        r = self.searcher.search_character(1, 'a', 'a', 'y')
        self.assertTrue(r['continue_search'])

    def test_cond_repeat_uppercase_Y(self):
        """== 'y' = False ; == 'Y' = True"""
        r = self.searcher.search_character(1, 'a', 'a', 'Y')
        self.assertTrue(r['continue_search'])

    def test_cond_repeat_both_False(self):
        """== 'y' = False ; == 'Y' = False"""
        r = self.searcher.search_character(1, 'a', 'a', 'n')
        self.assertFalse(r['continue_search'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
