#!/usr/bin/env python3
# coding: utf-8
from math import cos, sqrt


def analyze_dic(raw_dict, distance_max, ecart_min_inter_objet):
    """
    Fonction d'analyse de dictionnaire de valeurs

    :param raw_dict: Dictionnaire au format {angle en radian:distance associée en mm}
    :param distance_max: distance sous laquelle on considère un obstacle (mm)
    :param ecart_min_inter_objet: écart minimum pour considérer que 2 objets sont différents
    :return: list_bounds une liste contenant les angles ou couples d'angles (radians) associés aux objet détectés
    """

    # Initialisations
    list_bounds = []
    item = False
    precedent = False
    dernier_angle_avant_0 = max(raw_dict.keys())
    first = None

    # On ignore les distances nulles, car absurdes
    raw_dict = {k: v for k, v in raw_dict.items() if v != 0}

    # Angles et distances
    list_angles = list(raw_dict.keys())
    last_angle = list_angles[-1]
    list_distances = list(raw_dict.values())

    if list_distances[0] <= distance_max:
        item = True
        list_bounds.append([list_angles[0]])

    for i, (angle, distance) in enumerate(raw_dict.items()):
        ecart_points = sqrt(distance ** 2 + list_distances[i - 1] ** 2 - 2 * distance * list_distances[i - 1]
                            * cos(abs(list_angles[i - 1] - angle)))  # Al Kashi

        if not item and not precedent and distance <= distance_max:
            list_bounds.append([angle])
            item = True
            precedent = True

        if item and angle == dernier_angle_avant_0:
            list_bounds[0][0] = list_bounds[-1][0]
            list_bounds.pop()

        elif item and distance >= distance_max:
            list_bounds[-1].append(last_angle)
            item = False
            precedent = False

        elif item and ecart_points > ecart_min_inter_objet and distance <= distance_max and \
                raw_dict[last_angle] <= distance_max:
            list_bounds[-1].append(last_angle)
            item = True
            precedent = True
            list_bounds.append([angle])

        last_angle = angle
        if i == 0:
            first = (angle, distance)

    # On traite le premier item en dernier pour avoir accès au dernier
    if not item and not precedent and first[1] <= distance_max:
        list_bounds.append([first[0]])
    elif item and first[1] >= 3000:
        list_bounds[-1].append(first[0])
    n = len(list_bounds)

    for obstacle in range(n):
        if len(list_bounds[obstacle]) == 1:
            list_bounds[obstacle].append(list_bounds[obstacle][0])

    return list_bounds
