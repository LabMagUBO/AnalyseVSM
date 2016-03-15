#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Module «logger.py».
    Gère les fichiers de log et l'affichage sur le terminal.
"""
import logging
import os


def init_logger(name, output_dir, log_file=True):
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
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:

        # create console handler and set level to info
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s - %(name)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        """
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
        """
        logging.addLevelName( logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
        logging.addLevelName( logging.DEBUG, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
        logging.addLevelName( logging.WARNING, "\033[1;93m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
        logging.addLevelName( logging.ERROR, "\033[1;91m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
        logging.addLevelName( logging.CRITICAL, "\033[0;41m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))


    return logger
