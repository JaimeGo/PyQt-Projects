from objeto_gui import ObjetoGui
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from operaciones_matematicas import angulo_a_cursor, distancia, angulo_disparo, angulo_a_principal
from balas import BalaNormal, BalaExplosiva, BalaPenetrante, BalaRalentizante
from math import cos, sin, pi, isclose
from colisiones import principal_con_portales


class TanquePrincipal(ObjetoGui):
    def __init__(self, mainwindow, pos):
        super().__init__("assets/tanques/mio_up_none", pos, tamaño=(30, 30))
        self.cañon = ObjetoGui("assets/tanques/cañon", (pos[0] + 3, pos[1] + 2), tamaño=(20, 20))
        self.cursor = QtGui.QCursor()
        self.mainwindow = mainwindow
        self.mainwindow.añadir_objeto_gui(self)
        self.mainwindow.añadir_objeto_gui(self.cañon)

        self.fuerza = float(self.mainwindow.constantes["fuerza"])
        self.resistencia = float(self.mainwindow.constantes["resistencia"])
        self.velocidad_mov = float(self.mainwindow.constantes["velocidad_mov"])
        self.velocidad_tiro = float(self.mainwindow.constantes["velocidad_tiro"])
        self.radio = float(self.mainwindow.constantes["radio"])

        self.vida = float(self.mainwindow.constantes["vida"])

        self.cañon.barra_salud.setRange(0, float(self.mainwindow.constantes["vida"]))
        self.cañon.tiene_barra(self.vida)

    def manejar_colision(self):
        principal_con_portales(self)

    def refrescar_cañon(self):

        self.angulo_cañon = angulo_a_cursor((self.cursor.pos().x() - self.mainwindow.pos().x(),
                                             self.cursor.pos().y() - self.mainwindow.pos().y() - 25),
                                            (self.cord_x + 15,
                                             self.cord_y + 15))
        self.cañon.pixmap = QtGui.QPixmap(self.cañon.path_imagen)
        self.cañon.pixmap = self.cañon.pixmap.scaled(self.cañon.tamaño_x, self.cañon.tamaño_y)
        self.cañon.pixmap = self.cañon.pixmap.transformed(QtGui.QTransform().rotate(self.angulo_cañon))
        self.cañon.label.setFixedSize(25, 25)
        self.cañon.alinear(Qt.AlignCenter)
        self.cañon.label.setPixmap(self.cañon.pixmap)

        self.cañon.label.show()
        self.cañon.move(self.cord_x, self.cord_y)

    def refrescar_imagen_total(self):
        self.angulo_cañon = angulo_a_cursor((self.cursor.pos().x() - self.mainwindow.pos().x(),
                                             self.cursor.pos().y() - self.mainwindow.pos().y() - 25),
                                            (self.cord_x + 15,
                                             self.cord_y + 15))

        self.cañon.pixmap = QtGui.QPixmap(self.cañon.path_imagen)
        self.cañon.pixmap = self.cañon.pixmap.scaled(self.cañon.tamaño_x, self.cañon.tamaño_y)
        self.cañon.pixmap = self.cañon.pixmap.transformed(QtGui.QTransform().rotate(self.angulo_cañon))
        self.cañon.label.setFixedSize(25, 25)
        self.cañon.alinear(Qt.AlignCenter)
        self.cañon.label.setPixmap(self.cañon.pixmap)

        self.pixmap = QtGui.QPixmap(self.path_imagen)
        self.pixmap = self.pixmap.scaled(self.tamaño_x, self.tamaño_y)
        self.pixmap = self.pixmap.transformed(QtGui.QTransform().rotate(self.angulo_cañon))
        self.label.setFixedSize(35, 35)
        self.alinear(Qt.AlignCenter)
        self.label.setPixmap(self.pixmap)

        self.cañon.label.show()
        self.cañon.move(self.cord_x + 3, self.cord_y + 3)

        self.label.show()
        self.move(self.cord_x, self.cord_y)

    def disparar(self):
        angulo = angulo_disparo((self.cursor.pos().x() - self.mainwindow.pos().x(),
                                 self.cursor.pos().y() - self.mainwindow.pos().y() - 25),
                                (self.cord_x + 15,
                                 self.cord_y + 15))

        if self.mainwindow.mis_balas:
            bala_actual = self.mainwindow.mis_balas.pop()
            if bala_actual == "n":
                BalaNormal(self.mainwindow, (self.cord_x, self.cord_y), angulo)
            elif bala_actual == "e":
                BalaExplosiva(self.mainwindow, (self.cord_x, self.cord_y), angulo)
            elif bala_actual == "r":
                BalaRalentizante(self.mainwindow, (self.cord_x, self.cord_y), angulo)
            elif bala_actual == "p":
                BalaPenetrante(self.mainwindow, (self.cord_x, self.cord_y), angulo)

    @property
    def cord_x(self):
        return self._cord_x

    @cord_x.setter
    def cord_x(self, cord):
        self._cord_x = cord
        self.move(self._cord_x, self._cord_y)
        self.cañon.move(self._cord_x, self._cord_y)

    @property
    def cord_y(self):
        return self._cord_y

    @cord_y.setter
    def cord_y(self, cord):
        self._cord_y = cord
        self.move(self._cord_x, self._cord_y)
        self.cañon.move(self._cord_x, self._cord_y)


class TanqueEnemigo(ObjetoGui):
    def __init__(self, mainwindow, path, pos, tamaño):
        super().__init__(path, pos, tamaño)
        self.mainwindow = mainwindow
        self.angulo_tanque = 0

        self.velocidad_mov = 1
        self.tiempo_ralentizacion = 0

    def recuperar_velocidad(self):
        if self.tiempo_ralentizacion >= 0:
            self.tiempo_ralentizacion -= 0.025
            if self.tiempo_ralentizacion <= 0 and self.velocidad_mov != 1:
                self.velocidad_mov /= 0.5

    def disparar(self):
        pass

    def mover(self):
        pass

    def cambiar_segun_grado(self, x, y):

        if x == 0:
            x = 0.001

        razon = y / x

        # derecha
        if x >= 0 and razon < 0.4142 and razon > -0.4142:
            self.path_imagen = self.path_tipo + "_none_right"

        # abajo
        if x <= 0 and razon < 0.4142 and razon > -0.4142:
            self.path_imagen = self.path_tipo + "_none_left"

        # abajo
        if y >= 0 and (razon > 2.414 or razon < -2.414):
            self.path_imagen = self.path_tipo + "_down_none"

        # arriba
        if y <= 0 and (razon > 2.414 or razon < -2.414):
            self.path_imagen = self.path_tipo + "_up_none"

        # abajo_derecha
        if x >= 0 and y >= 0 and razon >= 0.4142 and razon <= 2.414:
            self.path_imagen = self.path_tipo + "_down_right"

        # arriba_derecha
        if x >= 0 and y <= 0 and razon <= -0.4142 and razon >= -2.414:
            self.path_imagen = self.path_tipo + "_up_right"

        # abajo_izquierda
        if x <= 0 and y >= 0 and razon <= -0.4142 and razon >= -2.414:
            self.path_imagen = self.path_tipo + "_down_left"

        # arriba_izquierda
        if x <= 0 and y <= 0 and razon >= 0.4142 and razon <= 2.414:
            self.path_imagen = self.path_tipo + "_up_left"

        self.nuevo_pixmap = QtGui.QPixmap(self.path_imagen)

        if "none" in self.path_imagen:
            self.nuevo_pixmap = self.nuevo_pixmap.scaled(self.tamaño_x - 5, self.tamaño_y - 5)
        else:
            self.nuevo_pixmap = self.nuevo_pixmap.scaled(self.tamaño_x, self.tamaño_y)

        self.label.setFixedSize(30, 30)
        self.alinear(Qt.AlignCenter)
        self.label.setPixmap(self.nuevo_pixmap)

        self.label.show()


class TanqueQuieto(TanqueEnemigo):
    def __init__(self, mainwindow, pos, orientacion):
        if orientacion == "derecha":
            super().__init__(mainwindow, "assets/tanques/quieto_none_right", pos, tamaño=(30, 30))
        if orientacion == "izquierda":
            super().__init__(mainwindow, "assets/tanques/quieto_none_left", pos, tamaño=(30, 30))
        if orientacion == "arriba":
            super().__init__(mainwindow, "assets/tanques/quieto_up_none", pos, tamaño=(30, 30))
        if orientacion == "abajo":
            super().__init__(mainwindow, "assets/tanques/quieto_down_none", pos, tamaño=(30, 30))

        mainwindow.añadir_objeto_gui(self)
        self.orientacion = orientacion
        self.mainwindow = mainwindow
        self.vida = 100
        self.tiene_barra(self.vida)
        self.fuerza = 1.1

        self.recompensa = 50

        self.tiempo_proximo_disparo = 0

    def disparar_quieto(self):
        angulo = None
        le_dispara = False

        if self.tiempo_proximo_disparo <= 0:

            if self.orientacion == "derecha":
                angulo = pi
                if self.mainwindow.tanque_principal.cord_x - self.cord_x >= 0 and isclose(
                        self.mainwindow.tanque_principal.cord_y, self.cord_y, abs_tol=5):
                    le_dispara = True

            if self.orientacion == "izquierda":
                angulo = 0
                if self.mainwindow.tanque_principal.cord_x - self.cord_x <= 0 and isclose(
                        self.mainwindow.tanque_principal.cord_y, self.cord_y, abs_tol=5):
                    le_dispara = True

            if self.orientacion == "arriba":
                angulo = 3 * pi / 2
                if self.mainwindow.tanque_principal.cord_y - self.cord_y <= 0 and isclose(
                        self.mainwindow.tanque_principal.cord_x, self.cord_x, abs_tol=5):
                    le_dispara = True

            if self.orientacion == "abajo":
                angulo = pi / 2
                if self.mainwindow.tanque_principal.cord_y - self.cord_y >= 0 and isclose(
                        self.mainwindow.tanque_principal.cord_x, self.cord_x, abs_tol=5):
                    le_dispara = True

            if le_dispara:
                BalaNormal(self.mainwindow, (self.cord_x, self.cord_y), angulo, atacante="tanque_quieto")
                self.tiempo_proximo_disparo = 1

        else:
            self.tiempo_proximo_disparo -= 0.025


class TanqueCirculo(TanqueEnemigo):
    def __init__(self, mainwindow, pos):
        super().__init__(mainwindow, "assets/tanques/circulo_up_none", pos, tamaño=(30, 30))
        mainwindow.añadir_objeto_gui(self)
        self.mainwindow = mainwindow
        self.vida = 100
        self.tiene_barra(self.vida)
        self.fuerza = 1.1
        self.parametro_mov = 0
        self.path_tipo = "assets/tanques/circulo"
        self.recompensa = 100

    def mover(self):
        self.parametro_mov += 0.015

        cambio_x = cos(self.parametro_mov)
        cambio_y = sin(self.parametro_mov)
        self.cord_x += cambio_x * self.velocidad_mov
        self.cord_y += cambio_y * self.velocidad_mov

        self.cambiar_segun_grado(cambio_x, cambio_y)

        for pared in self.mainwindow.lista_paredes_blandas:
            if distancia(self, pared) < 30:
                self.cord_x -= cambio_x * self.velocidad_mov
                self.cord_y -= cambio_y * self.velocidad_mov

        for pared in self.mainwindow.lista_paredes_duras:
            if distancia(self, pared) < 30:
                self.cord_x -= cambio_x * self.velocidad_mov
                self.cord_y -= cambio_y * self.velocidad_mov

        if distancia(self, self.mainwindow.tanque_principal) < 30:
            self.cord_x -= cambio_x * self.velocidad_mov
            self.cord_y -= cambio_y * self.velocidad_mov
            self.mainwindow.tanque_principal.cañon.salud -= 0.0001

        if self.cord_x <= 30 or self.cord_y <= 30 or self.cord_x >= 545 or self.cord_y >= 545:
            self.cord_x -= cambio_x * self.velocidad_mov
            self.cord_y -= cambio_y * self.velocidad_mov


class TanqueGuiador(TanqueEnemigo):
    def __init__(self, mainwindow, pos):
        super().__init__(mainwindow, "assets/tanques/guiador_up_none", pos, tamaño=(30, 30))
        mainwindow.añadir_objeto_gui(self)
        self.mainwindow = mainwindow
        self.vida = 100
        self.tiene_barra(self.vida)
        self.fuerza = 1.1
        self.path_tipo = "assets/tanques/guiador"
        self.recompensa = 200

    def mover(self):
        objetivo = self.mainwindow.tanque_principal
        dist = distancia(self, objetivo) + 0.0001
        dx = objetivo.cord_x - self.cord_x
        dy = objetivo.cord_y - self.cord_y

        cambio_x = dx / dist
        cambio_y = dy / dist

        self.cord_x += cambio_x * self.velocidad_mov
        self.cord_y += cambio_y * self.velocidad_mov

        self.cambiar_segun_grado(cambio_x, cambio_y)

        for pared in self.mainwindow.lista_paredes_blandas:
            if distancia(self, pared) < 30:
                self.cord_x -= cambio_x * self.velocidad_mov
                self.cord_y -= cambio_y * self.velocidad_mov

        for pared in self.mainwindow.lista_paredes_duras:
            if distancia(self, pared) < 30:
                self.cord_x -= cambio_x * self.velocidad_mov
                self.cord_y -= cambio_y * self.velocidad_mov

        if distancia(self, self.mainwindow.tanque_principal) < 30:
            self.cord_x -= cambio_x * self.velocidad_mov
            self.cord_y -= cambio_y * self.velocidad_mov
            self.mainwindow.tanque_principal.cañon.salud -= 0.001

        if self.cord_x <= 30 or self.cord_y <= 30 or self.cord_x >= 545 or self.cord_y >= 545:
            self.cord_x -= cambio_x * self.velocidad_mov
            self.cord_y -= cambio_y * self.velocidad_mov

    def disparar(self):
        angulo = angulo_disparo((self.mainwindow.tanque_principal.cord_x + 15,
                                 self.mainwindow.tanque_principal.cord_y + 15),
                                (self.cord_x + 15,
                                 self.cord_y + 15))

        BalaNormal(self.mainwindow, (self.cord_x, self.cord_y), angulo, atacante="tanque_guiador")


class TanqueGrande(TanqueEnemigo):
    def __init__(self, mainwindow, pos):
        super().__init__(mainwindow, "assets/tanques/grande_up_none", pos, tamaño=(30, 30))
        mainwindow.añadir_objeto_gui(self)
        self.mainwindow = mainwindow
        self.vida = 150
        self.tiene_barra(self.vida)
        self.fuerza = 1.5
        self.path_tipo = "assets/tanques/grande"
        self.recompensa = 400

    def mover(self):
        objetivo = self.mainwindow.tanque_principal
        dist = distancia(self, objetivo)
        dx = objetivo.cord_x - self.cord_x
        dy = objetivo.cord_y - self.cord_y

        cambio_x = dx / dist
        cambio_y = dy / dist

        self.cord_x += cambio_x * self.velocidad_mov
        self.cord_y += cambio_y * self.velocidad_mov

        self.cambiar_segun_grado(cambio_x, cambio_y)

        for pared in self.mainwindow.lista_paredes_blandas:
            if distancia(self, pared) < 30:
                pared.hide()
                self.mainwindow.lista_paredes_blandas.remove(pared)

        for pared in self.mainwindow.lista_paredes_duras:
            if distancia(self, pared) < 30:
                self.cord_x -= cambio_x * self.velocidad_mov
                self.cord_y -= cambio_y * self.velocidad_mov

        if distancia(self, self.mainwindow.tanque_principal) < 30:
            self.cord_x -= cambio_x * self.velocidad_mov
            self.cord_y -= cambio_y * self.velocidad_mov
            self.mainwindow.tanque_principal.cañon.salud -= 0.001

        if self.cord_x <= 30 or self.cord_y <= 30 or self.cord_x >= 545 or self.cord_y >= 545:
            self.cord_x -= cambio_x * self.velocidad_mov
            self.cord_y -= cambio_y * self.velocidad_mov

    def disparar(self):
        angulo = angulo_disparo((self.mainwindow.tanque_principal.cord_x + 15,
                                 self.mainwindow.tanque_principal.cord_y + 15),
                                (self.cord_x + 15,
                                 self.cord_y + 15))

        BalaNormal(self.mainwindow, (self.cord_x + 7, self.cord_y + 7), angulo, atacante="tanque_grande")
