
from PyQt5 import QtGui
from youtube_modifier import YtModifier

if __name__=="__main__":
    app = QtGui.QApplication([])

    yt_modifier=YtModifier()

    app.exec_()