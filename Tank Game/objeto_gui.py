


from PyQt4 import QtGui
from PyQt4.QtCore import Qt

style_barra = """
QProgressBar {

    margin-top: 3.4px;
}

QProgressBar::chunk {
    background-color: red;


}
"""

class ObjetoGui(QtGui.QWidget):
    def __init__(self,path_imagen,pos=(0,0),tamaño=(0,0),padre=None):
        super().__init__(padre)
        self.label=QtGui.QLabel(self)
        self.tamaño_x=tamaño[0]
        self.tamaño_y=tamaño[1]
        self.path_imagen=path_imagen
        self._cord_x=pos[0]
        self._cord_y=pos[1]
        self._salud_maxima = 100
        self.barra_salud = QtGui.QProgressBar(self)
        self.barra_salud.setValue(self._salud_maxima)
        self.barra_salud.setTextVisible(False)
        self.barra_salud.setMaximumSize(25, 5)
        self.barra_salud.hide()
        self.barra_salud.setStyleSheet(style_barra)

        self.alinear(Qt.AlignCenter)

        self.refrescar_pixmap()

        self.move(self._cord_x, self._cord_y)



    def refrescar_pixmap(self):
        self.pixmap = QtGui.QPixmap(self.path_imagen)

        if "up_left" in self.path_imagen or "up_right" in self.path_imagen or \
           "down_left" in self.path_imagen or "down_right" in self.path_imagen:
            self.pixmap = self.pixmap.scaled(self.tamaño_x+3,self.tamaño_y+3)
            self.label.setFixedSize(self.tamaño_x+3,self.tamaño_y+3)
        else:
            self.pixmap = self.pixmap.scaled(self.tamaño_x-5,self.tamaño_y-5)
            self.label.setFixedSize(self.tamaño_x-5,self.tamaño_y-5)

        self.label.setPixmap(self.pixmap)
        self.label.show()



    def cambiar_imagen(self,nuevo_path):
        self.path_imagen=nuevo_path
        self.refrescar_pixmap()

    def alinear(self,alineado):
        self.label.setAlignment(alineado)


    @property
    def angulo(self):
        return self._angulo

    @angulo.setter
    def angulo(self,angulo):
        self._angulo=angulo
        self.refrescar_pixmap()

    @property
    def cord_x(self):
        return self._cord_x

    @cord_x.setter
    def cord_x(self,cord):
        self._cord_x=cord
        self.move(self._cord_x,self._cord_y)


    @property
    def cord_y(self):
        return self._cord_y

    @cord_y.setter
    def cord_y(self,cord):
        self._cord_y=cord
        self.move(self._cord_x,self._cord_y)

    @property
    def salud(self):
        return self.barra_salud.value()

    @salud.setter
    def salud(self, puntos_vida):

        if puntos_vida > self._salud_maxima:
            puntos_vida = self._salud_maxima
        elif puntos_vida < 0:
            puntos_vida = 0
        self.barra_salud.setValue(puntos_vida)



    def tiene_barra(self,salud_maxima):
        self._salud_maxima=salud_maxima
        self.barra_salud.setValue(self._salud_maxima)
        self.barra_salud.show()




