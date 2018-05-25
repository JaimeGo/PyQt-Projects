from objeto_gui import ObjetoGui
from PyQt4.QtCore import Qt
from PyQt4 import QtGui
from math import cos, sin, pi
from colisiones import bala_normal_con_enemigo, \
    bala_explosiva_con_enemigo, bala_penetrante_con_enemigo, \
    bala_ralentizante_con_enemigo, normal_con_principal_general, \
    normal_con_principal_grande, bala_con_muralla, bala_con_paredes
from elementos import Portal
from operaciones_matematicas import distancia


class Bala(ObjetoGui):
    def __init__(self, path, pos, angulo_bala):
        super().__init__(path, pos, tamaño=(33, 33))
        self.pos = pos
        self.angulo_bala = angulo_bala

        self.sin_impacto = True

        self.pixmap = QtGui.QPixmap(self.path_imagen)
        if "normal" in self.path_imagen or "portal" in self.path_imagen:
            self.pixmap = self.pixmap.scaled(7, 7)
        else:
            self.pixmap = self.pixmap.scaled(4, 7)
        self.pixmap = self.pixmap.transformed(QtGui.QTransform().rotate(-90 - self.angulo_bala * 180 / pi))
        self.label.setFixedSize(30, 30)
        self.alinear(Qt.AlignCenter)
        self.label.setPixmap(self.pixmap)
        self.label.show()

    def mover_bala(self):

        self.cord_x -= cos(self.angulo_bala) * 2
        self.cord_y += sin(self.angulo_bala) * 2


class BalaNormal(Bala):
    def __init__(self, mainwindow, pos, angulo, atacante="tanque_principal"):
        super().__init__("assets/elementos/bala_normal", pos, angulo)
        self.mainwindow = mainwindow
        self.atacante = atacante
        mainwindow.añadir_objeto_gui(self)
        mainwindow.lista_balas_disparadas.append(self)

        if self.atacante == "tanque_grande":
            self.tamaño_x = 20
            self.tamaño_y = 20
            self.refrescar_pixmap()

    def manejar_colision(self):
        if self.atacante == "tanque_principal":
            bala_normal_con_enemigo(self)

        elif self.atacante == "tanque_guiador":
            normal_con_principal_general(self)

        elif self.atacante == "tanque_quieto":
            normal_con_principal_general(self)

        elif self.atacante == "tanque_grande":
            normal_con_principal_grande(self)

        bala_con_muralla(self)
        bala_con_paredes(self)


class BalaExplosiva(Bala):
    def __init__(self, mainwindow, pos, angulo):
        super().__init__("assets/elementos/bala_explosiva", pos, angulo)
        self.mainwindow = mainwindow
        mainwindow.añadir_objeto_gui(self)
        mainwindow.lista_balas_disparadas.append(self)

    def manejar_colision(self):
        bala_explosiva_con_enemigo(self)
        bala_con_muralla(self)
        bala_con_paredes(self)


class BalaPenetrante(Bala):
    def __init__(self, mainwindow, pos, angulo):
        super().__init__("assets/elementos/bala_penetrante", pos, angulo)
        self.mainwindow = mainwindow
        mainwindow.añadir_objeto_gui(self)
        mainwindow.lista_balas_disparadas.append(self)

    def manejar_colision(self):
        bala_penetrante_con_enemigo(self)
        bala_con_muralla(self)


class BalaRalentizante(Bala):
    def __init__(self, mainwindow, pos, angulo):
        super().__init__("assets/elementos/bala_ralentizante", pos, angulo)
        self.mainwindow = mainwindow
        mainwindow.añadir_objeto_gui(self)
        mainwindow.lista_balas_disparadas.append(self)

    def manejar_colision(self):
        bala_ralentizante_con_enemigo(self)
        bala_con_muralla(self)
        bala_con_paredes(self)


class BalaPortal(Bala):
    def __init__(self, mainwindow, pos, angulo):
        super().__init__("assets/elementos/bala_portal", pos, angulo)
        self.mainwindow = mainwindow
        mainwindow.añadir_objeto_gui(self)
        mainwindow.lista_balas_disparadas.append(self)

    def manejar_colision(self):
        if self.cord_x <= 15 and self.sin_impacto:
            portal = Portal(self.mainwindow, (self.cord_x - 15, self.cord_y))
            portal.lugar_aparicion = "derecha"
            self.mainwindow.lista_portales.append(portal)
            self.mainwindow.lista_balas_disparadas.remove(self)
            self.hide()
            self.sin_impacto = False

        if self.cord_x >= 555 and self.sin_impacto:
            portal = Portal(self.mainwindow, (self.cord_x + 15, self.cord_y))
            portal.lugar_aparicion = "izquierda"
            self.mainwindow.lista_portales.append(portal)
            self.mainwindow.lista_balas_disparadas.remove(self)
            self.hide()
            self.sin_impacto = False
        if self.cord_y <= 15 and self.sin_impacto:
            portal = Portal(self.mainwindow, (self.cord_x, self.cord_y - 15))
            portal.lugar_aparicion = "abajo"
            self.mainwindow.lista_portales.append(portal)
            self.mainwindow.lista_balas_disparadas.remove(self)
            self.hide()
            self.sin_impacto = False
        if self.cord_y >= 555 and self.sin_impacto:
            portal = Portal(self.mainwindow, (self.cord_x, self.cord_y + 15))
            portal.lugar_aparicion = "arriba"
            self.mainwindow.lista_portales.append(portal)
            self.mainwindow.lista_balas_disparadas.remove(self)
            self.hide()
            self.sin_impacto = False

        for enemigo in self.mainwindow.lista_enemigos:
            if distancia(self, enemigo) < 10:
                self.mainwindow.cuantos_portales_disparados -= 1
                self.hide()
                self.mainwindow.lista_balas_disparadas.remove(self)


class ImagenBalaN(Bala):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/bala_normal", pos, 3*pi/2)
        self.mainwindow = mainwindow
        mainwindow.añadir_objeto_gui(self)
        self.hide()

class ImagenBalaE(Bala):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/bala_explosiva", pos, 3*pi/2)
        self.mainwindow = mainwindow
        mainwindow.añadir_objeto_gui(self)
        self.hide()

class ImagenBalaP(Bala):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/bala_penetrante", pos, 3*pi/2)
        self.mainwindow = mainwindow
        mainwindow.añadir_objeto_gui(self)
        self.hide()


class ImagenBalaR(Bala):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/elementos/bala_ralentizante", pos, 3*pi/2)

        self.mainwindow = mainwindow
        mainwindow.añadir_objeto_gui(self)
        self.hide()


