#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implémentation des différentes méthodes de Condorcet
Sous la forme de classes

@author: hugo
"""


__all__ = ["Condorcet", "Schulze", "Black"]


from math import inf

import vote
import preference as pref
import pondere


class Condorcet(vote.Votation):
    """Système de vote respectant pour le critère de Condorcet.

    Énoncé par le marquis de Condorcet en 1784
    """

    def __init__(self, _choix):
        """Initialize le type abstrait de méthode de Condorcet."""
        super().__init__(_choix)

        self.referendums = {}
        for c in self.choix:
            self.referendums[c] = {}
            for cc in self.choix:
                self.referendums[c][cc] = 0

    def voter(self, bulletin):
        """Ajoute un bulletin de vote.

        sous la forme d'une préférence
        """
        super().voter(bulletin)

        assert isinstance(
            bulletin, pref.Preference), \
            "Le bulletin doit être de la classe Preference"

        for c in self.choix:
            for cc in self.choix:
                if bulletin.comparer_strict(c, cc):
                    self.referendums[c][cc] += 1

    @property
    def duels(self):
        """Calcule la matrice des duels.

        sous la forme d'un dictionnaire à deux entrées qui sont des choix.
        """
        D = {}

        for c in self.choix:
            D[c] = {}
            for cc in self.choix:
                D[c][cc] = max(0, self.referendums[c][cc] -
                               self.referendums[cc][c])

        return D

    def __repr__(self):
        """Représentation de ce système de Condorcet.

        grâce à la matrice des référendums
        """
        representation = ""

        # Les différents choix
        representation += "La matrice des duels pour"
        for c in self.choix:
            representation += " " + c
        representation += " :\n"

        # La matrice des duels
        D = self.duels
        max_length = 0
        for c in self.choix:
            for cc in self.choix:
                max_length = max(max_length, len(str(D[c][cc])))
        for c in self.choix:
            for cc in self.choix:
                representation += str(D[c][cc]) + " " * \
                    (max_length + 1 - len(str(D[c][cc])))
            representation += "\n"

        return representation[:-1]

    def copier(self, autre):
        """Copie et ajoute les votes de l'autre méthode de Condorcet."""
        super().copier(autre)

        for c in self.choix:
            for cc in self.choix:
                self.referendums[c][cc] += autre.referendums[c][cc]


class GagnantCondorcet(Condorcet):
    """Élie le gagnant de Condorcet ou personne."""
    @property
    def vainqueur(self):
        """Détermine le(s) gagnant(s) de Condorcet sous la forme d'une liste."""
        lc = len(self.choix)
        if lc == 0:
            return pref.preference_vide()

        d = self.duels
        gagnant = []
        for c in self.choix:
            i = 0
            while i < lc:
                if d[c][self.choix[i]] == 0 and c != self.choix[i]:
                    break
                i += 1
            if i == lc:
                gagnant.append(c)

        return gagnant

    @property
    def resultat(self):
        """Renvoie None car détermine seulement un vainqueur."""
        return None


class Schulze(Condorcet):
    """Méthode de Schulze.

    inventé par Markus Schulze en 1997 \n
    Critères respectés : \n
    Critères non respectés : \n
    """

    @property
    def ensemble_Schwartz(self):
        """Calcule l'ensemble de Schwartz.

        Complexité temporelle O(|C|^3)"""

        def convexe(gr, s):
            """Teste si la classe d'équivalence du sommet s est le graphe gr entier.

            algorithme d'exploration en largeur
            du graphe pondéré gr à partir du sommet s
            Complexité temporelle O(|C|^2)
            """

            pile = [s]
            non_marque = self.choix.copy()

            while len(pile) != 0:
                v = pile.pop(0)
                if v in non_marque:
                    non_marque.remove(v)
                    for w in self.choix:
                        if gr[v][w] > 0:
                            if w in non_marque:
                                pile.append(w)
                if len(non_marque) == 0:
                    return True

            return False

        D = self.duels
        S = []

        for c in self.choix:
            if convexe(D, c):
                S.append(c)

        return S

    @property
    def vainqueur(self):
        """Calcule le vainqueur élue par la méthode Schulze.

        Heuristique du chemin gagnant"""
        chemins = {}

        for c in self.choix:
            chemins[c] = {}
            for cc in self.choix:
                if c != cc:
                    chemins[c][cc] = self.referendums[c][cc] - self.referendums[cc][c]

        for c in self.choix:
            for cc in self.choix:
                if c != cc:
                    for ccc in self.choix:
                        if ccc not in (c, cc):
                            s = min(chemins[cc][c], chemins[c][ccc])
                            chemins[cc][ccc] = max(chemins[cc][ccc], s)

        r = []

        for c in self.choix:
            w = True
            for cc in self.choix:
                if c != cc:
                    if chemins[cc][c] > chemins[c][cc]:
                        w = False
                        break
            if w:
                r.append(c)

        return r

    @property
    def resultat(self):
        """Calcule le vainqueur élue par la méthode Schulze.

        Heuristique du chemin gagnant"""
        if len(self.choix) == 1:
            return pref.Preference(self.choix[0])

        chemins = self.duels.copy()

        for c in self.choix:
            for cc in self.choix:
                if c != cc:
                    for ccc in self.choix:
                        if ccc not in (c, cc):
                            s = min(chemins[cc][c], chemins[c][ccc])
                            chemins[cc][ccc] = min(chemins[cc][ccc], s)

        gagnants = []
        for c in self.choix:
            w = True
            for cc in self.choix:
                if c != cc:
                    if chemins[cc][c] > chemins[c][cc]:
                        w = False
                        break
            if w:
                gagnants.append(c)

        if len(gagnants) == 0:
            p = pref.Preference("")
            p.preordre.append(self.choix.copy())
            return p

        perdants = Schulze([c for c in self.choix if c not in gagnants])
        if len(perdants.choix) == 0:
            return pref.Preference("=".join(gagnants))

        for p in perdants.choix:
            for q in perdants.choix:
                perdants.referendums[p][q] = self.referendums[p][q]

        return pref.Preference("=".join(gagnants)) + perdants.resultat


class Black(Condorcet):
    """Méthode inventé par Duncan Black."""

    def __init__(self, _choix):
        """Initialization de la méthode Black"""
        super().__init__(_choix)

        self.borda = pondere.Borda(self.choix)

    def voter(self, bulletin):
        """Ajoute un bulletin de vote."""
        super().voter(bulletin)

        self.borda.voter(bulletin)

    @property
    def resultat(self):
        """Calcule la préférence collective donnée par la méthode Schulze."""
        lc = len(self.choix)
        if lc == 0:
            return pref.preference_vide()

        # Rechercher un gagnant de Condorcet
        d = self.duels
        for c in self.choix:
            i = 0
            while i < lc:
                if d[c][self.choix[i]] == 0 and c != self.choix[i]:
                    break
                i += 1
            if i == lc:
                perdants = Black(self.choix)
                perdants.choix.remove(c)
                perdants.borda.choix.remove(c)

                for p in perdants.choix:
                    for q in perdants.choix:
                        perdants.referendums[p][q] = self.referendums[p][q]
                    perdants.borda.points[p] = self.borda.points[p]

                return pref.Preference(c) + perdants.resultat

        # Méthode de Borda
        return self.borda.resultat


class Copeland(Condorcet):
    """Méthode inventé par Ramon Lull en 1299"""

    @property
    def r(self):
        """Calcule la matrice r avec le système 2/1/0."""
        # équivalent au système 1/(1/2)/0 usuel mais ne manipule que des entiers
        R = {}

        for c in self.choix:
            R[c] = {}
            for cc in self.choix:
                if self.referendums[c][cc] > self.referendums[cc][c]:
                    R[c][cc] = 2
                elif self.referendums[c][cc] == self.referendums[cc][c]:
                    R[c][cc] = 1
                else:
                    R[c][cc] = 0

        return R

    @property
    def resultat(self):
        """Calcule la préférence collective donnée par la méthode de Copeland."""
        somme = {}
        R = self.r
        for c in self.choix:
            somme[c] = 0
            for cc in self.choix:
                somme[c] += self.r[c][cc]

        # tri par insertion
        r = [] # resultat

        for c in self.choix:
            i = 0
            while i < len(r) and somme[c] <= r[i][0]:
                i += 1

            if len(r) > 0 and somme[c] == r[i-1][0]:
                r[i-1][1].append(c)
            else:
                r.insert(i, [somme[c], [c]])

        rp = pref.Preference("")  # résultat préférence
        for p in r:
            rp.preordre.append(p[1])

        return rp
