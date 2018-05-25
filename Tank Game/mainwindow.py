from PyQt4 import QtGui
from PyQt4 import QtCore
import string
from pausa_y_exit import añadir_botones_funcionales
from sys import exit
from pintar_fondo import PintarFondo
from unidades import TanquePrincipal
from math import sqrt, pi, sin, cos
import mecanica_juego
from balas import BalaPortal, BalaNormal,ImagenBalaR,ImagenBalaE,ImagenBalaN,ImagenBalaP
from operaciones_matematicas import angulo_disparo, distancia
from tienda import Tienda
from elementos import Bomba, Escudo
from constantes import Constantes




def comenzar_main_window(modo, control, etapa):
    main_widget = MainWindow()

    main_widget.modo = modo
    main_widget.control = control
    main_widget.etapa = etapa

    main_widget.show()
    main_widget.start_main(main_widget.run, 25)

    return main_widget


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()



        self.setWindowTitle('Hack Tanks')
        self.posicion = (200, 100)
        self.dimensiones = (600, 600)
        self.setGeometry(*self.posicion, *self.dimensiones)
        self.setFixedSize(*self.dimensiones)
        self.timer = QtCore.QTimer(self)
        self.cursor = QtGui.QCursor()
        self.lista_objetos_gui = []
        self.constantes = Constantes().diccionario

        self.imagen_pared = QtGui.QImage("assets/paredes/pared.png")
        self.imagen_fondo = QtGui.QImage("assets/fondo/fondo")

        self.pintar = PintarFondo()
        self.pixmap_fondo = self.pintar.pintar_paredes(
            self.imagen_pared, self.imagen_fondo, *self.dimensiones)

        self.background = QtGui.QLabel(self)
        self.background.resize(*self.dimensiones)
        self.background.setPixmap(self.pixmap_fondo)

        self.puntaje_label = QtGui.QLabel("Puntaje: ", self)
        self.etapa_label = QtGui.QLabel("Etapa: ", self)
        self.tiempo_restante_label = QtGui.QLabel("Tiempo restante: ", self)
        self.powerups_label = QtGui.QLabel("Power-ups adquiridos: ", self)

        self.font = QtGui.QFont("", 15)
        self.font.setBold(True)

        self.puntaje_label.setFixedSize(150, 20)
        self.puntaje_label.setStyleSheet("color:white;")
        self.puntaje_label.setFont(self.font)
        self.puntaje_label.move(20, 5)
        self.puntaje_label.show()

        self.etapa_label.setFixedSize(150, 20)
        self.etapa_label.setStyleSheet("color:white;")
        self.etapa_label.setFont(self.font)
        self.etapa_label.move(170, 5)
        self.etapa_label.show()

        self.tiempo_restante_label.setFixedSize(170, 20)
        self.tiempo_restante_label.setStyleSheet("color:white;")
        self.tiempo_restante_label.setFont(self.font)
        self.tiempo_restante_label.move(300, 5)
        self.tiempo_restante_label.show()

        self.powerups_label.setFixedSize(300, 20)
        self.powerups_label.setStyleSheet("color:white;")
        self.powerups_label.setFont(self.font)
        self.powerups_label.move(40, 575)
        self.powerups_label.show()

        self.pauseado = False

        añadir_botones_funcionales(self)

        self.tanque_principal = TanquePrincipal(self, (70, 300))

        self.otro_key = 0
        self.primera_presion = True

        self.cuantos_portales_disparados = 0

        self.tiempo_juego = 0

        self.parametro_aparicion = 5

        self.inicial_supervivencia_listo = False

        self.lista_enemigos = []
        self.lista_paredes_duras = []
        self.lista_paredes_blandas = []
        self.lista_balas_disparadas = []
        self.lista_elementos = []
        self.lista_explosiones = []
        self.lista_bombas = []
        self.lista_portales = []

        self.etapa = 1
        self.etapa_superada = True

        self.modo = ""
        self.control = ""

        self.efecto_aceleracion = 1

        self.tienda = Tienda(self)

        self.puntaje = 1000

        self.tiempo_tienda = 0

        self.mis_balas = ["n" for i in range(50)]
        self.mis_bombas = 1

        self.escudo = None

        self.ultimo_powerup = ""

        self.refrescar_labels()

        self.se_acabo = False
        self.resultado = ""

        self.imagen_r_1 = ImagenBalaR(self, (3, 470))
        self.imagen_r_2 = ImagenBalaR(self, (3, 500))
        self.imagen_r_3 = ImagenBalaR(self, (3, 530))

        self.imagen_n_1 = ImagenBalaN(self, (3, 470))
        self.imagen_n_2 = ImagenBalaN(self, (3, 500))
        self.imagen_n_3 = ImagenBalaN(self, (3, 530))

        self.imagen_e_1 = ImagenBalaE(self, (3, 470))
        self.imagen_e_2 = ImagenBalaE(self, (3, 500))
        self.imagen_e_3 = ImagenBalaE(self, (3, 530))

        self.imagen_p_1 = ImagenBalaP(self, (3, 470))
        self.imagen_p_2 = ImagenBalaP(self, (3, 500))
        self.imagen_p_3 = ImagenBalaP(self, (3, 530))




    def refrescar_balas(self):
        if len(self.mis_balas)>=3:
            bala_1=self.mis_balas[-1]
            bala_2=self.mis_balas[-2]
            bala_3=self.mis_balas[-3]

            self.imagen_r_1.hide()
            self.imagen_r_2.hide()
            self.imagen_r_3.hide()
            self.imagen_n_1.hide()
            self.imagen_n_2.hide()
            self.imagen_n_3.hide()
            self.imagen_e_1.hide()
            self.imagen_e_2.hide()
            self.imagen_e_3.hide()
            self.imagen_p_1.hide()
            self.imagen_p_2.hide()
            self.imagen_p_3.hide()


            if bala_1=="e":
                self.imagen_e_1.show()

            if bala_1 == "n":
                self.imagen_n_1.show()
            if bala_1 == "p":
                self.imagen_p_1.show()

            if bala_1 == "r":
                self.imagen_r_1.show()

            if bala_2== "e":
                self.imagen_e_2.show()

            if bala_2 == "n":
                self.imagen_n_2.show()
            if bala_2 == "p":
                self.imagen_p_2.show()

            if bala_2== "r":
                self.imagen_r_2.show()

            if bala_3== "e":
                self.imagen_e_3.show()

            if bala_3== "n":
                self.imagen_n_3.show()
            if bala_3== "p":
                self.imagen_p_3.show()

            if bala_3 == "r":
                self.imagen_r_3.show()

        else:
            self.imagen_r_1.hide()
            self.imagen_r_2.hide()
            self.imagen_r_3.hide()
            self.imagen_n_1.hide()
            self.imagen_n_2.hide()
            self.imagen_n_3.hide()
            self.imagen_e_1.hide()
            self.imagen_e_2.hide()
            self.imagen_e_3.hide()
            self.imagen_p_1.hide()
            self.imagen_p_2.hide()
            self.imagen_p_3.hide()



    def refrescar_labels(self):
        self.etapa_label.setText("Etapa: " + str(self.etapa))
        self.puntaje_label.setText("Puntaje: " + str(self.puntaje))
        self.tiempo_restante_label.setText(
            "Tiempo restante: " + str(round(int(self.constantes["tiempo_limite"]) - self.tiempo_juego)))
        self.powerups_label.setText("Power-ups adquiridos: " + self.ultimo_powerup)

    def keyPressEvent(self, event):
        if not self.pauseado:

            avance = 4 / sqrt(2)

            aceleracion = 0.05

            if event.key() == QtCore.Qt.Key_W and self.otro_key == QtCore.Qt.Key_A or \
                                    event.key() == QtCore.Qt.Key_A and self.otro_key == QtCore.Qt.Key_W:

                if self.control == "fijo":
                    self.tanque_principal.cord_x += -avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += -avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cambiar_imagen("assets/tanques/mio_up_left")
                else:
                    self.tanque_principal.cord_x += -avance * cos(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += -avance * sin(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                if self.tanque_principal.cord_x <= 30 or self.tanque_principal.cord_y <= 30:
                    self.tanque_principal.cord_x += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                for enemigo in self.lista_enemigos:
                    if distancia(self.tanque_principal, enemigo) < 30:
                        self.tanque_principal.cord_x += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cañon.salud -= 4
                for pared_blanda in self.lista_paredes_blandas:
                    if distancia(self.tanque_principal, pared_blanda) < 30:
                        self.tanque_principal.cord_x += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                for pared_dura in self.lista_paredes_duras:
                    if distancia(self.tanque_principal, pared_dura) < 30:
                        self.tanque_principal.cord_x += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                self.efecto_aceleracion += aceleracion



            elif event.key() == QtCore.Qt.Key_W and self.otro_key == QtCore.Qt.Key_D or \
                                    event.key() == QtCore.Qt.Key_D and self.otro_key == QtCore.Qt.Key_W:
                if self.control == "fijo":
                    self.tanque_principal.cord_x += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += -avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cambiar_imagen("assets/tanques/mio_up_right")
                else:
                    self.tanque_principal.cord_x += avance * cos(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += -avance * sin(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                if self.tanque_principal.cord_x >= 545 or self.tanque_principal.cord_y <= 30:
                    self.tanque_principal.cord_x -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                for enemigo in self.lista_enemigos:
                    if distancia(self.tanque_principal, enemigo) < 30:
                        self.tanque_principal.cord_x -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cañon.salud -= 4
                for pared_blanda in self.lista_paredes_blandas:
                    if distancia(self.tanque_principal, pared_blanda) < 30:
                        self.tanque_principal.cord_x -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                for pared_dura in self.lista_paredes_duras:
                    if distancia(self.tanque_principal, pared_dura) < 30:
                        self.tanque_principal.cord_x -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                self.efecto_aceleracion += aceleracion

            elif event.key() == QtCore.Qt.Key_S and self.otro_key == QtCore.Qt.Key_D or \
                                    event.key() == QtCore.Qt.Key_D and self.otro_key == QtCore.Qt.Key_S:
                if self.control == "fijo":
                    self.tanque_principal.cord_x += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cambiar_imagen("assets/tanques/mio_down_right")
                else:
                    self.tanque_principal.cord_x += avance * cos(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += avance * sin(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                if self.tanque_principal.cord_x >= 545 or self.tanque_principal.cord_y >= 545:
                    self.tanque_principal.cord_x -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                for enemigo in self.lista_enemigos:
                    if distancia(self.tanque_principal, enemigo) < 30:
                        self.tanque_principal.cord_x -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cañon.salud -= 4
                for pared_blanda in self.lista_paredes_blandas:
                    if distancia(self.tanque_principal, pared_blanda) < 30:
                        self.tanque_principal.cord_x -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                for pared_dura in self.lista_paredes_duras:
                    if distancia(self.tanque_principal, pared_dura) < 30:
                        self.tanque_principal.cord_x -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                self.efecto_aceleracion += aceleracion

            elif event.key() == QtCore.Qt.Key_A and self.otro_key == QtCore.Qt.Key_S or \
                                    event.key() == QtCore.Qt.Key_S and self.otro_key == QtCore.Qt.Key_A:
                if self.control == "fijo":

                    self.tanque_principal.cord_x += -avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cambiar_imagen("assets/tanques/mio_down_left")
                else:
                    self.tanque_principal.cord_x += -avance * cos(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += avance * sin(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                if self.tanque_principal.cord_x <= 30 or self.tanque_principal.cord_y >= 545:
                    self.tanque_principal.cord_x += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                for enemigo in self.lista_enemigos:
                    if distancia(self.tanque_principal, enemigo) < 30:
                        self.tanque_principal.cord_x += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cañon.salud -= 4
                for pared_blanda in self.lista_paredes_blandas:
                    if distancia(self.tanque_principal, pared_blanda) < 30:
                        self.tanque_principal.cord_x += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                for pared_dura in self.lista_paredes_duras:
                    if distancia(self.tanque_principal, pared_dura) < 30:
                        self.tanque_principal.cord_x += avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cord_y -= avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                self.efecto_aceleracion += aceleracion

            elif event.key() == QtCore.Qt.Key_W:
                if self.control == "fijo":
                    self.tanque_principal.cord_y += -4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cambiar_imagen("assets/tanques/mio_up_none")
                else:
                    self.tanque_principal.cord_x += -avance * cos(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += -avance * sin(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                if self.tanque_principal.cord_y <= 30:
                    self.tanque_principal.cord_y += 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                for enemigo in self.lista_enemigos:
                    if distancia(self.tanque_principal, enemigo) < 30:
                        self.tanque_principal.cord_y += 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cañon.salud -= 4
                for pared_blanda in self.lista_paredes_blandas:
                    if distancia(self.tanque_principal, pared_blanda) < 30:
                        self.tanque_principal.cord_y += 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                for pared_dura in self.lista_paredes_duras:
                    if distancia(self.tanque_principal, pared_dura) < 30:
                        self.tanque_principal.cord_y += 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                self.efecto_aceleracion += aceleracion

            elif event.key() == QtCore.Qt.Key_A:
                if self.control == "fijo":
                    self.tanque_principal.cord_x += -4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cambiar_imagen("assets/tanques/mio_none_left")
                else:

                    x = -avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    y = -avance * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                    self.tanque_principal.cord_x += x * cos(
                        self.tanque_principal.angulo_cañon) * y * sin(self.tanque_principal.angulo_cañon)
                    self.tanque_principal.cord_y += -x * sin(self.tanque_principal.angulo_cañon) + y * cos(
                        self.tanque_principal.angulo_cañon)

                if self.tanque_principal.cord_x <= 30:
                    self.tanque_principal.cord_x += 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                for enemigo in self.lista_enemigos:
                    if distancia(self.tanque_principal, enemigo) < 30:
                        self.tanque_principal.cord_x += 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cañon.salud -= 4
                for pared_blanda in self.lista_paredes_blandas:
                    if distancia(self.tanque_principal, pared_blanda) < 30:
                        self.tanque_principal.cord_x += 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                for pared_dura in self.lista_paredes_duras:
                    if distancia(self.tanque_principal, pared_dura) < 30:
                        self.tanque_principal.cord_x += 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                self.efecto_aceleracion += aceleracion

            elif event.key() == QtCore.Qt.Key_S:
                if self.control == "fijo":
                    self.tanque_principal.cord_y += 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cambiar_imagen("assets/tanques/mio_down_none")
                else:
                    self.tanque_principal.cord_x -= -avance * cos(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y -= -avance * sin(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                if self.tanque_principal.cord_y >= 545:
                    self.tanque_principal.cord_y -= 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                for enemigo in self.lista_enemigos:
                    if distancia(self.tanque_principal, enemigo) < 30:
                        self.tanque_principal.cord_y -= 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cañon.salud -= 4
                for pared_blanda in self.lista_paredes_blandas:
                    if distancia(self.tanque_principal, pared_blanda) < 30:
                        self.tanque_principal.cord_y -= 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                for pared_dura in self.lista_paredes_duras:
                    if distancia(self.tanque_principal, pared_dura) < 30:
                        self.tanque_principal.cord_y -= 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                self.efecto_aceleracion += aceleracion

            elif event.key() == QtCore.Qt.Key_D:
                if self.control == "fijo":
                    self.tanque_principal.cord_x += 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cambiar_imagen("assets/tanques/mio_none_right")
                else:
                    self.tanque_principal.cord_x -= -avance * sin(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                    self.tanque_principal.cord_y += -avance * cos(
                        self.tanque_principal.angulo_cañon) * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                if self.tanque_principal.cord_x >= 545:
                    self.tanque_principal.cord_x -= 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                for enemigo in self.lista_enemigos:
                    if distancia(self.tanque_principal, enemigo) < 30:
                        self.tanque_principal.cord_x -= 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                        self.tanque_principal.cañon.salud -= 4
                for pared_blanda in self.lista_paredes_blandas:
                    if distancia(self.tanque_principal, pared_blanda) < 30:
                        self.tanque_principal.cord_x -= 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion
                for pared_dura in self.lista_paredes_duras:
                    if distancia(self.tanque_principal, pared_dura) < 30:
                        self.tanque_principal.cord_x -= 4 * self.tanque_principal.velocidad_mov * self.efecto_aceleracion

                self.efecto_aceleracion += aceleracion

            elif event.key() == QtCore.Qt.Key_1:
                if self.cuantos_portales_disparados < 2:
                    angulo_portal = angulo_disparo((self.cursor.pos().x() - self.pos().x(),
                                                    self.cursor.pos().y() - self.pos().y() - 25),
                                                   (self.tanque_principal.cord_x + 15,
                                                    self.tanque_principal.cord_y + 15))
                    self.cuantos_portales_disparados += 1
                    BalaPortal(self, (self.tanque_principal.cord_x, self.tanque_principal.cord_y), angulo_portal)


            elif event.key() == QtCore.Qt.Key_2:
                if self.mis_bombas >= 1:
                    Bomba(self, (self.tanque_principal.cord_x, self.tanque_principal.cord_y))
                    self.mis_bombas -= 1

            elif event.key() == QtCore.Qt.Key_P:
                self.pauseado = True

            elif event.key() == QtCore.Qt.Key_G:
                exit(0)

            if self.primera_presion:
                self.otro_key = event.key()
                self.primera_presion = False

        else:
            if event.key() == QtCore.Qt.Key_P:
                self.pauseado = False

    def keyReleaseEvent(self, event):
        self.otro_key = -1
        self.primera_presion = True
        self.efecto_aceleracion = 1

    def mousePressEvent(self, event):
        self.tanque_principal.disparar()

    def añadir_objeto_gui(self, objeto_gui):
        objeto_gui.setParent(self)
        objeto_gui.show()
        self.lista_objetos_gui.append(objeto_gui)

    def start_main(self, main, delay=25):
        self.timer.timeout.connect(main)
        self.timer.start(delay)

    def run(self):
        mecanica_juego.run(self)
