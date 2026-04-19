"""
TEST FUNCTIONAL (a): Equivalence Partitioning
==============================================

1. Domeniul de intrari:
   - n: intreg pozitiv => 3 clase de echivalenta:
       N_1 = {n | 1 <= n <= 20}    (valid)
       N_2 = {n | n < 1}            (invalid - prea mic)
       N_3 = {n | n > 20}           (invalid - prea mare)
   - x: sirul de caractere (nu determina clase suplimentare)
   - c: caracter (nu determina clase suplimentare)
   - s (repeat_option): binar => 2 clase:
       S_1 = {'y'}
       S_2 = {'n'}

2. Domeniul de iesiri:
   - C_1(x) = {c | c se afla in x}
   - C_2(x) = {c | c nu se afla in x}

3. Clase globale (combinatii):
   C_111: n in N_1, c in C_1(x), s in S_1
   C_112: n in N_1, c in C_1(x), s in S_2
   C_121: n in N_1, c in C_2(x), s in S_1
   C_122: n in N_1, c in C_2(x), s in S_2
   C_2  : n in N_2
   C_3  : n in N_3

   Total: 6 clase => 6 reprezentanti / teste
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from string_searcher import StringSearcher


class TestEquivalencePartitioning(unittest.TestCase):
    """Cele 6 reprezentanti din clasele de echivalenta."""

    def setUp(self):
        self.searcher = StringSearcher()

    # C_111: n in [1,20], c se afla in x, s = 'y'
    # Reprezentant ales: (3, 'abc', 'a', 'y')
    def test_C111_valid_n_char_found_continue(self):
        result = self.searcher.search_character(3, 'abc', 'a', 'y')
        self.assertEqual(result['status'], 'OK')
        self.assertEqual(result['position'], 1)
        self.assertTrue(result['continue_search'])

    # C_112: n in [1,20], c se afla in x, s = 'n'
    def test_C112_valid_n_char_found_stop(self):
        result = self.searcher.search_character(3, 'abc', 'a', 'n')
        self.assertEqual(result['status'], 'OK')
        self.assertEqual(result['position'], 1)
        self.assertFalse(result['continue_search'])

    # C_121: n in [1,20], c NU se afla in x, s = 'y'
    def test_C121_valid_n_char_not_found_continue(self):
        result = self.searcher.search_character(3, 'abc', 'd', 'y')
        self.assertEqual(result['status'], 'OK')
        self.assertEqual(result['position'], -1)
        self.assertIn('does not appear', result['message'])
        self.assertTrue(result['continue_search'])

    # C_122: n in [1,20], c NU se afla in x, s = 'n'
    def test_C122_valid_n_char_not_found_stop(self):
        result = self.searcher.search_character(3, 'abc', 'd', 'n')
        self.assertEqual(result['status'], 'OK')
        self.assertEqual(result['position'], -1)
        self.assertFalse(result['continue_search'])

    # C_2: n < 1 (n = 0 reprezentant)
    def test_C2_n_too_small(self):
        result = self.searcher.search_character(0, '', 'a', 'n')
        self.assertEqual(result['status'], 'INVALID_N')
        self.assertIn('between 1 and 20', result['message'])

    # C_3: n > 20 (n = 25 reprezentant)
    def test_C3_n_too_large(self):
        result = self.searcher.search_character(
            25, 'a' * 25, 'a', 'n'
        )
        self.assertEqual(result['status'], 'INVALID_N')
        self.assertIn('between 1 and 20', result['message'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
