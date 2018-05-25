from PyQt4 import QtGui, uic, QtCore

formulario_1 = uic.loadUiType("invitacion.ui")


class Invitacion(formulario_1[0], formulario_1[1]):
    def __init__(self, cliente, chat_grupal, invitante, sala):
        super().__init__()

        self.cliente = cliente

        self.chat_grupal = chat_grupal

        self.setupUi(self)

        self.sala = sala

        if sala == "sala_3:::":
            sala = "\n que fue creada por su grupo"
        else:
            sala = sala[5]
        mensaje = "El usuario " + invitante + " lo ha invitado a la sala " + sala

        self.label.setText(mensaje)
        self.invitante = invitante

        self.show()

        self.pushButton.clicked.connect(self.aceptar)
        self.pushButton_2.clicked.connect(self.rechazar)

    def aceptar(self):
        self.cliente.sala = self.sala

        self.cliente.esperando_para_entrar = True

        self.cliente.menu.chat_grupal.label_14.setText("Esperando para entrar")
        self.cliente.menu.chat_grupal.label_4.setText("Esperando para entrar")
        self.cliente.menu.chat_grupal.label_6.setText("Esperando para entrar")

        self.chat_grupal.hide()

        self.chat_grupal.show()

        self.hide()

    def rechazar(self):
        self.hide()
