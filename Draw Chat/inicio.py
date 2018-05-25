from servidor import Servidor
from cliente import Cliente
from threading import Thread
from PyQt4 import QtGui

numero_clientes = 3

pos_inicial = (400, 250)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    Servidor()
    for i in range(numero_clientes):
        Cliente(pos_inicial)
        pos_inicial = (pos_inicial[0] + 30, pos_inicial[1] - 30)

    app.exec_()
