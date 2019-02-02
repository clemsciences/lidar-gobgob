#!/usr/bin/env python3
import logging.config
from csv import writer
from os import mkdir
from os.path import isdir
from time import sleep, time

from src.HL_connection import hl_connected
from src.HL_connection import hl_socket
from src.HL_connection import stop_com_hl
from src.ThreadData import ThreadData
from src.affichage import afficher_en_polaire, affichage, affichage_cartesien, affichage_polaire, \
    init_affichage_cartesien, init_affichage_polaire, affichage_brut_cartesien
from src.mesures import mesures

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
    # Liste des positions des anciens obstacles
    list_obstacles_precedente = []

    # Creation de socket pour communiquer avec le HL
    if hl_connected:
        socket = hl_socket()

    # Demarre le Thread recevant les donnees
    thread_data = ThreadData()
    thread_data.start()

    # Attente de quelques tours pour que le lidar prenne sa pleine vitesse et envoie assez de points
    sleep(1)

    # Initialisation de l'affichage
    if not hl_connected and affichage:
        print("Affichage init")
        if afficher_en_polaire:
            ax, fig = init_affichage_polaire()
        else:
            ax, fig = init_affichage_cartesien()

    # Initialisation des valeurs pour le calcul du temps d'exécution
    t = time()
    te = t
    ti = time()

    # Boucle de récupération,de traitement des données, d'envoi et d'affichage
    while True:
        # sleep(1)
        # Aucun interet à spammer, on a moins de chance de bloquer l'execution du thread temporairement

        # Calcul du temps d'exécution : aussi utilisé pour le Kalman
        te = (time() - t)
        t = time()
        # On récupère les données du scan du LiDAR et on fait les traitements
        dico, limits, list_obstacles, list_obstacles_precedente = mesures(te, list_obstacles_precedente, thread_data)
        # Envoi de la position du centre de l'obstacle détécté pour traitement par le pathfinding

        liste_envoyee = []
        for o in list_obstacles:
            angle = o.center
            r = dico[angle]
            liste_envoyee.append(str((r, angle)))
            envoi = ";".join(liste_envoyee)
            envoi = envoi + "\n"
        _loggerHl.debug("envoi au hl: %s.", envoi)
        data_writer.writerow(dico.values())
        if hl_connected:
            socket.send(envoi.encode('ascii'))
        thread_data.lidar.clean_input()
        # Affichage des obstacles, de la position Kalman, et des points détectés dans chaque obstacle
        if affichage:
            affichage_brut_cartesien(ax, dico, fig)
            # if afficher_en_polaire:
            #     affichage_polaire(limits, ax, list_obstacles, dico, fig)
            # else:
            #     affichage_cartesien(limits, ax, list_obstacles, dico, fig)
        # if time() - ti > 25:
        #     break

except KeyboardInterrupt:
    # Arrêt du système
    if hl_connected and socket:
        stop_com_hl(socket)
    _loggerPpl.info("ARRET DEMANDE.")
    if thread_data:
        thread_data.stop_lidar()
        thread_data.join()
        thread_data = None
    data_file.close()

finally:
    # Arrêt du système
    if hl_connected and socket:
        stop_com_hl(socket)
    if thread_data:
        thread_data.stop_lidar()
        thread_data.join()
        thread_data = None
    # data_file.close()
