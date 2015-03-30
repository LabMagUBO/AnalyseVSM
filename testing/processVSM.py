#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Programme de lancement du module «AnalyseVSM».
    Le module 'AnalyseVSM' définit l'ensemble des fonctions.
    Le script 'processVSM.py' est à placer, par ex., dans le dossier à analyser. Il sert à définir l'ensemble des variable nécessaires à l'analyse.

    Usage : 'data/' est le dossier contenant les cycles du VSM.
        -> python processVSM.py data/
"""

####################
# Importation «AnalyseVSM»
####################
## Si le module n'est pas installé (path python), on lui directement le chemin
module_path = '/Users/zorg/These/Documents/Programmes/Python_Modules/'
import sys
sys.path.append(module_path)

# on peut alors l'importer
from AnalyseVSM import *



####################
# Lancement du programme
####################

run_analyse()
