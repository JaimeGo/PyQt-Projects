from PyQt4 import QtGui, uic, QtCore
from sys import exit

formulario_1 = uic.loadUiType("puntajes.ui")


class DashboardPuntaje(formulario_1[0], formulario_1[1]):
    def __init__(self, cliente):
        super().__init__()

        self.cliente = cliente

        self.setupUi(self)

    def mostrar(self):
        self.hide()
        self.show()
