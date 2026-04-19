"""
TEST STRUCTURAL (a): Statement Coverage
========================================

Pentru a obtine acoperire la nivel de instructiune, ne concentram pe
instructiunile controlate de conditii. Conform tabelului din curs:

| Intrari | Rezultat | Instructiuni parcurse |
| n=1, x='a', c='a', s='y' | poz 1; cere alt char | 1..3,4,5,6,7,6,8,9..13,14,15,16,14,17,18,21..23,24,9..13 |
| ..., c='b', s='n'        | nu apare             | 14,15,14,17,19..20,21..23,24,25 |

Doua teste atent alese acopera toate instructiunile metodei principale.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from string_searcher import StringSearcher


class TestStatementCoverage(unittest.TestCase):
    """Acoperire la nivel de instructiune (statement coverage)."""

    def setUp(self):
        self.searcher = StringSearcher()

    def test_statement_coverage_path_1(self):
        """
        Acopera ramura found=True + continue_search=True
        Instructiuni parcurse: validare n OK, validare text OK, validare c OK,
        intra in while-ul de cautare, gaseste pe prima pozitie (a[i]==c => True),
        intra pe ramura if(found), seteaza continue=True (decizia
        'y'||'Y' ==> True pe primul operand).
        """
        r = self.searcher.search_character(1, 'a', 'a', 'y')
        self.assertEqual(r['position'], 1)
        self.assertEqual(r['status'], 'OK')
        self.assertTrue(r['continue_search'])

    def test_statement_coverage_path_2(self):
        """
        Acopera ramura found=False + continue_search=False
        Instructiuni parcurse: validare n OK, validare text OK, validare c OK,
        intra in while-ul de cautare, NU gaseste (a[i]==c => False de fiecare data),
        intra pe ramura else (not found), seteaza continue=False
        (ambele conditii False).
        """
        r = self.searcher.search_character(1, 'a', 'b', 'n')
        self.assertEqual(r['position'], -1)
        self.assertEqual(r['status'], 'OK')
        self.assertFalse(r['continue_search'])

    def test_statement_coverage_invalid_n(self):
        """
        Acopera instructiunile din ramura de validare n (INVALID_N).
        Cu cele 2 teste de mai sus + acesta avem statement coverage 100%
        pe metoda search_character.
        """
        r = self.searcher.search_character(0, '', 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_N')


if __name__ == '__main__':
    unittest.main(verbosity=2)
