from operaciones_matematicas import distancia
from random import randint, choice
from objeto_gui import ObjetoGui
from math import pi


class MiniExplosion(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/explosion", pos, tamaño=(25, 25))
        self.mainwindow = mainwindow
        mainwindow.añadir_objeto_gui(self)
        mainwindow.lista_explosiones.append(self)
        self.tiempo_hasta_desaparicion = 2

        self.tamaño_x -= 3
        self.tamaño_y -= 3
        self.refrescar_pixmap()

    def hacer_desaparer(self):
        if self.tiempo_hasta_desaparicion <= 0:
            self.hide()
            self.mainwindow.lista_explosiones.remove(self)

        else:
            self.tiempo_hasta_desaparicion -= 0.025


def principal_con_portales(self):
    for portal in self.mainwindow.lista_portales:
        if len(self.mainwindow.lista_portales) == 2:
            if distancia(self, portal) <= 50 and portal.tiempo_hasta_disponible <= 0:

                if self.mainwindow.lista_portales[1] == portal:
                    otro_portal = self.mainwindow.lista_portales[0]
                else:
                    otro_portal = self.mainwindow.lista_portales[1]
                portal.tiempo_hasta_disponible = 3
                otro_portal.tiempo_hasta_disponible = 3

                if otro_portal.lugar_aparicion == "derecha":
                    self.cord_x = otro_portal.cord_x + 30
                    self.cord_y = otro_portal.cord_y
                elif otro_portal.lugar_aparicion == "izquierda":
                    self.cord_x = otro_portal.cord_x - 30
                    self.cord_y = otro_portal.cord_y
                elif otro_portal.lugar_aparicion == "arriba":
                    self.cord_x = otro_portal.cord_x
                    self.cord_y = otro_portal.cord_y - 30
                elif otro_portal.lugar_aparicion == "abajo":
                    self.cord_x = otro_portal.cord_x
                    self.cord_y = otro_portal.cord_y + 30


def bala_con_muralla(self):
    if self.cord_x <= 20 or self.cord_y <= 20 or self.cord_x >= 550 or self.cord_y >= 550:
        self.hide()
        self.mainwindow.lista_balas_disparadas.remove(self)
        self.sin_impacto = False


def bala_con_paredes(self):
    for pared in self.mainwindow.lista_paredes_blandas:
        if distancia(self, pared) < 30:
            self.mainwindow.lista_paredes_blandas.remove(pared)
            pared.hide()
            self.mainwindow.lista_balas_disparadas.remove(self)
            self.hide()

    for pared in self.mainwindow.lista_paredes_duras:
        if distancia(self, pared) < 30:
            self.angulo_bala -= 90


def bala_normal_con_enemigo(self):
    for enemigo in self.mainwindow.lista_enemigos:
        if distancia(self, enemigo) < 10 and self.sin_impacto:
            enemigo.salud -= self.mainwindow.tanque_principal.fuerza * self.mainwindow.tanque_principal.velocidad_tiro * 10
            self.mainwindow.lista_balas_disparadas.remove(self)
            self.hide()
            self.sin_impacto = False


def bala_explosiva_con_enemigo(self):
    for enemigo in self.mainwindow.lista_enemigos:
        if distancia(self, enemigo) < 10 and self.sin_impacto:
            enemigo.salud -= self.mainwindow.tanque_principal.fuerza * 12
            self.mainwindow.lista_balas_disparadas.remove(self)
            self.hide()
            self.mainwindow.lista_explosiones.append(MiniExplosion(self.mainwindow, (self.cord_x, self.cord_y)))
            self.sin_impacto = False


def bala_penetrante_con_enemigo(self):
    for enemigo in self.mainwindow.lista_enemigos:
        if distancia(self, enemigo) < 10 and self.sin_impacto:
            enemigo.salud -= self.mainwindow.tanque_principal.fuerza * 10
            self.mainwindow.lista_balas_disparadas.remove(self)
            self.hide()
            self.sin_impacto = False


def bala_ralentizante_con_enemigo(self):
    for enemigo in self.mainwindow.lista_enemigos:
        if distancia(self, enemigo) < 10 and self.sin_impacto:
            enemigo.salud -= self.mainwindow.tanque_principal.fuerza * 10
            self.mainwindow.lista_balas_disparadas.remove(self)
            self.hide()
            enemigo.velocidad_mov *= 0.5
            enemigo.tiempo_ralentizacion = 5

            self.sin_impacto = False


def normal_con_principal_general(self):
    if distancia(self, self.mainwindow.tanque_principal) < 10 and self.sin_impacto:
        self.mainwindow.tanque_principal.cañon.salud -= 10
        self.mainwindow.lista_balas_disparadas.remove(self)
        self.hide()
        self.sin_impacto = False


def normal_con_principal_grande(self):
    if distancia(self, self.mainwindow.tanque_principal) < 10 and self.sin_impacto:
        self.mainwindow.tanque_principal.cañon.salud -= 15
        self.mainwindow.lista_balas_disparadas.remove(self)
        self.hide()
        self.sin_impacto = False


def powerup_rojo(self):
    if distancia(self, self.mainwindow.tanque_principal) < 20:
        self.hide()
        self.mainwindow.lista_elementos.remove(self)
        cantidad = randint(1, 3)
        self.mainwindow.ultimo_powerup = str(cantidad) + " Balas Explosivas"
        for i in range(cantidad):
            self.mainwindow.mis_balas.append("e")


def powerup_azul(self):
    if distancia(self, self.mainwindow.tanque_principal) < 20:
        self.hide()
        self.mainwindow.lista_elementos.remove(self)
        cantidad = randint(1, 3)
        self.mainwindow.ultimo_powerup = str(cantidad) + " Balas Ralentizantes"
        for i in range(cantidad):
            self.mainwindow.mis_balas.append("r")


def powerup_blanco(self):
    if distancia(self, self.mainwindow.tanque_principal) < 20:
        self.hide()
        self.mainwindow.lista_elementos.remove(self)
        cantidad = randint(1, 3)
        self.mainwindow.ultimo_powerup = str(cantidad) + " Balas Penetrantes"
        for i in range(cantidad):
            self.mainwindow.mis_balas.append("p")


def moneda(self):
    if distancia(self, self.mainwindow.tanque_principal) < 20:
        self.hide()
        self.mainwindow.lista_elementos.remove(self)
        cantidad = choice([50, 100, 150, 200])
        self.mainwindow.puntaje += cantidad
        self.mainwindow.ultimo_powerup = str(cantidad) + " Puntos"
