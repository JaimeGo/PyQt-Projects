from movimiento import mover, distancia
import gui
from gui.building import Building


def empieza_construir(aldeano, edificio, ociosos):
    adicion_vida = aldeano.velocidad_con

    edificio.constru.show()

    if edificio.__class__.__name__ == "Torreta":

        if edificio.puntos_vida + aldeano.velocidad_con >= 500:
            adicion_vida = 0
            edificio.puntos_vida = 500
            edificio.gui.health = 500
            edificio.constru.hide()
            edificio.gui.show()
            edificio.en_pie = True
            ociosos.append(aldeano)

    if edificio.__class__.__name__ == "Cuartel":

        if edificio.puntos_vida + aldeano.velocidad_con >= 1000:
            adicion_vida = 0
            edificio.puntos_vida = 1000
            edificio.gui.health = 1000
            edificio.constru.hide()
            edificio.gui.show()
            edificio.en_pie = True
            ociosos.append(aldeano)

    edificio.puntos_vida += adicion_vida
    edificio.gui.health += adicion_vida
    edificio.constru.health += adicion_vida


def construir_edificio_1(simul, edificio):
    obreros_ya_construyendo = []

    for aldeano in simul.aldeanos_construyendo_1:

        if distancia(aldeano, edificio) <= 5:
            obreros_ya_construyendo.append(aldeano)

        else:
            mover(aldeano, edificio)

    for aldeano in obreros_ya_construyendo:
        empieza_construir(aldeano, edificio, simul.aldeanos_ociosos_1)

    obreros_necesarios = edificio.unidades_para_construir - len(simul.aldeanos_construyendo_1)

    obreros_desocupados = simul.aldeanos_ociosos_1 + \
                          simul.aldeanos_recolectando_1 + \
                          simul.aldeanos_trayendo_1

    if len(obreros_desocupados) > obreros_necesarios:
        for i in range(obreros_necesarios):
            trabajador = obreros_desocupados[i]
            simul.aldeanos_construyendo_1.append(trabajador)
            if trabajador in simul.aldeanos_recolectando_1:
                simul.aldeanos_recolectando_1.remove(trabajador)
            if trabajador in simul.aldeanos_ociosos_1:
                simul.aldeanos_ociosos_1.remove(trabajador)

            if trabajador in simul.aldeanos_trayendo_1:
                simul.aldeanos_trayendo_1.remove(trabajador)


def construir_edificio_2(simul, edificio):
    obreros_ya_construyendo = []

    for aldeano in simul.aldeanos_construyendo_2:
        if distancia(aldeano, edificio) <= 5:
            obreros_ya_construyendo.append(aldeano)

        else:
            mover(aldeano, edificio)

    for aldeano in obreros_ya_construyendo:
        empieza_construir(aldeano, edificio, simul.aldeanos_ociosos_2)

    obreros_necesarios = edificio.unidades_para_construir - len(simul.aldeanos_construyendo_2)

    obreros_desocupados = simul.aldeanos_ociosos_2 + \
                          simul.aldeanos_recolectando_2 + \
                          simul.aldeanos_trayendo_2

    if len(obreros_desocupados) > obreros_necesarios:
        for i in range(obreros_necesarios):
            trabajador = obreros_desocupados[i]
            simul.aldeanos_construyendo_2.append(trabajador)
            if trabajador in simul.aldeanos_recolectando_2:
                simul.aldeanos_recolectando_2.remove(trabajador)
            if trabajador in simul.aldeanos_ociosos_2:
                simul.aldeanos_ociosos_2.remove(trabajador)

            if trabajador in simul.aldeanos_trayendo_2:
                simul.aldeanos_trayendo_2.remove(trabajador)
