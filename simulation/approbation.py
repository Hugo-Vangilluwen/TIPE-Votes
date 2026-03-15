#!/usr/bin/env python3
"""
Implémentation du vote par approbation

@author: hugo
"""

import math

import preference as pref
import pondere as pdr
import ensemble as ens


class DualePreference(pref.Preference):
    """Preference composé de deux classes d'équivalence pour la pseudo-égalité."""

    def __init__(self, _bulletin):
        """Initialise la la préférence duale."""
        super().__init__(_bulletin)

        assert len(self.preordre) <= 2

    __add__ = property(
        doc="(!) Cette méthode n'a plus de sens pour les préférences duales")
    __sub__ = property(
        doc="(!) Cette méthode n'a plus de sens pour les préférences duales")


class Approbation(pdr.Pondere):
    """Vote par approbation"""

    def voter(self, bulletin):
        """Ajoute un bulletin de vote.

        sous la forme d'une préférence
        """
        super().voter(bulletin)

        for c in bulletin.majorants():
            self.points[c] += 1


class EnsPrefDuales(ens.Ensemble):
    """Ensemble des relations de préordre duales sur l'ensemble C."""

    def _calcul_card(self):
        return len(self())

    def _calcul_ensemble(self):
        def aux(C):
            """Calcule l'ensemble des couples de partageant l'ensemble C."""
            if len(C) == 0:
                return [ ([], []) ]

            CC = C.copy()
            resultat = []

            i = CC.pop()
            a = aux(CC)
            resultat.extend([ (x + [i], y) for (x, y) in a])
            resultat.extend([ (x, y + [i]) for (x, y) in a])

            return resultat

        coupes = aux(self.choix)

        i = 0
        while i < len(coupes):
            j = i + 1
            while j < len(coupes):
                if (frozenset(coupes[i][0]) == frozenset(coupes[j][0]) \
                    and frozenset(coupes[i][1]) == frozenset(coupes[j][1])) \
                or (len(coupes[i][0]) == 0 and len(coupes[j][1]) == 0 \
                    and frozenset(coupes[i][1]) == frozenset(coupes[j][0])) \
                or (len(coupes[i][1]) == 0 and len(coupes[j][0]) == 0 \
                    and frozenset(coupes[i][0]) == frozenset(coupes[j][1])):
                    coupes.pop(j)
                j += 1
            i += 1

        resultat_pref = []
        for a in coupes:
            p = pref.preference_vide()
            if len(a[0]) > 0:
                p.preordre.append(a[0])
            if len(a[1]) > 0:
                p.preordre.append(a[1])
            resultat_pref.append(p)

        return resultat_pref


def representant_preordre_dual(C):
    """Calcule un système de représentant des relations de préordre duales par la relation de permutation."""
    E = []
    Ch = C.copy()
    CCh = []

    p = pref.preference_vide()
    p.preordre.append(Ch.copy())
    E.append(p)

    while len(Ch) > 1:
        CCh.append(Ch.pop())
        p = pref.preference_vide()
        p.preordre.append(Ch.copy())
        p.preordre.append(CCh.copy())
        E.append(p)

    return E
