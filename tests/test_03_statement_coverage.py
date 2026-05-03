"""
TEST STRUCTURAL (a): Statement Coverage
========================================

Conform CFG-ului din suportul de curs (pagina 5-6), nodurile grafului sunt:
    1-3, 4, 5, 6, 7, 8, 9-13, 14, 15, 16, 17, 18, 19-20, 21-23, 24, 25

Pentru a obtine acoperire la nivel de instructiune, ne concentram pe
instructiunile controlate de conditii. Conform tabelului din curs (pagina 6):

| Intrari                   | Rezultat               | Instructiuni parcurse                                      |
| n=1, x='a', c='a', s='y' | poz 1; cere alt char   | 1..3,4,5,6,7,6,8,9..13,14,15,16,14,17,18,21..23,24,9..13 |
| ..., c='b', s='n'         | nu apare               | 14,15,14,17,19..20,21..23,24,25                           |

Doua teste atent alese acopera toate instructiunile (nodurile) grafului.
In implementarea Python, buclele do-while (1-3/4 si 9-13/24) sunt inlocuite
de validari si parametri, dar acoperirea instructiunilor ramane echivalenta.
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
        Acopera nodurile: 4(False),5,6(True),7,6(False),8,9-13,14(True),
        15(True),16,14(False),17(True),18,21-23,24(True) => continue
        Instructiuni parcurse: validare n OK, citire caractere, cautare cu
        match pe prima pozitie (a[i]==c => True, nod 15->16), afisare pozitie
        (nod 18), continuare cautare (nod 24 => True).
        """
        r = self.searcher.search_character(1, 'a', 'a', 'y')
        self.assertEqual(r['position'], 1)
        self.assertEqual(r['status'], 'OK')
        self.assertTrue(r['continue_search'])

    def test_statement_coverage_path_2(self):
        """
        Acopera nodurile: 14(True),15(False),14(False),17(False),19-20,
        21-23,24(False),25
        Instructiuni parcurse: cautare fara match (nod 15 => False de fiecare
        data), afisare 'nu apare' (nod 19-20), oprire (nod 24 => False),
        terminare (nod 25: END).
        """
        r = self.searcher.search_character(1, 'a', 'b', 'n')
        self.assertEqual(r['position'], -1)
        self.assertEqual(r['status'], 'OK')
        self.assertFalse(r['continue_search'])

    def test_statement_coverage_invalid_n(self):
        """
        Acopera nodul 4(True) => reintoarcere la 1-3 (in curs, do-while).
        In implementarea Python, echivalent cu returnarea INVALID_N.
        Cu cele 2 teste de mai sus + acesta avem statement coverage 100%.
        """
        r = self.searcher.search_character(0, '', 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_N')


if __name__ == '__main__':
    unittest.main(verbosity=2)
