#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Programme de lancement de analyseVSM.py, sous forme de module
"""

# On commence par importer le module d'analyse


from analyseVSM import *

####################
# Varibles / Constantes
####################
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

# Condition d'analyse
centrer = True
rotation = True

# Analyse rotation#
# ex : fichier_001deg_n1.dat
#   -> prefix = "*chier_"
#   -> suffix "_n*"
prefix = "rot_"
suffix = "deg_"
file_rotation = 'rotation'

run()
