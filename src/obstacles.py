#!/usr/bin/env python3


class Obstacle:
    """"
    Classe permettant de créer des obstacles
    """

    def __init__(self, width, center):
        self.isMoving = False
        self.speed = 0.  # necessite que ce soit des vecteurs
        self.predictedPosition = [0, 0]
        self.updated = False
        self.width = width  # correspond à la liste des données (angle , distances ) de l'obstacle
        self.center = center  # valeur de milieu de l'objet calculé selon une méthode défini
        self.piste_obstacle = []

    def get_isMoving(self):
        return self.isMoving

    def get_speed(self):
        return self.speed

    def get_predictedPosition(self):
        return self.predictedPosition

    def get_predicted_Kalman(self):
        return self.predicted_Kalman

    def get_piste_obstacle(self):
        return self.piste_obstacle

    def get_width(self):
        return self.width

    def get_center(self):
        return self.center

    def get_updated(self):
        return self.updated

    def set_is_moving(self, is_moving):
        """

        :param is_moving: bool
        :return:
        """
        self.isMoving = is_moving

    def set_speed(self, vector):
        """

        :param vector: Vec
        :return:
        """
        self.speed = vector

    def set_predicted_Kalman(self,predictedKalman):
        """
        Position suivante de l'objet, predite avec Kalman
        :param is_moving: tuple
        :return:
        """
        self.predicted_Kalman = predictedKalman

    def set_new_position_piste(self,newPositionPiste):
        """
        Ajoute la derniere position de l'objet a sa liste de positions precedentes
        :param is_moving: tuple
        :return:
        """
        self.piste_obstacle.append(newPositionPiste)

    def set_predicted_position(self, predicted_position):
        """
        Position suivante de l'objet, predite si cet objet est suppose fixe
        :param predicted_position: tuple
        :return:
        """
        self.predictedPosition = predicted_position

    def set_width(self, width):
        """

        :param width: dict
        :return:
        """
        self.width = width

    def set_center(self, center):
        """

        :param center: tuple
        :return:
        """
        self.center = center

    def set_updated(self, updated):
        """

        :param updated: bool
        :return:
        """
        self.updated = updated

