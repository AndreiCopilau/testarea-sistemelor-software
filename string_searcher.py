"""
StringSearcher - clasa de testat pentru proiectul TSS T1 (Testare unitara in Python)

Algoritmul implementat reproduce si extinde exemplul din suportul de curs
(Functional Testing & Structural Testing) - cautarea unui caracter intr-un sir
de cel mult 20 de caractere.

Specificatie functionala:
    Pentru un intreg n aflat intre 1 si 20, se introduce un sir x de exact n
    caractere, apoi un caracter c care este cautat in x. Programul returneaza
    prima pozitie pe care apare c (indexare de la 1) sau un mesaj indicand ca
    nu a fost gasit. Utilizatorul poate continua cautarea pentru un nou
    caracter ('y'/'Y') sau poate iesi ('n'/'N').

Pre-conditii:
    n este intreg, 1 <= n <= 20
    x este string de lungime exact n
    c este un caracter (string de lungime 1)
    repeat_option in {'y', 'Y', 'n', 'N'}

Post-conditii:
    Returneaza un dict cu:
        - status: 'OK' sau 'INVALID_N'
        - position: pozitie 1-based daca gasit, -1 altfel
        - message: mesaj descriptiv
        - continue_search: bool (True daca user-ul vrea sa continue)
"""


class StringSearcher:
    MIN_LENGTH = 1
    MAX_LENGTH = 20

    def __init__(self):
        self.history = []  # istoric cautari (pentru testare suplimentara)

    def validate_n(self, n):
        """Valideaza ca n este in intervalul [1, 20]. Folosita pentru
        equivalence partitioning si boundary value analysis."""
        if n < self.MIN_LENGTH or n > self.MAX_LENGTH:
            return False
        return True

    def search_character(self, n, text, c, repeat_option):
        """
        Metoda principala - reproduce CFG-ul din suportul de curs.

        Numerotarea instructiunilor (corespondenta cu CFG-ul din curs):
            1-3: Citire si validare n (do-while echivalent)
            4:   while (n < 1 || n > 20)
            5:   afisare prompt
            6:   for i = 0; i < n; i++
            7:     citire caracter in a[i]
            8:   citire newline
            9-13: do { ... ; found = false
            14:   for(i=0; !found && i<n; i++)
            15:     if(a[i] == c)
            16:       found = true
            17:   if(found)
            18:     afisare pozitie
            19-20: else afisare nu apare
            21-23: prompt continuare + citire raspuns
            24:   } while ((response == 'y') || (response == 'Y'))
            25:   end
        """
        # 1-4: validare n (decizia: n < 1 || n > 20)
        if n < self.MIN_LENGTH or n > self.MAX_LENGTH:
            return {
                'status': 'INVALID_N',
                'position': -1,
                'message': f'Input an integer between {self.MIN_LENGTH} '
                           f'and {self.MAX_LENGTH}',
                'continue_search': False
            }

        # 5-7: validam ca text are exact n caractere
        if text is None or len(text) != n:
            return {
                'status': 'INVALID_TEXT',
                'position': -1,
                'message': f'Text must have exactly {n} characters',
                'continue_search': False
            }

        # 8: c trebuie sa fie un singur caracter
        if c is None or len(c) != 1:
            return {
                'status': 'INVALID_CHAR',
                'position': -1,
                'message': 'Search target must be exactly 1 character',
                'continue_search': False
            }

        # 9-16: cautare propriu-zisa
        # for(i=0; !found && i<n; i++) - decizie cu doua conditii (AND)
        found = False
        position = -1
        i = 0
        while (not found) and (i < n):  # condition: !found && i<n
            if text[i] == c:             # decizie: a[i] == c
                found = True
                position = i + 1  # 1-based, ca in spec din curs
            i += 1

        # 17-20: if(found)
        if found:
            message = f'character {c} appears at position {position}'
        else:
            message = f'character {c} does not appear in string'

        # 21-24: decizie cu OR pentru continuare:
        # (response == 'y') || (response == 'Y')
        continue_search = (repeat_option == 'y') or (repeat_option == 'Y')

        result = {
            'status': 'OK',
            'position': position,
            'message': message,
            'continue_search': continue_search
        }
        self.history.append(result)
        return result

    def get_history(self):
        """Returneaza istoricul cautarilor."""
        return list(self.history)

    def clear_history(self):
        """Sterge istoricul."""
        self.history = []
