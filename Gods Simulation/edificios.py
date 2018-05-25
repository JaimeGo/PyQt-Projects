class Estructura:
    def __init__(self, puntos_vida, gui):
        self.puntos_vida = puntos_vida
        self.en_pie = True
        self.atacado = False
        self.gui = gui


class Cuartel(Estructura):
    def __init__(self, puntos_vida, gui):
        super().__init__(puntos_vida, gui)
        self.guerreros_creados = 0
        self.ticks_guerrero = 0
        self.arqueros_creados = 0
        self.ticks_arquero = 0
        self.continuar = True
        self.constru = None
        self.unidades_para_construir = 3


class Torreta(Estructura):
    def __init__(self, puntos_vida, velocidad_ataque, puntos_daño, gui, rango):
        super().__init__(puntos_vida, gui)
        self.velocidad_ataque = velocidad_ataque
        self.puntos_daño = puntos_daño
        self.constru = None
        self.unidades_para_construir = 2
        self.rango = rango


class Templo(Estructura):
    def __init__(self, puntos_vida, gui):
        super().__init__(puntos_vida, gui)
        self.creando_aldeano = False
        self.ticks_creando_aldeano = 0
        self.ticks_creando_mascotas = 0
        self.mascotas_creadas = 0


class Mina(Estructura):
    def __init__(self, puntos_vida, gui):
        super().__init__(puntos_vida, gui)
