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


####################
# Modules à  importer
####################
#Modules de log / affichage
import logging

# Gestion des fichiers/dossiers
import os
import sys
import shutil
import fnmatch      # for pattern matching
import re           # for regular expression

#from os import path, makedirs, listdir
# Paquets science
import numpy as np
from matplotlib import pylab as pl
from scipy import optimize

## Importation des variables
from AnalyseVSM.variables import *




def init_logger(output_dir, log_file=True):
    """
        Méthode d'initialisation du module de logs.
        Niveau : DEBUG
        Créations des fichiers :
            — messages.log
            — erreurs.log

        Création du logger:
            logger = init_logger(chemin, log_file=True)

            log_file=True -> création de fichiers log
            log_file=False -> console uniquement

        Utilisation :
            logging.debug("debug message")
            logging.info("info message")
            logging.warning("warning message")
            logging.error("error message")
            logging.critical("critical message")
    """
    # Fichiers
    logFile_error = "erreurs.log"
    logFile_all = "messages.log"

    # Initialisation
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if log_file:
        # create error file handler and set level to error
        handler = logging.FileHandler(os.path.join(output_dir, logFile_error),"w", encoding=None, delay="true")
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # create debug file handler and set level to debug
        handler = logging.FileHandler(os.path.join(output_dir, logFile_all),"w")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logging.info("Fichiers de logs : '{0}', '{1}'".format(logFile_all, logFile_error))

    else:   #colorise la console
        logging.addLevelName( logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
        logging.addLevelName( logging.DEBUG, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
        logging.addLevelName( logging.WARNING, "\033[1;93m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
        logging.addLevelName( logging.ERROR, "\033[1;91m%s\033[1;0m" % logging.getLevelName(logging.ERROR))


    return logger

def create_folders(dos_plot, dos_export):
    # Folder creation
    for dir in [dos_plot, dos_export]:
            if not os.path.exists(dir):
                os.makedirs(dir)
                logger.info("Création du dossier {}.".format(dir))
            else:
                logger.info("Dossier {} existant.".format(dir))
                # On demande quoi faire
                choix_oui = np.array(['O', 'o', '', 'oui'])
                choix_non = np.array(['n', 'N', 'non'])
                reponse = input("Voulez-vous l'effacer? [Y/n]\n?")

                if reponse in choix_oui:
                    logger.info("Okayy... J'efface ça.")
                    shutil.rmtree(dir)
                    logger.info("Création du dossier {}.".format(dir))
                    os.makedirs(dir)
                elif reponse in choix_non:
                    logger.info("Je touche à rien.")
                else:
                    logger.error("Pas une réponse ça.")
                    logger.warn("Puisse que c'est ça, je quitte!!")
                    sys.exit(0)

def get_input():
    if len(sys.argv) > 1:
        dos = sys.argv[1]
        if os.path.exists(dos):
            logger.info("Dossier de données : {}".format(dos))
            return dos
        else:
            logger.error("Le dossier {} n'existe pas.".format(dos))
            logger.info("Je n'ai rien à faire. Au revoir.")
    else:
        logger.critical("Pas de dossier en argument. Usage : ./analyseVSM.py chemin/vers/data/")
        logger.critical("Argh... Je quitte!!!")

    sys.exit(0)

######### Functions ##############
def retrieve_data(file, dos):
    logger.info("Traitement de {}".format(file))

    # Ouverture du fichier de données (type string unicode)
    data = np.genfromtxt(file, dtype='str', delimiter="\t", skip_header=1, skip_footer=5, usecols=(0, 1, 2), unpack=False)

    # On remplace les ',' par des '.', et on convertit en nombre
    data = np.core.defchararray.replace(data, ',','.').astype(float)

    # On déballe le tableau
    H = data[:, 0]
    Mt = data[:, 1]
    Ml = data[:, 2]

    return H, Mt, Ml

def center_data(H, Mt, Ml, nb, H_centre):
    """
        Centre les donnée, en calculant la moyenne des points aux extrémité.
        Condition : aimantation saturée.
        Centrage pour Ml et Mt.
        Correction du décalage en champ avec H_centre : H <- H - H_centre
        Retourne Mt_corr, Ml_corr, Ms
    """
    milieu = np.floor(H.size / 2)

    #Champ
    H_corr = H - H_centre

    #Transverse
    Mt_moy = np.mean(np.concatenate((Mt[:nb], Mt[-nb:], Mt[milieu - nb : milieu + nb])))

    #Longitudinal
    Ml_max = np.mean(np.concatenate((Ml[:nb], Ml[-nb:])))
    Ml_min = np.mean(Ml[milieu - nb: milieu + nb])

    # on retourne Ml corrigé
    Ms = (Ml_max - Ml_min) / 2
    logger.info("Ms = {}".format(Ms))
    logger.info("Mt base = {}".format(Mt_moy))
    return H_corr, Mt - Mt_moy, Ml - (Ml_max + Ml_min) / 2, Ms

def inspect_data(H, Mt, Ml):
    """
        Calcule, en fonction des données :
            — Hc1, Hc2 : champs coercitifs
            — Mr1, Mr2 : aimantation  rémanentes
            — max(|Mt|) (aller et retour)
        H représente le champ, M le moment
        Les zéros sont déterminés par régression linéaire

        Retourne :
            — H_coer : deux champ coercitifs (gauche, droite)
            — Mr     : aimantations rémanentes
            — Mt_max : max de transverse
    """
    # Le tableau des champs coercitif : le 1 est celui de droite, le 0 celui de gauche
    H_coer = np.zeros(2)
    n_coer = np.zeros(2)
    Mr = np.zeros(2)
    Mt_max = np.zeros(2)

    # Signe initial de l'aimantation
    signe_Ml = (Ml[0] > 0)
    signe_H = (H[0] > 0)

    # Boucle sur les données
    for i in np.arange(1,H.size):
        # si changement de signe le Ml -> champ coercitif
        if (Ml[i] > 0) != signe_Ml:
            signe_Ml = not signe_Ml
            H_coer[signe_Ml] = H[i-1] - (H[i] - H[i-1])/(Ml[i] - Ml[i-1]) * Ml[i-1]
            n_coer[signe_Ml] = i

        # si le champ change de signe -> aimantation rémanente
        if (H[i] > 0) != signe_H:
            signe_H = not signe_H
            Mr[signe_H] = Ml[i-1] - (Ml[i] - Ml[i-1])/(H[i] - H[i-1]) * H[i-1]

    # Calcul du maximum, aller retour (doit être symétrique)
    demi = H.size / 2
    Mt_max[0] = np.amax(np.absolute(Mt[0:demi]))
    Mt_max[1] = np.amax(np.absolute(Mt[demi:]))

    return H_coer, Mr, Mt_max

def trace_cycle(H, Mt, Ml, H_coer, nom):
    """
        Trace et export le cycle Mt(H) et Ml(H)
    """
    Hc = round((H_coer[1] - H_coer[0]) / 2, 2)
    He = round((H_coer[1] + H_coer[0]) / 2, 2)

    #Création figure
    fig = pl.figure()
    fig.set_size_inches(18.5,10.5)
    fig.suptitle("{0}".format(nom, ))

    ax = fig.add_subplot(221)
    ax.grid(True)
    # Renseignements
    ax.plot(H, Ml*1e6, 'ro-', label='Ml')
    ax.plot(H, Mt*1e6, 'go-', label='Mt')
    ax.legend()

    y_lim = ax.get_ylim()
    x_lim = ax.get_xlim()
    x_text = (x_lim[1] - x_lim[0]) * 0.15 + x_lim[0]
    y_text = (y_lim[1] - y_lim[0]) * 0.8 + y_lim[0]
    ax.text(x_text, y_text, "Hc = {0}Oe\nHe = {1}Oe".format(Hc, He), style='italic', bbox={'facecolor':'white', 'alpha':1, 'pad':10})

    ax = fig.add_subplot(222)
    ax.grid(True)



    # Renseignements
    ax.set_title("zoom")
    ax.plot(H, Ml*1e6, 'ro-', label='Ml')
    ax.plot(H, Mt*1e6, 'go-', label='Mt')
    ax.legend()

    ax.set_xlim(H_min, H_max)

    #On trace en exportant
    file_plot = "{0}/{1}.pdf".format(dos_plot, nom)
    logger.info("Exportation du tracé : {}".format(file_plot))
    pl.savefig(file_plot, dpi=100)

    # Pas oublier de fermer la figure (libère la mémoire)
    pl.close(fig)

def trace_rotation(data, nom):
    """
        Trace l'évolution azimutal de data.
    """
    fig = pl.figure()
    fig.set_size_inches(18.5,18.5)
    coer = fig.add_subplot(221, polar=True)
    coer.grid(True)
    coer.plot(np.radians(data[:, 0]), np.abs((data[:, 1]-data[:,2])/2), 'ro-', label='Hc (Oe)')
    coer.legend()

    ex = fig.add_subplot(222, polar=True)
    ex.grid(True)
    ex.plot(np.radians(data[:, 0]), np.abs((data[:, 1]+data[:,2])/2), 'bo-', label='He (Oe)')
    ex.legend()

    rem = fig.add_subplot(224, polar = True)
    rem.grid(True)
    rem.plot(np.radians(data[:,0]), np.abs(data[:, 4] / data[:, 3]), 'mo-', label='Mr_1 / Ms')
    rem.plot(np.radians(data[:,0]), np.abs(data[:, 5] / data[:, 3]), 'co-', label='Mr_2 / Ms')
    rem.legend()

    trans = fig.add_subplot(223, polar = True)
    trans.grid(True)
    trans.plot(np.radians(data[:, 0]), np.abs(data[:, 6] / data[:, 3]), 'go-', label='min(Mt) (A m**2)')
    trans.plot(np.radians(data[:, 0]), np.abs(data[:, 7] / data[:, 3]), 'yo-', label='max(Mt) (A m**2)')
    trans.legend()

    #On trace en exportant
    file_plot = "{0}/{1}.pdf".format(dos_plot, nom)
    logger.info("Exportation du tracé azimutal : {}".format(file_plot))
    pl.savefig(file_plot, dpi=100)

    pl.close(fig)


def analyse_file(folder, file, draw=True):
    """
        Analyse un unique fichier 'file' dans le dossier 'folder'.
        Trace si draw=True.
        Retourne, dans l'ordre :
            H, Mt, Ml, H_coer, Ms
    """
    # On va chercher les données
    H, Mt, Ml = retrieve_data(folder + '/' + file, dos_plot)

    # Recentrage des cycles
    H_corr, Mt_corr, Ml_corr, Ms = center_data(H, Mt, Ml, n_Hsat, H_centre)

    # Calcul des champs coercitifs
    H_coer, Mr, Mt_max = inspect_data(H_corr, Mt_corr, Ml_corr)
    logger.info("\t-> Champs coercitifs : {}".format(H_coer))

    # On trace le cycle
    nom = os.path.splitext(file)[0]    #juste le nom, sans l'extention
    if draw:
        trace_cycle(H_corr, Mt_corr, Ml_corr, H_coer, nom)

    # On exporte les datas
    data = np.column_stack((H_corr, Mt, Ml, Mt_corr, Ml_corr))
    fichier = dos_export + '/' + nom + '.xdat'
    logger.info("Enregistrement des cycles dans {0}".format(fichier))
    np.savetxt(fichier, data, header='H(Oe)\t\t Mt brut(emu)\t\t Ml brut \t\t Mt corrigé \t\t Ml corrigé', comments='#')

    return H_corr, Mt_corr, Ml_corr, H_coer, Ms, Mr, Mt_max

def analyse_folder(folder):
    """
        Permet d'analyser tout un dossier.
    """
    for file in os.listdir(folder):
        if file.endswith(".dat"):
            analyse_file(folder, file, draw=True)

def analyse_rotation(folder, prefix, suffix):
    """
        Analyse un dossier, mais en rotation.
        Permet ainsi de tracer l'évolution azimutale de Hc, He, ...
    """
    # On liste les fichiers (tous, sans exception)
    liste = os.listdir(folder)

    # On crée le tableau de résultats (vide, on le remplira au fur et à mesure)
    # tableau : phi, Hc1, Hc2, Ms, Mr1, Mr2, Mt1, Mt2
    resultats = np.empty((0, 8), float)

    # On effectue un itération sur les fichiers
    for i, file in enumerate(liste):
        if fnmatch.fnmatch(file, "*{}*.dat".format(prefix)):  # liste tous les fichier data contenant prefix
            # Détermination de l'angle
            deminom = re.sub("{0}.*".format(suffix), '', file)
            phi = float(re.sub(".*{}".format(prefix), '', deminom))
            logger.info("VSM -> Angle phi = {} deg".format(phi))

            H, Mt, Ml, H_coer, Ms, Mr, Mt_max = analyse_file(folder, file, draw=True)

            # On retient les données
            resultats = np.append(resultats, np.array([[phi, H_coer[0], H_coer[1], Ms, Mr[0], Mr[1], Mt_max[0], Mt_max[1]]]), axis=0)

    #Finalement, on enregistre les résultats sur le disque
    nom = "{0}/{1}.dat".format(dos_export, file_rotation)
    np.savetxt(nom, resultats, header="angle phi (deg)\t\t Hc gauche (Oe)\t\t Hc droit (Oe)\t\t Ms (emu)", comments='#')

    # et on trace les rosaces
    trace_rotation(resultats, file_rotation)


####################
# Programme principal
####################

def run_analyse():
    global logger       #logger global, pour être utilisé partout

    # Création du logger (par défaut dans le répertoire courant)
    logger = init_logger('.', log_file=False)
    logger.info("Début du traitement...")

    # Enregistre le dossiers des données
    dos_cycles = get_input()

    # Création des dossiers utiles
    create_folders(dos_plot, dos_export)

    # Analyse et trace le dossier
    if not rotation: analyse_folder(dos_cycles)

    # Effectue une rotation
    if rotation: analyse_rotation(dos_cycles, prefix, suffix)


####################
# Lancement
####################
# Éxecution de main en cas de lancement du script, mais pas en cas d'importation.
if __name__ == "__main__":
    run_analyse()
