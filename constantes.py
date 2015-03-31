#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Constantes physiques.
"""
import numpy as np

# Perméabilité magnétique
mu_0 = 4*np.pi*1e-7 #H/m

def convert(val, type, sys):
    """
        Convertit «val» correspondant à la grandeur «type» dans le système d'unité «sys».
    """
    logger = init_logger("Fonction convert", '.', log_file=False)

    factors_cgs2si = {
        'E': 1e-7,          #Énergie :      erg    -> J
        'B': 1e-4,          #Ind. Mag.:     G      -> T
        'H': 1e3/4/np.pi,   #Champ Mag.:    Oe     -> A/m
        'm': 1e-3,          #Moment Mag :   emu    -> A.m²
        'M': 1e3            #Aimantation :  emu/cm³-> A/m
    }

    factor = factors_cgs2si('type')

    if sys == 'SI':
        return val * factor
    elif sys == 'CGS':
        return val / factor
    else:
        logger.error("Conversion : système d'unité inconnu")
        logger.warn("Je retourne la valeur sans la changer.")
        return val
