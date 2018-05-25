from PyQt4 import QtGui, uic, QtCore
from clase_curva import Curva
from dashboard_puntaje import DashboardPuntaje
from mini_chat import SeleccionAmigos
from invitacion import Invitacion
from historial import Historial

formulario_1 = uic.loadUiType("chat_grupal.ui")


class ChatGrupal(formulario_1[0], formulario_1[1]):
    def __init__(self, cliente, menu_inicial):
        super().__init__()

        self.cliente = cliente
        self.menu_inicial = menu_inicial

        self.lista_entidades = []

        self.setupUi(self)

        self.ultima_pos = (0, 0)

        self.pushButton.clicked.connect(self.enviar_publicacion)

        self.widget_1 = QtGui.QWidget()
        self.widget_1.setFixedSize(369, 199)

        self.scrollArea.setWidget(self.widget_1)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setEnabled(True)

        self.exceso_altura = 0
        self.publicaciones = 0

        self.scene = QtGui.QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.x_rect = 390
        self.y_rect = 50
        self.w_rect = 369
        self.h_rect = 239
        self.scene.setSceneRect(QtCore.QRectF(self.x_rect, self.y_rect, self.w_rect, self.h_rect))

        self.cursor = QtGui.QCursor()

        self.dashboard = DashboardPuntaje(self.cliente)

        self.grosor = 2
        self.pen = QtGui.QPen()
        self.pen.setWidth(self.grosor)

        self.primer_punto_linea_recta = None
        self.segundo_punto_linea_recta = None

        self.primer_punto_linea_curva = None
        self.segundo_punto_linea_curva = None

        self.recibiendo_linea_recta_1 = False
        self.recibiendo_linea_recta_2 = False

        self.recibiendo_linea_curva_1 = False
        self.recibiendo_linea_curva_2 = False

        self.color = "0:0:0"
        self.lista_colores_usados = ["0:0:0", "255:0:0", "0:255:0", "0:0:255"]
        self.lista_rgb_1 = [0, 0, 255]
        self.lista_rgb_2 = [0, 255, 0]
        self.lista_rgb_3 = [255, 0, 0]
        self.lista_rgb_4 = [0, 0, 0]

        self.style_1 = "QPushButton {background-color: rgb(" + str(self.lista_rgb_1[0]) + "," + str(
            self.lista_rgb_1[1]) + "," + str(self.lista_rgb_1[2]) + ");}"
        self.style_2 = "QPushButton {background-color: rgb(" + str(self.lista_rgb_2[0]) + "," + str(
            self.lista_rgb_2[1]) + "," + str(self.lista_rgb_2[2]) + ");}"
        self.style_3 = "QPushButton {background-color: rgb(" + str(self.lista_rgb_3[0]) + "," + str(
            self.lista_rgb_3[1]) + "," + str(self.lista_rgb_3[2]) + ");}"
        self.style_4 = "QPushButton {background-color: rgb(" + str(self.lista_rgb_4[0]) + "," + str(
            self.lista_rgb_4[1]) + "," + str(self.lista_rgb_4[2]) + ");}"

        self.pushButton_10.setStyleSheet(self.style_1)
        self.pushButton_11.setStyleSheet(self.style_2)
        self.pushButton_12.setStyleSheet(self.style_3)
        self.pushButton_13.setStyleSheet(self.style_4)

        self.pushButton_10.clicked.connect(self.cambiar_color_usado_1)
        self.pushButton_11.clicked.connect(self.cambiar_color_usado_2)
        self.pushButton_12.clicked.connect(self.cambiar_color_usado_3)
        self.pushButton_13.clicked.connect(self.cambiar_color_usado_4)

        self.pushButton_9.clicked.connect(self.dibujar_cuadrado)
        self.pushButton_8.clicked.connect(self.dibujar_linea_curva)
        self.pushButton_7.clicked.connect(self.dibujar_linea_recta)
        self.pushButton_6.clicked.connect(self.dibujar_rectangulo)
        self.pushButton_5.clicked.connect(self.dibujar_triangulo)
        self.pushButton_4.clicked.connect(self.dibujar_circulo)

        self.pushButton_16.clicked.connect(self.cambiar_color_rgb)

        self.pushButton_14.clicked.connect(self.amistad_desde_grupal)

        self.pushButton_2.clicked.connect(self.dashboard.mostrar)

        self.lista_amigos = []

        self.lista_ultima_figura = []

        self.historial = Historial(self.cliente)

        self.seleccion_chat_ind = SeleccionAmigos("ind", self.cliente)
        self.seleccion_chat_grup = SeleccionAmigos("grup", self.cliente)

        self.pushButton_17.clicked.connect(self.mostrar_minichat_ind)
        self.pushButton_18.clicked.connect(self.mostrar_minichat_grup)

        self.pushButton_3.clicked.connect(self.cliente.guardar_imagen)

        self.pushButton_19.clicked.connect(self.mover_figura)

        self.pushButton_20.clicked.connect(self.invitar_persona)

        self.pushButton_15.clicked.connect(self.mostrar_historial)

        self.usuario_inv = None
        self.sala_inv = None
        self.quien_inv = None

        self.usuario_amigo = None

    def mostrar_historial(self):
        self.historial.show()

    def recibir_invitacion(self):

        self.invitacion = Invitacion(self.cliente, self, self.quien_inv, self.sala_inv)

    def invitar_persona(self):

        if self.lineEdit_6.text() == self.cliente.usuario:
            self.lineEdit_6.setText("No puede autoinvitarse")
        else:
            content = "invitacion:" + self.lineEdit_6.text() + "," + self.cliente.sala + "," + self.cliente.usuario
            self.cliente.send_message_to_server(content)

    def mover_figura(self, input_x=None, input_y=None):
        try:
            x = self.lineEdit_4.text() if input_x == None else input_x
            y = "-" + self.lineEdit_5.text() if input_y == None else input_y

            x = float(x)
            y = float(y)

            for elem in self.lista_ultima_figura:
                elem.setPos(x, y)

            if self.cliente.soy_dibujante:
                self.cliente.send_message_to_server("mover_figura:" + str(x) + "," + str(y))


        except Exception:
            pass

    def mostrar_minichat_ind(self):
        self.seleccion_chat_ind.actualizar()
        self.seleccion_chat_ind.hide()
        self.seleccion_chat_ind.show()

    def mostrar_minichat_grup(self):
        self.seleccion_chat_grup.actualizar()
        self.seleccion_chat_grup.hide()
        self.seleccion_chat_grup.show()

    def rellenar_amigos(self):
        with open("amistades") as file:

            for line in file.readlines():
                line = line.strip()
                lista_amistad = line.split(":::")
                if self.cliente.usuario == lista_amistad[0]:
                    self.lista_amigos.append(lista_amistad[1])

    def amistad_desde_grupal(self):
        self.usuario_amigo = self.lineEdit_3.text()
        self.hacer_amigo()

    def hacer_amigo(self):

        if self.usuario_amigo not in self.lista_amigos and self.usuario_amigo != self.cliente.usuario:
            with open("base_datos_registro") as file:
                for line in file.readlines():
                    un_usuario = line.split(":::")[0]
                    if un_usuario == self.usuario_amigo:
                        with open("amistades", "a+") as file:
                            file.write(self.cliente.usuario + ":::" + self.usuario_amigo + "\n")
                            file.write(self.usuario_amigo + ":::" + self.cliente.usuario + "\n")
                            self.cliente.num_notificacion = 3
                            self.cliente.send_message_to_server(
                                "nueva_amistad:" + self.usuario_amigo + ":::" + self.cliente.usuario)

                        self.lista_amigos.append(self.usuario_amigo)

                        break
                else:
                    self.cliente.num_notificacion = 4
        else:
            self.cliente.num_notificacion = 5
        self.cliente.señal_notificacion.mi_senhal.emit()

    def cambiar_color_rgb(self):
        largo_incorrecto = False
        rgb_total = self.lineEdit_2.text()
        lista_rgb = rgb_total.split(":")
        if len(lista_rgb) != 3:
            largo_incorrecto = True
        if not largo_incorrecto:
            if int(lista_rgb[0]) <= 255 and int(lista_rgb[0]) >= 0 and \
                            int(lista_rgb[1]) <= 255 and int(lista_rgb[1]) >= 0 and \
                            int(lista_rgb[2]) <= 255 and int(lista_rgb[2]) >= 0:
                color = QtGui.QColor()
                color.setRgb(int(lista_rgb[0]), int(lista_rgb[1]), int(lista_rgb[2]))
                self.pen = QtGui.QPen()
                self.pen.setColor(color)
                self.lista_colores_usados.append((int(lista_rgb[0]), int(lista_rgb[1]), int(lista_rgb[2])))
                self.lineEdit_2.setText("Color cambiado")
                self.color = rgb_total
            else:
                self.lineEdit_2.setText("Color incorrecto")
        else:
            self.lineEdit_2.setText("Largo incorrecto")

    def cambiar_color_usado_1(self):

        self.color = str(self.lista_rgb_1[0]) + ":" + str(self.lista_rgb_1[1]) + ":" + str(self.lista_rgb_1[2])
        color = QtGui.QColor()
        color.setRgb(*self.lista_rgb_1)
        self.pen = QtGui.QPen()
        self.pen.setColor(color)

    def cambiar_color_usado_2(self):
        self.color = str(self.lista_rgb_2[0]) + ":" + str(self.lista_rgb_2[1]) + ":" + str(self.lista_rgb_2[2])
        color = QtGui.QColor()
        color.setRgb(*self.lista_rgb_2)
        self.pen = QtGui.QPen()
        self.pen.setColor(color)

    def cambiar_color_usado_3(self):
        self.color = str(self.lista_rgb_3[0]) + ":" + str(self.lista_rgb_3[1]) + ":" + str(self.lista_rgb_3[2])
        color = QtGui.QColor()
        color.setRgb(*self.lista_rgb_3)
        self.pen = QtGui.QPen()
        self.pen.setColor(color)

    def cambiar_color_usado_4(self):
        self.color = str(self.lista_rgb_4[0]) + ":" + str(self.lista_rgb_4[1]) + ":" + str(self.lista_rgb_4[2])
        color = QtGui.QColor()
        color.setRgb(*self.lista_rgb_4)
        self.pen = QtGui.QPen()
        self.pen.setColor(color)

    def cambiar_grosor(self):

        if self.cliente.soy_dibujante:

            for rb_id in range(1, 5):
                if getattr(self, 'radioButton_' + str(rb_id)).isChecked():
                    self.pen.setWidth(rb_id * 2)
                    self.grosor = rb_id * 2

    def dibujar_rectangulo(self):
        if self.cliente.soy_dibujante:
            self.cambiar_grosor()
            self.cliente.send_message_to_server("se_dibuja_rectangulo," + self.color + "," + str(self.grosor))

        if self.cliente.soy_dibujante or self.cliente.copiando_dibujo:

            rect = QtCore.QRectF(self.x_rect + self.w_rect / 2 - 50, self.y_rect + self.h_rect / 2 - 25, 100, 50)
            item = self.scene.addRect(rect, pen=self.pen)
            self.lista_ultima_figura = [item]

            self.lista_colores_usados.append(self.color)
            if not self.cliente.copiando_dibujo:
                self.refrescar_botones_color()
                self.cliente.señal_refrescar_colores.mi_senhal.emit()

            self.cliente.copiando_dibujo = False

    def dibujar_triangulo(self):
        if self.cliente.soy_dibujante:
            self.cambiar_grosor()
            self.cliente.send_message_to_server("se_dibuja_triangulo," + self.color + "," + str(self.grosor))

        if self.cliente.soy_dibujante or self.cliente.copiando_dibujo:
            cambio_x = 75
            cambio_y = 75
            item_1 = self.scene.addLine(50 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        100 + self.y_rect + self.h_rect / 2 - cambio_y,
                                        100 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        100 + self.y_rect + self.h_rect / 2 - cambio_y, pen=self.pen)
            item_2 = self.scene.addLine(50 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        100 + self.y_rect + self.h_rect / 2 - cambio_y,
                                        75 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        1 - 0.866025 + 50 + self.y_rect + self.h_rect / 2 - cambio_y, pen=self.pen)
            item_3 = self.scene.addLine(75 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        1 - 0.866025 + 50 + self.y_rect + self.h_rect / 2 - cambio_y,
                                        100 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        100 + self.y_rect + self.h_rect / 2 - cambio_y, pen=self.pen)

            self.lista_ultima_figura = [item_1, item_2, item_3]
            self.lista_colores_usados.append(self.color)
            if not self.cliente.copiando_dibujo:
                self.refrescar_botones_color()
                self.cliente.señal_refrescar_colores.mi_senhal.emit()

            self.cliente.copiando_dibujo = False

    def dibujar_circulo(self):

        if self.cliente.soy_dibujante:
            self.cambiar_grosor()
            self.cliente.send_message_to_server("se_dibuja_circulo," + self.color + "," + str(self.grosor))

        if self.cliente.soy_dibujante or self.cliente.copiando_dibujo:
            cambio_x = 75
            cambio_y = 75
            item = self.scene.addEllipse(50 + self.x_rect + self.w_rect / 2 - cambio_x,
                                         50 + self.y_rect + self.h_rect / 2 - cambio_y,
                                         50,
                                         50, pen=self.pen)
            self.lista_ultima_figura = [item]
            self.lista_colores_usados.append(self.color)
            if not self.cliente.copiando_dibujo:
                self.refrescar_botones_color()
                self.cliente.señal_refrescar_colores.mi_senhal.emit()

            self.cliente.copiando_dibujo = False

    def dibujar_cuadrado(self):
        if self.cliente.soy_dibujante:
            self.cambiar_grosor()
            self.cliente.send_message_to_server("se_dibuja_cuadrado," + self.color + "," + str(self.grosor))

        if self.cliente.soy_dibujante or self.cliente.copiando_dibujo:
            cambio_x = 75
            cambio_y = 75
            item_1 = self.scene.addLine(50 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        50 + self.y_rect + self.h_rect / 2 - cambio_y,
                                        100 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        50 + self.y_rect + self.h_rect / 2 - cambio_y, pen=self.pen)
            item_2 = self.scene.addLine(50 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        50 + self.y_rect + self.h_rect / 2 - cambio_y,
                                        50 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        100 + self.y_rect + self.h_rect / 2 - cambio_y, pen=self.pen)
            item_3 = self.scene.addLine(100 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        100 + self.y_rect + self.h_rect / 2 - cambio_y,
                                        100 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        50 + self.y_rect + self.h_rect / 2 - cambio_y, pen=self.pen)
            item_4 = self.scene.addLine(100 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        100 + self.y_rect + self.h_rect / 2 - cambio_y,
                                        50 + self.x_rect + self.w_rect / 2 - cambio_x,
                                        100 + self.y_rect + self.h_rect / 2 - cambio_y, pen=self.pen)

            self.lista_ultima_figura = [item_1, item_2, item_3, item_4]
            self.lista_colores_usados.append(self.color)

            if not self.cliente.copiando_dibujo:
                self.refrescar_botones_color()
                self.cliente.señal_refrescar_colores.mi_senhal.emit()

            self.cliente.copiando_dibujo = False

    def dibujar_linea_recta(self):
        if self.cliente.soy_dibujante:
            self.cambiar_grosor()
            if not self.recibiendo_linea_recta_1:
                self.recibiendo_linea_recta_1 = True
                self.lista_colores_usados.append(self.color)

                if not self.cliente.copiando_dibujo:
                    self.refrescar_botones_color()
                    self.cliente.señal_refrescar_colores.mi_senhal.emit()

    def dibujar_linea_curva(self):
        if self.cliente.soy_dibujante:
            self.cambiar_grosor()

            if not self.recibiendo_linea_curva_1:
                self.recibiendo_linea_curva_1 = True
                self.lista_colores_usados.append(self.color)

                if not self.cliente.copiando_dibujo:
                    self.refrescar_botones_color()
                    self.cliente.señal_refrescar_colores.mi_senhal.emit()

    def enviar_publicacion(self):

        texto = self.lineEdit.text()

        self.cliente.send_message_to_server("imprimir_chat_grupal:" + self.cliente.usuario + ": " + texto)

    def en_graphic_view(self):
        if self.cursor.pos().x() > self.pos().x() + 390 and \
                        self.cursor.pos().x() < self.pos().x() + 390 + self.graphicsView.width() and \
                        self.cursor.pos().y() > self.pos().y() + 50 + 22 and \
                        self.cursor.pos().y() < self.pos().y() + 50 + 22 + self.graphicsView.height():
            return True

        return False

    def mousePressEvent(self, event):

        if self.en_graphic_view:

            if self.recibiendo_linea_recta_2:

                self.segundo_punto_linea_recta = (self.cursor.pos().x() - self.pos().x() - 390,
                                                  self.cursor.pos().y() - self.pos().y() - 50 - 22)

                cambio_x = 190
                cambio_y = 125
                x1 = self.primer_punto_linea_recta[0] + self.x_rect + self.w_rect / 2 - cambio_x
                y1 = self.primer_punto_linea_recta[1] + self.y_rect + self.h_rect / 2 - cambio_y
                x2 = self.segundo_punto_linea_recta[0] + self.x_rect + self.w_rect / 2 - cambio_x
                y2 = self.segundo_punto_linea_recta[1] + self.y_rect + self.h_rect / 2 - cambio_y

                item = self.scene.addLine(x1, y1, x2, y2, pen=self.pen)
                self.lista_ultima_figura = [item]

                if self.cliente.soy_dibujante:
                    self.cambiar_grosor()
                    self.cliente.send_message_to_server(
                        "se_dibuja_linea_recta," + self.color + "," + str(self.grosor) + "," + str(x1) + "," + str(
                            y1) + "," + str(x2) + "," + str(y2))

                self.recibiendo_linea_recta_2 = False



            elif self.recibiendo_linea_recta_1:

                self.primer_punto_linea_recta = (self.cursor.pos().x() - self.pos().x() - 390,
                                                 self.cursor.pos().y() - self.pos().y() - 50 - 22)

                self.recibiendo_linea_recta_1 = False
                self.recibiendo_linea_recta_2 = True

            if self.recibiendo_linea_curva_2:

                self.segundo_punto_linea_curva = (self.cursor.pos().x() - self.pos().x() - 390,
                                                  self.cursor.pos().y() - self.pos().y() - 50 - 22)

                cambio_x = 190
                cambio_y = 125
                x1 = self.primer_punto_linea_curva[0] + self.x_rect + self.w_rect / 2 - cambio_x
                y1 = self.primer_punto_linea_curva[1] + self.y_rect + self.h_rect / 2 - cambio_y
                x2 = self.segundo_punto_linea_curva[0] + self.x_rect + self.w_rect / 2 - cambio_x
                y2 = self.segundo_punto_linea_curva[1] + self.y_rect + self.h_rect / 2 - cambio_y

                primer_punto = QtCore.QPointF(x1, y1)
                segundo_punto = QtCore.QPointF(x2, y2)
                curva = Curva(self.pen, primer_punto, segundo_punto)

                item = self.scene.addItem(curva)
                self.lista_ultima_figura = [item]

                if self.cliente.soy_dibujante:
                    self.cambiar_grosor()
                    self.cliente.send_message_to_server(
                        "se_dibuja_linea_curva," + self.color + "," + str(self.grosor) + "," + str(
                            x1) + "," + str(y1) + "," + str(x2) + "," + str(y2))

                self.recibiendo_linea_curva_2 = False



            elif self.recibiendo_linea_curva_1:

                self.primer_punto_linea_curva = (self.cursor.pos().x() - self.pos().x() - 390,
                                                 self.cursor.pos().y() - self.pos().y() - 50 - 22)

                self.recibiendo_linea_curva_1 = False
                self.recibiendo_linea_curva_2 = True

    def cambiar_color_grosor(self, rgb_dibujante, grosor_dibujante):
        self.color = rgb_dibujante
        color = QtGui.QColor()
        color_dibujante = rgb_dibujante.split(":")
        color.setRgb(int(color_dibujante[0]), int(color_dibujante[1]), int(color_dibujante[2]))
        self.pen = QtGui.QPen()
        self.pen.setColor(color)
        self.pen.setWidth(int(grosor_dibujante))

    def refrescar_botones_color(self):
        dict_colores = {}
        for color in self.lista_colores_usados:
            dict_colores.update({color: self.lista_colores_usados.count(color)})

        def orden(elem_tupla):
            return elem_tupla[1]

        lista_tuplas = list(dict_colores.items())

        lista_sorted = sorted(lista_tuplas, key=orden, reverse=True)

        cont = 0
        for color, num in lista_sorted[:4]:
            lista_color = color.split(":")

            if cont == 0:
                self.lista_rgb_1[0] = int(lista_color[0])
                self.lista_rgb_1[1] = int(lista_color[1])
                self.lista_rgb_1[2] = int(lista_color[2])

            if cont == 1:
                self.lista_rgb_2[0] = int(lista_color[0])
                self.lista_rgb_2[1] = int(lista_color[1])
                self.lista_rgb_2[2] = int(lista_color[2])

            if cont == 2:
                self.lista_rgb_3[0] = int(lista_color[0])
                self.lista_rgb_3[1] = int(lista_color[1])
                self.lista_rgb_3[2] = int(lista_color[2])

            if cont == 3:
                self.lista_rgb_4[0] = int(lista_color[0])
                self.lista_rgb_4[1] = int(lista_color[1])
                self.lista_rgb_4[2] = int(lista_color[2])

            cont += 1

        self.style_1 = "QPushButton {background-color: rgb(" + str(self.lista_rgb_1[0]) + "," + str(
            self.lista_rgb_1[1]) + "," + str(self.lista_rgb_1[2]) + ");}"
        self.style_2 = "QPushButton {background-color: rgb(" + str(self.lista_rgb_2[0]) + "," + str(
            self.lista_rgb_2[1]) + "," + str(self.lista_rgb_2[2]) + ");}"
        self.style_3 = "QPushButton {background-color: rgb(" + str(self.lista_rgb_3[0]) + "," + str(
            self.lista_rgb_3[1]) + "," + str(self.lista_rgb_3[2]) + ");}"
        self.style_4 = "QPushButton {background-color: rgb(" + str(self.lista_rgb_4[0]) + "," + str(
            self.lista_rgb_4[1]) + "," + str(self.lista_rgb_4[2]) + ");}"


def closeEvent(self, event):
    self.hide()
    self.cliente.disconnect()
