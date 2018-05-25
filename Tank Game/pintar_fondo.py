from PyQt4 import QtGui


class PintarFondo:
    def __init__(self):
        self.cantidad_tiles = 20

    def pintar_paredes(self, pared, fondo, height_ventana, width_ventana):

        fondo = fondo.scaled(width_ventana, height_ventana)

        width_pared = round(width_ventana / self.cantidad_tiles)
        height_pared = round(height_ventana / self.cantidad_tiles)

        pared = pared.scaled(width_pared, height_pared)

        tienda = QtGui.QImage("assets/fondo/tienda")
        tienda = tienda.scaled(120, 120)

        cargador = QtGui.QImage("assets/fondo/cargador_balas")
        cargador = cargador.scaled(22, 90)

        painter = QtGui.QPainter()

        painter.begin(fondo)

        for i in range(self.cantidad_tiles):
            painter.drawImage(pared.width() * i, 0, pared)

        for i in range(self.cantidad_tiles):
            painter.drawImage(pared.width() * i, (self.cantidad_tiles - 1) * height_pared, pared)

        for i in range(self.cantidad_tiles):
            painter.drawImage(0, i * pared.height(), pared)

        for i in range(self.cantidad_tiles):
            painter.drawImage((self.cantidad_tiles - 1) * width_pared, i * pared.height(), pared)

        painter.drawImage(450, 450, tienda)

        painter.drawImage(4, 470, cargador)

        painter.end()

        nuevo_fondo = QtGui.QPixmap.fromImage(fondo)

        return nuevo_fondo
