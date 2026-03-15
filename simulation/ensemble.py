#!/usr/bin/env python3
"""
Un jour, peut-être, je mettrai une description à ce fichier.

@author: hugo
"""


import preference as pref

import math
from abc import ABC, abstractmethod


def prechoix(n):
    """Calcul un ensemble de choix de cardinal n"""
    return list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:n])

class Ensemble(ABC):

    def __init__(self, _choix):
        self.choix = _choix
        self._cardinal = None
        self._ensemble = None

    def copy(self):
        return self.__class__(self.choix.copy())

    def remove(self, x):
        self.choix.remove(x)

    def __str__(self):
        return "Ensemble : " + str(self())

    @abstractmethod
    def _calcul_card(self):
        pass

    # self.card est nécessaire si jamais le cardinal est trop grand
    @property
    def card(self):
        if self._cardinal is None:
            self._cardinal = self._calcul_card()

        return self._cardinal

    def __len__(self):
        return self.card

    @abstractmethod
    def _calcul_ensemble(self):
        pass

    def __call__(self):
        if self._ensemble is None:
            self._ensemble = self._calcul_ensemble()

        return self._ensemble


class Prechoix(Ensemble):
    """Ensemble de choix de cardinal n"""
    def __init__(self, _n):
        self.n = _n
        self._cardinal = None
        self._ensemble = None

    def _calcul_card(self):
        return self.n

    def _calcul_ensemble(self):
        return list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.n])


class EnsembleOrdres(Ensemble):
    """Ensemble des relations d'ordre sur l'ensemble C."""

    def _calcul_card(self):
        return math.factorial(len(self.choix))

    def _calcul_ensemble(self):
        def aux(C):
            if len(C) == 0:
                return [pref.preference_stricte_vide()]

            resultat = []

            for c in C:
                CC = C.copy()
                CC.remove(c)
                O = aux(CC)
                resultat += [pref.PreferenceStricte(c) + o for o in O]

            return resultat

        return aux(self.choix)


class EnsemblePreordres(Ensemble):
    """Ensemble des relations de préordre sur l'ensemble C."""

    def _calcul_card(self):
        return len(self())

    def _calcul_ensemble(self):
        def aux(C):
            if len(C) == 0:
                return [pref.preference_vide()]

            resultat = []

            for c in C:
                CC = C.copy()
                CC.remove(c)
                O = aux(CC)
                resultat += [pref.Preference(c) + o for o in O] + \
                    [pref.Preference(c) - o for o in O]

            i = 0
            while i < len(resultat):
                j = i + 1
                while j < len(resultat):
                    if resultat[i] == resultat[j]:
                        resultat.pop(j)
                    j += 1
                i += 1

            return resultat

        return aux(self.choix)


class Applications(Ensemble):
    """Ensemble des applications de E dans F sous la forme de dictionnaire."""

    def __init__(self, _E, _F):
        self.E = _E
        self.F = _F
        self._cardinal = None
        self._ensemble = None

    def _calcul_card(self):
        return len(self.F) ** len(self.E)

    def _calcul_ensemble(self):
        if len(self.F) == 0:
            return []

        def aux(EE):
            if len(EE) == 0:
                return []

            if len(EE) == 1:
                resultat = []
                for f in self.F():
                    resultat.append({EE[0]: f})
                return resultat

            resultat = []
            app = applications(EE[1:], self.F())

            for f in self.F():
                resultat.extend([{EE[0]: f} | phi for phi in app])

            return resultat

        return aux(self.E())

def applications(E, F):
    """Calcule l'ensemble des applications de E dans F sous la forme de dictionnaire."""
    if len(E) == 0 or len(F) == 0:
        return []

    if len(E) == 1:
        resultat = []
        for f in F:
            resultat.append({E[0]: f})
        return resultat

    resultat = []
    app = applications(E[1:], F)

    for f in F:
        resultat.extend([{E[0]: f} | phi for phi in app])

    return resultat

def nb_applications(len_E, len_F):
    """Calcule le cardinal de l'ensemble des applications de E dans F"""
    return len_F**len_E


class SingletonVide(Ensemble):
    """Singleton d'une préférence vide"""

    def _calcul_card(self):
        return 1

    def _calcul_ensemble(self):
        return [pref.preference_vide()]


def representant_ordre(C):
    """Calcule un système de représentant des relations d'ordre par la relation de permutation."""
    p = pref.preference_stricte_vide()
    p.preordre = [[c] for c in C]
    return [p]


def representant_preordre(C):
    """Calcule un système de représentant des relations d'ordre par la relation de permutation."""
    if len(C) == 0:
        return [pref.preference_vide()]
    if len(C) == 1:
        return [pref.Preference(C[0])]

    resultat = []

    for r in representant_preordre(C[1:]):
        resultat.append(pref.Preference(C[0]) + r)
        resultat.append(pref.Preference(C[0]) - r)

    return resultat


def representant_famille(E, F):
    """Calcule un système de représentant de la famille E^F par la relation de permutation."""
    memoization_aux = {}

    def auxiliaire(E, n):
        """Description à mettre ici."""
        if (tuple(E), n) not in memoization_aux:

            if n == 1:
                return [{e: 1} for e in E]

            r = []
            EE = E.copy()
            while len(EE) > 0:
                i = auxiliaire(EE, n-1)
                e = EE.pop()
                for j in i:
                    tmp = j.copy()
                    if e in tmp:
                        tmp[e] += 1
                    else:
                        tmp[e] = 1
                    r.append(tmp)

            memoization_aux[(tuple(E), n)] = r

        return memoization_aux[(tuple(E), n)]

    resultat = []
    total = math.factorial(len(F))

    for i in auxiliaire(E, len(F)):
        nb = total
        for j in i:
            nb //= math.factorial(i[j])

        tmp = {}
        acc = 0
        for j in i:
            while i[j] > 0:
                tmp[F[acc]] = j
                acc += 1
                i[j] -= 1

        resultat.append((tmp, nb))

    return resultat

def singleton_vide(x):
    """Retourne un singleton d'une préférence vide"""
    return [pref.preference_vide()]
