from mainwindow import comenzar_main_window
from PyQt4 import uic, QtCore, QtGui
from menu_inicial import MenuInicial

if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = MenuInicial()
    form.show()
    app.exec_()
