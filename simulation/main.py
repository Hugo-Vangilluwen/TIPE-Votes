#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fichier principal

@author: hugo
"""


import preference as pref
import ensemble as ens
import probabilite as proba
import pondere
import condorcet
import approbation as appro


def graphe_tous_criteres_ordre(Methode, NB_CHOIX, NB_ELECTEURS):
    """Trace les graphes pour tous les critères."""

    proba.graphe_proba(Methode,
                     ens.EnsembleOrdres, ens.EnsembleOrdres, ens.representant_ordre,
                     proba.honnetete, NB_CHOIX, NB_ELECTEURS, "ordres")

    proba.graphe_proba(Methode,
                     ens.EnsembleOrdres, ens.EnsembleOrdres, ens.representant_ordre,
                     proba.participation, NB_CHOIX, NB_ELECTEURS, "ordres")

    proba.graphe_proba(Methode,
                     ens.SingletonVide, ens.EnsembleOrdres, ens.singleton_vide,
                     proba.critereCondorcet, NB_CHOIX, NB_ELECTEURS, "ordres")

    proba.graphe_proba(Methode,
                     ens.SingletonVide, ens.EnsembleOrdres, ens.singleton_vide,
                     proba.unique_vainqueur, NB_CHOIX, NB_ELECTEURS, "ordres")


def graphe_tous_criteres_preordre(Methode, NB_CHOIX, NB_ELECTEURS):
    """Trace les graphes pour tous les critères."""

    proba.graphe_proba(Methode,
                     ens.EnsemblePreordres, ens.EnsemblePreordres, ens.representant_preordre,
                     proba.honnetete, NB_CHOIX, NB_ELECTEURS, "préordres")

    proba.graphe_proba(Methode,
                     ens.EnsemblePreordres, ens.EnsemblePreordres, ens.representant_preordre,
                     proba.participation, NB_CHOIX, NB_ELECTEURS, "préordres")

    proba.graphe_proba(Methode,
                     ens.SingletonVide, ens.EnsemblePreordres, ens.singleton_vide,
                     proba.critereCondorcet, NB_CHOIX, NB_ELECTEURS, "préordres")

    proba.graphe_proba(Methode,
                     ens.SingletonVide, ens.EnsemblePreordres, ens.singleton_vide,
                     proba.unique_vainqueur, NB_CHOIX, NB_ELECTEURS, "préordres")

def graphe_tous_criteres_preordredual(Methode, NB_CHOIX, NB_ELECTEURS):
    """Trace les graphes pour tous les critères."""

    # proba.graphe_proba(Methode,
    #                  appro.EnsPrefDuales, appro.EnsPrefDuales, appro.representant_preordre_dual,
    #                  proba.honnetete, NB_CHOIX, NB_ELECTEURS, "préordresduals")
    #
    # proba.graphe_proba(Methode,
    #                  appro.EnsPrefDuales, appro.EnsPrefDuales, appro.representant_preordre_dual,
    #                  proba.participation, NB_CHOIX, NB_ELECTEURS, "préordresduals")
    #
    # proba.graphe_proba(Methode,
    #                  appro.EnsPrefDuales, appro.EnsPrefDuales, appro.representant_preordre_dual,
    #                  proba.critereCondorcet, NB_CHOIX, NB_ELECTEURS, "préordresduals")

    proba.graphe_proba(Methode,
                     appro.EnsPrefDuales, appro.EnsPrefDuales, appro.representant_preordre_dual,
                     proba.unique_vainqueur, NB_CHOIX, NB_ELECTEURS, "préordresduals")


if __name__ == "__main__":
    # for vote in [pondere.Uninominal, pondere.Borda, condorcet.Copeland, condorcet.Black]:
    #     graphe_tous_criteres_ordre(vote, 3, 30)

    for vote in [pondere.Borda, condorcet.Copeland, condorcet.Black]:
        graphe_tous_criteres_preordre(vote, 3, 10)

    # graphe_tous_criteres_preordre(condorcet.Schulze, 3, 8)
    # graphe_tous_criteres_preordredual(appro.Approbation, 3, 25)
