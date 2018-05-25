from PyQt4 import QtGui
from mini_chat import SeleccionAmigos

if __name__ == "__main__":
    app = QtGui.QApplication([])
    a = SeleccionAmigos("indl", 1,
                        ["juan", "pedro", "diego", "a", "juan", "pedro", "diego", "a", "juan", "pedro", "diego", "a"])
    a.show()

    app.exec_()
