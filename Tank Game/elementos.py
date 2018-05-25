from objeto_gui import ObjetoGui
from PyQt4.QtCore import Qt
from PyQt4 import QtGui
from math import cos, sin, pi
from operaciones_matematicas import distancia, angulo_a_cursor
from random import choice
from colisiones import powerup_azul, powerup_blanco, powerup_rojo, moneda


class ParedDura(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/paredes/pared_dura", pos, tamaño=(35, 35))
        mainwindow.añadir_objeto_gui(self)


class ParedBlanda(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/paredes/pared_blanda", pos, tamaño=(35, 35))
        mainwindow.añadir_objeto_gui(self)


class Portal(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/portal", pos, tamaño=(35, 35))
        mainwindow.añadir_objeto_gui(self)
        self.lugar_aparicion = ""
        self.tiempo_hasta_disponible = 0

    def hacer_disponible(self):
        if self.tiempo_hasta_disponible >= 0:
            self.tiempo_hasta_disponible -= 0.025


class PowerUpExplosiva(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/powerup_rojo", pos, tamaño=(25, 25))
        mainwindow.añadir_objeto_gui(self)
        self.mainwindow = mainwindow

    def manejar_colision(self):
        powerup_rojo(self)


class PowerUpRalentizante(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/powerup_azul", pos, tamaño=(25, 25))
        mainwindow.añadir_objeto_gui(self)
        self.mainwindow = mainwindow

    def manejar_colision(self):
        powerup_azul(self)


class PowerUpPenetrante(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/powerup_blanco", pos, tamaño=(25, 25))
        mainwindow.añadir_objeto_gui(self)
        self.mainwindow = mainwindow

    def manejar_colision(self):
        powerup_blanco(self)


class Moneda(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/moneda", pos, tamaño=(25, 25))
        mainwindow.añadir_objeto_gui(self)
        self.mainwindow = mainwindow

    def manejar_colision(self):
        moneda(self)


class Escudo:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.mainwindow.escudo = self
        self.protecciones_restantes = 3
        self.cursor = QtGui.QCursor()

    def proteger(self):

        for bala in self.mainwindow.lista_balas_disparadas:

            angulo_cursor = 270 + angulo_a_cursor((self.cursor.pos().x() - self.mainwindow.pos().x(),
                                                   self.cursor.pos().y() - self.mainwindow.pos().y() - 25),
                                                  (self.mainwindow.tanque_principal.cord_x + 15,
                                                   self.mainwindow.tanque_principal.cord_y + 15))
            angulo_bala = bala.angulo_bala * 180 / pi % 360

            diferencia_angulos = angulo_cursor - angulo_bala

            condicion_cañon = False

            if diferencia_angulos > 270 or diferencia_angulos < 90:
                condicion_cañon = True

            if distancia(self.mainwindow.tanque_principal, bala) < 20 and condicion_cañon:
                bala.hide()
                self.mainwindow.lista_balas_disparadas.remove(bala)
                self.protecciones_restantes -= 1

                if self.protecciones_restantes == 0:
                    self.mainwindow.escudo = None


class PowerUpEscudo(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/escudo", pos, tamaño=(25, 25))
        mainwindow.añadir_objeto_gui(self)
        self.mainwindow = mainwindow

    def manejar_colision(self):
        if distancia(self, self.mainwindow.tanque_principal) < 10:
            self.hide()
            self.mainwindow.lista_elementos.remove(self)
            self.mainwindow.escudo = Escudo(self.mainwindow)


class Bomba(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/bomba", pos, tamaño=(25, 25))
        mainwindow.añadir_objeto_gui(self)
        mainwindow.lista_bombas.append(self)
        self.mainwindow = mainwindow
        self.tiempo_hasta_boom = 3

    def tick(self):
        self.tiempo_hasta_boom -= 0.025
        if self.tiempo_hasta_boom <= 0:
            self.hide()
            self.mainwindow.lista_bombas.remove(self)
            self.mainwindow.lista_explosiones.append(Explosion(self.mainwindow, (self.cord_x, self.cord_y)))
            for enemigo in self.mainwindow.lista_enemigos:
                if distancia(self, enemigo) <= self.mainwindow.tanque_principal.radio:
                    enemigo.salud -= 40


class Explosion(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/explosion", pos, tamaño=(25, 25))
        self.mainwindow = mainwindow
        mainwindow.añadir_objeto_gui(self)
        mainwindow.lista_explosiones.append(self)
        self.tiempo_hasta_desaparicion = 2

    def hacer_desaparer(self):
        if self.tiempo_hasta_desaparicion <= 0:
            self.hide()
            self.mainwindow.lista_explosiones.remove(self)

        else:
            self.tiempo_hasta_desaparicion -= 0.025


def crear_powerup(mainwindow, pos):
    elegido = choice(["moneda", "escudo", "penetrante", "ralentizante", "explosiva"])
    powerup = None

    if elegido == "moneda":
        powerup = Moneda(mainwindow, pos)

    if elegido == "escudo":
        powerup = PowerUpEscudo(mainwindow, pos)

    if elegido == "penetrante":
        powerup = PowerUpPenetrante(mainwindow, pos)

    if elegido == "ralentizante":
        powerup = PowerUpRalentizante(mainwindow, pos)

    if elegido == "explosiva":
        powerup = PowerUpExplosiva(mainwindow, pos)

    mainwindow.lista_elementos.append(powerup)
