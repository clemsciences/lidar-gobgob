#!/usr/bin/env python3
from time import sleep, time

import lib.rplidar as rplidar
import configparser
from math import cos, sin, pi

from src.analyze_dic import analyze_dic
from src.data_generator import generator
from src.liaison_objets import liaison_objets
import pylab as pl

# Nombre de tests, pour le calcul de temps moyens
N_TESTS = 1
affichage_continu = True

Te = 1.  # Période d'échantillonnage pour le Kalman, à voir pour la mettre à jour en continu
list_obstacles_precedente = []  # Liste des positions des anciens obstacles

# Recuperationnage de la config
config = configparser.ConfigParser()
config.read('config.ini', encoding="utf-8")
nombre_tours = float(config['MESURES']['nombre_tours'])
resolution_degre = float(config['MESURES']['resolution_degre'])
resolution = 0.5*2*pi/360 # en radian
distance_max = int(config['DETECTION']['distance_max'])
distance_infini = int(config['DETECTION']['distance_infini'])
ecart_min_inter_objet = int(config['DETECTION']['ecart_min_inter_objet'])
tolerance_predicted_fixe_r = int(config['OBSTACLES FIXES OU MOBILES']['tolerance_predicted_fixe_r'])
tolerance_predicted_fixe_theta = int(config['OBSTACLES FIXES OU MOBILES']['tolerance_predicted_fixe_theta'])
tolerance_predicted_fixe = [tolerance_predicted_fixe_r, tolerance_predicted_fixe_theta]
tolerance_kalman_r = int(config['OBSTACLES FIXES OU MOBILES']['tolerance_kalman_r'])
tolerance_kalman_theta = int(config['OBSTACLES FIXES OU MOBILES']['tolerance_kalman_theta'])
tolerance_kalman = [tolerance_kalman_r, tolerance_kalman_theta]
seuil_association = seuil_association = int(config['OBSTACLES FIXES OU MOBILES']['seuil_association'])

try:
        # Le lidar:
        lidar = rplidar.RPLidar("/dev/ttyUSB0")
        lidar.start_motor()
        sleep(3)  # Laisse le temps au lidar de prendre sa vitesse

        tot = 0    # Mesure du temps d'execution
        pl.ion()
        fig = pl.figure()
        ax = fig.add_subplot(111, polar=True)  # polaire !
        ax.set_xlim(0, +distance_max)
        ax.set_ylim(2*pi)
        ax.axhline(0, 0)
        ax.axvline(0, 0)
        r = []
        theta = []
        ax.scatter(theta, r)

        while affichage_continu:
            for i in range(N_TESTS):
                t = time()
                dico = generator(lidar, nombre_tours, resolution_degre)
                print(dico)
                lidar.stop()
                limits = analyze_dic(dico, distance_max, ecart_min_inter_objet)
                print("Ostacles détectés aux angles:", limits)

                list_obstacles, list_obstacles_precedente = liaison_objets(dico, limits, seuil_association,
                                                                           Te, list_obstacles_precedente)

                list_detected = []
                for detected in limits:
                    for n in range(len(detected)):
                        list_detected.append(detected[n])

                ax.clear()
                ax.set_xlim(0, 2*pi)
                ax.set_ylim(0, +distance_max)
                ax.axhline(0, 0)
                ax.axvline(0, 0)

                for o in list_obstacles:
                    angle = o.center
                    r = dico[angle]
                    print("nb_obstacles: ", len(list_obstacles))
                    circle = pl.Circle((r*cos(angle), r*sin(angle)), o.width/2, transform=ax.transData._b, color='g',
                                       alpha=0.4)
                    ax.add_artist(circle)

                    if o.get_predicted_kalman() is not None:
                        x_kalman = o.get_predicted_kalman()[0][0]
                        y_kalman = o.get_predicted_kalman()[0][2]
                        print("position kalman: ", x_kalman, " et ", y_kalman)
                        circle = pl.Circle((x_kalman, y_kalman), o.width / 2, transform=ax.transData._b,
                                       color='b',
                                       alpha=0.4)

                        ax.add_artist(circle)

                # Listes des positions des obstacles à afficher
                detected_r = [dico[detected] for detected in list_detected]
                detected_theta = [detected for detected in list_detected]

                # Listes des positions des points à afficher
                r = [distance for distance in dico.values()]
                theta = [angle for angle in dico.keys()]

                t = time()-t
                print("Temps d'execution:", t)

                pl.plot(theta, r, 'ro', markersize=0.6)
                pl.plot(detected_theta, detected_r, 'bo', markersize=1.8)
                pl.grid()
                fig.canvas.draw()
                lidar.start()

except KeyboardInterrupt:
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
