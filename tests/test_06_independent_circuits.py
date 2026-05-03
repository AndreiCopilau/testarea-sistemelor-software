"""
TEST STRUCTURAL (g): Testarea Circuitelor Independente
======================================================

Complexitatea ciclomatica McCabe (conform suportului de curs, pagina 14):

    Graful complet conectat (arc de la 25 la 1):
        n = 16 noduri, e = 22 arce
        V(G) = e - n + 1 = 22 - 16 + 1 = 7

    (sau, fara arcul de inchidere: V(G) = e - n + 2 = 21 - 16 + 2 = 7)

Asadar, avem nevoie de 7 circuite independente.

Set de baza conform cursului (pagina 14):
    a) 1..3, 4, 5, 6, 8, 9..13, 14, 17, 18, 21..23, 24, 25, 1..3
       => traseu complet: found=True, afisare pozitie
    b) 1..3, 4, 5, 6, 8, 9..13, 14, 17, 19..20, 21..23, 24, 25, 1..3
       => traseu complet: found=False, afisare 'nu apare'
    c) 1..3, 4, 1..3
       => bucla do-while validare n (n invalid => re-prompt)
    d) 6, 7, 6
       => bucla for citire caractere (iteratie suplimentara)
    e) 14, 15, 14
       => bucla cautare: a[i]!=c, continua cautarea
    f) 14, 15, 16, 14
       => bucla cautare: a[i]==c, found=true
    g) 9..13, 14, 17, 18, 21..23, 24, 9..13
       => bucla repeat: utilizatorul continua cautarea (response='y'/'Y')

In implementarea Python, buclele interactive (c, d, g) sunt simulate prin
parametri. Testele acopera toate cele 7 circuite prin echivalenta functionala.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from string_searcher import StringSearcher


class TestIndependentCircuits(unittest.TestCase):
    """7 teste pentru cele 7 circuite independente identificate.

    Acopera complexitatea ciclomatica V(G) = 7 conform cursului (pagina 14).
    """

    def setUp(self):
        self.searcher = StringSearcher()

    def test_circuit_a_full_path_found(self):
        """Circuit a) 1..3,4,5,6,8,9..13,14,17,18,21..23,24,25
        Traseu complet: caracter gasit, afisare pozitie, oprire."""
        r = self.searcher.search_character(3, 'abc', 'b', 'n')
        self.assertEqual(r['status'], 'OK')
        self.assertEqual(r['position'], 2)
        self.assertEqual(r['message'], 'character b appears at position 2')
        self.assertFalse(r['continue_search'])

    def test_circuit_b_full_path_not_found(self):
        """Circuit b) 1..3,4,5,6,8,9..13,14,17,19..20,21..23,24,25
        Traseu complet: caracter negasit, afisare 'nu apare', oprire."""
        r = self.searcher.search_character(3, 'abc', 'z', 'n')
        self.assertEqual(r['status'], 'OK')
        self.assertEqual(r['position'], -1)
        self.assertIn('does not appear', r['message'])
        self.assertFalse(r['continue_search'])

    def test_circuit_c_validation_loop(self):
        """Circuit c) 1..3,4,1..3
        Bucla do-while validare n (n invalid => re-prompt).
        In Python: return INVALID_N."""
        r = self.searcher.search_character(0, '', 'x', 'n')
        self.assertEqual(r['status'], 'INVALID_N')

    def test_circuit_d_char_reading_loop(self):
        """Circuit d) 6,7,6
        Bucla for citire caractere - iteratii multiple.
        In Python: text cu mai multe caractere (n>1) exercita bucla."""
        r = self.searcher.search_character(5, 'abcde', 'e', 'n')
        self.assertEqual(r['status'], 'OK')
        self.assertEqual(r['position'], 5)

    def test_circuit_e_search_loop_no_match(self):
        """Circuit e) 14,15,14
        Bucla cautare: a[i]!=c, nod 15 => False, intoarcere la 14."""
        r = self.searcher.search_character(3, 'abc', 'c', 'n')
        self.assertEqual(r['status'], 'OK')
        self.assertEqual(r['position'], 3)

    def test_circuit_f_search_loop_match(self):
        """Circuit f) 14,15,16,14
        Bucla cautare: a[i]==c, nod 15 => True, nod 16 (found=true)."""
        r = self.searcher.search_character(1, 'a', 'a', 'n')
        self.assertEqual(r['status'], 'OK')
        self.assertEqual(r['position'], 1)

    def test_circuit_g_repeat_search(self):
        """Circuit g) 9..13,14,17,18,21..23,24,9..13
        Bucla repeat: utilizatorul continua cautarea (response='y').
        In Python: continue_search=True."""
        r = self.searcher.search_character(3, 'abc', 'a', 'y')
        self.assertEqual(r['status'], 'OK')
        self.assertEqual(r['position'], 1)
        self.assertTrue(r['continue_search'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
