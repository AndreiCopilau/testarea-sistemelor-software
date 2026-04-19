"""
TEST STRUCTURAL (b): Decision Coverage / Branch Coverage
========================================================

Decizii din metoda search_character:
    (1) n < MIN_LENGTH or n > MAX_LENGTH         (validare n)
    (2) text is None or len(text) != n           (validare text)
    (3) c is None or len(c) != 1                 (validare c)
    (4) (not found) and (i < n)                  (loop de cautare)
    (5) text[i] == c                             (match caracter)
    (6) if found                                 (rezultat cautare)
    (7) repeat_option == 'y' or repeat_option == 'Y'  (continuare)

Pentru branch coverage, fiecare decizie trebuie sa ia atat True cat si False.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from string_searcher import StringSearcher


class TestBranchCoverage(unittest.TestCase):
    """Acoperire la nivel de ramura. Conform tabelului din curs:
    (25, _, _, _) -> validare n False (in sensul invers: n>20 => True)
    (1, 'a', 'a', 'y') -> gaseste, continua
    (1, 'a', 'b', 'n') -> nu gaseste, opreste
    """

    def setUp(self):
        self.searcher = StringSearcher()

    def test_branch_invalid_n_too_large(self):
        """Decizia (1) = True (ramura True a validarii n)."""
        r = self.searcher.search_character(25, 'a' * 25, 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_N')

    def test_branch_invalid_n_too_small(self):
        """Decizia (1) = True pe celalalt operand."""
        r = self.searcher.search_character(0, '', 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_N')

    def test_branch_found_and_continue(self):
        """Decizia (1)=False, (4) ia ambele valori, (5)=True, (6)=True,
        (7)=True (primul operand)."""
        r = self.searcher.search_character(1, 'a', 'a', 'y')
        self.assertEqual(r['position'], 1)
        self.assertTrue(r['continue_search'])

    def test_branch_not_found_and_stop(self):
        """(5)=False de fiecare data, (6)=False, (7)=False pe ambii operanzi."""
        r = self.searcher.search_character(1, 'a', 'b', 'n')
        self.assertEqual(r['position'], -1)
        self.assertFalse(r['continue_search'])

    def test_branch_invalid_text_none(self):
        """Decizia (2) = True (ramura None pe text)."""
        r = self.searcher.search_character(3, None, 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_TEXT')

    def test_branch_invalid_text_wrong_length(self):
        """Decizia (2) = True pe celalalt operand (len(text) != n)."""
        r = self.searcher.search_character(3, 'ab', 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_TEXT')

    def test_branch_invalid_char_none(self):
        """Decizia (3) = True (c is None)."""
        r = self.searcher.search_character(3, 'abc', None, 'n')
        self.assertEqual(r['status'], 'INVALID_CHAR')

    def test_branch_invalid_char_wrong_length(self):
        """Decizia (3) = True (len(c) != 1)."""
        r = self.searcher.search_character(3, 'abc', 'ab', 'n')
        self.assertEqual(r['status'], 'INVALID_CHAR')


if __name__ == '__main__':
    unittest.main(verbosity=2)
