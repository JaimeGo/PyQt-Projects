import gui
from gui.kinds.human import Human
from gui.kinds.skull import Skull
from gui.kinds.orc import Orc
from gui.building import Building, Temple

from unidades import Guerrero, \
    Arquero, Mascota, Aldeano, Hero, \
    crear_guerrero_1, crear_guerrero_2, \
    crear_arquero_1, crear_arquero_2, \
    crear_mascota_1, crear_mascota_2

from random import expovariate, randint, choice
from math import cos, sin
from movimiento import angulo_a_entidad, casi_igual
from edificios import Mina, Templo, Torreta, Cuartel
from ataque import atacar, mas_cercano, muerte_1, muerte_2, \
    eliminar_aldeanos, ataque_cristian_1, ataque_cristian_2, ataque_torreta
from estadisticas import Estadisticas
from construir import construir_edificio_1, construir_edificio_2
from poderes import plaga_1, plaga_2, berserker_1, berserker_2, \
    terremoto_1, terremoto_2, invocar_muertos_1, invocar_muertos_2, \
    glaciar_1, glaciar_2, elegir_poder

from dioses import efecto_flo, efecto_godolfo, efecto_pezoa, efecto_jundead

from sys import exit


class Simulacion:
    def __init__(self,
                 tiempo_max_sim,
                 dios_1,
                 raza_1,
                 tasa_invocacion_1,
                 intervalo_1,
                 dios_2,
                 raza_2,
                 tasa_invocacion_2,
                 intervalo_2):

        self.tiempo_max_sim = tiempo_max_sim
        self.tiempo_sim = 0

        self.dios_1 = dios_1
        self.raza_1 = raza_1
        self.tasa_invocacion_1 = tasa_invocacion_1
        self.tiempo_heroe_1 = round(expovariate(tasa_invocacion_1 + 0.5))

        lista_intervalo_1 = intervalo_1.split(":")

        self.guerreros_ciclo_1 = int(lista_intervalo_1[0])
        self.arqueros_ciclo_1 = int(lista_intervalo_1[1])
        self.mascotas_ciclo_1 = int(lista_intervalo_1[2])

        self.dios_2 = dios_2
        self.raza_2 = raza_2
        self.tasa_invocacion_2 = tasa_invocacion_2
        self.tiempo_heroe_2 = round(expovariate(tasa_invocacion_2 + 0.5))

        lista_intervalo_2 = intervalo_2.split(":")

        self.guerreros_ciclo_2 = int(lista_intervalo_2[0])
        self.arqueros_ciclo_2 = int(lista_intervalo_2[1])
        self.mascotas_ciclo_2 = int(lista_intervalo_2[2])

        # objetivo

        self.unidad_objetivo = choice(["arqueros", "guerreros", "mascotas"])

        self.posibles_objetivos = {1: ("Recolectar ", "unidades de oro"),
                                   2: ("Eliminar", " " + self.unidad_objetivo),
                                   3: ("Crear ", " unidades")}

        self.target = {1: str(randint(200, 500)),
                       2: str(randint(5, 10)),
                       3: str(randint(5, 10))}

        self.objetivo_num = choice([1, 2, 3])

        self.objetivo = self.posibles_objetivos.get(self.objetivo_num)[0] + self.target.get(self.objetivo_num) + \
                        self.posibles_objetivos.get(self.objetivo_num)[1]

        gui.set_objective(self.objetivo)

        self.maximo_objetivo = int(self.target.get(self.objetivo_num))
        self.cantidad_lograda_1 = 0
        self.cantidad_lograda_2 = 0

        self.objetivo_logrado_1 = False
        self.objetivo_logrado_2 = False
        self.objetivo_alcanzado = False

        self.set_objetivos_logrados_1 = set()
        self.set_objetivos_logrados_2 = set()

        self.poder_1 = elegir_poder(1)

        self.poder_2 = elegir_poder(2, excluido=self.poder_1.__name__)

        # poderes

        self.ticks_plaga = 0
        self.plaga_en_proceso = False
        self.ticks_berserker = 0
        self.berserker_en_proceso = False
        self.duplicar_daño = True
        self.lista_unidades_muertas_1 = []
        self.lista_unidades_muertas_2 = []
        self.muertos_invocados = False
        self.ticks_glaciar = 0
        self.glaciar_en_proceso_1 = False
        self.glaciar_en_proceso_2 = False
        self.glaciar_terminado = False
        self.ticks_terremoto = 0
        self.max_terremotos = randint(120, 600)
        self.terremoto_en_proceso = False

        self.poder_en_proceso_1 = False
        self.poder_en_proceso_2 = False
        self.ocupar_poder_1 = False
        self.ocupar_poder_2 = False
        self.cambiar_objetivo = False

        self.unidad_1 = None
        self.unidad_2 = None

        self.max_tropas_1 = 0
        self.max_tropas_2 = 0

        # parámetros de heroes
        self.mascotas_orco_creadas_1 = False
        self.mascotas_orco_creadas_2 = False

        self.vidas_heroe_esqueleto = 3

        self.ticks_cristianizacion = 0

        if self.raza_1 == "humanos":
            self.unidad_1 = Human
            self.max_tropas_1 = 25

        if self.raza_2 == "humanos":
            self.unidad_2 = Human
            self.max_tropas_2 = 25

        if self.raza_1 == "orcos":
            self.unidad_1 = Orc
            self.max_tropas_1 = 20

        if self.raza_2 == "orcos":
            self.unidad_2 = Orc
            self.max_tropas_2 = 20

        if self.raza_1 == "muertos vivientes":
            self.unidad_1 = Skull
            self.max_tropas_1 = 30

        if self.raza_2 == "muertos vivientes":
            self.unidad_2 = Skull
            self.max_tropas_2 = 30

        self.modificador_daño_2 = 1
        self.modificador_velocidad_2 = 1
        self.modificador_vida_2 = 1

        if self.unidad_2.__name__ == "Orc":
            self.modificador_daño_2 = 1.2

        if self.unidad_2.__name__ == "Skull":
            self.modificador_vida_2 = 0.8
            self.modificador_velocidad_2 = 0.8

        self.modificador_daño_1 = 1
        self.modificador_velocidad_1 = 1
        self.modificador_vida_1 = 1
        if self.unidad_1.__name__ == "Orc":
            self.modificador_daño_1 = 1.2

        if self.unidad_1.__name__ == "Skull":
            self.modificador_vida_1 = 0.8
            self.modificador_velocidad_1 = 0.8

        self.lista_guerreros_1 = []
        self.lista_arqueros_1 = []
        self.lista_mascotas_1 = []

        self.lista_guerreros_2 = []
        self.lista_arqueros_2 = []
        self.lista_mascotas_2 = []

        # dioses
        self.no_mover_mascotas_1 = False
        self.no_mover_mascotas_2 = False

        self.pezoa_funcionando_1 = False
        self.pezoa_funcionando_1 = False

        self.rodolfo_funcionando_1 = False
        self.rodolfo_funcionando_1 = False

        self.jundead_funcionando_1 = False
        self.jundead_funcionando_1 = False

        efecto_pezoa(self)
        efecto_flo(self)
        efecto_godolfo(self)
        efecto_jundead(self)

        self.gold_1 = 800
        self.gold_2 = 800
        gui.set_gold_t1(self.gold_1)
        gui.set_gold_t2(self.gold_2)

        self.x_cuartel_1, self.y_cuartel_1 = 0, 0
        self.x_cuartel_2, self.y_cuartel_2 = 0, 0
        self.x_templo_1, self.y_templo_1 = 0, 0
        self.x_templo_2, self.y_templo_2 = 0, 0
        self.x_mina_1, self.y_mina_1 = 0, 0
        self.x_mina_2, self.y_mina_2 = 0, 0
        self.x_torreta_1, self.y_torreta_1 = 0, 0
        self.x_torreta_2, self.y_torreta_2 = 0, 0

        mapa_edificios = open("mapa.csv")

        primera_linea = mapa_edificios.readline().strip().split(",")

        indice_x = primera_linea.index("X")
        indice_y = primera_linea.index("Y")
        indice_tipo = primera_linea.index("TIPO")
        indice_ejercito = primera_linea.index("EJERCITO")

        for linea in mapa_edificios.readlines():
            lista_linea = linea.strip().split(",")

            if lista_linea[indice_tipo] == "Cuartel" and lista_linea[indice_ejercito] == "1":
                self.x_cuartel_1 = int(lista_linea[indice_x])
                self.y_cuartel_1 = int(lista_linea[indice_y])

            if lista_linea[indice_tipo] == "Cuartel" and lista_linea[indice_ejercito] == "2":
                self.x_cuartel_2 = int(lista_linea[indice_x])
                self.y_cuartel_2 = int(lista_linea[indice_y])

            if lista_linea[indice_tipo] == "Templo" and lista_linea[indice_ejercito] == "1":
                self.x_templo_1 = int(lista_linea[indice_x])
                self.y_templo_1 = int(lista_linea[indice_y])

            if lista_linea[indice_tipo] == "Templo" and lista_linea[indice_ejercito] == "2":
                self.x_templo_2 = int(lista_linea[indice_x])
                self.y_templo_2 = int(lista_linea[indice_y])

            if lista_linea[indice_tipo] == "Mina" and lista_linea[indice_ejercito] == "1":
                self.x_mina_1 = int(lista_linea[indice_x])
                self.y_mina_1 = int(lista_linea[indice_y])

            if lista_linea[indice_tipo] == "Mina" and lista_linea[indice_ejercito] == "2":
                self.x_mina_2 = int(lista_linea[indice_x])
                self.y_mina_2 = int(lista_linea[indice_y])

            if lista_linea[indice_tipo] == "Torreta" and lista_linea[indice_ejercito] == "1":
                self.x_torreta_1 = int(lista_linea[indice_x])
                self.y_torreta_1 = int(lista_linea[indice_y])

            if lista_linea[indice_tipo] == "Torreta" and lista_linea[indice_ejercito] == "2":
                self.x_torreta_2 = int(lista_linea[indice_x])
                self.y_torreta_2 = int(lista_linea[indice_y])

        # comenzamos con los cuatro edificios para cada raza

        self.templo_1_gui = Temple(self.dios_1, pos=(self.x_templo_1, self.y_templo_1), hp=1500)
        self.templo_2_gui = Temple(self.dios_2, pos=(self.x_templo_2, self.y_templo_2), hp=1500)
        self.mina_1_gui = Building("mine", pos=(self.x_mina_1, self.y_mina_1))
        self.mina_2_gui = Building("mine", pos=(self.x_mina_2, self.y_mina_2))
        self.cuartel_1_gui = Building("barracks", pos=(self.x_cuartel_1, self.y_cuartel_1), hp=1000)
        self.cuartel_2_gui = Building("barracks", pos=(self.x_cuartel_2, self.y_cuartel_2), hp=1000)
        self.torreta_1_gui = Building("tower", pos=(self.x_torreta_1, self.y_torreta_1), hp=500)
        self.torreta_2_gui = Building("tower", pos=(self.x_torreta_2, self.y_torreta_2), hp=500)

        self.templo_1 = Templo(puntos_vida=1500, gui=self.templo_1_gui)
        self.templo_2 = Templo(puntos_vida=1500, gui=self.templo_2_gui)
        self.mina_1 = Mina(puntos_vida=1, gui=self.mina_1_gui)
        self.mina_2 = Mina(puntos_vida=1, gui=self.mina_2_gui)
        self.cuartel_1 = Cuartel(puntos_vida=1000, gui=self.cuartel_1_gui)
        self.cuartel_2 = Cuartel(puntos_vida=1000, gui=self.cuartel_2_gui)
        self.torreta_1 = Torreta(puntos_vida=500, velocidad_ataque=1.2, puntos_daño=1, gui=self.torreta_1_gui,
                                 rango=160)
        self.torreta_2 = Torreta(puntos_vida=500, velocidad_ataque=1.2, puntos_daño=1, gui=self.torreta_2_gui,
                                 rango=160)

        gui.add_entity(self.templo_1.gui)
        gui.add_entity(self.templo_2.gui)
        gui.add_entity(self.mina_1.gui)
        gui.add_entity(self.mina_2.gui)
        gui.add_entity(self.cuartel_1.gui)
        gui.add_entity(self.cuartel_2.gui)
        gui.add_entity(self.torreta_1.gui)
        gui.add_entity(self.torreta_2.gui)

        torreta_construccion_gui_1 = Building("tower_construccion", pos=(self.x_torreta_1, self.y_torreta_1), hp=500)
        torreta_construccion_gui_2 = Building("tower_construccion", pos=(self.x_torreta_2, self.y_torreta_2), hp=500)
        cuartel_construccion_gui_1 = Building("barracks_construccion", pos=(self.x_cuartel_1, self.y_cuartel_1),
                                              hp=1000)
        cuartel_construccion_gui_2 = Building("barracks_construccion", pos=(self.x_cuartel_2, self.y_cuartel_2),
                                              hp=1000)

        gui.add_entity(torreta_construccion_gui_1)
        torreta_construccion_gui_1.hide()
        torreta_construccion_gui_1.health = 0
        gui.add_entity(torreta_construccion_gui_2)
        torreta_construccion_gui_2.hide()
        torreta_construccion_gui_2.health = 0
        gui.add_entity(cuartel_construccion_gui_1)
        cuartel_construccion_gui_1.hide()
        cuartel_construccion_gui_1.health = 0
        gui.add_entity(cuartel_construccion_gui_2)
        cuartel_construccion_gui_2.hide()
        cuartel_construccion_gui_2.health = 0

        self.cuartel_1.constru = cuartel_construccion_gui_1
        self.cuartel_2.constru = cuartel_construccion_gui_2
        self.torreta_1.constru = torreta_construccion_gui_1
        self.torreta_2.constru = torreta_construccion_gui_2

        # comenzamos con 5 aldeanos
        self.lista_aldeanos_total_1 = []
        self.lista_aldeanos_total_2 = []

        self.aldeanos_ociosos_1 = []
        self.aldeanos_ociosos_2 = []

        for i in range(5):
            esparcir_x = randint(0, 50)
            esparcir_y = randint(0, 100)

            aldeano_1_gui = self.unidad_1("villager", pos=(self.x_templo_1 + esparcir_x, self.y_templo_1 + esparcir_y),
                                          hp=25)
            aldeano_2_gui = self.unidad_2("villager", pos=(self.x_templo_2 + esparcir_x, self.y_templo_2 + esparcir_y),
                                          hp=25)

            gui.add_entity(aldeano_1_gui)
            gui.add_entity(aldeano_2_gui)

            aldeano_1 = Aldeano(25, 1, 1, 1, randint(0, 5), aldeano_1_gui)
            aldeano_2 = Aldeano(25, 1, 1, 1, randint(0, 5), aldeano_2_gui)

            self.aldeanos_ociosos_1.append(aldeano_1)
            self.aldeanos_ociosos_2.append(aldeano_2)
            self.lista_aldeanos_total_1.append(aldeano_1)
            self.lista_aldeanos_total_2.append(aldeano_2)

        self.aldeanos_recolectando_1 = []
        self.aldeanos_recolectando_2 = []

        self.aldeanos_construyendo_1 = []
        self.aldeanos_construyendo_2 = []

        self.aldeanos_trayendo_1 = []
        self.aldeanos_trayendo_2 = []

        self.hero_1 = None
        self.hero_2 = None

        self.heroe_1_presente = False
        self.heroe_2_presente = False

        self.estadisticas = Estadisticas()

        self.lista_aldeanos_eliminados_1 = []
        self.lista_aldeanos_eliminados_2 = []

        self.torreta_1_pagada = True
        self.torreta_2_pagada = True
        self.cuartel_1_pagado = True
        self.cuartel_2_pagado = True

    def tick(self):

        if self.tiempo_sim >= self.tiempo_max_sim or self.templo_1.en_pie == False or self.templo_2.en_pie == False:

            if self.templo_2.en_pie == False:
                self.estadisticas.resultado_final = self.raza_1

            elif self.templo_1.en_pie == False:
                self.estadisticas.resultado_final = self.raza_2

            self.estadisticas.tasa_extraccion_1 /= self.tiempo_sim
            self.estadisticas.tasa_extraccion_2 /= self.tiempo_sim

            self.estadisticas.tasa_creacion_1 = self.estadisticas.guerreros_creados_1 + \
                                                self.estadisticas.arqueros_creados_1 + \
                                                self.estadisticas.mascotas_creadas_1
            self.estadisticas.tasa_creacion_1 /= self.tiempo_sim

            self.estadisticas.tasa_creacion_2 = self.estadisticas.guerreros_creados_2 + \
                                                self.estadisticas.arqueros_creados_2 + \
                                                self.estadisticas.mascotas_creadas_2
            self.estadisticas.tasa_creacion_2 /= self.tiempo_sim

            self.estadisticas.tasa_muerte_1 = self.estadisticas.guerreros_muertos_1 + \
                                              self.estadisticas.arqueros_muertos_1 + \
                                              self.estadisticas.mascotas_muertas_1

            self.estadisticas.tasa_muerte_2 = self.estadisticas.guerreros_muertos_2 + \
                                              self.estadisticas.arqueros_muertos_2 + \
                                              self.estadisticas.mascotas_muertas_2

            self.estadisticas.tasa_muerte_1 /= self.tiempo_sim
            self.estadisticas.tasa_muerte_2 /= self.tiempo_sim

            print("Guerreros muertos 1: ", self.estadisticas.guerreros_muertos_1, "\n",
                  "Arqueros muertos 1: ", self.estadisticas.arqueros_muertos_1, "\n",
                  "Mascotas muertas 1: ", self.estadisticas.mascotas_muertas_1, "\n",
                  "Guerreros muertos 2: ", self.estadisticas.guerreros_muertos_2, "\n",
                  "Arqueros muertos 2: ", self.estadisticas.arqueros_muertos_2, "\n",
                  "Mascotas muertas 2: ", self.estadisticas.mascotas_muertas_2, "\n",
                  "Guerreros creados 1: ", self.estadisticas.guerreros_creados_1, "\n",
                  "Arqueros creados 1: ", self.estadisticas.arqueros_creados_1, "\n",
                  "Mascotas creadas 1: ", self.estadisticas.mascotas_creadas_1, "\n",
                  "Guerreros creados 2: ", self.estadisticas.guerreros_creados_2, "\n",
                  "Arqueros creados 2: ", self.estadisticas.arqueros_creados_2, "\n",
                  "Mascotas creadas 2: ", self.estadisticas.mascotas_creadas_2, "\n",
                  "Poderes usados 1: ", self.estadisticas.poderes_usados_1, "\n",
                  "Poderes usados 2: ", self.estadisticas.poderes_usados_2, "\n",
                  "Efecto poder 1: ", self.estadisticas.efecto_poder_1, "\n",
                  "Efecto poder 2: ", self.estadisticas.efecto_poder_2, "\n",
                  "Tasa muerte 1: ", self.estadisticas.tasa_muerte_1, "\n",
                  "Tasa muerte 2: ", self.estadisticas.tasa_muerte_2, "\n",
                  "Tasa creacion 1: ", self.estadisticas.tasa_creacion_1, "\n",
                  "Tasa creacion 2: ", self.estadisticas.tasa_creacion_2, "\n",
                  "Oro gastado 1: ", self.estadisticas.oro_gastado_1, "\n",
                  "Oro gastado 2: ", self.estadisticas.oro_gastado_2, "\n",
                  "Tasa extracción 1: ", self.estadisticas.tasa_extraccion_1, "\n",
                  "Tasa extracción 2: ", self.estadisticas.tasa_extraccion_2, "\n",
                  "Resultado: Han ganado los " + self.estadisticas.resultado_final)

            exit(0)

        # se añaden números para que las unidades no estén muy cerca
        esparcir_x = randint(0, 50)
        esparcir_y = randint(0, 100)

        # mandamos los aldeanos ociosos a la mina
        for aldeano in self.aldeanos_ociosos_1:

            if casi_igual(aldeano.gui.cord_x, self.x_mina_1) and casi_igual(aldeano.gui.cord_y, self.y_mina_1):
                if len(self.aldeanos_recolectando_1) <= 5:
                    self.aldeanos_recolectando_1.append(aldeano)
                    self.aldeanos_ociosos_1.remove(aldeano)
                    aldeano.gui.hide()


            else:
                angulo = angulo_a_entidad(aldeano, self.x_mina_1, self.y_mina_1)
                aldeano.gui.cord_x += cos(angulo) * aldeano.velocidad_mov
                aldeano.gui.cord_y += sin(angulo) * aldeano.velocidad_mov

        for aldeano in self.aldeanos_ociosos_2:
            if casi_igual(aldeano.gui.cord_x, self.x_mina_2) and casi_igual(aldeano.gui.cord_y, self.y_mina_2):
                if len(self.aldeanos_recolectando_2) <= 5:
                    self.aldeanos_recolectando_2.append(aldeano)
                    self.aldeanos_ociosos_2.remove(aldeano)
                    aldeano.gui.hide()

            else:
                angulo = angulo_a_entidad(aldeano, self.x_mina_2, self.y_mina_2)
                aldeano.gui.cord_x += cos(angulo) * aldeano.velocidad_mov
                aldeano.gui.cord_y += sin(angulo) * aldeano.velocidad_mov

        # esperamos 5 segundos en la mina
        for aldeano in self.aldeanos_recolectando_1:
            if aldeano.ticks_en_mina >= 200:
                self.aldeanos_trayendo_1.append(aldeano)
                self.aldeanos_recolectando_1.remove(aldeano)
                aldeano.ticks_en_mina = 0
                aldeano.gui.show()

            else:
                aldeano.ticks_en_mina += 1

        for aldeano in self.aldeanos_recolectando_2:
            if aldeano.ticks_en_mina >= 200:
                self.aldeanos_trayendo_2.append(aldeano)
                self.aldeanos_recolectando_2.remove(aldeano)
                aldeano.ticks_en_mina = 0
                aldeano.gui.show()

            else:
                aldeano.ticks_en_mina += 1

        # mandamos los aldeanos que salieron al templo
        for aldeano in self.aldeanos_trayendo_1:
            if casi_igual(aldeano.gui.cord_x, self.x_templo_1) and casi_igual(aldeano.gui.cord_y, self.y_templo_1):
                self.gold_1 += 10 + aldeano.fuerza
                self.estadisticas.tasa_extraccion_1 += 10 + aldeano.fuerza
                gui.set_gold_t1(self.gold_1)
                self.aldeanos_ociosos_1.append(aldeano)
                self.aldeanos_trayendo_1.remove(aldeano)
                if self.objetivo.startswith("Recolectar"):
                    self.cantidad_lograda_1 += 10 + aldeano.fuerza
            else:
                angulo = angulo_a_entidad(aldeano, self.x_templo_1, self.y_templo_1)
                aldeano.gui.cord_x += cos(angulo) * aldeano.velocidad_mov
                aldeano.gui.cord_y += sin(angulo) * aldeano.velocidad_mov

        for aldeano in self.aldeanos_trayendo_2:
            if casi_igual(aldeano.gui.cord_x, self.x_templo_2) and casi_igual(aldeano.gui.cord_y, self.y_templo_2):
                self.gold_2 += 10 + aldeano.fuerza
                self.estadisticas.tasa_extraccion_2 += 10 + aldeano.fuerza
                gui.set_gold_t2(self.gold_2)
                self.aldeanos_ociosos_2.append(aldeano)
                self.aldeanos_trayendo_2.remove(aldeano)
                if self.objetivo.startswith("Recolectar"):
                    self.cantidad_lograda_2 += 10 + aldeano.fuerza
            else:
                angulo = angulo_a_entidad(aldeano, self.x_templo_2, self.y_templo_2)
                aldeano.gui.cord_x += cos(angulo) * aldeano.velocidad_mov
                aldeano.gui.cord_y += sin(angulo) * aldeano.velocidad_mov

        self.lista_aldeanos_total_1 = self.aldeanos_recolectando_1 + \
                                      self.aldeanos_trayendo_1 + \
                                      self.aldeanos_ociosos_1 + \
                                      self.aldeanos_construyendo_1

        self.lista_aldeanos_total_2 = self.aldeanos_recolectando_2 + \
                                      self.aldeanos_trayendo_2 + \
                                      self.aldeanos_ociosos_2 + \
                                      self.aldeanos_construyendo_2

        total_aldeanos_1 = len(self.lista_aldeanos_total_1)

        total_aldeanos_2 = len(self.lista_aldeanos_total_2)

        # si faltan aldeanos los creamos
        if total_aldeanos_1 < 6:

            self.templo_1.creando_aldeano = True
            if self.templo_1.ticks_creando_aldeano >= 200:

                aldeano_1_gui = self.unidad_1("villager",
                                              pos=(self.x_templo_1, self.y_templo_1), hp=25)

                aldeano_1 = Aldeano(25, 1, 1, 1, randint(0, 5), aldeano_1_gui)

                gui.add_entity(aldeano_1_gui)
                self.aldeanos_ociosos_1.append(aldeano_1)
                self.templo_1.creando_aldeano = False
                self.gold_1 -= 10
                self.estadisticas.oro_gastado_1 -= 10
                gui.set_gold_t1(self.gold_1)
                self.templo_1.ticks_creando_aldeano = 0

            else:
                self.templo_1.ticks_creando_aldeano += 1

        if total_aldeanos_2 < 6:
            self.templo_2.creando_aldeano = True
            if self.templo_2.ticks_creando_aldeano >= 200:
                aldeano_2_gui = self.unidad_2("villager",
                                              pos=(self.x_templo_2, self.y_templo_2), hp=25)

                aldeano_2 = Aldeano(25, 1, 1, 1, randint(0, 5), aldeano_2_gui)

                gui.add_entity(aldeano_2_gui)
                self.aldeanos_ociosos_2.append(aldeano_2)
                self.templo_2.creando_aldeano = False
                self.gold_2 -= 10
                self.estadisticas.oro_gastado_2 -= 10
                gui.set_gold_t2(self.gold_2)
                self.templo_2.ticks_creando_aldeano = 0
            else:
                self.templo_2.ticks_creando_aldeano += 1

        total_tropas_1 = len(self.lista_guerreros_1) + \
                         len(self.lista_arqueros_1) + \
                         len(self.lista_mascotas_1)

        total_tropas_2 = len(self.lista_guerreros_2) + \
                         len(self.lista_arqueros_2) + \
                         len(self.lista_mascotas_2)

        # si faltan tropas las creamos
        if total_tropas_1 < self.max_tropas_1:

            # creamos los guerreros
            if self.cuartel_1.guerreros_creados < self.guerreros_ciclo_1 and \
                            self.gold_1 > 20 and self.cuartel_1.en_pie:
                crear_guerrero_1(self, gui, self.modificador_daño_1, self.modificador_velocidad_1,
                                 self.modificador_vida_1)


            # creamos los arqueros
            elif self.cuartel_1.arqueros_creados < self.arqueros_ciclo_1 and \
                            self.gold_1 > 30 and self.cuartel_1.en_pie:
                crear_arquero_1(self, gui, self.modificador_daño_1, self.modificador_velocidad_1,
                                self.modificador_vida_1)

            # creamos las mascotas
            if self.cuartel_1.arqueros_creados == self.arqueros_ciclo_1 and self.gold_1 > 50:
                crear_mascota_1(self, gui, self.modificador_daño_1, self.modificador_velocidad_1,
                                self.modificador_vida_1)

        if total_tropas_2 < self.max_tropas_2:

            if self.cuartel_2.guerreros_creados < self.guerreros_ciclo_2 and \
                            self.gold_1 > 20 and self.cuartel_2.en_pie:

                crear_guerrero_2(self, gui, self.modificador_daño_2, self.modificador_velocidad_2,
                                 self.modificador_vida_2)

            elif self.cuartel_2.arqueros_creados < self.arqueros_ciclo_2 and \
                            self.gold_1 > 30 and self.cuartel_2.en_pie:

                crear_arquero_2(self, gui, self.modificador_daño_2, self.modificador_velocidad_2,
                                self.modificador_vida_2)

            if self.cuartel_2.arqueros_creados == self.arqueros_ciclo_2 and self.gold_1 > 50:
                crear_mascota_2(self, gui, self.modificador_daño_2, self.modificador_velocidad_2,
                                self.modificador_vida_2)

        # reiniciamos el ciclo
        if self.templo_1.mascotas_creadas == self.mascotas_ciclo_1:
            self.cuartel_1.guerreros_creados = 0
            self.cuartel_1.arqueros_creados = 0
            self.templo_1.mascotas_creadas = 0

        if self.templo_2.mascotas_creadas == self.mascotas_ciclo_2:
            self.cuartel_2.guerreros_creados = 0
            self.cuartel_2.arqueros_creados = 0
            self.templo_2.mascotas_creadas = 0

        # si el heroe desaparece, se reinicia el tiempo de aparición
        if not self.heroe_1_presente:
            self.tiempo_heroe_1 = self.tiempo_sim + round(expovariate(self.tasa_invocacion_1))

        if not self.heroe_2_presente:
            self.tiempo_heroe_2 = self.tiempo_sim + round(expovariate(self.tasa_invocacion_2))

        # llega el héroe

        if self.tiempo_sim >= self.tiempo_heroe_1 and not self.heroe_1_presente:
            hero_1_gui = self.unidad_1("hero",
                                       pos=(self.x_templo_1 + esparcir_x, self.y_templo_1 + esparcir_y), hp=100)
            gui.add_entity(hero_1_gui)

            if self.unidad_1.__name__ == "Orc":
                self.hero_1 = Hero(velocidad_mov=1.5, puntos_vida=100, puntos_daño=1, rango=20,
                                   gui=hero_1_gui)

            if self.unidad_1.__name__ == "Human":
                self.hero_1 = Hero(velocidad_mov=1.5, puntos_vida=100, puntos_daño=3, rango=5,
                                   gui=hero_1_gui)

            if self.unidad_1.__name__ == "Skull":
                self.hero_1 = Hero(velocidad_mov=1.5, puntos_vida=50, puntos_daño=3, rango=5,
                                   gui=hero_1_gui)
                self.hero_1.gui.health = 50
            self.heroe_1_presente = True

        if self.tiempo_sim >= self.tiempo_heroe_2 and not self.heroe_2_presente:

            hero_2_gui = self.unidad_2("hero",
                                       pos=(self.x_templo_2 + esparcir_x, self.y_templo_2 + esparcir_y), hp=100)
            gui.add_entity(hero_2_gui)

            if self.unidad_2.__name__ == "Orc":
                self.hero_2 = Hero(velocidad_mov=1.5, puntos_vida=100, puntos_daño=1, rango=20,
                                   gui=hero_2_gui)

            if self.unidad_2.__name__ == "Human":
                self.hero_2 = Hero(velocidad_mov=1.5, puntos_vida=100, puntos_daño=3, rango=5,
                                   gui=hero_2_gui)

            if self.unidad_2.__name__ == "Skull":
                self.hero_2 = Hero(velocidad_mov=1.5, puntos_vida=100, puntos_daño=3, rango=5,
                                   gui=hero_2_gui)
            self.heroe_2_presente = True

        # ataque de las unidades

        self.ejercito_1 = self.lista_guerreros_1 + self.lista_arqueros_1 + self.lista_mascotas_1
        self.objetivos_1 = self.ejercito_1[:] + self.lista_aldeanos_total_1

        self.objetivos_1.append(self.templo_1)

        if self.cuartel_1.en_pie:
            self.objetivos_1.append(self.cuartel_1)

        if self.torreta_1.en_pie:
            self.objetivos_1.append(self.torreta_1)

        self.objetivos_1.append(self.hero_1)

        self.ejercito_2 = self.lista_guerreros_2 + self.lista_arqueros_2 + self.lista_mascotas_2
        self.objetivos_2 = self.ejercito_2[:] + self.lista_aldeanos_total_2

        self.objetivos_2.append(self.templo_2)
        if self.cuartel_2.en_pie:
            self.objetivos_2.append(self.cuartel_2)
        if self.torreta_2.en_pie:
            self.objetivos_2.append(self.torreta_2)

        self.objetivos_2.append(self.hero_2)

        if self.unidad_1.__name__ == "Human":

            for combatiente in self.ejercito_1:

                if combatiente.__class__.__name__ == "Mascota" and self.no_mover_mascotas_1:
                    pass


                elif len(self.ejercito_1) >= 0.75 * len(self.ejercito_2) or combatiente.atacado == True:
                    enemigo = mas_cercano(combatiente, self.objetivos_2)
                    if enemigo and not self.glaciar_en_proceso_2:

                        if enemigo.puntos_vida >= 0:

                            atacar(combatiente, enemigo)
                            enemigo.atacado = True
                        else:
                            seguir = muerte_1(self, enemigo)
                            if not seguir:
                                break

        if self.unidad_1.__name__ == "Orc":
            for combatiente in self.ejercito_1:
                enemigo = mas_cercano(combatiente, self.objetivos_2)

                if combatiente.__class__.__name__ == "Mascota" and self.no_mover_mascotas_1:
                    pass
                elif enemigo and not self.glaciar_en_proceso_2:
                    if enemigo.puntos_vida >= 0:

                        atacar(combatiente, enemigo)
                        enemigo.atacado = True
                    else:
                        seguir = muerte_1(self, enemigo)
                        if not seguir:
                            break

        if self.unidad_1.__name__ == "Skull":
            for combatiente in self.ejercito_1:
                enemigo = self.templo_2
                if combatiente.__class__.__name__ == "Mascota" and self.no_mover_mascotas_1:
                    pass

                else:
                    if combatiente.atacado == True:
                        enemigo = mas_cercano(combatiente, self.objetivos_2)
                    if enemigo and not self.glaciar_en_proceso_2:

                        if enemigo.puntos_vida >= 0:

                            atacar(combatiente, enemigo)
                            enemigo.atacado = True
                        else:
                            seguir = muerte_1(self, enemigo)
                            if not seguir:
                                break

        # ataque torres
        enemigo = mas_cercano(self.torreta_1, self.objetivos_2)
        if enemigo.puntos_vida >= 0:

            ataque_torreta(self.torreta_1, enemigo)
            enemigo.atacado = True
        else:
            muerte_1(self, enemigo)

        # ejercito 2


        if self.unidad_2.__name__ == "Human":

            for combatiente in self.ejercito_1:
                if combatiente.__class__.__name__ == "Mascota" and self.no_mover_mascotas_2:
                    pass
                if len(self.ejercito_2) >= 0.75 * len(self.ejercito_1) or combatiente.atacado == True:
                    enemigo = mas_cercano(combatiente, self.objetivos_1)
                    if enemigo and self.glaciar_en_proceso_1 == False:

                        if enemigo.puntos_vida >= 0:

                            atacar(combatiente, enemigo)
                            enemigo.atacado = True
                        else:
                            seguir = muerte_2(self, enemigo)
                            if not seguir:
                                break

        if self.unidad_2.__name__ == "Orc":
            for combatiente in self.ejercito_1:
                enemigo = mas_cercano(combatiente, self.objetivos_1)
                if combatiente.__class__.__name__ == "Mascota" and self.no_mover_mascotas_2:
                    pass

                elif enemigo and self.glaciar_en_proceso_1 == False:
                    if enemigo.puntos_vida >= 0:

                        atacar(combatiente, enemigo)
                        enemigo.atacado = True
                    else:
                        seguir = muerte_2(self, enemigo)
                        if not seguir:
                            break

        if self.unidad_2.__name__ == "Skull":
            for combatiente in self.ejercito_2:
                enemigo = self.templo_1
                if combatiente.__class__.__name__ == "Mascota" and self.no_mover_mascotas_2:
                    pass

                else:
                    if combatiente.atacado == True:
                        enemigo = mas_cercano(combatiente, self.objetivos_1)
                    if enemigo and self.glaciar_en_proceso_1 == False:
                        if enemigo.puntos_vida >= 0:

                            atacar(combatiente, enemigo)
                            enemigo.atacado = True
                        else:
                            seguir = muerte_2(self, enemigo)
                            if not seguir:
                                break

        # ataque torres
        enemigo = mas_cercano(self.torreta_2, self.objetivos_1)
        if enemigo.puntos_vida >= 0:

            ataque_torreta(self.torreta_2, enemigo)
            enemigo.atacado = True
        else:
            muerte_2(self, enemigo)

        # ataque héroes

        if self.heroe_1_presente:
            if self.unidad_1.__name__ == "Orc":
                if not self.mascotas_orco_creadas_1:
                    mascota_1_gui = self.unidad_1("pet",
                                                  pos=(self.x_templo_1 + esparcir_x, self.y_templo_1 + esparcir_y),
                                                  hp=35)
                    mascota_2_gui = self.unidad_1("pet",
                                                  pos=(self.x_templo_1 + 5, self.y_templo_1 + 10),
                                                  hp=35)
                    gui.add_entity(mascota_1_gui)
                    gui.add_entity(mascota_2_gui)
                    mascota_1 = Mascota(velocidad_mov=1.3 * self.modificador_velocidad_1,
                                        puntos_vida=35 * self.modificador_vida_1,
                                        puntos_daño=0.65 * self.modificador_daño_1, rango=15, gui=mascota_1_gui)
                    mascota_2 = Mascota(velocidad_mov=1.3 * self.modificador_velocidad_1,
                                        puntos_vida=35 * self.modificador_vida_1,
                                        puntos_daño=0.65 * self.modificador_daño_1, rango=15, gui=mascota_2_gui)
                    self.lista_mascotas_1.append(mascota_1)

                    self.lista_mascotas_1.append(mascota_2)

                    self.mascotas_orco_creadas_1 = True

                enemigo = mas_cercano(self.hero_1, self.objetivos_2)
                if enemigo:
                    if enemigo.puntos_vida >= 0:

                        atacar(self.hero_1, enemigo)
                        enemigo.atacado = True
                    else:
                        muerte_1(self, enemigo)

            if self.unidad_1.__name__ == "Human":

                enemigo = mas_cercano(self.hero_1, self.objetivos_2)
                if enemigo:
                    if enemigo.puntos_vida >= 0:

                        ataque_cristian_1(self.hero_1, enemigo, self)
                        enemigo.atacado = True
                    else:
                        muerte_1(self, enemigo)

            if self.unidad_1.__name__ == "Skull":
                enemigo = mas_cercano(self.hero_1, self.objetivos_2)
                if enemigo:
                    if enemigo.puntos_vida >= 0:

                        atacar(self.hero_1, enemigo)
                        enemigo.atacado = True
                    else:
                        muerte_1(self, enemigo)

        # héroe ejército 2

        if self.heroe_2_presente:
            if self.unidad_2.__name__ == "Orc":
                if not self.mascotas_orco_creadas_1:
                    mascota_1_gui = self.unidad_2("pet",
                                                  pos=(self.x_templo_2 + esparcir_x, self.y_templo_2 + esparcir_y),
                                                  hp=35)
                    mascota_2_gui = self.unidad_2("pet",
                                                  pos=(self.x_templo_2 + esparcir_x, self.y_templo_2 + esparcir_y),
                                                  hp=35)
                    gui.add_entity(mascota_2_gui)
                    gui.add_entity(mascota_2_gui)
                    mascota_1 = Mascota(velocidad_mov=1.3 * self.modificador_velocidad_2,
                                        puntos_vida=35 * self.modificador_vida_2,
                                        puntos_daño=0.65 * self.modificador_daño_2, rango=15, gui=mascota_1_gui)
                    mascota_2 = Mascota(velocidad_mov=1.3 * self.modificador_velocidad_2,
                                        puntos_vida=35 * self.modificador_vida_2,
                                        puntos_daño=0.65 * self.modificador_daño_2, rango=15, gui=mascota_2_gui)
                    self.lista_mascotas_2.append(mascota_1)

                    self.lista_mascotas_2.append(mascota_2)

                    self.mascotas_orco_creadas_2 = True

                enemigo = mas_cercano(self.hero_2, self.objetivos_1)
                if enemigo:
                    if enemigo.puntos_vida >= 0:

                        atacar(self.hero_2, enemigo)
                        enemigo.atacado = True
                    else:
                        muerte_2(self, enemigo)

            if self.unidad_2.__name__ == "Human":
                enemigo = mas_cercano(self.hero_2, self.objetivos_1)
                if enemigo:
                    if enemigo.puntos_vida >= 0:

                        ataque_cristian_2(self.hero_2, enemigo, self)
                        enemigo.atacado = True
                    else:
                        muerte_2(self, enemigo)

            if self.unidad_2.__name__ == "Skull":

                enemigo = mas_cercano(self.hero_2, self.objetivos_1)
                if enemigo:
                    if enemigo.puntos_vida >= 0:

                        atacar(self.hero_2, enemigo)
                        enemigo.atacado = True
                    else:
                        muerte_2(self, enemigo)

        # los aldeanos muertos se eliminan de las listas
        eliminar_aldeanos(self)

        # se reconstruyen los edificios que no están en pie
        if self.torreta_1.en_pie == False:
            if self.torreta_1_pagada == False:
                self.gold_1 -= 150
                gui.set_gold_t1(self.gold_1)
                self.torreta_1_pagada = True
                self.estadisticas.oro_gastado_1 += 150

            construir_edificio_1(self, self.torreta_1)

        if self.torreta_2.en_pie == False:
            if self.torreta_2_pagada == False:
                self.gold_2 -= 150
                gui.set_gold_t2(self.gold_1)
                self.torreta_2_pagada = True
                self.estadisticas.oro_gastado_2 += 150

            construir_edificio_2(self, self.torreta_2)

        if self.cuartel_1.en_pie == False:
            if self.cuartel_1_pagado == False:
                self.gold_1 -= 100
                gui.set_gold_t1(self.gold_1)
                self.cuartel_1_pagado = True

            construir_edificio_1(self, self.cuartel_1)

        if self.cuartel_2.en_pie == False:
            if self.cuartel_1_pagado == False:
                self.gold_2 -= 100
                gui.set_gold_t2(self.gold_2)
                self.cuartel_2_pagado = True
                self.estadisticas.oro_gastado_2 += 100

            construir_edificio_2(self, self.cuartel_2)

        if self.cuartel_1.en_pie and self.torreta_1.en_pie:
            for aldeano in self.aldeanos_construyendo_1:
                self.aldeanos_ociosos_1.append(aldeano)
                self.aldeanos_construyendo_1.remove(aldeano)

        if self.cuartel_2.en_pie and self.torreta_2.en_pie:
            for aldeano in self.aldeanos_construyendo_2:
                self.aldeanos_ociosos_2.append(aldeano)
                self.aldeanos_construyendo_2.remove(aldeano)

        # para probar un poder:
        # glaciar_1(self)
        # terremoto_2(self)
        # etc

        # si se cumple el objetivo se ocupa el poder y se cambia el objetivo
        if self.cantidad_lograda_1 >= self.maximo_objetivo and not self.objetivo_logrado_2:

            if self.objetivo not in self.set_objetivos_logrados_1:
                self.set_objetivos_logrados_1.add(self.objetivo)
                self.objetivo_logrado_1 = True
                self.ocupar_poder_1 = True
                self.cambiar_objetivo = True
                self.estadisticas.poderes_usados_1 += 1

        if self.cantidad_lograda_2 >= self.maximo_objetivo and not self.objetivo_logrado_1:

            if self.objetivo not in self.set_objetivos_logrados_2:
                self.set_objetivos_logrados_2.add(self.objetivo)
                self.objetivo_logrado_2 = True
                self.ocupar_poder_2 = True
                self.cambiar_objetivo = True
                self.estadisticas.poderes_usados_2 += 1
        if self.cambiar_objetivo:
            self.objetivo_num = choice([1, 2, 3])
            self.objetivo = self.posibles_objetivos.get(self.objetivo_num)[0] + self.target.get(self.objetivo_num) + \
                            self.posibles_objetivos.get(self.objetivo_num)[1]
            gui.set_objective(self.objetivo)
            self.maximo_objetivo = int(self.target.get(self.objetivo_num))
            self.cambiar_objetivo = False
            self.cantidad_lograda_1 = 0
            self.cantidad_lograda_2 = 0

        if self.ocupar_poder_1:

            self.poder_1(self)
            if self.poder_en_proceso_1 == False:
                self.ocupar_poder_1 = False

        if self.ocupar_poder_2:

            self.poder_1(self)
            if self.poder_en_proceso_2 == False:
                self.ocupar_poder_2 = False

        if self.ticks_terremoto == self.max_terremotos:
            self.terremoto_en_proceso = False

        self.tiempo_sim += 0.025
