#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Définition de la classe Env

    à faire :
        — soustraire le signal de la canne
        — choix des unités
        — facteur pour tracer les courbes (milli, micro, …)
"""

# Gestion des fichiers/dossiers
import sys
import os
import shutil
import fnmatch      # for pattern matching
import re           # for regular expression

# Sciences
import numpy as np
from matplotlib import pylab as pl

# Pour les logs
from AnalyseVSM.logger import *

################################################################################
# Définition de la classe
################################################################################
class Mesures(object):
    """
        Classe général «Mesures».
        Définit l'ensemble des variables de mesure.
        à compléter…
    """

    def __init__(self):
        """
            Méthode __init__ : définit les attributs par défaut.
        """
        ####################
        # Varibles / Constantes
        ####################
        # Ces variables permette de définir le comportement des méthodes.
        ## Paramètres courbes
        #zoom
        self.H_min = -20
        self.H_max = 20

        self.H_nMoy = 20     # nombre de points utilisé pour déterminer la pente
        self.H_shift = 0.3  # biais de la sonde de hall(en Oe)

        ###### Variable
        # Dossiers
        #dos_cycles -> en argument du script
        self.dos_plot = "pdf"
        self.dos_export = "xdat"

        ####################
        # Analy
        ####################
        # Centrage de Ml et Mt.
        self.do_center = True


        ####################
        # Varibles / Constantes
        ####################
        # Permet de tracer la rotation. L'analyse prend alors en compte les angles selon le prefix et le suffix, et n'analyse pas les autres fichiers.
        # ex : fichier_001deg_n1.dat
        #   -> prefix = "*chier_"
        #   -> suffix "_n*"
        self.do_rotation = True
        self.prefix = "rot_"
        self.suffix = "deg_"
        self.file_rot = 'rotation'

    def init(self, dossier=''):
        """
            Applique les attributs après éventuelles modifications.
        """
        # On commence par définir un logger
        self.logger = init_logger(type(self).__name__, '.', log_file=False)

        # On recherche le dossier contenant les cycles
        self.dos_cycles = self.set_dosCycles(dossier)

        # Création des dossiers utiles
        self.create_folders(self.dos_plot, self.dos_export)

    def set_dosCycles(self, dos):
        """
            Définit le dossier contenant les données.
            Si un dossier est donné lors de l'initialisation, ce dernier est pris par défaut.
            Sinon (dossier '' ou inexistant), regarde si un argument est présent lors du lancement du script.
            Stoppe si aucun dossier n'existe.
        """
        if dos == '':
            return self.get_input()
        else:
            if os.path.exists(dos):
                self.logger.info("Dossier de données : '{}'".format(dos))
                return dos
            else:
                self.logger.error("Le dossier '{}' n'existe pas.".format(dos))
                if len(sys.argv) > 1:
                    self.logger.info("Je tente le dossier en argument")
                    return self.get_input()
                self.logger.error("Pas d'autres choix.")
                self.logger.info("Je n'ai rien à faire. Au revoir.")
        sys.exit(0)

    def get_input(self):
        """
            Va chercher l'argument du script.
            Stoppe si le dossier n'existe pas.
        """
        if len(sys.argv) > 1:
            dos = sys.argv[1]
            if os.path.exists(dos):
                self.logger.info("Dossier de données : '{}'".format(dos))
                return dos
            else:
                self.logger.error("Le dossier '{}' n'existe pas.".format(dos))
                self.logger.info("Je n'ai rien à faire. Au revoir.")
        else:
            self.logger.critical("Pas de dossier en argument. Usage : ./analyseVSM.py chemin/vers/data/")
            self.logger.critical("Argh... Je quitte!!!")

        sys.exit(0)

    def create_folders(self, dos_plot, dos_export):
        # Folder creation
        for dir in [dos_plot, dos_export]:
                if not os.path.exists(dir):
                    os.makedirs(dir)
                    self.logger.info("Création du dossier '{}'.".format(dir))
                else:
                    self.logger.info("Dossier '{}' existant.".format(dir))
                    # On demande quoi faire
                    choix_oui = np.array(['O', 'o', '', 'oui'])
                    choix_non = np.array(['n', 'N', 'non'])
                    reponse = input("Voulez-vous l'effacer? [Y/n]\n?")

                    if reponse in choix_oui:
                        self.logger.info("Okayy... J'efface ça.")
                        shutil.rmtree(dir)
                        self.logger.info("Création du dossier '{}'.".format(dir))
                        os.makedirs(dir)
                    elif reponse in choix_non:
                        self.logger.info("Je touche à rien.")
                    else:
                        self.logger.error("Pas une réponse ça.")
                        self.logger.warn("Puisse que c'est ça, je quitte!!")
                        sys.exit(0)

    def read_cycle(self, filepath):
        """
            Méthode de lecture du cycle.
            file, dos
        """
        self.logger.info("Traitement de '{}'".format(filepath))

        # Ouverture du fichier de données (type string unicode)
        data = np.genfromtxt(filepath, dtype='str', delimiter="\t", skip_header=1, skip_footer=5, usecols=(0, 1, 2), unpack=False)

        # On remplace les ',' par des '.', et on convertit en nombre
        data = np.core.defchararray.replace(data, ',','.').astype(float)

        # On place les données dans un cycle
        c = Cycle(self, 'CGS')
        c.set_data(data)

        return c

    def analyse_folder(self):
        """
            Permet d'analyser tout un dossier.
        """

        for file in os.listdir(self.dos_cycles):
            if file.endswith(".dat"):
                filepath = "{0}/{1}".format(self.dos_cycles, file)
                self.analyse_file(filepath)

    def analyse_file(self, filepath):
        """
            Analyse un unique fichier 'filepath'.
            Trace si draw=True.
        """

        # Lecture du fichier
        c = self.read_cycle(filepath)

        # Recentrage des données en fonction des paramètres de mesure
        c.do_center(self)

        # Calcul des champs coercitifs et autres caractéristiques
        c.calc_properties()

        # Tracé du cycle
        filename = os.path.basename(os.path.splitext(filepath)[0])    #juste le nom, sans l'extention
        file_plot = "{0}/{1}.pdf".format(self.dos_plot, filename)
        c.plot(file_plot)

        # Export du cycle
        file_out = "{0}/{1}.dat".format(self.dos_export, filename)
        c.export(file_out)

        # On retour le cycle, si on s'en sert après
        return c

    def analyse_rotation(self):
        """
            Analyse un dossier, mais en rotation.
            Permet ainsi de tracer l'évolution azimutale de Hc, He, ...
            , folder, prefix, suffix
        """
        # On liste les fichiers (tous, sans exception)
        liste = os.listdir(self.dos_cycles)

        rot = Rotation(self)

        # On effectue un itération sur les fichiers
        for i, file in enumerate(liste):
            if fnmatch.fnmatch(file, "*{}*.dat".format(self.prefix)):  # liste tous les fichiers data contenant prefix
                # chemin du fichier
                filepath = "{0}/{1}".format(self.dos_cycles, file)

                # Détermination de l'angle
                deminom = re.sub("{0}.*".format(self.suffix), '', file)
                phi = float(re.sub(".*{}".format(self.prefix), '', deminom))

                self.logger.info("VSM -> Angle phi = {} deg".format(phi))

                # On calcul les paramètres du cycle
                c = self.analyse_file(filepath)

                # et on enregistre les paramètres du cycle
                rot.add_cycle(c, phi)

        # Dans le cas où c'est dans le désordre
        rot.order_data()

        # Finalement, on enregistre les résultats dans un fichier
        rot.export()

        # et on trace
        rot.plot()


    def run_analyse(self):
        self.logger.info("Début du traitement...")
        # Analyse et trace le dossier
        if not self.rotation: self.analyse_folder()

        # Effectue une rotation
        if self.rotation: self.analyse_rotation()

class Cycle(object):
    """
        Object cycle.
        Création : c = Cycle('CGS')

        Méthodes :
            set_unit(unit)
            set_data(data)
            do_center(meas)
            calc_properties()

        Object cycle, contenant :
            — H, Ml, Mt
            — Ms
            — H_corr, Ml_corr,
            — unit ('CGS' ou 'SI', CGS par défaut)
        à compléter
    """
    def __init__(self, mes, unit='CGS'):
        # On crée le logger
        self.logger = init_logger(type(self).__name__, '.', log_file=False)

        # On définie l'unité du cycle
        self.set_unit(unit)

        self.H_min = mes.H_min
        self.H_max = mes.H_max

    def set_unit(self, unit):
        """
            Méthode définissant l'unité.
        """
        if unit == ('CGS' or 'SI'):
            self.unit = unit
        else:
            self.logger.error("Initialisation Cycle : unité '{}' non reconnue.")
            self.logger.warn("Je considère qu'il s'agit de l'unité CGS.")
            self.unit = 'CGS'

    def set_data(self, data):
        self.H = data[:, 0]
        self.Ml = data[:, 2]
        self.Mt = data[:, 1]

    def do_center(self, mes):
        """
            Centre les données, en calculant la moyenne des points aux extrémité.
            Condition : aimantation saturée.
            Centrage pour Ml et Mt.
            Correction du décalage en champ avec H_centre : H <- H - H_centre
            Retourne Mt_corr, Ml_corr, Ms
        """
        # Nombre de points utilisés pour la moyenne
        nb = mes.H_nMoy

        # Partage le cycle en deux
        milieu = np.floor(self.H.size / 2)

        # Modification du champ
        self.H_corr = self.H - mes.H_shift

        #Transverse
        Mt_moy = np.mean(np.concatenate((self.Mt[:nb], self.Mt[-nb:], self.Mt[milieu - nb : milieu + nb])))

        #Longitudinal
        Ml_max = np.mean(np.concatenate((self.Ml[:nb], self.Ml[-nb:])))
        Ml_min = np.mean(self.Ml[milieu - nb: milieu + nb])

        # On enregistre l'aimantation à saturation
        self.Ms = (Ml_max - Ml_min) / 2
        self.logger.info("Ms = {}".format(self.Ms))
        self.logger.info("Mt base = {}".format(Mt_moy))

        # et Mt_corr, Ml_corr
        self.Mt_corr = self.Mt - Mt_moy
        self.Ml_corr = self.Ml - (Ml_max + Ml_min) / 2

    def calc_properties(self):
        """
            Calcule, en fonction des données :
                — Hc1, Hc2 : champs coercitifs
                — Mr1, Mr2 : aimantation  rémanentes
                — max(|Mt|) (aller et retour)
            H représente le champ, M le moment
            Les zéros sont déterminés par régression linéaire

            Enregistre :
                — H_coer : deux champ coercitifs (gauche, droite)
                — Mr     : aimantations rémanentes
                — Mt_max : max de transverse
        """
        # Le tableau des champs coercitif : le 1 est celui de droite, le 0 celui de gauche
        self.H_coer = np.zeros(2)
        self.Mr = np.zeros(2)
        self.Mt_max = np.zeros(2)

        # On copie les tableaux pour plus de clarté
        H = self.H_corr
        Mt = self.Mt_corr
        Ml = self.Ml_corr

        # Signe initial de l'aimantation
        signe_Ml = (Ml[0] > 0)
        signe_H = (H[0] > 0)

        # Boucle sur les données
        for i in np.arange(1,H.size):
            # si changement de signe le Ml -> champ coercitif
            if (Ml[i] > 0) != signe_Ml:
                signe_Ml = not signe_Ml
                self.H_coer[signe_Ml] = H[i-1] - (H[i] - H[i-1])/(Ml[i] - Ml[i-1]) * Ml[i-1]

            # si le champ change de signe -> aimantation rémanente
            if (H[i] > 0) != signe_H:
                signe_H = not signe_H
                self.Mr[signe_H] = Ml[i-1] - (Ml[i] - Ml[i-1])/(H[i] - H[i-1]) * H[i-1]

        # Calcul du maximum, aller retour (doit être symétrique)
        demi = H.size / 2
        self.Mt_max[0] = np.amax(np.absolute(Mt[:demi]))
        self.Mt_max[1] = np.amax(np.absolute(Mt[demi:]))

    def plot(self, file):
        """
            Trace et export le cycle Mt(H) et Ml(H)
        """
        Hc = round((self.H_coer[1] - self.H_coer[0]) / 2, 2)
        He = round((self.H_coer[1] + self.H_coer[0]) / 2, 2)

        #Création figure
        fig = pl.figure()
        fig.set_size_inches(18.5,10.5)
        #fig.suptitle("{0}".format(file))

        ax = fig.add_subplot(221)
        ax.grid(True)
        # Renseignements
        ax.plot(self.H_corr, self.Ml_corr, 'ro-', label='Ml')
        ax.plot(self.H_corr, self.Mt_corr, 'go-', label='Mt')
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
        ax.plot(self.H_corr, self.Ml_corr, 'ro-', label='Ml')
        ax.plot(self.H_corr, self.Mt_corr, 'go-', label='Mt')
        ax.legend()

        ax.set_xlim(self.H_min, self.H_max)

        #On trace en exportant
        self.logger.info("Exportation du tracé : {}".format(file))
        pl.savefig(file, dpi=100)

        # Pas oublier de fermer la figure (libère la mémoire)
        pl.close(fig)

    def export(self, file):
        """
            Exporte les données.
            Format :

        """
        # On exporte les datas
        data = np.column_stack((self.H, self.Mt, self.Ml, self.H_corr, self.Mt_corr, self.Ml_corr))
        self.logger.info("Enregistrement des cycles dans {0}".format(file))

        header = """ Ms = {0} emu
        Hc = {1} Oe
        He = {2} Oe
        H(Oe) brut\t\t Mt brut(emu)\t\t Ml brut \t\t H corrigé \t\t Mt corrigé \t\t Ml corrigé
        """.format(self.Ms, (self.H_coer[1] - self.H_coer[0])/2, (self.H_coer[1] + self.H_coer[0])/2)
        np.savetxt(file, data, header=header, comments='#')

class Rotation(object):
    """
        Classe pour la rotation.
    """
    def __init__(self, mes):
        # On crée le logger
        self.logger = init_logger(type(self).__name__, '.', log_file=False)

        # On crée le tableau de résultats (vide, on le remplira au fur et à mesure)
        # tableau : phi, Hc1, Hc2, Ms, Mr1, Mr2, Mt1, Mt2
        self.tab = np.empty((0, 8), float)

        self.file_export = "{0}/{1}.dat".format(mes.dos_export, mes.file_rot)
        self.file_plot = "{0}/{1}.pdf".format(mes.dos_plot, mes.file_rot)

    def add_cycle(self, cycle, phi):
        """
            Ajoute les paramètres du cycle en argument au tableau, selon l'angle donné.
        """
        # On retient les données
        parameters = np.array([[phi, cycle.H_coer[0], cycle.H_coer[1], cycle.Ms, cycle.Mr[0], cycle.Mr[1], cycle.Mt_max[0], cycle.Mt_max[1]]])
        self.tab = np.append(self.tab, parameters, axis=0)

    def order_data(self):
        # sorting the data along the angle column
        self.tab = self.tab[self.tab[:, 0].argsort()]

    def export(self):
        # exporting data
        np.savetxt(
            self.file_export,
            self.tab,
            header="angle phi (deg)\t\t Hc- (Oe)\t\t Hc+ (Oe)\t\t Ms (emu)\t\t Mr+ (emu) \t\t Mr-(emu) \t\t Mt_max (emu)+ \t\t Mt_max - (emu)",
            comments='#'
        )


    def plot(self):
        """
            Trace l'évolution azimutal de data.
        """
        data = self.tab

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
        self.logger.info("Exportation du tracé azimutal : {}".format(self.file_plot))
        pl.savefig(self.file_plot, dpi=100)

        pl.close(fig)
