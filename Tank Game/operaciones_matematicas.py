from math import atan2, isclose, pi, sqrt


def angulo_a_cursor(pos_1, pos_2):
    # en grados

    dy = pos_2[1] - pos_1[1]
    dx = pos_2[0] - pos_1[0]
    angulo = atan2(dy, dx) * 180 / pi

    return angulo - 90


def angulo_disparo(pos_1, pos_2):
    # en radianes

    dy = pos_2[1] - pos_1[1]
    dx = pos_2[0] - pos_1[0]
    angulo = atan2(dy, dx)
    angulo = 2 * pi - angulo

    return angulo


def angulo_a_principal(pos_1, pos_2):
    # en grados

    dy = pos_2[1] - pos_1[1]
    dx = pos_2[0] - pos_1[0]
    angulo = atan2(dy, dx) * 180 / pi

    return angulo - 90


def casi_igual(magnitud_1, magnitud_2):
    return isclose(magnitud_1, magnitud_2, abs_tol=5)


def distancia(unidad_1, unidad_2):
    delta_x = unidad_1.cord_x - unidad_2.cord_x
    delta_y = unidad_1.cord_y - unidad_2.cord_y
    dist = sqrt(delta_x ** 2 + delta_y ** 2)

    return dist
