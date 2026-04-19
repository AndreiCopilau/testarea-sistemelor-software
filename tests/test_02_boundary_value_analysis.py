"""
TEST FUNCTIONAL (b): Boundary Value Analysis (BVA)
==================================================

Valori de frontiera identificate (din clasele de echivalenta):
    - n: 0, 1, 20, 21
    - c: poate fi pe prima sau pe ultima pozitie din x

Distributia testelor:
    N_1: 1, 20
    N_2: 0
    N_3: 21
    C_1: c_11 = c pe prima pozitie din x
         c_12 = c pe ultima pozitie din x

Total cazuri:
    C_111: (1, 'a', 'a', 'y), (20, '...', 'a', 'y), (20, '...', 'u', 'y)
                                                          (3 cazuri)
    C_112: la fel cu 'n' in loc de 'y'                    (3 cazuri)
    C_121: (1, 'a', 'b', 'y'), (20, '...', 'z', 'y')      (2 cazuri)
    C_122: la fel cu 'n' in loc de 'y'                    (2 cazuri)
    C_2  : (0, _, _, _)                                    (1 caz)
    C_3  : (21, _, _, _)                                   (1 caz)
                                                  ------------------
                                                  Total: 12 teste
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from string_searcher import StringSearcher


class TestBoundaryValueAnalysis(unittest.TestCase):
    """12 teste BVA conform tabelului din suportul de curs."""

    # Sirul de 20 de caractere folosit in cursul (litere distincte)
    STRING_20 = 'abcdefghijklmnoprstu'  # exact 20 caractere

    def setUp(self):
        self.searcher = StringSearcher()
        # verificare lungime
        assert len(self.STRING_20) == 20

    # === C_111: valid, found, continue ===
    # (1, 'a', 'a', 'y')
    def test_C111_n1_first_pos_continue(self):
        r = self.searcher.search_character(1, 'a', 'a', 'y')
        self.assertEqual(r['position'], 1)
        self.assertTrue(r['continue_search'])

    # (20, STRING_20, 'a', 'y') - c pe prima pozitie
    def test_C111_n20_first_pos_continue(self):
        r = self.searcher.search_character(20, self.STRING_20, 'a', 'y')
        self.assertEqual(r['position'], 1)
        self.assertTrue(r['continue_search'])

    # (20, STRING_20, 'u', 'y') - c pe ultima pozitie
    def test_C111_n20_last_pos_continue(self):
        r = self.searcher.search_character(20, self.STRING_20, 'u', 'y')
        self.assertEqual(r['position'], 20)
        self.assertTrue(r['continue_search'])

    # === C_112: valid, found, stop ===
    def test_C112_n1_first_pos_stop(self):
        r = self.searcher.search_character(1, 'a', 'a', 'n')
        self.assertEqual(r['position'], 1)
        self.assertFalse(r['continue_search'])

    def test_C112_n20_first_pos_stop(self):
        r = self.searcher.search_character(20, self.STRING_20, 'a', 'n')
        self.assertEqual(r['position'], 1)
        self.assertFalse(r['continue_search'])

    def test_C112_n20_last_pos_stop(self):
        r = self.searcher.search_character(20, self.STRING_20, 'u', 'n')
        self.assertEqual(r['position'], 20)
        self.assertFalse(r['continue_search'])

    # === C_121: valid, NOT found, continue ===
    def test_C121_n1_not_found_continue(self):
        r = self.searcher.search_character(1, 'a', 'b', 'y')
        self.assertEqual(r['position'], -1)
        self.assertTrue(r['continue_search'])

    def test_C121_n20_not_found_continue(self):
        r = self.searcher.search_character(20, self.STRING_20, 'z', 'y')
        self.assertEqual(r['position'], -1)
        self.assertTrue(r['continue_search'])

    # === C_122: valid, NOT found, stop ===
    def test_C122_n1_not_found_stop(self):
        r = self.searcher.search_character(1, 'a', 'b', 'n')
        self.assertEqual(r['position'], -1)
        self.assertFalse(r['continue_search'])

    def test_C122_n20_not_found_stop(self):
        r = self.searcher.search_character(20, self.STRING_20, 'z', 'n')
        self.assertEqual(r['position'], -1)
        self.assertFalse(r['continue_search'])

    # === C_2: n < 1 (boundary: n = 0) ===
    def test_C2_boundary_n_zero(self):
        r = self.searcher.search_character(0, '', 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_N')

    # === C_3: n > 20 (boundary: n = 21) ===
    def test_C3_boundary_n_21(self):
        r = self.searcher.search_character(21, 'a' * 21, 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_N')


if __name__ == '__main__':
    unittest.main(verbosity=2)
