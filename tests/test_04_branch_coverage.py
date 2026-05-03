"""
TEST STRUCTURAL (b): Decision Coverage / Branch Coverage
========================================================

Conform CFG-ului din suportul de curs (pagina 8), deciziile sunt:
    (1) while (n<1 || n>20)                      -- nod 4
    (2) for (i=0; i<n; i++)                      -- nod 6
    (3) for (i=0; !found && i<n; i++)            -- nod 14
    (4) if (a[i] == c)                           -- nod 15
    (5) if (found)                               -- nod 17
    (6) while ((response=='y') || (response=='Y'))  -- nod 24

In implementarea Python, deciziile (2) si (6) sunt implicite (text e parametru,
repeat_option e parametru), iar decizia (1) corespunde validarii n.
Se adauga deciziile Python-specifice pentru validare text (nod N2) si char (nod N3).

Pentru branch coverage, fiecare decizie trebuie sa ia atat True cat si False.

Conform tabelului din curs (pagina 8):
| Intrari                   | Rezultat               | Decizii acoperite |
| n=25                      | Cere reintroducere     | (1)=True          |
| n=1, x='a', c='a', s='y' | Afiseaza pozitia 1     | (1)=F,(3)=T/F,(4)=T,(5)=T,(6)=T |
| ..., c='b', s='n'         | Nu apare               | (4)=F,(5)=F,(6)=F |
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from string_searcher import StringSearcher


class TestBranchCoverage(unittest.TestCase):
    """Acoperire la nivel de ramura. Conform tabelului din curs (pagina 8):
    (25, _, _, _) -> nod 4: True (n>20, reintoarcere la 1-3)
    (1, 'a', 'a', 'y') -> nod 4:F, 14:T/F, 15:T, 17:T, 24:T
    (1, 'a', 'b', 'n') -> nod 15:F, 17:F, 24:F->25:END
    """

    def setUp(self):
        self.searcher = StringSearcher()

    def test_branch_invalid_n_too_large(self):
        """Nod 4: True (n>20 => reintoarcere la 1-3). In Python: INVALID_N."""
        r = self.searcher.search_character(25, 'a' * 25, 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_N')

    def test_branch_invalid_n_too_small(self):
        """Nod 4: True (n<1 => reintoarcere la 1-3). In Python: INVALID_N."""
        r = self.searcher.search_character(0, '', 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_N')

    def test_branch_found_and_continue(self):
        """Nod 4:False, 14:True/False, 15:True(match), 17:True(found),
        24:True(continue)."""
        r = self.searcher.search_character(1, 'a', 'a', 'y')
        self.assertEqual(r['position'], 1)
        self.assertTrue(r['continue_search'])

    def test_branch_not_found_and_stop(self):
        """Nod 15:False(no match), 17:False(not found), 24:False(stop)->25:END."""
        r = self.searcher.search_character(1, 'a', 'b', 'n')
        self.assertEqual(r['position'], -1)
        self.assertFalse(r['continue_search'])

    def test_branch_invalid_text_none(self):
        """Validare text: True (text is None). Python-specific, nod implicit."""
        r = self.searcher.search_character(3, None, 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_TEXT')

    def test_branch_invalid_text_wrong_length(self):
        """Validare text: True (len(text) != n). Python-specific, nod implicit."""
        r = self.searcher.search_character(3, 'ab', 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_TEXT')

    def test_branch_invalid_char_none(self):
        """Validare c: True (c is None). Python-specific, nod implicit."""
        r = self.searcher.search_character(3, 'abc', None, 'n')
        self.assertEqual(r['status'], 'INVALID_CHAR')

    def test_branch_invalid_char_wrong_length(self):
        """Validare c: True (len(c) != 1). Python-specific, nod implicit."""
        r = self.searcher.search_character(3, 'abc', 'ab', 'n')
        self.assertEqual(r['status'], 'INVALID_CHAR')


if __name__ == '__main__':
    unittest.main(verbosity=2)
