#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implémentation des scrutins pondérés

@author: hugo
"""

from abc import abstractmethod

from vote import Votation
from preference import Preference, PreferenceStricte


__all__ = ["Uninominal", "Borda"]


class Pondere(Votation):
    """Système de vote pondéré"""

    def __init__(self, _choix):
        """Initialise le système uninominal."""
        super().__init__(_choix)

        self.points = {c: 0 for c in self.choix}

    @abstractmethod
    def voter(self, bulletin):
        """Ajoute un bulletin de vote.

        sous la forme d'une préférence stricte
        """
        assert isinstance(
            bulletin, Preference), \
            "Le bulletin doit être de la classe Preference"

        super().voter(bulletin)

    def __repr__(self):
        """Représentation du scrutin uninominal."""
        return str(self.points)

    @property
    def vainqueur(self):
        """Calcule le vainqueur élue par le scrutin uninominal."""
        maxi = 0
        v = []

        for c in self.choix:
            if self.points[c] > maxi:
                maxi = self.points[c]
                v = [c]
            elif self.points[c] == maxi:
                v.append(c)

        return v

    @property
    def resultat(self):
        """Calcule la préférence collective donnée par le scrutin uninominal."""
        r = []  # résultat

        # tri par insertion
        for c in self.choix:
            i = 0
            while i < len(r) and self.points[c] <= r[i][0]:
                i += 1

            if len(r) > 0 and self.points[c] == r[i-1][0]:
                r[i-1][1].append(c)
            else:
                r.insert(i, [self.points[c], [c]])

        rp = Preference("")  # résultat préférence
        for p in r:
            rp.preordre.append(p[1])

        return rp

    def copier(self, autre):
        """Copie et ajoute les votes de l'autre méthode de Condorcet."""
        super().copier(autre)

        for c in self.choix:
            self.points[c] += autre.points[c]


class Uninominal(Pondere):
    """Système uninominal à un tour"""

    def voter(self, bulletin):
        """Ajoute un bulletin de vote.

        sous la forme d'une préférence
        """
        assert isinstance(
            bulletin, PreferenceStricte), \
            "Le bulletin doit être de la classe PreferenceStricte"

        super().voter(bulletin)

        self.points[bulletin.majorants()[0]] += 1

# Légèrement adapté pour accepter tous les relations de préordre
# et pas seulement celle ayant un majorant unique. \n
# Pour cela, chaque électeur dispose d'une voie répartie équitablement entre ses majorants


class Borda(Pondere):
    """Méthode de Borda classique"""

    def voter(self, bulletin):
        """Ajoute un bulletin de vote.

        sous la forme d'une préférence
        """
        super().voter(bulletin)

        pts = len(self.choix)
        b = bulletin.copier()
        while pts > 0:
            m = b.majorants()
            for i in m:
                self.points[i] += pts
            pts -= len(m)
            b.preordre.pop(0)
