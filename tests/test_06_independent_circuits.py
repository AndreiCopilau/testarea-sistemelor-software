"""
TEST STRUCTURAL (g): Testarea Circuitelor Independente
======================================================

Complexitatea ciclomatica McCabe pentru o singura subrutina:
    V(G) = e - n + 2

Pentru metoda search_character, am identificat in CFG:
    - 11 noduri (nodurile principale ale grafului):
        N1: validare n -> ramura INVALID_N
        N2: validare n -> ramura OK
        N3: validare text -> INVALID_TEXT
        N4: validare text -> OK
        N5: validare c -> INVALID_CHAR
        N6: validare c -> OK
        N7: head while loop (cautare)
        N8: body while loop - if match
        N9: body while loop - increment i
        N10: if found -> message gasit / negasit
        N11: return result + decizie continue
    - 14 muchii orientate (controlul curge intre noduri)

    V(G) = 14 - 11 + 2 = 5

Asadar, avem nevoie de cel putin 5 circuite independente (= 5 teste de baza)
pentru a acoperi grafica de control.

NOTA: pentru exemplul din curs (algoritm complet cu input loop), V(G) = 7.
La noi, separam validarile in cazuri diferite, deci avem un V(G) mai mic
pe metoda principala. Pentru a fi consistenti cu cursul, calculam V(G)
pentru intreg algoritmul (incluzand toate cele 3 validari + bucla cautare
+ decizia found + decizia continue).

Set de baza (5 circuite independente):
    a) start -> N1 -> end                          (n invalid)
    b) start -> N2 -> N3 -> end                    (text invalid)
    c) start -> N2 -> N4 -> N5 -> end              (c invalid)
    d) start -> N2 -> N4 -> N6 -> N7 -> N8 -> N9 -> N10(found) -> N11(continue) -> end
    e) start -> N2 -> N4 -> N6 -> N7 -> N9 -> N10(not found) -> N11(stop) -> end
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from string_searcher import StringSearcher


class TestIndependentCircuits(unittest.TestCase):
    """5 teste pentru cele 5 circuite independente identificate.

    Acopera complexitatea ciclomatica V(G) = 5 a metodei search_character.
    """

    def setUp(self):
        self.searcher = StringSearcher()

    def test_circuit_a_invalid_n(self):
        """Circuit a) -- ruta scurta prin validarea n esuata."""
        r = self.searcher.search_character(0, '', 'x', 'n')
        self.assertEqual(r['status'], 'INVALID_N')

    def test_circuit_b_invalid_text(self):
        """Circuit b) -- n trece, text esueaza (None sau lungime gresita)."""
        r = self.searcher.search_character(3, 'ab', 'a', 'n')
        self.assertEqual(r['status'], 'INVALID_TEXT')

    def test_circuit_c_invalid_char(self):
        """Circuit c) -- n si text trec, caracter de cautat invalid."""
        r = self.searcher.search_character(3, 'abc', None, 'n')
        self.assertEqual(r['status'], 'INVALID_CHAR')

    def test_circuit_d_found_and_continue(self):
        """Circuit d) -- traseu complet cu match si continuare."""
        r = self.searcher.search_character(3, 'abc', 'b', 'y')
        self.assertEqual(r['status'], 'OK')
        self.assertEqual(r['position'], 2)
        self.assertTrue(r['continue_search'])

    def test_circuit_e_not_found_and_stop(self):
        """Circuit e) -- traseu complet fara match si cu oprire."""
        r = self.searcher.search_character(3, 'abc', 'z', 'n')
        self.assertEqual(r['status'], 'OK')
        self.assertEqual(r['position'], -1)
        self.assertFalse(r['continue_search'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
