from movimiento import angulo_a_entidad, casi_igual
from math import sqrt, cos, sin

from movimiento import distancia, mover


def atacar(unidad_1, unidad_2):
    dist = distancia(unidad_1, unidad_2)
    rango_maximo = unidad_1.rango if unidad_1.__class__.__name__ == "Arquero" \
        else 5
    if dist > rango_maximo:

        mover(unidad_1, unidad_2)



    else:

        unidad_2.puntos_vida -= unidad_1.puntos_daño
        unidad_2.gui.health -= unidad_1.puntos_daño


def mas_cercano(unidad, lista_enemigos):
    nemesis = None
    distancia_nemesis = 100000
    if lista_enemigos:
        nemesis = lista_enemigos[0]

        for enemigo in lista_enemigos:
            if enemigo:
                distancia_analizada = distancia(unidad, enemigo)
                if distancia_analizada < distancia_nemesis:
                    nemesis = enemigo
                    distancia_nemesis = distancia_analizada

    return nemesis


def muerte_1(simul, enemigo):
    if not simul.berserker_en_proceso and simul.ticks_berserker < 160:

        if enemigo.__class__.__name__ == "Guerrero":
            simul.estadisticas.guerreros_muertos_2 += 1
            enemigo.gui.hide()
            simul.lista_guerreros_2.remove(enemigo)
            if simul.unidad_objetivo == "guerreros" and simul.objetivo_num == 2:
                simul.cantidad_lograda_1 += 1
            simul.lista_unidades_muertas_2.append(enemigo)

        if enemigo.__class__.__name__ == "Arquero":
            simul.estadisticas.arqueros_muertos_2 += 1
            enemigo.gui.hide()
            simul.lista_arqueros_2.remove(enemigo)
            if simul.unidad_objetivo == "arqueros" and simul.objetivo_num == 2:
                simul.cantidad_lograda_1 += 1

            simul.lista_unidades_muertas_2.append(enemigo)

        if enemigo.__class__.__name__ == "Mascota":
            simul.estadisticas.mascotas_muertas_2 += 1
            enemigo.gui.hide()
            simul.lista_mascotas_2.remove(enemigo)
            if simul.unidad_objetivo == "mascotas" and simul.objetivo_num == 2:
                simul.cantidad_lograda_1 += 1

            simul.lista_unidades_muertas_2.append(enemigo)

        if enemigo.__class__.__name__ == "Templo":
            simul.templo_2.en_pie = False

            return False

        if enemigo.__class__.__name__ == "Torreta":
            enemigo.en_pie = False
            simul.torreta_pagada_2 = False
            enemigo.gui.hide()

        if enemigo.__class__.__name__ == "Cuartel":
            enemigo.en_pie = False
            simul.cuartel_pagado_2 = False
            enemigo.gui.hide()

        if enemigo.__class__.__name__ == "Aldeano":
            enemigo.gui.hide()
            simul.lista_aldeanos_eliminados_2.append(enemigo)

        if enemigo.__class__.__name__ == "Hero":
            if simul.unidad_2.__name__ == "Skull":
                simul.vidas_heroe_esqueleto -= 1
                enemigo.puntos_vida = 50
                enemigo.gui.health = 50
                if simul.vidas_heroe_esqueleto == 0:
                    enemigo.gui.hide()
                    simul.heroe_2_presente = False
                    simul.vidas_heroe_esqueleto = 3



            else:
                enemigo.gui.hide()
                simul.heroe_2_presente = False

                if simul.unidad_2.__name__ == "Orc":
                    simul.mascotas_orco_creadas_1 = False
                    simul.mascotas_orco_creadas_2 = False

        simul.ejercito_2 = simul.lista_guerreros_2 + simul.lista_arqueros_2 + simul.lista_mascotas_2

        simul.objetivos_2.remove(enemigo)

        return True


def muerte_2(simul, enemigo):
    if not simul.berserker_en_proceso and simul.ticks_berserker < 160:

        if enemigo.__class__.__name__ == "Guerrero":
            simul.estadisticas.guerreros_muertos_1 += 1
            enemigo.gui.hide()
            simul.lista_guerreros_1.remove(enemigo)
            if simul.unidad_objetivo == "guerreros" and simul.objetivo_num == 2:
                simul.cantidad_lograda_2 += 1
            simul.lista_unidades_muertas_1.append(enemigo)

        if enemigo.__class__.__name__ == "Arquero":
            simul.estadisticas.arqueros_muertos_1 += 1
            enemigo.gui.hide()
            simul.lista_arqueros_1.remove(enemigo)
            if simul.unidad_objetivo == "arqueros" and simul.objetivo_num == 2:
                simul.cantidad_lograda_2 += 1

            simul.lista_unidades_muertas_1.append(enemigo)

        if enemigo.__class__.__name__ == "Mascota":
            simul.estadisticas.mascotas_muertas_1 += 1
            enemigo.gui.hide()
            simul.lista_mascotas_1.remove(enemigo)
            if simul.unidad_objetivo == "mascotas" and simul.objetivo_num == 2:
                simul.cantidad_lograda_2 += 1

            simul.lista_unidades_muertas_1.append(enemigo)

        if enemigo.__class__.__name__ == "Templo":
            simul.templo_1.en_pie = False
            return False

        if enemigo.__class__.__name__ == "Torreta":
            simul.torreta_1.en_pie = False
            simul.torreta_pagada_1 = False
            simul.torreta_1.gui.hide()

        if enemigo.__class__.__name__ == "Cuartel":
            simul.cuartel_1.en_pie = False
            simul.cuartel_pagado_1 = False
            simul.cuartel_1.gui.hide()

        if enemigo.__class__.__name__ == "Aldeano":
            enemigo.gui.hide()
            simul.lista_aldeanos_eliminados_1.append(enemigo)

        if enemigo.__class__.__name__ == "Hero":
            if simul.unidad_1.__name__ == "Skull":
                enemigo.gui.health = 100
                enemigo.puntos_vida = 100

                simul.vidas_heroe_esqueleto -= 1
                if simul.vidas_heroe_esqueleto == 0:
                    enemigo.gui.hide()
                    simul.heroe_1_presente = False
                    simul.vidas_heroe_esqueleto = 3
            else:
                enemigo.gui.hide()
                simul.heroe_1_presente = False

                if simul.unidad_2.__name__ == "Orc":
                    simul.mascotas_orco_creadas_1 = False
                    simul.mascotas_orco_creadas_2 = False

        simul.ejercito_1 = simul.lista_guerreros_1 + simul.lista_arqueros_1 + simul.lista_mascotas_1

        simul.objetivos_1.remove(enemigo)

        return True


def eliminar_aldeanos(simul):
    for aldeano in simul.lista_aldeanos_eliminados_1:
        if aldeano in simul.aldeanos_ociosos_1:
            simul.aldeanos_ociosos_1.remove(aldeano)

        if aldeano in simul.aldeanos_recolectando_1:
            simul.aldeanos_recolectando_1.remove(aldeano)

        if aldeano in simul.aldeanos_construyendo_1:
            simul.aldeanos_construyendo_1.remove(aldeano)

        if aldeano in simul.aldeanos_trayendo_1:
            simul.aldeanos_trayendo_1.remove(aldeano)

    for aldeano in simul.lista_aldeanos_eliminados_2:
        if aldeano in simul.aldeanos_ociosos_2:
            simul.aldeanos_ociosos_2.remove(aldeano)

        if aldeano in simul.aldeanos_recolectando_2:
            simul.aldeanos_recolectando_2.remove(aldeano)

        if aldeano in simul.aldeanos_construyendo_2:
            simul.aldeanos_construyendo_2.remove(aldeano)

        if aldeano in simul.aldeanos_trayendo_2:
            simul.aldeanos_trayendo_2.remove(aldeano)


def ataque_cristian_1(unidad_1, unidad_2, simul):
    if unidad_2.__class__.__name__ == "Hero":
        atacar(unidad_1, unidad_2)

    else:
        dist = distancia(unidad_1, unidad_2)
        rango_maximo = unidad_1.rango
        if dist > rango_maximo:
            mover(unidad_1, unidad_2)

        else:

            simul.ticks_cristianizacion += 1
            if simul.ticks_cristianizacion == 80:
                if unidad_2.__class__.__name__ == "Guerrero":
                    simul.lista_guerreros_2.remove(unidad_2)
                    simul.lista_guerreros_1.append(unidad_2)
                if unidad_2.__class__.__name__ == "Arquero":
                    simul.lista_arqueros_2.remove(unidad_2)
                    simul.lista_arqueros_1.append(unidad_2)
                if unidad_2.__class__.__name__ == "Mascota":
                    simul.lista_mascotas_2.remove(unidad_2)
                    simul.lista_mascotas_1.append(unidad_2)

                simul.ticks_cristianizacion = 0


def ataque_cristian_2(unidad_1, unidad_2, simul):
    if unidad_2.__class__.__name__ == "Hero":
        atacar(unidad_1, unidad_2)

    else:

        dist = distancia(unidad_1, unidad_2)
        rango_maximo = unidad_1.rango

        if dist > rango_maximo:
            mover(unidad_1, unidad_2)

        else:

            simul.ticks_cristianizacion += 1
            if simul.ticks_cristianizacion == 80:
                if unidad_2.__class__.__name__ == "Guerrero":
                    simul.lista_guerreros_1.remove(unidad_2)
                    simul.lista_guerreros_2.append(unidad_2)
                if unidad_2.__class__.__name__ == "Arquero":
                    simul.lista_arqueros_1.remove(unidad_2)
                    simul.lista_arqueros_2.append(unidad_2)
                if unidad_2.__class__.__name__ == "Mascota":
                    simul.lista_mascotas_1.remove(unidad_2)
                    simul.lista_mascotas_2.append(unidad_2)

                simul.ticks_cristianizacion = 0


def ataque_torreta(torreta, enemigo):
    dist = distancia(torreta, enemigo)
    rango = torreta.rango

    if dist <= rango:
        enemigo.puntos_vida -= torreta.puntos_daño * torreta.velocidad_ataque
        enemigo.gui.health -= torreta.puntos_daño * torreta.velocidad_ataque
