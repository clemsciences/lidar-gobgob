#!/usr/bin/env python3

import sys
from csv import reader
from os.path import isdir
from src.affichage import affichage, affichage_brut_cartesien_une_image, init_affichage_brut_cartesien

if not isdir("./Logs/"):
    print("No measure to read")
    sys.exit(0)

n_last_lines = 10
last_lines = []
with open("Logs/RawData.logs", "r") as f:
    data_reader = reader(f, delimiter=" ")
    for line in data_reader:
        last_lines.append(line)
        if len(last_lines) >= n_last_lines:
            last_lines.pop(0)

if not last_lines:
    print("The log file is void")
    sys.exit(0)

ax = None
fig = None

# Initialisation de l'affichage
if affichage:
    print("Affichage init")
    ax, fig = init_affichage_brut_cartesien()

measures = [measure for line in last_lines for measure in line[1:] if ":" in measure]
dico = {float(m.split(":")[0]): float(m.split(":")[0]) for measure in measures for m in measure.split(":")}

# Affichage des points
if affichage:
    affichage_brut_cartesien_une_image(ax, dico, fig)
else:
    print(dico)
