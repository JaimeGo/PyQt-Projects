from PyQt4 import uic, QtCore, QtGui
import operator

formulario_1 = uic.loadUiType("ui_widget_display.ui")

formulario_2 = uic.loadUiType("ui_registro_puntaje.ui")


class DisplayPuntaje(formulario_1[0], formulario_1[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        dicc_puntaje = {}

        lista_principal = [["None", "None"] for i in range(10)]

        with open("puntajes_anteriores.txt") as archivo:
            for linea in archivo.readlines():
                lista_linea = linea.strip().split(",")
                dicc_puntaje.update({lista_linea[0]: lista_linea[1]})

        lista_tuplas_sorteadas = sorted(dicc_puntaje.items(), key=operator.itemgetter(1), reverse=True)

        min = len(lista_tuplas_sorteadas) if len(lista_tuplas_sorteadas) <= 10 else 10

        for i in range(min):
            lista_principal[i][0] = lista_tuplas_sorteadas[i][0]
            lista_principal[i][1] = lista_tuplas_sorteadas[i][1]

        self.label_12.setText(lista_principal[0][1])
        self.label_13.setText(lista_principal[1][1])
        self.label_14.setText(lista_principal[2][1])
        self.label_15.setText(lista_principal[3][1])
        self.label_16.setText(lista_principal[4][1])
        self.label_17.setText(lista_principal[5][1])
        self.label_18.setText(lista_principal[6][1])
        self.label_19.setText(lista_principal[7][1])
        self.label_20.setText(lista_principal[8][1])
        self.label_21.setText(lista_principal[9][1])

        self.label_22.setText(lista_principal[0][0])
        self.label_23.setText(lista_principal[1][0])
        self.label_24.setText(lista_principal[2][0])
        self.label_25.setText(lista_principal[3][0])
        self.label_26.setText(lista_principal[4][0])
        self.label_27.setText(lista_principal[5][0])
        self.label_28.setText(lista_principal[6][0])
        self.label_29.setText(lista_principal[7][0])
        self.label_30.setText(lista_principal[8][0])
        self.label_31.setText(lista_principal[9][0])


class MenuRegistro(formulario_2[0], formulario_2[1]):
    def __init__(self, puntaje):
        super().__init__()
        self.setupUi(self)
        self.puntaje = puntaje

        self.pushButton.clicked.connect(self.continuar)
        self.label_3.setText(str(self.puntaje))

        self.show()

    def continuar(self):
        nombre = self.lineEdit.text()
        with open("puntajes_anteriores.txt", "a+") as archivo:
            archivo.write("\n" + nombre + "," + str(self.puntaje))

        self.hide()
        self.display = DisplayPuntaje()
        self.display.show()
