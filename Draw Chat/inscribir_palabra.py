from PyQt4 import QtGui, uic, QtCore

formulario_1 = uic.loadUiType("inscripcion_palabra.ui")


class InscripcionPalabra(formulario_1[0], formulario_1[1]):
    def __init__(self, cliente, chat_grupal):
        super().__init__()

        self.cliente = cliente

        self.chat_grupal = chat_grupal

        self.setupUi(self)

        self.pushButton.clicked.connect(self.continuar)

    def continuar(self):
        palabra = self.lineEdit.text()
        self.cliente.send_message_to_server("palabra_elegida:" + palabra)
        self.hide()
