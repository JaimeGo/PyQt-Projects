import socket
from pickle import dumps, loads
from random import randint, random
from sys import exit
from threading import Thread

from PyQt4 import QtGui, QtCore
from menu_inicial import MenuInicial
from inscribir_palabra import InscripcionPalabra
from clase_curva import Curva
from time import sleep

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 1238


class MiSenhal(QtCore.QObject):
    mi_senhal = QtCore.pyqtSignal()


class Cliente:
    def __init__(self, pos, host=None, port=None):

        host = DEFAULT_HOST if host is None else host
        port = DEFAULT_PORT if port is None else port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_list = list()
        self.is_alive = True

        self.sala = "sala_1:::"
        self.usuario = None

        self.señal_publicar_chat_grupal = MiSenhal()
        self.señal_publicar_chat_grupal.mi_senhal.connect(self.publicar_en_chat)

        self.señal_publicar_retenidos_grupal = MiSenhal()
        self.señal_publicar_retenidos_grupal.mi_senhal.connect(self.publicar_retenidos)

        self.señal_pedir_palabra_grupal = MiSenhal()
        self.señal_pedir_palabra_grupal.mi_senhal.connect(self.pedir_palabra)

        self.señal_notificacion = MiSenhal()
        self.señal_notificacion.mi_senhal.connect(self.notificar)

        self.señal_minichat_ind = MiSenhal()
        self.señal_minichat_ind.mi_senhal.connect(self.publicar_en_ind)

        self.señal_minichat_grup = MiSenhal()
        self.señal_minichat_grup.mi_senhal.connect(self.publicar_en_grup)

        self.señal_minichat_ind_texto = MiSenhal()
        self.señal_minichat_ind_texto.mi_senhal.connect(self.publicar_texto_ind)

        self.señal_minichat_grup_texto = MiSenhal()
        self.señal_minichat_grup_texto.mi_senhal.connect(self.publicar_texto_grup)

        self.señal_refrescar_colores = MiSenhal()
        self.señal_refrescar_colores.mi_senhal.connect(self.refrescar_colores)

        self.señal_recibir_invitacion = MiSenhal()
        self.señal_recibir_invitacion.mi_senhal.connect(self.recibir_invitacion)

        self.señal_historial = MiSenhal()
        self.señal_historial.mi_senhal.connect(self.actualizar_historial)

        self.ultima_frase_chat = None
        self.lista_mensajes_retenidos = []

        self.lista_puntajes = ["-", "-", "-", "-", "-", "-"]

        self.tiempo_restante = 120

        self.soy_dibujante = False
        self.copiando_dibujo = False

        self.puntaje = 0
        self.ya_adivinaste = False

        self.num_notificacion = 0

        self.lista_en_minichat = []

        self.ultimo_mensaje_chat_ind = None
        self.ultimo_mensaje_chat_grup = None

        self.ultimo_texto_chat_ind = None
        self.ultimo_texto_chat_grup = None

        self.ultimo_num_imagen = 1

        self.esperando_para_entrar = False

        try:

            self.socket.connect((host, port))

            self.receiver = Thread(target=self.hear_message_from_server)
            self.receiver.daemon = True
            self.receiver.start()

            self.menu = MenuInicial(self)
            self.actualizar_dashboard(*self.lista_puntajes)
            self.menu.move(*pos)
            self.menu.show()


        except socket.error:
            print("No fue posible realizar la conexión")
            exit()

    def recibir_invitacion(self):
        self.menu.chat_grupal.recibir_invitacion()

    def publicar_en_chat(self):

        texto = self.ultima_frase_chat

        self.publicar(texto)

    def publicar_retenidos(self):
        for mensaje in self.lista_mensajes_retenidos:
            self.publicar(mensaje)

    def pedir_palabra(self):

        self.peticion_palabra = InscripcionPalabra(self, self.menu)

        self.peticion_palabra.show()

    def publicar(self, mensaje):

        self.label_ocupado_1 = QtGui.QLabel()
        self.label_ocupado_1.setText(mensaje)

        self.label_ocupado_1.setParent(self.menu.chat_grupal.widget_1)

        self.label_ocupado_1.move(self.menu.chat_grupal.ultima_pos[0], self.menu.chat_grupal.ultima_pos[1])
        self.label_ocupado_1.show()

        self.menu.chat_grupal.lista_entidades.append(self.label_ocupado_1)

        self.menu.chat_grupal.ultima_pos = (
            self.menu.chat_grupal.ultima_pos[0], self.menu.chat_grupal.ultima_pos[1] + 15)
        if self.menu.chat_grupal.publicaciones >= 10:
            self.menu.chat_grupal.exceso_altura += 15

        self.menu.chat_grupal.widget_1.setFixedSize(367, 150 + self.menu.chat_grupal.exceso_altura)
        self.menu.chat_grupal.publicaciones += 1

        self.menu.chat_grupal.scrollArea.ensureVisible(0, 150 + self.menu.chat_grupal.exceso_altura)

        print(self.label_ocupado_1.width())

    def chatear_desde_minichat(self, mensaje):
        cadena_usuarios = ","
        cadena_usuarios = cadena_usuarios.join(self.lista_en_minichat)
        mensaje_mod = "minichat:" + mensaje + ":::" + cadena_usuarios
        self.send_message_to_server(mensaje_mod)

    def refrescar_colores(self):
        self.menu.chat_grupal.pushButton_10.setStyleSheet(self.menu.chat_grupal.style_1)
        self.menu.chat_grupal.pushButton_11.setStyleSheet(self.menu.chat_grupal.style_2)
        self.menu.chat_grupal.pushButton_12.setStyleSheet(self.menu.chat_grupal.style_3)
        self.menu.chat_grupal.pushButton_13.setStyleSheet(self.menu.chat_grupal.style_4)

    def notificar(self):
        mensaje = ""
        if self.num_notificacion == 1:
            mensaje = "[notificacion] ¡Estás cerca!"
        if self.num_notificacion == 2:
            mensaje = "[notificacion] ¡Adivinaste!"

        if self.num_notificacion == 3:
            mensaje = "[notificacion] Nuevo amigo"

        if self.num_notificacion == 4:
            mensaje = "[notificacion] Amigo no encontrado"
        if self.num_notificacion == 5:
            mensaje = "[notificacion] Amigo ya conocido"
        self.publicar(mensaje)

    def hear_message_from_server(self):

        while self.is_alive:
            data = self.socket.recv(1024)
            if data:
                content = loads(data)
                sala_content = content[:9]
                content = content[9:]
                self.current_list.append(content)
                print("Servidor: {}".format(content))

                if content.startswith("partida_grupal_con:"):

                    lista_jugadores = content[len("partida_grupal_con:"):].split(",")
                    if self.usuario in lista_jugadores:
                        self.sala = "sala_3:::"
                        self.menu.chat_grupal.hide()
                        self.menu.chat_grupal.show()

                if content.startswith("empieza_ronda"):
                    self.esperando_para_entrar = False

                if sala_content == self.sala:

                    if content.startswith("imprimir_chat_grupal:"):
                        self.ultima_frase_chat = content[len("imprimir_chat_grupal:"):]

                        self.señal_publicar_chat_grupal.mi_senhal.emit()

                    if content.startswith("paso_tiempo_preparacion:"):
                        print(self.soy_dibujante, self.tiempo_restante)
                        self.tiempo_restante = int(content[len("paso_tiempo_preparacion:"):])
                        self.menu.chat_grupal.label_6.setText(str(self.tiempo_restante) + " seg.")
                        self.menu.chat_grupal.label_14.setText("Preparación")
                        self.menu.chat_grupal.label_4.setText("Tiempo de preparación")
                        if self.tiempo_restante == 0:
                            self.menu.chat_grupal.label_14.setText("Esperando a elección de palabra")
                            self.menu.chat_grupal.label_4.setText("No es tu turno. ¡Adivina!")
                    if content.startswith("paso_tiempo_grupal:"):
                        print(self.soy_dibujante, self.tiempo_restante)
                        self.tiempo_restante = int(content[len("paso_tiempo_grupal:"):])

                        self.menu.chat_grupal.label_6.setText(str(self.tiempo_restante) + " seg.")
                        self.menu.chat_grupal.label_14.setText("Ronda en curso")

                    if content.startswith("tu_dibujas"):
                        self.soy_dibujante = True
                        self.señal_pedir_palabra_grupal.mi_senhal.emit()
                        self.menu.chat_grupal.label_4.setText("Es tu turno. ¡Dibuja!")

                    if content.startswith("termina_ronda"):
                        self.soy_dibujante = False
                        self.ya_adivinaste = False

                    if content.startswith("se_dibuja_cuadrado"):
                        self.copiando_dibujo = True
                        lista_datos = content.split(",")
                        self.menu.chat_grupal.cambiar_color_grosor(lista_datos[1], lista_datos[2])
                        self.menu.chat_grupal.dibujar_cuadrado()

                    if content.startswith("se_dibuja_circulo"):
                        self.copiando_dibujo = True
                        lista_datos = content.split(",")
                        self.menu.chat_grupal.cambiar_color_grosor(lista_datos[1], lista_datos[2])
                        self.menu.chat_grupal.dibujar_circulo()

                    if content.startswith("se_dibuja_rectangulo"):
                        self.copiando_dibujo = True
                        lista_datos = content.split(",")
                        self.menu.chat_grupal.cambiar_color_grosor(lista_datos[1], lista_datos[2])
                        self.menu.chat_grupal.dibujar_rectangulo()

                    if content.startswith("se_dibuja_triangulo"):
                        self.copiando_dibujo = True
                        lista_datos = content.split(",")
                        self.menu.chat_grupal.cambiar_color_grosor(lista_datos[1], lista_datos[2])
                        self.menu.chat_grupal.dibujar_triangulo()

                    if content.startswith("se_dibuja_linea_recta"):
                        self.copiando_dibujo = True
                        lista_datos = content.split(",")
                        self.menu.chat_grupal.cambiar_color_grosor(lista_datos[1], lista_datos[2])
                        self.menu.chat_grupal.scene.addLine(float(lista_datos[3]), float(lista_datos[4]),
                                                            float(lista_datos[5]), float(lista_datos[6]),
                                                            pen=self.menu.chat_grupal.pen)

                    if content.startswith("se_dibuja_linea_curva"):
                        self.copiando_dibujo = True
                        lista_datos = content.split(",")
                        self.menu.chat_grupal.cambiar_color_grosor(lista_datos[1], lista_datos[2])
                        primer_punto = QtCore.QPointF(float(lista_datos[3]), float(lista_datos[4]))
                        segundo_punto = QtCore.QPointF(float(lista_datos[5]), float(lista_datos[6]))

                        curva = Curva(self.menu.chat_grupal.pen, primer_punto, segundo_punto)
                        self.menu.chat_grupal.scene.addItem(curva)

                    if content.startswith("adivinaste_y_ganaste:"):
                        self.puntaje += int(content[len("adivinaste_y_ganaste:"):])
                        self.menu.chat_grupal.label_2.setText(str(self.puntaje))
                        self.ya_adivinaste = True
                        self.menu.chat_grupal.label_14.setText("¡Ya adivinaste!")
                        self.num_notificacion = 2
                        self.señal_notificacion.mi_senhal.emit()
                    if content.startswith("mensaje_retenido:"):
                        self.ultima_frase_chat = "[mensaje_retenido] " + content[len(
                            "mensaje_retenido:" + "imprimir_chat_grupal:"):]
                        print("FRASEEEE", self.usuario, self.ultima_frase_chat)
                        self.lista_mensajes_retenidos.append(self.ultima_frase_chat)

                    if content.startswith("fin_mensajes_retenidos"):
                        self.señal_publicar_retenidos_grupal.mi_senhal.emit()

                    if content.startswith("estas_cerca"):
                        self.num_notificacion = 1
                        self.señal_notificacion.mi_senhal.emit()
                    if content.startswith("los_puntajes_son:"):
                        self.lista_puntajes = content[len("los_puntajes_son:"):].split(",")
                        self.actualizar_dashboard(*self.lista_puntajes)

                    if content.startswith("minichat:"):
                        lista_datos = content[len("minichat:"):].split(":::")
                        mensaje = lista_datos[0] + ": " + lista_datos[2]
                        if lista_datos[1] == "ind":

                            self.ultimo_mensaje_chat_ind = mensaje
                            self.señal_minichat_ind.mi_senhal.emit()
                        else:
                            self.ultimo_mensaje_chat_grup = mensaje
                            self.señal_minichat_grup.mi_senhal.emit()

                    if content.startswith("texto_minichat:::"):
                        lista_datos = content[len("texto_minichat:::"):].split(":::")
                        mensaje = lista_datos[0]

                        if lista_datos[1] == "ind":

                            self.ultimo_texto_chat_ind = mensaje
                            self.señal_minichat_ind_texto.mi_senhal.emit()
                        else:
                            self.ultimo_texto_chat_grup = mensaje
                            self.señal_minichat_grup_texto.mi_senhal.emit()

                    if content.startswith("nueva_amistad:"):
                        lista_datos = content[len("nueva_amistad:"):].split(":::")
                        posible_yo = lista_datos[0]
                        el_otro = lista_datos[1]

                        if posible_yo == self.usuario:
                            self.menu.chat_grupal.lista_amigos.append(el_otro)

                    if content.startswith("mover_figura:"):
                        lista_datos = content[len("mover_figura:"):].split(",")
                        self.menu.chat_grupal.mover_figura(lista_datos[0], lista_datos[1])

                    if content.startswith("premio_por_dotes_artisticas:"):
                        puntaje_extra = content[len("premio_por_dotes_artisticas:"):]
                        print(puntaje_extra)
                        self.puntaje += int(puntaje_extra)
                        self.menu.chat_grupal.label_2.setText(str(self.puntaje))

                    if content.startswith("invitacion:"):
                        lista_datos = content[len("invitacion:"):].split(",")
                        self.menu.chat_grupal.usuario_inv = lista_datos[0]
                        self.menu.chat_grupal.sala_inv = lista_datos[1]
                        self.menu.chat_grupal.quien_inv = lista_datos[2]
                        if self.usuario == self.menu.chat_grupal.usuario_inv:
                            self.señal_recibir_invitacion.mi_senhal.emit()

                    if content.startswith("historial_es:"):
                        lista_datos = content[len("historial_es:"):].split(",")
                        self.lista_historial = lista_datos
                        self.señal_historial.mi_senhal.emit()

    def actualizar_historial(self):
        self.menu.chat_grupal.historial.actualizar()

    def guardar_imagen(self):
        pixmap = QtGui.QPixmap(QtCore.QSize(400, 400))
        pixmap.fill()
        painter = QtGui.QPainter()
        painter.begin(pixmap)
        self.menu.chat_grupal.graphicsView.render(painter)
        pixmap.save("imagenes_guardadas/imagen_" + str(self.ultimo_num_imagen) + ".png")
        self.ultimo_num_imagen += 1
        painter.end()

    def publicar_en_ind(self):
        self.menu.chat_grupal.seleccion_chat_ind.mini_chat_ind.publicar_chat(self.ultimo_mensaje_chat_ind)

    def publicar_en_grup(self):
        self.menu.chat_grupal.seleccion_chat_grup.mini_chat_grup.publicar_chat(self.ultimo_mensaje_chat_grup)

    def publicar_texto_ind(self):
        self.menu.chat_grupal.seleccion_chat_ind.mini_chat_ind.publicar_texto(self.ultimo_texto_chat_ind)

    def publicar_texto_grup(self):
        self.menu.chat_grupal.seleccion_chat_grup.mini_chat_grup.publicar_texto(self.ultimo_texto_chat_grup)

    def actualizar_dashboard(self, nombre_1, puntaje_1, nombre_2, puntaje_2, nombre_3, puntaje_3):
        self.menu.chat_grupal.dashboard.label_5.setText(nombre_1)
        self.menu.chat_grupal.dashboard.label_6.setText(nombre_2)
        self.menu.chat_grupal.dashboard.label_7.setText(nombre_3)

        self.menu.chat_grupal.dashboard.label_8.setText(puntaje_1)
        self.menu.chat_grupal.dashboard.label_10.setText(puntaje_2)
        self.menu.chat_grupal.dashboard.label_9.setText(puntaje_3)

    def send_message_to_server(self, contenido):

        contenido = self.sala + contenido

        print("Enviando... {}".format(contenido))
        final_content = dumps(contenido)
        self.socket.send(final_content)

    def disconnect(self):

        print("<== Conexión cerrada ==>")
        self.is_alive = False
        self.send_message_to_server("comando:terminar_conexion")

        self.socket.shutdown(socket.SHUT_RD)
        self.socket.detach()
        self.socket.close()
