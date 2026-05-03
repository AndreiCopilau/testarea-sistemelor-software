"""
Teste auxiliare pentru metodele helper (validate_n, get_history,
clear_history). Necesare pentru a atinge 100% statement & branch
coverage pe clasa StringSearcher.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from string_searcher import StringSearcher


class TestAuxiliaryMethods(unittest.TestCase):

    def setUp(self):
        self.searcher = StringSearcher()

    def test_validate_n_valid(self):
        self.assertTrue(self.searcher.validate_n(1))
        self.assertTrue(self.searcher.validate_n(10))
        self.assertTrue(self.searcher.validate_n(20))

    def test_validate_n_invalid(self):
        self.assertFalse(self.searcher.validate_n(0))
        self.assertFalse(self.searcher.validate_n(-3))
        self.assertFalse(self.searcher.validate_n(21))
        self.assertFalse(self.searcher.validate_n(100))

    def test_history_starts_empty(self):
        self.assertEqual(self.searcher.get_history(), [])

    def test_history_records_searches(self):
        self.searcher.search_character(3, 'abc', 'a', 'n')
        self.searcher.search_character(3, 'abc', 'b', 'n')
        history = self.searcher.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['position'], 1)
        self.assertEqual(history[1]['position'], 2)

    def test_history_does_not_record_invalid(self):
        """Cautarile invalide nu ajung sa actualizeze history."""
        self.searcher.search_character(0, '', 'a', 'n')
        self.searcher.search_character(3, None, 'a', 'n')
        self.assertEqual(self.searcher.get_history(), [])

    def test_clear_history(self):
        self.searcher.search_character(1, 'a', 'a', 'n')
        self.assertEqual(len(self.searcher.get_history()), 1)
        self.searcher.clear_history()
        self.assertEqual(self.searcher.get_history(), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
