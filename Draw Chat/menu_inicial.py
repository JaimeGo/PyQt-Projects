from PyQt4 import QtGui, uic, QtCore
from sys import exit
from chat_grupal import ChatGrupal

formulario_1 = uic.loadUiType("menu_inicio.ui")


class MenuInicial(formulario_1[0], formulario_1[1]):
    def __init__(self, cliente):
        super().__init__()

        self.cliente = cliente

        self.setupUi(self)
        self.pushButton.clicked.connect(self.registrarse)
        self.pushButton_2.clicked.connect(self.ingresar)
        self.pushButton_3.clicked.connect(self.salir)
        self.menu_ingreso = MenuIngreso(self.cliente, self)
        self.menu_registro = MenuRegistro(self.cliente, self)
        self.chat_grupal = ChatGrupal(self.cliente, self)
        self.seleccion_sala = SeleccionSala(self.cliente, self)

    def registrarse(self):
        self.hide()
        self.menu_registro.show()

    def ingresar(self):
        self.hide()
        self.menu_ingreso.show()

    def salir(self):
        self.cliente.disconnect()
        self.hide()
        exit(0)

    def closeEvent(self, event):
        self.hide()
        self.cliente.disconnect()


formulario_2 = uic.loadUiType("ingreso.ui")


class MenuIngreso(formulario_2[0], formulario_2[1]):
    def __init__(self, cliente, menu_inicial):
        super().__init__()

        self.cliente = cliente
        self.menu_inicial = menu_inicial

        self.setupUi(self)
        self.pushButton.clicked.connect(self.continuar)

    def continuar(self):
        usuario = self.lineEdit.text()
        contraseña = self.lineEdit_2.text()

        seguir_escuchando = True
        primer_largo = len(self.cliente.current_list)

        self.cliente.send_message_to_server("antiguo_usuario:" + usuario + "," + contraseña)

        while seguir_escuchando:
            if len(self.cliente.current_list) > primer_largo:

                if self.cliente.current_list[-1] == "contraseña_aceptada":
                    print("SE ACEPTÓ!!!")
                    seguir_escuchando = False
                    self.hide()
                    self.menu_inicial.seleccion_sala.show()
                    self.cliente.usuario = usuario
                    self.cliente.menu.chat_grupal.rellenar_amigos()


                elif self.cliente.current_list[-1] == "contraseña_rechazada":
                    print("SE RECHAZÓ!!!")
                    seguir_escuchando = False
                    self.label_3.setText("Error: Datos incorrectos")
                    self.label_3.setStyleSheet("QLabel {color:red}")
                    self.lineEdit.clear()
                    self.lineEdit_2.clear()

    def closeEvent(self, event):
        self.hide()
        self.cliente.disconnect()


formulario_3 = uic.loadUiType("registro.ui")


class MenuRegistro(formulario_3[0], formulario_3[1]):
    def __init__(self, cliente, menu_inicial):
        super().__init__()

        self.cliente = cliente
        self.menu_inicial = menu_inicial

        self.setupUi(self)
        self.pushButton.clicked.connect(self.continuar)

    def continuar(self):
        usuario = self.lineEdit.text()
        contraseña = self.lineEdit_2.text()
        confirmacion = self.lineEdit_3.text()

        if len(usuario) == 0 or len(contraseña) == 0 or len(confirmacion) == 0:
            self.label_4.setText("Error: Falta información")
            self.label_4.setStyleSheet("QLabel {color:red}")
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
        elif contraseña != confirmacion:
            self.label_4.setText("Error: Contraseñas no coinciden")
            self.label_4.setStyleSheet("QLabel {color:red}")
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()

        else:
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.cliente.send_message_to_server("nuevo_usuario:" + usuario + "," + contraseña)
            self.hide()
            self.menu_inicial.show()

    def closeEvent(self, event):
        self.hide()
        self.cliente.disconnect()


formulario_4 = uic.loadUiType("seleccion_sala.ui")


class SeleccionSala(formulario_4[0], formulario_4[1]):
    def __init__(self, cliente, menu_inicial):
        super().__init__()

        self.cliente = cliente
        self.menu_inicial = menu_inicial

        self.setupUi(self)
        self.pushButton.clicked.connect(self.entrar_1)
        self.pushButton_2.clicked.connect(self.entrar_2)
        self.pushButton_3.clicked.connect(self.entrar_3)

    def entrar_1(self):
        self.cliente.sala = "sala_1:::"

        self.hide()
        self.menu_inicial.chat_grupal.show()
        self.cliente.send_message_to_server("empieza_partida:")

    def entrar_2(self):
        self.cliente.sala = "sala_2:::"
        self.hide()
        self.menu_inicial.chat_grupal.show()
        self.cliente.send_message_to_server("empieza_partida:")

    def entrar_3(self):
        self.cliente.sala = "sala_3:::"
        self.hide()
        self.menu_inicial.chat_grupal.mostrar_minichat_grup()
