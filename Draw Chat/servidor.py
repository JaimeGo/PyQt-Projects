import socket
from pickle import dumps, loads
from random import randint, random, choice
from sys import exit
from threading import Thread
from validacion import encriptar_y_guardar, comparar_usuario
from PyQt4 import QtCore
from time import sleep

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 1238

TIEMPO_RONDA = 120
TIEMPO_PREPARACION = 5


class MiSenhal(QtCore.QObject):
    mi_senhal = QtCore.pyqtSignal()


class Servidor:
    def __init__(self, host=None, port=None):

        host = DEFAULT_HOST if host is None else host
        port = DEFAULT_PORT if port is None else port

        self.current_list = list()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.is_alive = True

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

        self.socket.listen(5)

        self.connections = list()
        self.acceptor = Thread(target=self._accept_client, daemon=True)
        self.acceptor.start()

        self.dict_puntajes_grupal_1 = {}
        self.dict_sockets_grupal_1 = {}
        self.lista_mensajes_sockets_correctos_1 = []
        self.lista_sockets_ronda_grupal_1 = []
        self.lista_sockets_utilizados_grupal_1 = []
        self.lista_sockets_correctos_ronda_1 = []
        self.partida_en_curso_grupal_1 = False
        self.palabra_ronda_grupal_1 = None
        self.empieza_ronda_grupal_1 = False
        self.orden_dibujo_mandada_1 = False
        self.socket_dibujante_ronda_grupal_1 = None

        self.dict_puntajes_grupal_2 = {}
        self.dict_sockets_grupal_2 = {}
        self.lista_mensajes_sockets_correctos_2 = []
        self.lista_sockets_ronda_grupal_2 = []
        self.lista_sockets_utilizados_grupal_2 = []
        self.lista_sockets_correctos_ronda_2 = []
        self.partida_en_curso_grupal_2 = False
        self.palabra_ronda_grupal_2 = None
        self.empieza_ronda_grupal_2 = False
        self.orden_dibujo_mandada_2 = False
        self.socket_dibujante_ronda_grupal_2 = None

        self.dict_puntajes_grupal_3 = {}
        self.dict_sockets_grupal_3 = {}
        self.lista_mensajes_sockets_correctos_3 = []
        self.lista_sockets_ronda_grupal_3 = []
        self.lista_sockets_utilizados_grupal_3 = []
        self.lista_sockets_correctos_ronda_3 = []
        self.partida_en_curso_grupal_3 = False
        self.palabra_ronda_grupal_3 = None
        self.empieza_ronda_grupal_3 = False
        self.orden_dibujo_mandada_3 = False
        self.socket_dibujante_ronda_grupal_3 = None

        self.sala = "sala_1:::"

        self.señal_empezar_grupal = MiSenhal()
        self.señal_empezar_grupal.mi_senhal.connect(self.empieza_juego_grupal)

        self.num_partida_1 = 0
        self.num_ronda_1 = 1
        self.num_partida_2 = 0
        self.num_ronda_2 = 1
        self.num_partida_3 = 0
        self.num_ronda_3 = 1

        self.nombre_ganador_1 = "-"
        self.nombre_ganador_2 = "-"
        self.nombre_ganador_3 = "-"

    def _accept_client(self):

        while self.is_alive:
            client_socket, client_address = self.socket.accept()
            client_thread = Thread(target=self.hear_message_from_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()
            print("Nuevo cliente: {}".format(client_address))
            self.connections.append((client_socket, client_thread))

    def hear_message_from_client(self, client_socket):

        conexion_activa = True
        while self.is_alive and conexion_activa:
            data = client_socket.recv(1024)
            content = loads(data)
            sala_content = content[:9]
            self.sala = sala_content
            content = content[9:]
            self.current_list.append(content)
            print("Client: {}".format(content))

            if content == "comando:terminar_conexion":

                conexion_activa = False

                for tuple in self.connections:
                    if tuple[0] == client_socket:
                        self.connections.remove(tuple)

                        if not self.connections:
                            self.disconnect()

            elif content.startswith("nuevo_usuario:"):
                lista_datos = content[len("nuevo_usuario:"):].split(",")
                usuario = lista_datos[0]
                contraseña = lista_datos[1]
                encriptar_y_guardar(usuario, contraseña)

            elif content.startswith("antiguo_usuario:"):

                lista_datos = content[len("antiguo_usuario:"):].split(",")
                usuario = lista_datos[0]
                contraseña = lista_datos[1]
                if comparar_usuario(usuario, contraseña):
                    final_content = dumps(sala_content + "contraseña_aceptada")
                    client_socket.send(final_content)

                    if sala_content == "sala_1:::":
                        self.dict_sockets_grupal_1.update({usuario: client_socket})

                    if sala_content == "sala_2:::":
                        self.dict_sockets_grupal_2.update({usuario: client_socket})

                    if sala_content == "sala_3:::":
                        self.dict_sockets_grupal_3.update({usuario: client_socket})
                        if len(self.dict_sockets_grupal_3) >= 2 and not self.partida_en_curso_grupal_3:
                            print("EMPIEZA PARTIDA")
                            self.señal_empezar_grupal.mi_senhal.emit()
                else:
                    final_content = dumps(sala_content + "contraseña_rechazada")
                    client_socket.send(final_content)

            elif content.startswith("empieza_partida"):
                print("A")
                print(content)
                if sala_content == "sala_1:::":
                    print("B")
                    if len(self.dict_sockets_grupal_1) >= 2 and not self.partida_en_curso_grupal_1:
                        print("EMPIEZA PARTIDA")
                        self.señal_empezar_grupal.mi_senhal.emit()

                if sala_content == "sala_2:::":
                    if len(self.dict_sockets_grupal_2) >= 2 and not self.partida_en_curso_grupal_2:
                        print("EMPIEZA PARTIDA")
                        self.señal_empezar_grupal.mi_senhal.emit()

                if sala_content == "sala_2:::":
                    if len(self.dict_sockets_grupal_3) >= 2 and not self.partida_en_curso_grupal_3:
                        print("EMPIEZA PARTIDA")
                        self.señal_empezar_grupal.mi_senhal.emit()


            elif content.startswith("imprimir_chat_grupal:"):
                lista_datos = content.split(":")

                self.evaluar_palabra(lista_datos[1], content[len(lista_datos[0]) + len(lista_datos[1]) + 2:],
                                     client_socket)
                if sala_content == "sala_1:::":
                    if client_socket not in self.lista_sockets_correctos_ronda_1 and \
                                    self.socket_dibujante_ronda_grupal_1 != client_socket:

                        self.send_message_to_clients(content)

                    else:
                        self.lista_mensajes_sockets_correctos_1.append(content)

                if sala_content == "sala_2:::":
                    if client_socket not in self.lista_sockets_correctos_ronda_2 and \
                                    self.socket_dibujante_ronda_grupal_2 != client_socket:

                        self.send_message_to_clients(content)

                    else:
                        self.lista_mensajes_sockets_correctos_2.append(content)
                if sala_content == "sala_3:::":
                    if client_socket not in self.lista_sockets_correctos_ronda_3 and \
                                    self.socket_dibujante_ronda_grupal_1 != client_socket:

                        self.send_message_to_clients(content)

                    else:
                        self.lista_mensajes_sockets_correctos_3.append(content)


            elif content.startswith("palabra_elegida:"):
                if sala_content == "sala_1:::":
                    self.palabra_ronda_grupal_1 = content[len("palabra_elegida:"):]
                    self.empieza_ronda_grupal_1 = True

                if sala_content == "sala_2:::":
                    self.palabra_ronda_grupal_2 = content[len("palabra_elegida:"):]
                    self.empieza_ronda_grupal_2 = True

                if sala_content == "sala_3:::":
                    self.palabra_ronda_grupal_3 = content[len("palabra_elegida:"):]
                    self.empieza_ronda_grupal_3 = True

            if content.startswith("empieza_ronda"):
                pass

            if content.startswith("se_dibuja"):
                self.mandar_no_dibujantes_grupal(content)

            if content.startswith("minichat:"):
                lista_datos = content[len("minichat:"):].split(":::")
                mensaje = lista_datos[0] + ":::" + lista_datos[1] + ":::" + lista_datos[2]
                lista_destinatarios = lista_datos[3].split(",")
                nuevo_mensaje = "minichat:" + mensaje

                if sala_content == "sala_1:::":
                    for usuario, socket in self.dict_sockets_grupal_1.items():
                        if usuario in lista_destinatarios:
                            contenido = dumps(sala_content + nuevo_mensaje)
                            socket.send(contenido)

                if sala_content == "sala_2:::":
                    for usuario, socket in self.dict_sockets_grupal_2.items():
                        if usuario in lista_destinatarios:
                            contenido = dumps(sala_content + nuevo_mensaje)
                            socket.send(contenido)

                if sala_content == "sala_3:::":
                    for usuario, socket in self.dict_sockets_grupal_3.items():
                        if usuario in lista_destinatarios:
                            contenido = dumps(sala_content + nuevo_mensaje)
                            socket.send(contenido)

            if content.startswith("texto_minichat:"):
                lista_datos = content[len("texto_minichat:"):].split(":::")
                mensaje = lista_datos[0]
                lista_destinatarios = lista_datos[1].split(",")
                nuevo_mensaje = "texto_minichat:" + mensaje + ":::" + lista_datos[2]

                if sala_content == "sala_1:::":
                    for usuario, socket in self.dict_sockets_grupal_1.items():
                        if usuario in lista_destinatarios:
                            contenido = dumps(sala_content + nuevo_mensaje)
                            socket.send(contenido)

                if sala_content == "sala_2:::":
                    for usuario, socket in self.dict_sockets_grupal_2.items():
                        if usuario in lista_destinatarios:
                            contenido = dumps(sala_content + nuevo_mensaje)
                            socket.send(contenido)

                if sala_content == "sala_3:::":
                    for usuario, socket in self.dict_sockets_grupal_3.items():
                        if usuario in lista_destinatarios:
                            contenido = dumps(sala_content + nuevo_mensaje)
                            socket.send(contenido)

            if content.startswith("nueva_amistad:"):
                self.send_message_to_clients(content)

            if content.startswith("mover_figura:"):
                self.mandar_no_dibujantes_grupal(content)

            if content.startswith("partida_grupal_con:"):
                self.send_message_to_clients(content)

            if content.startswith("invitacion:"):
                self.send_message_to_clients(content)

    def send_message_to_clients(self, contenido):

        print("Enviando... {}".format(self.sala + contenido))
        final_content = dumps(self.sala + contenido)
        for client_socket, client_thread in self.connections:
            client_socket.send(final_content)

    def mandar_mensaje_a_grupal(self, contenido):

        print("Enviando... {}".format(self.sala + contenido))

        if self.sala == "sala_1:::":

            final_content = dumps(self.sala + contenido)
            for client_socket in self.dict_sockets_grupal_1.values():
                client_socket.send(final_content)

        if self.sala == "sala_1:::":

            final_content = dumps(self.sala + contenido)
            for client_socket in self.dict_sockets_grupal_2.values():
                client_socket.send(final_content)

        if self.sala == "sala_1:::":

            final_content = dumps(self.sala + contenido)
            for client_socket in self.dict_sockets_grupal_3.values():
                client_socket.send(final_content)

    def mandar_no_dibujantes_grupal(self, contenido):

        print("Enviando... {}".format(contenido))
        lista_no_dibujantes = []
        if self.sala == "sala_1:::":
            lista_no_dibujantes = filter(lambda x: x != self.socket_dibujante_ronda_grupal_1,
                                         list(self.dict_sockets_grupal_1.values()))

        if self.sala == "sala_2:::":
            lista_no_dibujantes = filter(lambda x: x != self.socket_dibujante_ronda_grupal_2,
                                         list(self.dict_sockets_grupal_2.values()))

        if self.sala == "sala_3:::":
            lista_no_dibujantes = filter(lambda x: x != self.socket_dibujante_ronda_grupal_3,
                                         list(self.dict_sockets_grupal_3.values()))

        final_content = dumps(self.sala + contenido)
        for client_socket in lista_no_dibujantes:
            client_socket.send(final_content)

    def empieza_juego_grupal(self):
        if self.sala == "sala_1:::":
            self.thread_tiempo_1 = QtCore.QTimer()
            self.thread_tiempo_1.timeout.connect(self.paso_tiempo_1)
            self.thread_tiempo_1.start(1000)
            self.tiempo_preparacion_grupal_1 = TIEMPO_PREPARACION
            self.tiempo_ronda_grupal_1 = TIEMPO_RONDA

            self.mandar_mensaje_a_grupal("empieza_juego")

            self.mandar_mensaje_a_grupal("empieza_ronda")

            self.elegir_dibujante()

            self.thread_actualizacion_1 = QtCore.QTimer()
            self.thread_actualizacion_1.timeout.connect(self.actualizacion_1)
            self.thread_actualizacion_1.start(100)

            self.tiempo_preparacion_aux_1 = TIEMPO_PREPARACION
            self.tiempo_ronda_aux_1 = TIEMPO_RONDA - 0.7

        if self.sala == "sala_2:::":
            self.thread_tiempo_2 = QtCore.QTimer()
            self.thread_tiempo_2.timeout.connect(self.paso_tiempo_2)
            self.thread_tiempo_2.start(1000)
            self.tiempo_preparacion_grupal_2 = TIEMPO_PREPARACION
            self.tiempo_ronda_grupal_2 = TIEMPO_RONDA

            self.mandar_mensaje_a_grupal("empieza_juego")
            self.mandar_mensaje_a_grupal("empieza_ronda")

            self.elegir_dibujante()

            self.thread_actualizacion_2 = QtCore.QTimer()
            self.thread_actualizacion_2.timeout.connect(self.actualizacion_2)
            self.thread_actualizacion_2.start(100)

            self.tiempo_preparacion_aux_2 = TIEMPO_PREPARACION
            self.tiempo_ronda_aux_2 = TIEMPO_RONDA - 0.7

        if self.sala == "sala_3:::":
            self.thread_tiempo_3 = QtCore.QTimer()
            self.thread_tiempo_3.timeout.connect(self.paso_tiempo_3)
            self.thread_tiempo_3.start(1000)
            self.tiempo_preparacion_grupal_3 = TIEMPO_PREPARACION
            self.tiempo_ronda_grupal_3 = TIEMPO_RONDA

            self.mandar_mensaje_a_grupal("empieza_juego")
            self.mandar_mensaje_a_grupal("empieza_ronda")

            self.elegir_dibujante()

            self.thread_actualizacion_3 = QtCore.QTimer()
            self.thread_actualizacion_3.timeout.connect(self.actualizacion_3)
            self.thread_actualizacion_3.start(100)

            self.tiempo_preparacion_aux_3 = TIEMPO_PREPARACION
            self.tiempo_ronda_aux_3 = TIEMPO_RONDA - 0.7

    def actualizacion_1(self):
        if self.tiempo_preparacion_aux_1 > 0:
            self.tiempo_preparacion_aux_1 -= 0.1
        if self.empieza_ronda_grupal_1 and self.tiempo_ronda_aux_1 > 0:
            self.tiempo_ronda_aux_1 -= 0.1

        if not self.empieza_ronda_grupal_1:
            self.tiempo_ronda_aux_1 = TIEMPO_RONDA - 0.7

        if round(self.tiempo_ronda_aux_1, 1) == 0:
            self.tiempo_preparacion_aux_1 = TIEMPO_PREPARACION
            self.tiempo_ronda_aux_1 = TIEMPO_RONDA - 0.7

        if round(self.tiempo_ronda_aux_1, 1) == 0.1:
            self.sala = "sala_1:::"
            self.mandar_puntajes()

        if round(self.tiempo_ronda_aux_1, 1) == 0.2:
            self.sala = "sala_1:::"
            self.mandar_mensajes_retenidos()

        if round(self.tiempo_ronda_aux_1, 1) == 0.3:
            self.sala = "sala_1:::"

            self.num_ronda_1 += 1
            self.mandar_historial()

    def actualizacion_2(self):
        if self.tiempo_preparacion_aux_2 > 0:
            self.tiempo_preparacion_aux_2 -= 0.1
        if self.empieza_ronda_grupal_2 and self.tiempo_ronda_aux_2 > 0:
            self.tiempo_ronda_aux_2 -= 0.1

        if not self.empieza_ronda_grupal_2:
            self.tiempo_ronda_aux_2 = TIEMPO_RONDA - 0.7

        if round(self.tiempo_ronda_aux_2, 1) == 0:
            self.tiempo_preparacion_aux_2 = TIEMPO_PREPARACION
            self.tiempo_ronda_aux_2 = TIEMPO_RONDA - 0.7

        if round(self.tiempo_ronda_aux_2, 1) == 0.1:
            self.sala = "sala_2:::"
            self.mandar_puntajes()

        if round(self.tiempo_ronda_aux_2, 1) == 0.2:
            self.sala = "sala_2:::"
            self.mandar_mensajes_retenidos()

        if round(self.tiempo_ronda_aux_2, 1) == 0.3:
            self.sala = "sala_2:::"
            self.num_ronda_2 += 1

            self.mandar_historial()

    def actualizacion_3(self):
        if self.tiempo_preparacion_aux_3 > 0:
            self.tiempo_preparacion_aux_3 -= 0.1
        if self.empieza_ronda_grupal_3 and self.tiempo_ronda_aux_3 > 0:
            self.tiempo_ronda_aux_3 -= 0.1

        if not self.empieza_ronda_grupal_3:
            self.tiempo_ronda_aux_3 = TIEMPO_RONDA - 0.7

        if round(self.tiempo_ronda_aux_3, 1) == 0:
            self.tiempo_preparacion_aux_3 = TIEMPO_PREPARACION
            self.tiempo_ronda_aux_3 = TIEMPO_RONDA - 0.7

        if round(self.tiempo_ronda_aux_3, 1) == 0.1:
            self.sala = "sala_3:::"
            self.mandar_puntajes()

        if round(self.tiempo_ronda_aux_3, 1) == 0.2:
            self.sala = "sala_3:::"
            self.mandar_mensajes_retenidos()

        if round(self.tiempo_ronda_aux_3, 1) == 0.3:
            self.sala = "sala_3:::"
            self.num_ronda_3 += 1
            self.mandar_historial()

    def elegir_dibujante(self):
        if self.sala == "sala_1:::":
            lista_posibles_dibujantes = filter(lambda x: x not in self.lista_sockets_utilizados_grupal_1,
                                               list(self.dict_sockets_grupal_1.values()))
            self.socket_dibujante_ronda_grupal_1 = choice(list(lista_posibles_dibujantes))
            self.lista_sockets_utilizados_grupal_1.append(self.socket_dibujante_ronda_grupal_1)

        if self.sala == "sala_2:::":
            lista_posibles_dibujantes = filter(lambda x: x not in self.lista_sockets_utilizados_grupal_2,
                                               list(self.dict_sockets_grupal_2.values()))
            self.socket_dibujante_ronda_grupal_2 = choice(list(lista_posibles_dibujantes))
            self.lista_sockets_utilizados_grupal_2.append(self.socket_dibujante_ronda_grupal_2)

        if self.sala == "sala_3:::":
            lista_posibles_dibujantes = filter(lambda x: x not in self.lista_sockets_utilizados_grupal_3,
                                               list(self.dict_sockets_grupal_3.values()))
            self.socket_dibujante_ronda_grupal_3 = choice(list(lista_posibles_dibujantes))
            self.lista_sockets_utilizados_grupal_3.append(self.socket_dibujante_ronda_grupal_3)

    def paso_tiempo_1(self):
        if self.tiempo_ronda_grupal_1 == 0:
            self.sala = "sala_1:::"

            self.mandar_recompensa_dibujo()
            self.mandar_mensaje_a_grupal("termina_ronda")

            self.lista_sockets_correctos_ronda_1 = []
            self.lista_mensajes_sockets_correctos_1 = []
            self.tiempo_preparacion_grupal_1 = TIEMPO_PREPARACION
            self.tiempo_ronda_grupal_1 = TIEMPO_RONDA
            self.empieza_ronda_grupal_1 = False
            self.orden_dibujo_mandada_1 = False
            self.elegir_dibujante()

            self.mandar_mensaje_a_grupal("empieza_ronda")

            if len(self.lista_sockets_utilizados_grupal_1) == len(self.dict_sockets_grupal_1):
                self.sala = "sala_1:::"
                self.mandar_mensaje_a_grupal("termina_juego")
                self.num_partida_1 += 1

                self.lista_sockets_utilizados_grupal_1 = []

        if self.tiempo_preparacion_grupal_1 > 0:
            self.tiempo_preparacion_grupal_1 -= 1
            self.sala = "sala_1:::"
            self.mandar_mensaje_a_grupal("paso_tiempo_preparacion:" + str(self.tiempo_preparacion_grupal_1))

        else:
            if not self.orden_dibujo_mandada_1:
                final_content = dumps("sala_1:::" + "tu_dibujas")
                self.socket_dibujante_ronda_grupal_1.send(final_content)
                self.orden_dibujo_mandada_1 = True

        if self.empieza_ronda_grupal_1 and self.tiempo_ronda_grupal_1 > 0:
            self.tiempo_ronda_grupal_1 -= 1
            self.sala = "sala_1:::"
            self.mandar_mensaje_a_grupal("paso_tiempo_grupal:" + str(self.tiempo_ronda_grupal_1))

    def paso_tiempo_2(self):

        if self.tiempo_ronda_grupal_2 == 0:
            self.sala = "sala_2:::"

            self.mandar_recompensa_dibujo()
            self.mandar_mensaje_a_grupal("termina_ronda")

            self.lista_sockets_correctos_ronda_2 = []
            self.lista_mensajes_sockets_correctos_2 = []
            self.tiempo_preparacion_grupal_2 = TIEMPO_PREPARACION
            self.tiempo_ronda_grupal_2 = TIEMPO_RONDA
            self.empieza_ronda_grupal_2 = False
            self.orden_dibujo_mandada_2 = False
            self.elegir_dibujante()

            self.mandar_mensaje_a_grupal("empieza_ronda")

            if len(self.lista_sockets_utilizados_grupal_2) == len(self.dict_sockets_grupal_2):
                self.sala = "sala_2:::"
                self.mandar_mensaje_a_grupal("termina_juego")
                self.num_partida_2 += 1

                self.lista_sockets_utilizados_grupal_2 = []

        if self.tiempo_preparacion_grupal_2 > 0:
            self.tiempo_preparacion_grupal_2 -= 1
            self.sala = "sala_2:::"
            self.mandar_mensaje_a_grupal("paso_tiempo_preparacion:" + str(self.tiempo_preparacion_grupal_2))

        else:
            if not self.orden_dibujo_mandada_2:
                final_content = dumps("sala_2:::" + "tu_dibujas")
                self.socket_dibujante_ronda_grupal_2.send(final_content)
                self.orden_dibujo_mandada_2 = True

        if self.empieza_ronda_grupal_2 and self.tiempo_ronda_grupal_2 > 0:
            self.tiempo_ronda_grupal_2 -= 1
            self.sala = "sala_2:::"
            self.mandar_mensaje_a_grupal("paso_tiempo_grupal:" + str(self.tiempo_ronda_grupal_2))

    def paso_tiempo_3(self):
        if self.tiempo_ronda_grupal_3 == 0:
            self.sala = "sala_3:::"
            self.mandar_recompensa_dibujo()
            self.mandar_mensaje_a_grupal("termina_ronda")

            self.lista_sockets_correctos_ronda_3 = []
            self.lista_mensajes_sockets_correctos_3 = []
            self.tiempo_preparacion_grupal_3 = TIEMPO_PREPARACION
            self.tiempo_ronda_grupal_3 = TIEMPO_RONDA
            self.empieza_ronda_grupal_3 = False
            self.orden_dibujo_mandada_3 = False
            self.elegir_dibujante()

            self.sala = "sala_3:::"
            self.mandar_mensaje_a_grupal("empieza_ronda")

            if len(self.lista_sockets_utilizados_grupal_3) == len(self.dict_sockets_grupal_3):
                self.sala = "sala_3:::"
                self.mandar_mensaje_a_grupal("termina_juego")
                self.num_partida_3 += 1

                self.lista_sockets_utilizados_grupal_3 = []

        if self.tiempo_preparacion_grupal_3 > 0:
            self.tiempo_preparacion_grupal_3 -= 1
            self.sala = "sala_3:::"
            self.mandar_mensaje_a_grupal("paso_tiempo_preparacion:" + str(self.tiempo_preparacion_grupal_3))

        else:
            if not self.orden_dibujo_mandada_3:
                final_content = dumps("sala_3:::" + "tu_dibujas")
                self.socket_dibujante_ronda_grupal_3.send(final_content)
                self.orden_dibujo_mandada_3 = True

        if self.empieza_ronda_grupal_3 and self.tiempo_ronda_grupal_3 > 0:
            self.tiempo_ronda_grupal_3 -= 1
            self.sala = "sala_3:::"
            self.mandar_mensaje_a_grupal("paso_tiempo_grupal:" + str(self.tiempo_ronda_grupal_3))

    def mandar_historial(self):
        mensaje = "historial_es:"
        if self.sala == "sala_1:::":
            mensaje += str(self.num_partida_1) + "," + str(self.num_ronda_1) + "," + str(
                len(self.dict_sockets_grupal_1)) + "," + str(len(self.lista_sockets_correctos_ronda_1))
            self.mandar_mensaje_a_grupal(mensaje)

        if self.sala == "sala_2:::":
            mensaje += str(self.num_partida_2) + "," + str(self.num_ronda_2) + "," + str(
                len(self.dict_sockets_grupal_2)) + "," + str(len(self.lista_sockets_correctos_ronda_2))
            self.mandar_mensaje_a_grupal(mensaje)

        if self.sala == "sala_3:::":
            mensaje += str(self.num_partida_3) + "," + str(self.num_ronda_3) + "," + str(
                len(self.dict_sockets_grupal_3)) + "," + str(len(self.lista_sockets_correctos_ronda_3))
            self.mandar_mensaje_a_grupal(mensaje)

    def mandar_recompensa_dibujo(self):
        print("Se ocupa1")
        if self.sala == "sala_1:::":
            print(len(self.lista_sockets_correctos_ronda_1), self.socket_dibujante_ronda_grupal_1)
            mensaje = dumps(
                self.sala + "premio_por_dotes_artisticas:" + str(5 * len(self.lista_sockets_correctos_ronda_1)))
            self.socket_dibujante_ronda_grupal_1.send(mensaje)

        if self.sala == "sala_2:::":
            mensaje = dumps(
                self.sala + "premio_por_dotes_artisticas:" + str(5 * len(self.lista_sockets_correctos_ronda_2) - 1))
            self.socket_dibujante_ronda_grupal_2.send(mensaje)

        if self.sala == "sala_3:::":
            mensaje = dumps(
                self.sala + "premio_por_dotes_artisticas:" + str(5 * len(self.lista_sockets_correctos_ronda_3) - 1))
            self.socket_dibujante_ronda_grupal_3.send(mensaje)

    def mandar_mensajes_retenidos(self):
        if self.sala == "sala_1:::":

            for socket in self.lista_sockets_correctos_ronda_1:

                for mensaje in self.lista_mensajes_sockets_correctos_1:
                    print("\('_')/ holaaa")
                    print("\('_')/")
                    print("\('_')/")
                    print("\('_')/ dejemos un tiempo entre cada mensaje...")
                    content = dumps(self.sala + "mensaje_retenido:" + mensaje)
                    socket.send(content)
                content = dumps(self.sala + "fin_mensajes_retenidos")
                socket.send(content)

        if self.sala == "sala_2:::":

            for socket in self.lista_sockets_correctos_ronda_2:

                for mensaje in self.lista_mensajes_sockets_correctos_2:
                    print("\('_')/ holaaa")
                    print("\('_')/")
                    print("\('_')/")
                    print("\('_')/ dejemos un tiempo entre cada mensaje...")
                    content = dumps(self.sala + "mensaje_retenido:" + mensaje)
                    socket.send(content)
                content = dumps(self.sala + "fin_mensajes_retenidos")
                socket.send(content)

        if self.sala == "sala_3:::":

            for socket in self.lista_sockets_correctos_ronda_3:

                for mensaje in self.lista_mensajes_sockets_correctos_3:
                    print("\('_')/ holaaa")
                    print("\('_')/")
                    print("\('_')/")
                    print("\('_')/ dejemos un tiempo entre cada mensaje retenido...")
                    content = dumps(self.sala + "mensaje_retenido:" + mensaje)
                    socket.send(content)
                content = dumps(self.sala + "fin_mensajes_retenidos")
                socket.send(content)

    def mandar_puntajes(self):
        if self.sala == "sala_1:::":
            lista_sorteada = sorted(list(self.dict_puntajes_grupal_1.items()), key=lambda x: x[1], reverse=True)
            (n2, p2) = ("-", "-")
            (n3, p3) = ("-", "-")
            (n1, p1) = ("-", "-")
            if len(lista_sorteada) >= 1:
                (n1, p1) = lista_sorteada[0]
            if len(lista_sorteada) >= 2:
                (n2, p2) = lista_sorteada[1]
            if len(lista_sorteada) >= 3:
                (n3, p3) = lista_sorteada[2]
            mensaje = "los_puntajes_son:" + n1 + "," + str(p1) + "," + n2 + "," + str(p2) + "," + n3 + "," + str(p3)
            self.mandar_mensaje_a_grupal(mensaje)

        if self.sala == "sala_2:::":
            lista_sorteada = sorted(list(self.dict_puntajes_grupal_2.items()), key=lambda x: x[1], reverse=True)
            (n2, p2) = ("-", "-")
            (n3, p3) = ("-", "-")
            (n1, p1) = ("-", "-")
            if len(lista_sorteada) >= 1:
                (n1, p1) = lista_sorteada[0]
            if len(lista_sorteada) >= 2:
                (n2, p2) = lista_sorteada[1]
            if len(lista_sorteada) >= 3:
                (n3, p3) = lista_sorteada[2]
            mensaje = "los_puntajes_son:" + n1 + "," + str(p1) + "," + n2 + "," + str(p2) + "," + n3 + "," + str(p3)
            self.mandar_mensaje_a_grupal(mensaje)

        if self.sala == "sala_3:::":
            lista_sorteada = sorted(list(self.dict_puntajes_grupal_3.items()), key=lambda x: x[1], reverse=True)
            (n2, p2) = ("-", "-")
            (n3, p3) = ("-", "-")
            (n1, p1) = ("-", "-")
            if len(lista_sorteada) >= 1:
                (n1, p1) = lista_sorteada[0]
            if len(lista_sorteada) >= 2:
                (n2, p2) = lista_sorteada[1]
            if len(lista_sorteada) >= 3:
                (n3, p3) = lista_sorteada[2]
            mensaje = "los_puntajes_son:" + n1 + "," + str(p1) + "," + n2 + "," + str(p2) + "," + n3 + "," + str(p3)
            self.mandar_mensaje_a_grupal(mensaje)

    def evaluar_palabra(self, usuario, palabra, socket):

        if self.sala == "sala_1:::" and socket != self.socket_dibujante_ronda_grupal_1:

            if socket not in self.lista_sockets_correctos_ronda_1:
                if self.palabra_ronda_grupal_1 == palabra.strip():
                    self.lista_sockets_correctos_ronda_1.append(socket)
                    puntaje = "1"
                    if self.lista_sockets_correctos_ronda_1.index(socket) == 0:
                        puntaje = "10"

                    if self.lista_sockets_correctos_ronda_1.index(socket) == 1:
                        puntaje = "5"
                    if self.lista_sockets_correctos_ronda_1.index(socket) == 2:
                        puntaje = "3"
                    if usuario not in self.dict_puntajes_grupal_1.keys():
                        self.dict_puntajes_grupal_1.update({usuario: int(puntaje)})
                    else:
                        puntaje_anterior = int(self.dict_puntajes_grupal_1[usuario])
                        self.dict_puntajes_grupal_1.update({usuario: puntaje_anterior + int(puntaje)})
                        print(puntaje_anterior, int(puntaje))
                    print("DICT Puntaje", self.dict_puntajes_grupal_1)
                    final_content = dumps(self.sala + "adivinaste_y_ganaste:" + puntaje)
                    socket.send(final_content)
                if self.palabra_ronda_grupal_1:
                    if len(self.palabra_ronda_grupal_1) == len(palabra.strip()):
                        coincidencias = 0
                        for i in range(len(palabra.strip())):
                            if self.palabra_ronda_grupal_1[i] == palabra.strip()[i]:
                                coincidencias += 1
                        if coincidencias == len(palabra.strip()) - 1:
                            final_content = dumps("estas_cerca")
                            socket.send(final_content)

        if self.sala == "sala_2:::" and socket != self.socket_dibujante_ronda_grupal_2:

            if socket not in self.lista_sockets_correctos_ronda_2:
                if self.palabra_ronda_grupal_2 == palabra.strip():
                    self.lista_sockets_correctos_ronda_2.append(socket)
                    puntaje = "1"
                    if self.lista_sockets_correctos_ronda_2.index(socket) == 0:
                        puntaje = "10"

                    if self.lista_sockets_correctos_ronda_2.index(socket) == 1:
                        puntaje = "5"
                    if self.lista_sockets_correctos_ronda_2.index(socket) == 2:
                        puntaje = "3"
                    if usuario not in self.dict_puntajes_grupal_2.keys():
                        self.dict_puntajes_grupal_2.update({usuario: int(puntaje)})
                    else:
                        puntaje_anterior = int(self.dict_puntajes_grupal_2[usuario])
                        self.dict_puntajes_grupal_2.update({usuario: puntaje_anterior + int(puntaje)})
                        print(puntaje_anterior, int(puntaje))
                    print("DICT Puntaje", self.dict_puntajes_grupal_2)
                    final_content = dumps(self.sala + "adivinaste_y_ganaste:" + puntaje)
                    socket.send(final_content)
                if self.palabra_ronda_grupal_2:
                    if len(self.palabra_ronda_grupal_2) == len(palabra.strip()):
                        coincidencias = 0
                        for i in range(len(palabra.strip())):
                            if self.palabra_ronda_grupal_2[i] == palabra.strip()[i]:
                                coincidencias += 1
                        if coincidencias == len(palabra.strip()) - 1:
                            final_content = dumps("estas_cerca")
                            socket.send(final_content)

        if self.sala == "sala_3:::" and socket != self.socket_dibujante_ronda_grupal_3:

            if socket not in self.lista_sockets_correctos_ronda_3:
                if self.palabra_ronda_grupal_3 == palabra.strip():
                    self.lista_sockets_correctos_ronda_3.append(socket)
                    puntaje = "1"
                    if self.lista_sockets_correctos_ronda_3.index(socket) == 0:
                        puntaje = "10"

                    if self.lista_sockets_correctos_ronda_3.index(socket) == 1:
                        puntaje = "5"
                    if self.lista_sockets_correctos_ronda_3.index(socket) == 2:
                        puntaje = "3"
                    if usuario not in self.dict_puntajes_grupal_3.keys():
                        self.dict_puntajes_grupal_3.update({usuario: int(puntaje)})
                    else:
                        puntaje_anterior = int(self.dict_puntajes_grupal_3[usuario])
                        self.dict_puntajes_grupal_3.update({usuario: puntaje_anterior + int(puntaje)})
                        print(puntaje_anterior, int(puntaje))
                    print("DICT Puntaje", self.dict_puntajes_grupal_3)
                    final_content = dumps(self.sala + "adivinaste_y_ganaste:" + puntaje)
                    socket.send(final_content)
                if self.palabra_ronda_grupal_3:
                    if len(self.palabra_ronda_grupal_3) == len(palabra.strip()):
                        coincidencias = 0
                        for i in range(len(palabra.strip())):
                            if self.palabra_ronda_grupal_3[i] == palabra.strip()[i]:
                                coincidencias += 1
                        if coincidencias == len(palabra.strip()) - 1:
                            final_content = dumps("estas_cerca")
                            socket.send(final_content)

    def disconnect(self):

        self.is_alive = False

        self.socket.detach()
        self.socket.close()
