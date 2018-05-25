from math import atan2, pi, isclose, sqrt


def angulo_a_entidad(unidad, cord_x, cord_y):
    y = unidad.gui.cord_y - cord_y
    x = unidad.gui.cord_x - cord_x
    angulo = atan2(y, x) * 180 / pi
    return angulo


def casi_igual(cord_1, cord_2):
    return isclose(cord_1, cord_2, abs_tol=5)


def distancia(unidad_1, unidad_2):
    delta_x = unidad_1.gui.cord_x - unidad_2.gui.cord_x
    delta_y = unidad_1.gui.cord_y - unidad_2.gui.cord_y
    dist = sqrt(delta_x ** 2 + delta_y ** 2)

    return dist


def mover(unidad_1, unidad_2):
    dist = distancia(unidad_1, unidad_2)
    dx = unidad_2.gui.cord_x - unidad_1.gui.cord_x
    dy = unidad_2.gui.cord_y - unidad_1.gui.cord_y

    unidad_1.gui.cord_x += dx * unidad_1.velocidad_mov / dist
    unidad_1.gui.cord_y += dy * unidad_1.velocidad_mov / dist
