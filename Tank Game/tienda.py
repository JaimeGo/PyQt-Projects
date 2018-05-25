from PyQt4 import uic, QtCore, QtGui

formulario = uic.loadUiType("ui_tienda.ui")


class Tienda(formulario[0], formulario[1]):
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        super().__init__()
        self.setupUi(self)
        self.pushButton_11.clicked.connect(self.se_continua)
        self.pushButton.clicked.connect(self.subir_fuerza)
        self.pushButton_2.clicked.connect(self.subir_resistencia)
        self.pushButton_3.clicked.connect(self.subir_vida)
        self.pushButton_4.clicked.connect(self.subir_velocidad)
        self.pushButton_5.clicked.connect(self.subir_velocidad_tiro)
        self.pushButton_6.clicked.connect(self.subir_radio_bomba)
        self.pushButton_8.clicked.connect(self.comprar_explosiva)
        self.pushButton_10.clicked.connect(self.comprar_ralentizante)
        self.pushButton_7.clicked.connect(self.comprar_penetrante)
        self.pushButton_9.clicked.connect(self.comprar_bomba)

        self.costo_fuerza = int(self.mainwindow.constantes["costo_fuerza_inicial"])
        self.costo_resistencia = int(self.mainwindow.constantes["costo_resistencia_inicial"])
        self.costo_vida = int(self.mainwindow.constantes["costo_vida_inicial"])
        self.costo_velocidad = int(self.mainwindow.constantes["costo_velocidad_inicial"])
        self.costo_velocidad_tiro = int(self.mainwindow.constantes["costo_vel_tiro_inicial"])
        self.costo_radio = int(self.mainwindow.constantes["costo_radio_inicial"])

    def refrescar_labels(self):
        self.label_2.setText("Subir Fuerza (" + str(self.costo_fuerza) + " p.)")
        self.label_3.setText("Subir Resistencia (" + str(self.costo_resistencia) + " p.)")
        self.label_4.setText("Subir Vida (" + str(self.costo_vida) + " p.)")
        self.label_5.setText("Subir Velocidad (" + str(self.costo_velocidad) + " p.)")
        self.label_6.setText("Subir Vel. de Tiro (" + str(self.costo_velocidad_tiro) + " p.)")
        self.label_7.setText("Subir radio de bomba (" + str(self.costo_radio) + " p.)")

    def closeEvent(self, event):
        self.se_continua()

    def se_continua(self):
        self.hide()
        self.mainwindow.pauseado = False
        self.mainwindow.tiempo_tienda = 3

    def subir_fuerza(self):
        if self.mainwindow.puntaje >= self.costo_fuerza:
            self.mainwindow.tanque_principal.fuerza += 0.1
            self.mainwindow.puntaje -= self.costo_fuerza
            self.costo_fuerza += int(self.mainwindow.constantes["aumento_costo_stats"])
            self.refrescar_labels()
            self.label_13.setText(str(self.mainwindow.puntaje))

    def subir_resistencia(self):
        if self.mainwindow.puntaje >= self.costo_resistencia:
            self.mainwindow.tanque_principal.resistencia += 0.1
            self.mainwindow.puntaje -= self.costo_resistencia
            self.costo_resistencia += int(self.mainwindow.constantes["aumento_costo_stats"])
            self.refrescar_labels()
            self.label_13.setText(str(self.mainwindow.puntaje))

    def subir_vida(self):
        if self.mainwindow.puntaje >= self.costo_vida:
            self.mainwindow.tanque_principal.vida += 2
            self.mainwindow.puntaje -= self.costo_vida
            self.costo_vida += int(self.mainwindow.constantes["aumento_costo_stats"])
            self.refrescar_labels()
            self.label_13.setText(str(self.mainwindow.puntaje))

    def subir_velocidad(self):
        if self.mainwindow.puntaje >= self.costo_velocidad:
            self.mainwindow.tanque_principal.velocidad_mov += 0.1
            self.mainwindow.puntaje -= self.costo_velocidad
            self.costo_velocidad += int(self.mainwindow.constantes["aumento_costo_stats"])
            self.refrescar_labels()
            self.label_13.setText(str(self.mainwindow.puntaje))

    def subir_velocidad_tiro(self):
        if self.mainwindow.puntaje >= self.costo_velocidad_tiro:
            self.mainwindow.tanque_principal.velocidad_tiro += 0.1
            self.mainwindow.puntaje -= self.costo_velocidad_tiro
            self.costo_velocidad_tiro += int(self.mainwindow.constantes["aumento_costo_stats"])
            self.refrescar_labels()
            self.label_13.setText(str(self.mainwindow.puntaje))

    def subir_radio_bomba(self):
        if self.mainwindow.puntaje >= self.costo_radio:
            self.mainwindow.tanque_principal.radio += 5
            self.mainwindow.puntaje -= self.costo_radio
            self.costo_radio += int(self.mainwindow.constantes["aumento_costo_stats"])
            self.refrescar_labels()
            self.label_13.setText(str(self.mainwindow.puntaje))

    def comprar_explosiva(self):
        if self.mainwindow.puntaje >= 50:
            self.mainwindow.mis_balas.append("e")
            self.mainwindow.puntaje -= 50
            self.label_13.setText(str(self.mainwindow.puntaje))

    def comprar_ralentizante(self):
        if self.mainwindow.puntaje >= 50:
            self.mainwindow.mis_balas.append("r")
            self.mainwindow.puntaje -= 50
            self.label_13.setText(str(self.mainwindow.puntaje))

    def comprar_penetrante(self):
        if self.mainwindow.puntaje >= 50:
            self.mainwindow.mis_balas.append("p")
            self.mainwindow.puntaje -= 50
            self.label_13.setText(str(self.mainwindow.puntaje))

    def comprar_bomba(self):
        if self.mainwindow.puntaje >= 100:
            self.mainwindow.mis_bombas += 1
            self.mainwindow.puntaje -= 100
            self.label_13.setText(str(self.mainwindow.puntaje))
