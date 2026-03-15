#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implémentation des préférences formalisé en relation de préordre
Sous la forme de classes

@author: hugo
"""


import math


__all__ = ["Preference", "PreferenceStricte",
           "preference_vide", "preference_stricte_vide"]


class Preference:
    """Les preferences sont des préordres partiels.

    Elles peuvent être individuelles ou collectives. \n
    Méthodes :
        - __init__
        - choix
        - comparer_strict
        - comparer
        - majorants
        - minorants
        - __repr__
        - __add__
        - copier
    """

    def __init__(self, bulletin):
        """Initialize la préférence à partir d'une chaîne de caractère.

        sous la forme A>C=B c'est-à-dire
        les différents choix possibles séparés par > ou =.
        """

        assert isinstance(
            bulletin, str), "bulletin doit être un string de la forme A>C=B"

        # le préordre est représenté sous la forme
        self.preordre = []

        if bulletin != "":
            self.preordre.append([])
            tampon = ""
            for c in bulletin:  # itération dans les caractères du bulletin
                if c == ">":
                    self.preordre[-1].append(tampon.strip())
                    tampon = ""
                    self.preordre.append([])
                elif c == "=":
                    self.preordre[-1].append(tampon.strip())
                    tampon = ""
                else:
                    tampon += c
            self.preordre[-1].append(tampon.strip())

    @property
    def choix(self):
        """Calcule l'ensemble des choix sur lesquels la préférence est définie."""
        choix = []

        for p in self.preordre:
            choix += p

        return choix

    def comparer_strict(self, a, b):
        """Compare de façon stricte les deux choix A et B selon cette préférence.

        retourne False si A et B ne sont pas présents dans cette préférence
        """
        assert isinstance(a, str) and isinstance(b, str)

        for i in self.preordre:
            if b in i:
                return False
            if a in i:
                return True

        return False

    def comparer(self, a, b):
        """Compare de façon large les deux choix A et B selon cette préférence.

        retourne True si A et B ne sont pas présents dans cette préférence
        """
        assert isinstance(a, str) and isinstance(b, str)

        for i in self.preordre:
            if a in i:
                return True
            if b in i:
                return False

        return True

    def comparer_ensembles(self, A, B):
        """Compare deux ensembles."""
        if len(B) == 0:
            return True

        if len(A) == 0:
            for b in B:
                if b not in self.majorants():
                    return True
            return False

        a = self.majorants(A)[0]
        b = self.majorants(B)[0]

        if self.comparer(a, b) and self.comparer(a, b):
            AA = A.copy()
            AA.remove(a)
            BB = B.copy()
            BB.remove(b)
            return self.comparer_ensembles(AA, BB)

        return self.comparer(a, b)

    def comparer_preordres(self, theta, iota):
        """Compare deux relations de préordre."""
        assert frozenset(theta.choix) == frozenset(
            iota.choix), "Les préordres doivent être avoir sur les domaines de définition."

        if len(theta.choix) == 0:
            return True

        if frozenset(theta.majorants()) == frozenset(iota.majorants()):
            A = theta.copier()
            A.preordre.pop(0)
            B = iota.copier()
            B.preordre.pop(0)
            return self.comparer_preordres(A, B)

        return self.comparer_ensembles(theta.majorants(), iota.majorants())

    def majorants(self, A=None):
        """Calcule l'ensemble des majorants."""
        if A is None:
            return self.preordre[0]

        i = 0
        while i < len(self.preordre) and len(frozenset(self.preordre[i]) & frozenset(A)) == 0:
            i += 1
        if i == len(self.preordre):
            return []
        # Gros problème d'optimization ici
        return list(frozenset(self.preordre[i]) & frozenset(A))

    @property
    def minorants(self):
        """Calcule l'ensemble des minorants."""
        return self.preordre[-1]

    def __str__(self):
        """Convertit la préférence en chaîne de caractère"""
        if len(self.preordre) == 0:
            return ""

        def repr_egaux(e):
            """Calcule la chaîne de caractère répresentant les éléments du tableaux e.

            Préconditions :
                - e est non vide \n
                - les éléments du tableaux e sont considérés comme égaux"""
            resultat = e[0]

            for i in range(1, len(e)):
                resultat += " = " + e[i]

            return resultat

        resultat = repr_egaux(self.preordre[0])

        for i in range(1, len(self.preordre)):
            resultat += " > " + repr_egaux(self.preordre[i])

        return resultat

    def __repr__(self):
        """Représentation de la préférence."""
        return str(self)

    def __add__(self, autre):
        """Ajoute deux préférences portant sur des choix disjoints."""
        # tester si les choix sont disjoints
        c1 = self.choix
        c2 = autre.choix
        for c in c1:
            assert c not in c2, str(c) + " est dans " + str(c2)
        for c in c2:
            assert c not in c1, str(c) + " est dans " + str(c1)

        somme = preference_vide()
        somme.preordre = self.preordre.copy()
        for p in autre.preordre:
            somme.preordre.append(p)

        return somme

    def __sub__(self, autre):
        """Colle deux préférence portant sur des choix disjoints."""
        # tester si les choix sont disjoints
        c1 = self.choix
        c2 = autre.choix
        for c in c1:
            assert c not in c2, str(c) + " est dans " + c2
        for c in c2:
            assert c not in c1, str(c) + " est dans " + c1

        somme = preference_vide()
        somme.preordre = self.preordre.copy()
        if len(autre.preordre) > 0:
            somme.preordre[-1].extend(autre.preordre[0])
            for p in autre.preordre[1:]:
                somme.preordre.append(p)

        return somme

    def copier(self):
        """Copie cette préférence."""
        autre = preference_vide()

        for p in self.preordre:
            autre.preordre.append(p)

        return autre

    def __eq__(self, autre):
        """Teste si self et autre sont égaux"""
        if not isinstance(autre, Preference):
            print(autre, type(autre))
        if len(self.choix) != len(autre.choix):
            return False

        for i in range(len(self.preordre)):
            if frozenset(self.preordre[i]) != frozenset(autre.preordre[i]):
                return False

        return True

    def __hash__(self):
        """Calcul le hachage."""
        tmp = []
        for p in self.preordre:
            tmp.append(tuple(p))
        return hash(tuple(tmp))

    def cardinal_équivalence(self):
        """Calcule le cardinal de la classe d'équivalence de cette relation de préordre."""
        produit = math.factorial(len(self.choix))

        for p in self.preordre:
            produit //= math.factorial(len(p))

        return produit


class PreferenceStricte(Preference):
    """Les préférences strictes sont des relations d'ordre.

    Méthodes:
        - _init__
        - choix
        - comparer
        - majorants
        - minorants
        - _repr__
        - __add__"""

    def __init__(self, bulletin):
        """Initialize la préférence à partir d'une chaîne de caractère.

        sous la forme A>C>B c'est-à-dire
        les différents choix possibles séparés par >.
        """
        if isinstance(bulletin, str):
            assert bulletin.find('=') == -1, "La préférence doit être stricte"
            super().__init__(bulletin)

        elif isinstance(bulletin, Preference):
            self.preordre = []

            for p in bulletin.preordre:
                self.preordre.append(p.copy())

        else:
            raise TypeError(f'type de "{bulletin}" inconnu : {type(bulletin)}')

    def __add__(self, autre):
        """Ajoute deux préférences portant sur des choix disjoints."""
        assert isinstance(autre, PreferenceStricte)

        # tester si les choix sont disjoints
        c1 = self.choix
        c2 = autre.choix
        for c in c1:
            assert c not in c2, str(c) + " est dans " + c2
        for c in c2:
            assert c not in c1, str(c) + " est dans " + c1

        somme = preference_stricte_vide()
        somme.preordre = self.preordre.copy()
        for p in autre.preordre:
            somme.preordre.append(p)

        return somme

    # comparer_strict = property(
    #     doc="(!) Cette méthode est équivalente à comparer")
    __sub__ = property(
        doc="(!) Cette méthode n'a plus de sens pour les préférences strictes")


def preference_vide():
    """Calcule un préférence définie sur l'ensemble vide."""
    p = Preference("")
    p.preordre.clear()
    return p


def preference_stricte_vide():
    """Calcule un préférence stricte définie sur l'ensemble vide."""
    p = PreferenceStricte("")
    p.preordre.clear()
    return p
