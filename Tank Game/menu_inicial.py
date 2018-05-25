from mainwindow import comenzar_main_window
from PyQt4 import uic, QtCore, QtGui

formulario_1 = uic.loadUiType("ui_menu_inicial.ui")
formulario_2 = uic.loadUiType("ui_resultado.ui")


class WidgetResultado(formulario_2[0], formulario_2[1]):
    def __init__(self, menu_inicial):
        super().__init__()
        self.setupUi(self)
        self.menu_inicial = menu_inicial
        self.pushButton.clicked.connect(self.salir)
        self.resultado = "None"
        self.puntaje = 0

    def refrescar_labels(self):
        if self.resultado == "gano":
            self.label.setText("¡Has ganado!")
        if self.resultado == "perdio":
            self.label.setText("Has perdido")

        self.label_2.setText("Tu puntaje fue: " + str(self.puntaje))

    def salir(self):
        self.hide()
        self.menu_inicial.show()


class MenuInicial(formulario_1[0], formulario_1[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.empezar_juego)

        self.modo = ""
        self.control = ""
        self.etapa = 1

        self.timer = QtCore.QTimer(self)

    def empezar_juego(self):
        if getattr(self, 'radioButton_1').isChecked():
            self.modo = "survival"

        if getattr(self, 'radioButton_2').isChecked():
            self.modo = "etapas"

        if getattr(self, 'radioButton_3').isChecked():
            self.control = "fijo"

        if getattr(self, 'radioButton_4').isChecked():
            self.control = "mouse"

        if getattr(self, 'radioButton_1i').isChecked():
            self.etapa = 1

        if getattr(self, 'radioButton_2i').isChecked():
            self.etapa = 2

        if getattr(self, 'radioButton_3i').isChecked():
            self.etapa = 3

        if getattr(self, 'radioButton_4i').isChecked():
            self.etapa = 4

        if getattr(self, 'radioButton_5i').isChecked():
            self.etapa = 5

        if getattr(self, 'radioButton_6i').isChecked():
            self.etapa = 6

        if getattr(self, 'radioButton_7i').isChecked():
            self.etapa = 7

        if getattr(self, 'radioButton_8i').isChecked():
            self.etapa = 8

        self.hide()

        self.mainwindow = comenzar_main_window(self.modo, self.control, self.etapa)

        self.widget_resultado = WidgetResultado(self)

        self.timer.timeout.connect(self.run)
        self.timer.start(25)

        self.seguir = True

    def run(self):
        if self.mainwindow.se_acabo and self.seguir:
            self.mainwindow.hide()
            self.widget_resultado.resultado = self.mainwindow.resultado
            self.widget_resultado.puntaje = self.mainwindow.puntaje
            self.widget_resultado.refrescar_labels()
            self.widget_resultado.show()
            self.seguir = False
