####################
# Modules à  importer
####################
#Modules de log / affichage
#import logging

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

from AnalyseVSM.variables import *
from AnalyseVSM.analyse import *
