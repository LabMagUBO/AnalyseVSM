#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Programme de lancement du module «AnalyseVSM».
    Le module 'AnalyseVSM' définit l'ensemble des fonctions.
    Le script 'processVSM.py' est à placer, par ex., dans le dossier à analyser. Il sert à définir l'ensemble des variable nécessaires à l'analyse.

    Usage : 'data/' est le dossier contenant les cycles du VSM.
        -> python processVSM.py data/
"""

## Si le module n'est pas installé (path python), on lui directement le chemin
module_path = '/Users/zorg/These/Documents/Programmes/Python_Modules/'
import sys
sys.path.append(module_path)

# On peut alors importer le module princippal
from AnalyseVSM import *


## Création de l'environnement
scpy = Mesures()

## Modification des paramètres par défaut
scpy.dos_cycles = ''

####################
# Varibles / Constantes
####################
# Ces variables permette de définir le comportement des méthodes.
## Paramètres courbes
#zoom
scpy.H_min = -20
scpy.H_max = 20

scpy.n_Hmoy = 40     # nombre de points utilisé pour déterminer la pente
scpy.n_Hslope = 40     # nombre de points utilisé pour déterminer la moyenne
scpy.H_shift = 0.  # biais de la sonde de hall(en Oe)

###### Variable
# Dossiers
#dos_cycles -> en argument du script
scpy.dos_plot = "pdf"
scpy.dos_export = "xdat"

####################
# Analyse
####################
# Enlève la pente
scpy.do_slope = True

# Centrage de Ml et Mt.
scpy.do_center = True


####################
# Varibles / Constantes
####################
# Permet de tracer la rotation. L'analyse prend alors en compte les angles selon le prefix et le suffix, et n'analyse pas les autres fichiers.
# ex : fichier_001deg_n1.dat
#   -> prefix = "*chier_"
#   -> suffix "_n*"
scpy.rotation = True
scpy.prefix = "YDPB19-"
scpy.suffix = ".dat"
scpy.file_rotation = 'rotation'

# On initialise
scpy.init()



####################
# Lancement du programme
####################
scpy.run_analyse()
