import numpy as np

################################################################################
# Constantes physiques
################################################################################
mu_0 = 4*np.pi*1e-7 #H/m

class parametres(object):

    def __init__(self):
        var = False


####################
# Varibles / Constantes
####################
# Ces variables permette de définir le comportement des méthodes.
## Paramètres courbes
#zoom
H_min = -20
H_max = 20

n_Hsat = 20     # nombre de points utilisé pour déterminer la pente
H_centre = 0.3  # biais de la sonde de hall(en Oe)

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
