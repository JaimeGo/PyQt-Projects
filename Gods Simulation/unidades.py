from random import randint


class Unidad:
    def __init__(self, puntos_vida, velocidad_mov, gui):
        self.puntos_vida = puntos_vida
        self.velocidad_mov = velocidad_mov
        self.atacado = False
        self.gui = gui


class Aldeano(Unidad):
    def __init__(self, puntos_vida, velocidad_mov, velocidad_rec, velocidad_con, fuerza, gui):
        super().__init__(puntos_vida, velocidad_mov, gui)
        self.velocidad_con = velocidad_con
        self.velocidad_rec = velocidad_rec
        self.fuerza = fuerza
        self.ticks_en_mina = 0


class Peleador(Unidad):
    def __init__(self, puntos_vida, velocidad_mov, puntos_daño, gui):
        super().__init__(puntos_vida, velocidad_mov, gui)
        self.puntos_daño = puntos_daño


class Guerrero(Peleador):
    def __init__(self, velocidad_mov, puntos_vida, puntos_daño, rango, gui):
        super().__init__(puntos_vida, velocidad_mov, puntos_daño, gui)
        self.rango = rango


class Arquero(Peleador):
    def __init__(self, velocidad_mov, puntos_vida, puntos_daño, rango, gui):
        super().__init__(puntos_vida, velocidad_mov, puntos_daño, gui)
        self.rango = rango


class Mascota(Peleador):
    def __init__(self, velocidad_mov, puntos_vida, puntos_daño, rango, gui):
        super().__init__(puntos_vida, velocidad_mov, puntos_daño, gui)
        self.rango = rango


class Hero(Peleador):
    def __init__(self, velocidad_mov, puntos_vida, puntos_daño, rango, gui):
        super().__init__(puntos_vida, velocidad_mov, puntos_daño, gui)
        self.rango = rango


def crear_guerrero_1(simul, gui, modificador_daño_1, modificador_velocidad_1, modificador_vida_1):
    esparcir_x = randint(0, 50)
    esparcir_y = randint(0, 100)

    simul.cuartel_1.ticks_guerrero += 1
    if simul.cuartel_1.ticks_guerrero == 200:
        guerrero_1_gui = simul.unidad_1("warrior",
                                        pos=(simul.x_cuartel_1 + esparcir_x, simul.y_cuartel_1 + esparcir_y),
                                        hp=50 * modificador_vida_1)

        gui.add_entity(guerrero_1_gui)
        guerrero_1 = Guerrero(velocidad_mov=1.1 * modificador_velocidad_1,
                              puntos_vida=50 * modificador_vida_1, puntos_daño=1 * modificador_daño_1, rango=5,
                              gui=guerrero_1_gui)
        simul.lista_guerreros_1.append(guerrero_1)
        simul.cuartel_1.guerreros_creados += 1
        simul.cuartel_1.ticks_guerrero = 0
        simul.gold_1 -= 20
        gui.set_gold_t1(simul.gold_1)
        simul.estadisticas.oro_gastado_1 += 20
        simul.estadisticas.guerreros_creados_1 += 1
        if simul.objetivo.startswith("Crear"):
            if simul.dios_1 != "flo":
                simul.cantidad_lograda_1 += 1


def crear_guerrero_2(simul, gui, modificador_daño_2, modificador_velocidad_2, modificador_vida_2):
    esparcir_x = randint(0, 50)
    esparcir_y = randint(0, 100)

    simul.cuartel_2.ticks_guerrero += 1
    if simul.cuartel_2.ticks_guerrero == 200:
        guerrero_2_gui = simul.unidad_2("warrior",
                                        pos=(simul.x_cuartel_2 + esparcir_x, simul.y_cuartel_2 + esparcir_y),
                                        hp=50 * modificador_vida_2)

        gui.add_entity(guerrero_2_gui)
        guerrero_2 = Guerrero(velocidad_mov=1.1 * modificador_velocidad_2,
                              puntos_vida=50 * modificador_vida_2, puntos_daño=1 * modificador_daño_2, rango=5,
                              gui=guerrero_2_gui)
        simul.lista_guerreros_2.append(guerrero_2)
        simul.cuartel_2.guerreros_creados += 1
        simul.cuartel_2.ticks_guerrero = 0
        simul.gold_2 -= 20
        gui.set_gold_t1(simul.gold_2)
        simul.estadisticas.oro_gastado_2 += 20
        simul.estadisticas.guerreros_creados_2 += 1
        if simul.objetivo.startswith("Crear"):
            if simul.dios_2 != "flo":
                simul.cantidad_lograda_2 += 1


def crear_arquero_1(simul, gui, modificador_daño_1, modificador_velocidad_1, modificador_vida_1):
    esparcir_x = randint(0, 50)
    esparcir_y = randint(0, 100)
    simul.cuartel_1.ticks_arquero += 1
    if simul.cuartel_1.ticks_arquero == 200:
        arquero_1_gui = simul.unidad_1("distance",
                                       pos=(simul.x_cuartel_1 + esparcir_x, simul.y_cuartel_1 + esparcir_y),
                                       hp=40 * modificador_vida_1)

        gui.add_entity(arquero_1_gui)
        arquero_1 = Arquero(velocidad_mov=1.2 * modificador_velocidad_1, puntos_vida=40 * modificador_vida_1,
                            puntos_daño=0.75 * modificador_daño_1, rango=110,
                            gui=arquero_1_gui)
        simul.lista_arqueros_1.append(arquero_1)
        simul.cuartel_1.arqueros_creados += 1
        simul.cuartel_1.ticks_arquero = 0
        simul.gold_1 -= 30
        gui.set_gold_t1(simul.gold_1)
        simul.estadisticas.oro_gastado_1 += 30
        simul.estadisticas.arqueros_creados_1 += 1
        if simul.objetivo.startswith("Crear"):
            if simul.dios_1 != "flo":
                simul.cantidad_lograda_2 += 1


def crear_arquero_2(simul, gui, modificador_daño_2, modificador_velocidad_2, modificador_vida_2):
    esparcir_x = randint(0, 50)
    esparcir_y = randint(0, 100)
    simul.cuartel_2.ticks_arquero += 1
    if simul.cuartel_2.ticks_arquero == 200:
        arquero_2_gui = simul.unidad_2("distance",
                                       pos=(simul.x_cuartel_2 + esparcir_x, simul.y_cuartel_2 + esparcir_y),
                                       hp=40 * modificador_vida_2)

        gui.add_entity(arquero_2_gui)
        arquero_2 = Arquero(velocidad_mov=1.2 * modificador_velocidad_2, puntos_vida=40 * modificador_vida_2,
                            puntos_daño=0.75 * modificador_daño_2, rango=110,
                            gui=arquero_2_gui)
        simul.lista_arqueros_2.append(arquero_2)
        simul.cuartel_2.arqueros_creados += 1
        simul.cuartel_2.ticks_arquero = 0
        simul.gold_2 -= 30
        gui.set_gold_t1(simul.gold_2)
        simul.estadisticas.oro_gastado_2 += 30
        simul.estadisticas.arqueros_creados_2 += 1
        if simul.objetivo.startswith("Crear"):
            if simul.dios_2 != "flo":
                simul.cantidad_lograda_2 += 1


def crear_mascota_1(simul, gui, modificador_daño_1, modificador_velocidad_1, modificador_vida_1):
    esparcir_x = randint(0, 50)
    esparcir_y = randint(0, 100)
    if not simul.templo_1.creando_aldeano:
        simul.templo_1.ticks_creando_mascotas += 1
        if simul.templo_1.ticks_creando_mascotas == 200:
            mascota_1_gui = simul.unidad_1("pet", pos=(simul.x_templo_1 + esparcir_x, simul.y_templo_1 + esparcir_y),
                                           hp=35 * modificador_vida_1)
            gui.add_entity(mascota_1_gui)
            mascota_1 = Mascota(velocidad_mov=1.3 * modificador_velocidad_1, puntos_vida=35 * modificador_vida_1,
                                puntos_daño=0.65 * modificador_daño_1, rango=70, gui=mascota_1_gui)
            simul.lista_mascotas_1.append(mascota_1)
            simul.templo_1.mascotas_creadas += 1
            simul.templo_1.ticks_creando_mascotas = 0
            simul.gold_1 -= 50
            gui.set_gold_t1(simul.gold_1)
            simul.estadisticas.oro_gastado_1 += 50
            simul.estadisticas.mascotas_creadas_1 += 1
            if simul.objetivo.startswith("Crear"):
                if simul.dios_1 == "flo":
                    simul.cantidad_lograda_1 += 1


def crear_mascota_2(simul, gui, modificador_daño_2, modificador_velocidad_2, modificador_vida_2):
    esparcir_x = randint(0, 50)
    esparcir_y = randint(0, 100)
    if not simul.templo_2.creando_aldeano:
        simul.templo_2.ticks_creando_mascotas += 1
        if simul.templo_2.ticks_creando_mascotas == 200:
            mascota_2_gui = simul.unidad_2("pet", pos=(simul.x_templo_2 + esparcir_x, simul.y_templo_2 + esparcir_y),
                                           hp=35 * modificador_vida_2)
            gui.add_entity(mascota_2_gui)
            mascota_2 = Mascota(velocidad_mov=1.3 * modificador_velocidad_2, puntos_vida=35 * modificador_vida_2,
                                puntos_daño=0.65 * modificador_daño_2, rango=70, gui=mascota_2_gui)
            simul.lista_mascotas_2.append(mascota_2)
            simul.templo_2.mascotas_creadas += 1
            simul.templo_2.ticks_creando_mascotas = 0
            simul.gold_2 -= 50
            gui.set_gold_t1(simul.gold_2)
            simul.estadisticas.oro_gastado_2 += 50
            simul.estadisticas.mascotas_creadas_2 += 1
            if simul.objetivo.startswith("Crear"):
                if simul.dios_2 == "flo":
                    simul.cantidad_lograda_2 += 1
