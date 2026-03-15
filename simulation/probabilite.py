#!/usr/bin/env python3
"""
Un jour, peut-être, je mettrai une description à ce fichier.

@author: hugo
"""

import ensemble as ens
import condorcet as cdr

import sys
import os
import multiprocessing.pool
import datetime
import matplotlib.pyplot as plt
import numpy as np


__all__ = ["participation", "honnetete", "critereCondorcet", "graphe_indice"]


class WorkerProbabilite:
    """worker class"""

    def __init__(self, _vote, _choix, _E, _T, _R):
        self.vote = _vote
        self.choix = _choix
        self.E = _E
        self.T = _T
        self.R = _R

    def __call__(self, theta):
        ssomme = 0

        v = self.vote(self.choix())
        for i in theta[0]:
            v.voter(theta[0][i])

        for t in self.T:
            w = self.vote(self.choix())
            w.copier(v)
            if self.R(self.vote, self.choix, w, t, self.E, theta[0]):
                ssomme += t.cardinal_équivalence() # 1

        return ssomme * theta[1]


def probabilite_critere(vote, choix, OV, E, S, T, R):
    """Calcule la probabilité de la relation binaire R définie sur E x F.

    S est un système de représentant de E dont les éléments sont des préférences.
    OV est l'ensemble des applications de D_O dans V."""
    somme = 0
    WP = WorkerProbabilite(vote, choix, E, T, R)
    with multiprocessing.pool.Pool(
        processes=max(len(os.sched_getaffinity(0))-1, 1)
        ) as mypool:
        for sous_somme in mypool.map(
            func=WP,
            iterable=S):
            somme += sous_somme

    return somme / (OV.card*len(E))

    # Sans parallélisme
    # for s in S:
    #     somme += WorkerProbabilite(vote, choix, E, T, R)(s)


def graphe_proba(vote, E_class, O_class, T_fct, R, nb_choix, nb_electeurs, nature_O):
    """Trace le graphe de la valeur de l'indice en fonction du nombre d'électeurs."""
    print(f'Système de vote : {vote.__name__}', f'Nombre de choix : {nb_choix}',
          f'Nombre d\'électeurs : {nb_electeurs}', f'Critère : critère {R.__doc__}', sep='\n')
    X = list(range(1, nb_electeurs+1))

    directory_name = f'./figures/{R.__name__}'
    graph_name = f'{directory_name}/graphe_{vote.__name__}_{nature_O}_{nb_choix}_{nb_electeurs}.png'
    data_name = f'{directory_name}/tableaux/{vote.__name__}_{nature_O}.txt'
    try:
        Y = np.loadtxt(data_name)
        print('Données chargées')
        # ajouter les lignes et colonnes manquantes
        while len(Y) < nb_choix-1:
            Y = np.r_[ Y, [np.zeros(Y.shape[1])] ]
        while len(Y[0]) < nb_electeurs:
            Y = np.c_[ Y, np.zeros(Y.shape[0]) ]
    except:
        Y = np.zeros((nb_choix-1, nb_electeurs))

    print()

    t1 = datetime.datetime.now()

    for j in range(2, nb_choix+1):
        C = ens.Prechoix(j)
        E = E_class(C())
        O = O_class(C())
        T = T_fct(C())

        for n in range(1, nb_electeurs+1):
            print(j, n, end="", sep="-", flush=True)

            if Y[j-2][n-1] == 0:
                S = ens.representant_famille(O(), list(range(n)))
                Y[j-2][n-1] = probabilite_critere(vote, C, ens.Applications(ens.Prechoix(n), O), E, S, T, R)

            print('\r', end="", flush=True)
            print(Y[j-2][n-1], "  ", flush=True)

        print(flush=True)
        plt.plot(X, Y[j-2][0:nb_electeurs])

    t2 = datetime.datetime.now()
    print(f'Temps de calcul : {t2 - t1}')
    print()

    plt.title(f'Probabilité {R.__doc__} dans {vote.__name__} ({nature_O})')
    plt.grid()

    try:
        plt.savefig(graph_name)
        np.savetxt(data_name, Y)
    except:
        print(f'Impossible d\'enregistrer le fichier dans {file_name}', file=sys.stderr)

    plt.show()


def VraiCritere(vote, choix, v, iota, E, votants):
    """vrai"""
    return True

def participation(vote, choix, v, iota, E, votants):
    """de participation"""
    r1 = v.resultat

    v.voter(iota)
    r2 = v.resultat

    return iota.comparer_preordres(r2, r1)


def honnetete(vote, choix, v, iota, E, votants):
    """d'honnêteté"""
    w = vote(choix())
    w.copier(v)
    w.voter(iota)

    EE = E().copy()
    EE.remove(iota)

    for e in EE:
        u = vote(choix())
        u.copier(v)
        u.voter(e)
        if not iota.comparer_preordres(w.resultat, u.resultat):
            return False

    return True


def critereCondorcet(vote, choix, v, iota, E, votants):
    """de Condorcet"""
    gc = cdr.GagnantCondorcet(choix())
    for i in votants:
        gc.voter(votants[i])
    g = gc.vainqueur

    if len(g) == 0:
        return True

    return len(frozenset(v.vainqueur) & frozenset(g)) > 0

def unique_vainqueur(vote, choix, v, iota, E, votants):
    """d'unicité du vainqueur"""
    return len(v.vainqueur) == 1
