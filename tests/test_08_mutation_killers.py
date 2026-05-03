"""
TESTE SUPLIMENTARE PENTRU MUTATION TESTING
==========================================

Conform cerintei din tema (T1):
    "analiza raport creat de generatorul de mutanti, teste suplimentare
     pentru a omori 2 dintre mutantii neechivalenti ramasi in viata"

Tool folosit: mutmut 3.5.0
Comanda:      mutmut run

REZULTAT INITIAL (cu cele 50 de teste din strategiile clasice):
    - 101 mutanti generati
    - 68 omorati (killed)
    - 32 supravietuiesc (survived)
    -  1 timeout

ANALIZA MUTANTILOR ALESI (neechivalenti = chiar schimba comportamentul
observabil):

----------------------------------------------------------------------
MUTANTUL 8 -- search_character__mutmut_8
----------------------------------------------------------------------
Diferenta:
    -            'position': -1,
    +            'XXpositionXX': -1,
(in branch-ul INVALID_N)

De ce supravietuieste: testele de equivalence/BVA pentru INVALID_N
verifica doar 'status', nu si 'position'.

Test pentru a-l omori: verificam ca pe INVALID_N raspunsul are cheia
'position' = -1.

----------------------------------------------------------------------
MUTANTUL 72 -- search_character__mutmut_72
----------------------------------------------------------------------
Diferenta:
    -        message = f'character {c} appears at position {position}'
    +        message = None
(in branch-ul if found:)

De ce supravietuieste: testele existente verifica 'position', dar nu si
continutul exact al campului 'message' atunci cand caracterul e gasit.

Test pentru a-l omori: verificam ca pe found=True, mesajul este un sir
non-None care contine caracterul cautat si pozitia.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from string_searcher import StringSearcher


class TestMutationKillers(unittest.TestCase):
    """Teste suplimentare construite explicit pentru a omori mutantii
    neechivalenti supravietuitori identificati de mutmut."""

    def setUp(self):
        self.searcher = StringSearcher()

    # ==========================================================
    # Test pentru a omori MUTANTUL 8
    # Original:  'position': -1
    # Mutant:    'XXpositionXX': -1
    # ==========================================================
    def test_kill_mutant_8_invalid_n_response_has_position_key(self):
        """Pe INVALID_N, raspunsul TREBUIE sa aiba cheia 'position' = -1.
        Mutantul schimba cheia in 'XXpositionXX', deci accesul la
        result['position'] va lipsi."""
        result = self.searcher.search_character(0, '', 'a', 'n')
        self.assertIn('position', result,
                      "Cheia 'position' trebuie sa existe in raspuns")
        self.assertNotIn('XXpositionXX', result,
                         "Cheia mutata 'XXpositionXX' nu trebuie sa apara")
        self.assertEqual(result['position'], -1)

    def test_kill_mutant_8_invalid_n_too_large(self):
        """Acelasi test pentru ramura n > 20."""
        result = self.searcher.search_character(21, 'a' * 21, 'a', 'n')
        self.assertIn('position', result)
        self.assertEqual(result['position'], -1)

    # ==========================================================
    # Test pentru a omori MUTANTUL 72
    # Original:  message = f'character {c} appears at position {position}'
    # Mutant:    message = None
    # ==========================================================
    def test_kill_mutant_72_found_message_is_not_none(self):
        """Cand un caracter este gasit, mesajul TREBUIE sa fie un string
        non-None care descrie pozitia. Mutantul seteaza message = None."""
        result = self.searcher.search_character(3, 'abc', 'b', 'n')
        self.assertIsNotNone(result['message'],
                             "Mesajul nu trebuie sa fie None la found=True")
        self.assertIsInstance(result['message'], str,
                              "Mesajul trebuie sa fie string")

    def test_kill_mutant_72_found_message_contains_position(self):
        """Mesajul de succes trebuie sa contina cuvantul 'position' si
        valoarea pozitiei gasite."""
        result = self.searcher.search_character(5, 'abcde', 'd', 'n')
        self.assertIsNotNone(result['message'])
        self.assertIn('position', result['message'].lower())
        self.assertIn('4', result['message'])  # pozitia 1-based

    def test_kill_mutant_72_found_message_contains_char(self):
        """Mesajul de succes trebuie sa contina caracterul cautat."""
        result = self.searcher.search_character(3, 'xyz', 'y', 'n')
        self.assertIsNotNone(result['message'])
        self.assertIn('y', result['message'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
