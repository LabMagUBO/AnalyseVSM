#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Programme analyseVSM.py.

    Ce programme permet d'analyser les fichiers produits par le VSM.

    Capacité :
        — simple cycle, cycles multiples
        — cycles multiples en rotation (tracé des évolutions azimutales)
        — Mesure de l'aimantation en rotation

    Usage :
        ./chemin/vers/analyseVSM.py chemin/vers/dossier/        -> si executable
        python chemin/vers/analyseVSM.py chemin/vers/dossier/

        Crée les dossiers suivants :
        pdf, xdat

    Variables :
        dosOut



    Fonctionnalité à implémenter :
        - soustraire le signal de la canne
"""



# Gestion des fichiers/dossiers
import os
import sys
import fnmatch      # for pattern matching
import re           # for regular expression

# Paquets science
import numpy as np
from matplotlib import pylab as pl
from scipy import optimize

## Importation des constantes/variables
from AnalyseVSM.contantes import *
from AnalyseVSM.Env import *


####################
# Lancement
####################
# Éxecution de main en cas de lancement du script, mais pas en cas d'importation.
if __name__ == "__main__":
    run_analyse()
