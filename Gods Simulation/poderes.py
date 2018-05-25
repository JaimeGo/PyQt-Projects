# parámetros a añadir en simulación:
# ticks_plaga
# plaga_en_proceso=False
# ticks_berserker
# berserker_en_proceso
# lista_unidades_muertas_1
# ticks_glaciar
# glaciar_en_proceso_1


from ataque import muerte_1, muerte_2
from random import choice


def elegir_poder(ind_ejercito, excluido=None):
    dict_1 = {1: plaga_1,
              2: berserker_1,
              3: terremoto_1,
              4: invocar_muertos_1,
              5: glaciar_1}

    dict_2 = {1: plaga_2,
              2: berserker_2,
              3: terremoto_2,
              4: invocar_muertos_2,
              5: glaciar_2}

    posibilidades = [1, 2, 3, 4, 5]
    if excluido:
        no_sirve = 0
        if ind_ejercito == 1:
            no_sirve = list(dict_1.keys())[list(dict_1.values()).index(excluido)]
        if ind_ejercito == 2:
            no_sirve = list(dict_2.keys())[list(x.__name__ for x in dict_1.values()).index(excluido)]
        posibilidades.remove(no_sirve)

    rand = choice(posibilidades)
    if ind_ejercito == 1:
        return dict_1[rand]

    if ind_ejercito == 2:
        return dict_2[rand]


def plaga_1(simul):
    simul.ticks_plaga += 1
    for unidad in simul.ejercito_2:
        unidad.velocidad_mov -= 0.001
        unidad.puntos_vida -= 1
        unidad.gui.health -= 1
        if unidad.puntos_vida <= 0:
            muerte_1(simul, unidad)
    if simul.ticks_plaga == 120:
        simul.plaga_en_proceso = False
        simul.ticks_plaga = 0
        simul.poder_en_proceso_1 = False


def plaga_2(simul):
    simul.ticks_plaga += 1
    for unidad in simul.ejercito_1:
        unidad.velocidad_mov -= 0.001
        unidad.puntos_vida -= 1
        unidad.gui.health -= 1
        if unidad.puntos_vida <= 0:
            muerte_2(simul, unidad)
    if simul.ticks_plaga == 120:
        simul.plaga_en_proceso = False
        simul.ticks_plaga = 0
        simul.poder_en_proceso_2 = False


def berserker_1(simul):
    simul.ticks_berserker += 1

    for unidad in simul.ejercito_2:
        unidad.puntos_vida = 1
        unidad.gui.health = 1
        unidad.puntos_daño *= 2

    if simul.ticks_berserker == 160:
        simul.berserker_en_proceso = False
        simul.ticks_berserker = 0
        simul.poder_en_proceso_1 = False


def berserker_2(simul):
    simul.ticks_berserker += 1

    for unidad in simul.ejercito_1:
        unidad.puntos_vida = 1
        unidad.gui.health = 1
        if simul.duplicar_daño:
            unidad.puntos_daño *= 2
            simul.duplicar_daño = False

    if simul.ticks_berserker == 160:
        simul.berserker_en_proceso = False
        simul.ticks_berserker = 0
        simul.poder_en_proceso_2 = False


def terremoto_1(simul):
    cuartel = simul.cuartel_2
    torreta = simul.torreta_2
    templo = simul.templo_2
    torreta.puntos_vida -= 1
    torreta.gui.health -= 1
    cuartel.puntos_vida -= 1
    cuartel.gui.health -= 1
    if templo.puntos_vida >= 10:
        templo.puntos_vida -= 1
        templo.gui.health -= 1

    if cuartel.puntos_vida <= 0:
        muerte_1(simul, cuartel)

    if torreta.puntos_vida <= 0:
        muerte_1(simul, torreta)
    simul.ticks_terremoto += 1


def terremoto_2(simul):
    if simul.terremoto_en_proceso == True:
        cuartel = simul.cuartel_1
        torreta = simul.torreta_1
        templo = simul.templo_1
        torreta.puntos_vida -= 1
        torreta.gui.health -= 1
        cuartel.puntos_vida -= 1
        cuartel.gui.health -= 1
        if templo.puntos_vida >= 10:
            templo.puntos_vida -= 1
            templo.gui.health -= 1

        if cuartel.puntos_vida <= 0:
            muerte_2(simul, cuartel)

        if torreta.puntos_vida <= 0:
            muerte_2(simul, torreta)
        simul.ticks_terremoto += 1


def invocar_muertos_1(simul):
    if len(simul.lista_unidades_muertas_1) >= 7 and not simul.muertos_invocados:

        for i in range(7):
            vuelto = simul.lista_unidades_muertas_1[i]

            if vuelto.__class__.__name__ == "Guerrero":
                simul.lista_guerreros_1.append(vuelto)
                vuelto.puntos_vida = 25
                vuelto.gui.health = 25

            if vuelto.__class__.__name__ == "Arquero":
                simul.lista_arqueros_1.append(vuelto)
                vuelto.puntos_vida = 20
                vuelto.gui.health = 20

            if vuelto.__class__.__name__ == "Mascota":
                simul.lista_mascotas_1.append(vuelto)
                vuelto.puntos_vida = 18
                vuelto.gui.health = 18
            simul.lista_unidades_muertas_1.remove(vuelto)
            vuelto.gui.show()

            simul.muertos_invocados = True

            simul.poder_en_proceso_1 = False


def invocar_muertos_2(simul):
    if len(simul.lista_unidades_muertas_2) >= 7 and not simul.muertos_invocados:

        for i in range(7):
            vuelto = simul.lista_unidades_muertas_2[i]
            if vuelto.__class__.__name__ == "Guerrero":
                simul.lista_guerreros_2.append(vuelto)
                vuelto.puntos_vida = 25
                vuelto.gui.health = 25

            if vuelto.__class__.__name__ == "Arquero":
                simul.lista_arqueros_2.append(vuelto)
                vuelto.puntos_vida = 20
                vuelto.gui.health = 20

            if vuelto.__class__.__name__ == "Mascota":
                simul.lista_mascotas_2.append(vuelto)
                vuelto.puntos_vida = 18
                vuelto.gui.health = 18
            simul.lista_unidades_muertas_2.remove(vuelto)

            vuelto.gui.show()

            simul.muertos_invocados = True

            simul.poder_en_proceso_2 = False


def glaciar_1(simul):
    if not simul.glaciar_terminado:

        simul.ticks_glaciar += 1
        simul.glaciar_en_proceso_1 = True
        if simul.ticks_glaciar == 280:
            simul.glaciar_en_proceso_1 = False
            simul.ticks_glaciar = 0
            simul.glaciar_terminado = True


def glaciar_2(simul):
    if not simul.glaciar_terminado:
        simul.ticks_glaciar += 1
        simul.glaciar_en_proceso_2 = True
        if simul.ticks_glaciar == 280:
            simul.glaciar_en_proceso_2 = False
            simul.ticks_glaciar = 0
            simul.glaciar_terminado = True
