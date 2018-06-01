#!/usr/bin/env python3
# coding: utf-8
from threading import Thread
import queue
from serial.tools.list_ports import comports
from libs.rplidar import RPLidar as Rp
import configparser
import logging.config
import threading

_loggerRoot = logging.getLogger("ppl")

config = configparser.ConfigParser()
config.read('./configs/config.ini', encoding="utf-8")
resolution_degre = float(config['MESURES']['resolution_degre'])
nombre_tours = float(config['MESURES']['nombre_tours'])


class ThreadData(Thread):

    def __init__(self):  # initialisation du LiDAR.
        _loggerRoot.info("Lancement thread de recuperation des donnees.")
        Thread.__init__(self)
        try:
            self.lidar = Rp(comports()[0].device)  # Tente de se connecter au premier port Serie disponible
        except IndexError:
            _loggerRoot.error("Pas de connexion serie disponible.")
            exit()
        self.lidar.start_motor()
        self.lidar.start()
        self.resolution = resolution_degre
        self.running = True
        self.generated_data = []
        self.readyData = queue.Queue()

    def run(self):
        # Liste contenant les donnees d'un scan entier = un tour
        self.generated_data = [0 for _ in range(int((360. / self.resolution)))]
        i = 0  # on utilise un booleen pour verifier reinitialiser les valeurs non update sur un tour
        # afin d'eviter de garder des valeurs obselete
        previous_bool = False
        around = self.resolution * 10

        for newTurn, quality, angle, distance in self.lidar.iter_measures():  # on recupere les valeurs du lidar
            if newTurn and not previous_bool:  # Si True precede d un False, on est sur un nouveau tour
                previous_bool = True
                # On enregistre le tour scanne dans la queue, sous forme de liste de distances
                print("NEW DATA")
                self.readyData.put(self.generated_data.copy())
            elif not newTurn:
                previous_bool = False
            angle = ((round(angle / around, 1) * around) % 360.)
            # l'indice dans la liste determine l'angle du lidar, on reduit ainsi la liste.
            self.generated_data[int(angle/self.resolution)] = distance
            if not self.running:
                break

    def stop_lidar(self):  # methode pour arreter le LiDAR
        self.running = False
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()

