from PyQt4 import QtGui, uic, QtCore

formulario_1 = uic.loadUiType("historial.ui")


class Historial(formulario_1[0], formulario_1[1]):
    def __init__(self, cliente):
        super().__init__()

        self.cliente = cliente

        self.setupUi(self)

        self.widget_1 = QtGui.QWidget()

        self.widget_1.setFixedSize(290, 150)

        self.ultima_pos = (0, 0)

        self.scrollArea.setWidget(self.widget_1)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setEnabled(True)

        self.publicaciones = 0
        self.exceso_altura = 0

        self.lista_labels = []

    def actualizar(self):
        partida = self.cliente.lista_historial[0]
        ronda = self.cliente.lista_historial[1]
        participantes = self.cliente.lista_historial[2]
        ganadores = self.cliente.lista_historial[3]

        self.un_label_1 = QtGui.QLabel()

        self.un_label_1.setText(partida + "/" + ronda)

        self.un_label_1.setParent(self.widget_1)

        self.un_label_2 = QtGui.QLabel()

        self.un_label_2.setText(participantes)

        self.un_label_2.setParent(self.widget_1)

        self.un_label_3 = QtGui.QLabel()

        self.un_label_3.setText(ganadores)

        self.un_label_3.setParent(self.widget_1)

        self.un_label_4 = QtGui.QLabel()

        self.un_label_4.setText("-")

        self.un_label_4.setParent(self.widget_1)

        self.un_label_1.move(self.ultima_pos[0], self.ultima_pos[1])

        self.un_label_1.show()

        self.un_label_2.move(self.ultima_pos[0] + 100, self.ultima_pos[1])

        self.un_label_2.show()

        self.un_label_3.move(self.ultima_pos[0] + 190, self.ultima_pos[1])

        self.un_label_3.show()

        self.un_label_4.move(self.ultima_pos[0] + 270, self.ultima_pos[1])

        self.un_label_4.show()

        self.lista_labels.append(self.un_label_1)
        self.lista_labels.append(self.un_label_2)
        self.lista_labels.append(self.un_label_3)
        self.lista_labels.append(self.un_label_4)

        self.ultima_pos = (
            self.ultima_pos[0], self.ultima_pos[1] + 15)
        if self.publicaciones >= 9:
            self.exceso_altura += 15

        self.widget_1.setFixedSize(380, 180 + self.exceso_altura)
        self.publicaciones += 1

        self.scrollArea.ensureVisible(0, 180 + self.exceso_altura)
