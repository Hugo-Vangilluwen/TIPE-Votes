#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implémentation d'un classe abstraite pour les différents systèmes de votes

@author: hugo
"""

__all__ = ["Preference", "Votation"]


from abc import ABC, abstractmethod

from preference import Preference


class Votation(ABC):
    """Classe abstraite représentant n'importe quel système de vote.

    Un systèeme de vote est une fonction de O^V à valeur dans O
    où :
        - O est l'ensemble des préordres sur l'ensembles des choix
        - V l'ensemble des votants"""

    def __init__(self, _choix):
        """Initialise le type abstrait de système de vote.

        _choix est une liste des différents choix possibles.
        """
        assert isinstance(
            _choix, list), "Les choix doivent être rassemblés dans une liste"
        self.choix = _choix.copy()

        self.nb_electeurs = 0

    @abstractmethod
    def voter(self, bulletin):
        """Définition abstracte de l'ajout d'un bulletin de vote."""
        self.nb_electeurs += 1

    def __repr__(self):
        """Retourne une représentation du système de vote."""
        return self.__str__()

    @property
    def vainqueur(self):
        """Calcule le vainqueur de l'élection."""
        return self.resultat.preordre[0]

    @property
    @abstractmethod
    def resultat(self):
        """Calcule le résultat de l'élection sous la forme d'une préférence (collective)."""
        return Preference([])

    @abstractmethod
    def copier(self, autre):
        """Copie et ajoute les votes de l'autre système de vote dans ce système de vote."""
        self.nb_electeurs += autre.nb_electeurs

        for c in autre.choix:
            assert c in self.choix, str(
                c) + " n'est pas dans " + str(self.choix)
