#!/usr/bin/env python3
import logging.config
from csv import writer
from os import mkdir
from os.path import isdir
from time import sleep, time

from src.ThreadData import ThreadData
from src.affichage import afficher_en_polaire, affichage, \
    init_affichage_cartesien, init_affichage_polaire, affichage_brut_cartesien
from src.mesures import mesures_bruts

if not isdir("./Logs/"):
    mkdir("./Logs/")


logging.config.fileConfig('./configs/config_log.ini')
_loggerPpl = logging.getLogger("ppl")
_loggerHl = logging.getLogger("hl")
data_file = open("Logs/RawData.logs", "a")
data_writer = writer(data_file, delimiter=" ")
data_writer.writerow(["#NEW"])
socket = None
thread_data = None
ax = None
fig = None
envoi = None


try:
    # Demarre le Thread recevant les données
    thread_data = ThreadData()
    thread_data.start()

    # Attente de quelques tours pour que le lidar prenne sa pleine vitesse et envoie assez de points
    sleep(1)

    # Initialisation de l'affichage
    if affichage:
        print("Affichage init")
        if afficher_en_polaire:
            ax, fig = init_affichage_polaire()
        else:
            ax, fig = init_affichage_cartesien()

    # Boucle de récupération, de traitement des données, d'envoi et d'affichage
    while True:

        # On récupère les données du scan du LiDAR et on fait les traitements
        dico = mesures_bruts(thread_data)

        # enregistrement des mesures
        data_writer.writerow([str(time())]+[str(k)+":"+str(dico[k]) for k in dico])

        thread_data.lidar.clean_input()
        # Affichage des obstacles, de la position Kalman, et des points détectés dans chaque obstacle
        if affichage:
            affichage_brut_cartesien(ax, dico, fig)

except KeyboardInterrupt:
    # Arrêt du système
    _loggerPpl.info("ARRET DEMANDE.")
    if thread_data:
        thread_data.stop_lidar()
        thread_data.join()
        thread_data = None
    data_file.close()

finally:
    # Arrêt du système
    if thread_data:
        thread_data.stop_lidar()
        thread_data.join()
        thread_data = None
    # data_file.close()
