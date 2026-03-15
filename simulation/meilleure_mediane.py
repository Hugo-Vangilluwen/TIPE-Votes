#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implémentation des différentes méthodes par meilleur médiane
Sous la forme de classes

@author: hugo
"""

# N'est plus à jour avec vote.py !!!


__all__ = ["Jugement", "Majoritaire", "Typique", "Central", "Usuel"]


from abc import abstractmethod

from vote import Votation


class Jugement(Votation):
    """Classe abstraite qui décrit les systèmes de vote par meilleur médiane.

    Méthodes définies :
    __init__(self, C, V)
    voter(self, bulletin)
    Propriétés définies :
    mediane
    vainqueur
    """

    # __slots__ = ["choix", "valeurs", "notes"]

    def __init__(self, _choix, V):
        """Initialize le type abstrait de jugement par meilleur médiane.

        _choix est une liste des différents choix possibles
        V est la liste ordonnée (de la meilleur à la pire) des valeurs données par les électeurs
        """
        super().__init__(_choix)

        assert isinstance(
            V, list), "Les valeurs doivent être rassemblés dans une liste"
        self.valeurs = V

        self.notes = {}
        for c in self.choix:
            self.notes[c] = {}
            for v in self.valeurs:
                self.notes[c][v] = 0

    def voter(self, bulletin):
        """Ajoute un bulletin de vote.

        sous la forme d'un dictionnaire
        qui, à chaque choix, associe une valeur
        """
        super().voter(bulletin)

        for c in bulletin:
            self.notes[c][bulletin[c]] += 1

    @property
    def mediane(self):
        """Calcule les médianes de chaque candidat."""
        M = {}

        for c in self.choix:
            acc = 0
            for (v, nb) in self.notes[c].items():
                acc += nb
                if acc >= self.nb_electeurs // 2:
                    M[c] = v
                    break

        return M

    def partisants(self, n=1):
        """Calcule les opposants de chaque candidat (n est le degré)."""
        p = {}
        M = self.mediane

        for c in self.choix:
            acc = 0
            for v in self.valeurs[: max(0, self.valeurs.index(M[c]) - n + 1)]:
                acc += self.notes[c][v]
            p[c] = acc / self.nb_electeurs

        return p

    def opposants(self, n=1):
        """Calcule les opposants de chaque candidat (n est le degré)."""
        q = {}
        M = self.mediane

        self.valeurs.reverse()

        for c in self.choix:
            acc = 0
            for v in self.valeurs[: max(0, self.valeurs.index(M[c]) - n + 1)]:
                acc += self.notes[c][v]
            q[c] = acc / self.nb_electeurs

        self.valeurs.reverse()

        return q

    @abstractmethod
    def departage(self, n=1):
        """Calcule le score de chaque candiat.

        selon la règle de départage des choix
        propre à chaque classe enfant
        n est le degré pour les opposant et partisants
        """

    @property
    def vainqueur(self):
        """Calcule le vainqueur de l'élection."""
        M = self.mediane
        v = self.choix[0]

        # recherche du maximum
        for c in self.choix:
            if self.valeurs.index(M[v]) < self.valeurs.index(M[c]):
                v = c
            elif self.valeurs.index(M[v]) == self.valeurs.index(M[c]):
                n = 0
                while n < self.choix:
                    D = self.departage(n)
                    if D[v] < D[c]:
                        v = c
                        break

        return v

    def __repr__(self):
        """Retourne une chaîne de caractère le représentant."""
        return str(self.notes)

    def copier(self, autre):
        """Copie et ajoute les votes de l'autre jugement dans ce jugement."""
        super().copier(autre)

        for v in autre.valeurs:
            assert v in self.valeurs

        for c in self.choix:
            for v in self.valeurs:
                self.notes[c][v] += autre.notes[c][v]


class Majoritaire(Jugement):
    """Jugement majoritaire / Majority judgement."""

    def departage(self, n=1):
        """Le plus grand entre p et -q"""
        q = self.opposants(n)
        p = self.partisants(n)

        D = {}

        for c in self.choix:
            if q[c] <= p[c]:
                D[c] = p[c]
            else:
                D[c] = -q[c]

        return D


class Typique(Jugement):
    """Jugement typique / Difference."""

    def departage(self, n=1):
        """p - q"""
        q = self.opposants(n)
        p = self.partisants(n)

        D = {}

        for c in self.choix:
            D[c] = p[c] - q[c]

        return D


class Central(Jugement):
    """Jugement central / Relative share."""

    def departage(self, n=1):
        r"""1/2 * (p - q) / (p + q + \epsilon)"""
        q = self.opposants(n)
        p = self.partisants(n)

        D = {}

        for c in self.choix:
            D[c] = 1/2 * (p[c] - q[c]) \
                / (p[c] + q[c] + (1/self.nb_electeurs) * 10**(-100))

        return D


class Usuel(Jugement):
    """Jugement usuel / Normalized difference."""

    def departage(self, n=1):
        """1/2 * (p - q) / (1 - p - q)"""
        q = self.opposants(n)
        p = self.partisants(n)

        D = {}

        for c in self.choix:
            D[c] = 1/2 * (p[c] - q[c]) / (1 - p[c] - q[c])

        return D
