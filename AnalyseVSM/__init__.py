#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Fichier d'initialisation du module.
    À importer en premier.
"""
__version__ = '0.2, 2016-03-15'

# Modules généraux
#import os
#import sys
#import shutil
#import fnmatch      # for pattern matching
#import re           # for regular expression

#from os import path, makedirs, listdir
# Paquets science
#import numpy as np
#from matplotlib import pylab as pl
#from scipy import optimize


# Sous-modules «AnalyseVSM»
from AnalyseVSM.logger import *
from AnalyseVSM.constantes import *
from AnalyseVSM.Classes import *
#from AnalyseVSM.analyse import *

logger = init_logger(__name__, '.')
logger.info("*********************************************")
logger.info(" Version {}".format(__version__))
logger.info("*********************************************")
logger.info("""
                    o
                     \_/\o
                    ( Oo)                    \|/
                    (_=-)  .===O-  ~~Z~A~P~~ -O-
                    /   \_/U'                /|\\
                    ||  |_/
                    \\\\  |
                    {K ||
                     | PP
                     | ||
                     (__\\\\

""")
logger.info("*********************************************")
