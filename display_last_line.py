#!/usr/bin/env python3

import sys
from csv import reader
from os.path import isdir
from src.affichage import afficher_en_polaire, affichage, \
    init_affichage_cartesien, init_affichage_polaire, affichage_brut_cartesien

if not isdir("./Logs/"):
    print("No measure to read")
    sys.exit(0)

with open("Logs/RawData.logs", "r") as f:
    data_reader = reader(f, delimiter=" ")
    line = ""
    for line in data_reader:
        pass

if not line:
    print("The log file is void")
    sys.exit(0)

ax = None
fig = None

# Initialisation de l'affichage
if affichage:
    print("Affichage init")
    if afficher_en_polaire:
        ax, fig = init_affichage_polaire()
    else:
        ax, fig = init_affichage_cartesien()
print(line[:10])
 
dico = {angle: distance for measure in line[1:] for angle, distance in measure.split(":")}
# Affichage des points
if affichage:
    affichage_brut_cartesien(ax, dico, fig)
else:
    print(dico)
