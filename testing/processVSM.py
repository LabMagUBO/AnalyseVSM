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
# Varibles / Constantes
####################
# Ces variables permette de définir le comportement des méthodes.
# Physique
mu_0 = 4*np.pi*1e-7 #H/m

## Paramètres courbes
#zoom
H_min = -20
H_max = 20

n_Hsat = 20     # nombre de points utilisé pour déterminer la pente

###### Variable
# Dossiers
#dos_cycles -> en argument du script
dos_plot = "pdf"
dos_export = "xdat"

####################
# Analy
####################
# Centrage de Ml et Mt.
centrer = True


####################
# Varibles / Constantes
####################
# Permet de tracer la rotation. L'analyse prend alors en compte les angles selon le prefix et le suffix, et n'analyse pas les autres fichiers.
# ex : fichier_001deg_n1.dat
#   -> prefix = "*chier_"
#   -> suffix "_n*"
rotation = True
prefix = "rot_"
suffix = "deg_"
file_rotation = 'rotation'


####################
# Lancement du programme
####################
run()
