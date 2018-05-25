from PyQt4 import QtGui, uic, QtCore


class Curva(QtGui.QGraphicsItem):
    def __init__(self, pen, primer_punto, segundo_punto):
        super().__init__(None, None)
        self.primer_punto = primer_punto
        self.segundo_punto = segundo_punto
        self.punto_intermedio_1 = QtCore.QPointF((primer_punto.x() + segundo_punto.x()) / 2 - 10,
                                                 (primer_punto.y() + segundo_punto.y()) / 2 - 20)
        self.punto_intermedio_2 = QtCore.QPointF((primer_punto.x() + segundo_punto.x()) / 2 + 10,
                                                 (primer_punto.y() + segundo_punto.y()) / 2 - 20)
        self.pen = pen
        self.path = QtGui.QPainterPath()
        self.path.moveTo(self.primer_punto)
        self.path.cubicTo(self.punto_intermedio_1.x(), self.punto_intermedio_1.y(), self.punto_intermedio_2.x(),
                          self.punto_intermedio_2.y(), self.segundo_punto.x(), self.segundo_punto.y())
        self.palabra = None

    def boundingRect(self):
        return self.path.boundingRect()

    def paint(self, painter, option, widget):
        painter.setPen(self.pen.color())
        painter.setBrush(self.pen.color())
        painter.strokePath(self.path, painter.pen())
