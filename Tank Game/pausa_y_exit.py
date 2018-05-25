from PyQt4 import QtGui
from PyQt4 import QtCore
from sys import exit


def añadir_botones_funcionales(mainwindow):
    mainwindow.icono_exit = QtGui.QIcon("assets/botones/salir")
    mainwindow.icono_pause = QtGui.QIcon("assets/botones/pausa")

    mainwindow.boton_exit = QtGui.QPushButton('', mainwindow)
    mainwindow.boton_pause = QtGui.QPushButton('', mainwindow)

    mainwindow.boton_exit.setIcon(mainwindow.icono_exit)
    mainwindow.boton_pause.setIcon(mainwindow.icono_pause)

    mainwindow.boton_pause.setIconSize(QtCore.QSize(30, 30))
    mainwindow.boton_exit.setIconSize(QtCore.QSize(30, 30))

    mainwindow.boton_exit.setFixedSize(30, 30)
    mainwindow.boton_pause.setFixedSize(30, 30)

    style = "QPushButton { border-radius: 10px; }"

    mainwindow.boton_exit.setStyleSheet(style)
    mainwindow.boton_pause.setStyleSheet(style)

    mainwindow.boton_exit.move(570, 0)
    mainwindow.boton_pause.move(540, 0)

    def pause_clickeado():

        if not mainwindow.pauseado:
            mainwindow.pauseado = True

            mainwindow.icono_pause = QtGui.QIcon("assets/botones/continuar")

            mainwindow.boton_pause.setIcon(mainwindow.icono_pause)

        else:
            mainwindow.pauseado = False

            mainwindow.icono_pause = QtGui.QIcon("assets/botones/pausa")

            mainwindow.boton_pause.setIcon(mainwindow.icono_pause)

    def exit_clickeado():
        exit(0)

    mainwindow.boton_pause.clicked.connect(pause_clickeado)
    mainwindow.boton_exit.clicked.connect(exit_clickeado)
