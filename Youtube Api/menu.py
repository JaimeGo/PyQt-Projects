

from PyQt4 import QtGui, uic, QtCore
import json
import os


formulario_1 = uic.loadUiType("menu_inicial.ui")


class MenuInicial(formulario_1[0], formulario_1[1]):
    def __init__(self, dict_listas,yt_modifier):
        super().__init__()

        self.dict_listas=dict_listas

        self.yt_modifier=yt_modifier

        self.setupUi(self)

        self.pushButton.clicked.connect(self.crear_lista)

        self.pushButton_2.clicked.connect(self.comentar_video)

        self.pushButton_3.clicked.connect(self.estadisticas)

        self.seleccion_lista=SeleccionLista(self.dict_listas,self.yt_modifier,self)

        self.seleccion_datos=SeleccionDatos(self.dict_listas,self.yt_modifier,self)

        self.datos_video=DatosVideos(self.dict_listas,self.yt_modifier,self)

        self.comentario_inicial=ComentarioInicial(self.dict_listas,self.yt_modifier,self)

        self.comentario_final=ComentarioFinal(self.dict_listas,self.yt_modifier,self)

        self.seleccion_est=SeleccionListaEst(self.dict_listas,self.yt_modifier,self)

        self.parametros=Parametros(self.dict_listas,self.yt_modifier,self)

        self.estadisticas=Estadisticas(self.dict_listas,self.yt_modifier,self)


    def crear_lista(self):
        self.seleccion_lista.show()


    def comentar_video(self):
        self.comentario_inicial.actualizar()
        self.comentario_inicial.show()

    def estadisticas(self):
        self.seleccion_est.actualizar()
        self.seleccion_est.show()



    def closeEvent(self,e):
        os.remove("inicio.py-oauth2.json")








formulario_2 = uic.loadUiType("seleccion_lista.ui")


class SeleccionLista(formulario_2[0], formulario_2[1]):
    def __init__(self, dict_listas,yt_modifier,menu_inicial):
        super().__init__()

        self.dict_listas=dict_listas

        self.yt_modifier=yt_modifier

        self.menu_inicial=menu_inicial

        self.setupUi(self)


        self.lista_labels = []
        self.lista_entidades = []

        self.widget_1 = QtGui.QWidget()
        self.widget_1.setFixedSize(360,200)
        self.ultima_pos = (0, 0)

        self.scrollArea.setWidget(self.widget_1)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setEnabled(True)

        self.publicaciones = 0
        self.exceso_altura = 0


        self.pushButton.clicked.connect(self.continuar)

        self.actualizar()



    def continuar(self):


        for i in range(len(self.lista_entidades)):
            if self.lista_entidades[i].isChecked():
                self.yt_modifier.nombre_lista_elegida=self.lista_labels[i].text()

        self.yt_modifier.crear_lista_rep()
        self.yt_modifier.youtube_search()
        self.yt_modifier.añadir_a_lista()

        self.hide()
        self.menu_inicial.seleccion_datos.actualizar()
        self.menu_inicial.seleccion_datos.show()


    def actualizar(self):


        self.ultima_pos = (0, 0)
        self.publicaciones = 0
        self.exceso_altura = 0

        for label in self.lista_labels:
            label.setParent(None)
        for rb in self.lista_entidades:
            rb.setParent(None)

        self.lista_labels = []
        self.lista_entidades = []
        self.label_ocupado = None
        self.rb_ocupado = None

        for nombre, valor in self.dict_listas["playlists"].items():
            self.label_ocupado = QtGui.QLabel()

            self.rb_ocupado = QtGui.QRadioButton()


            self.label_ocupado.setText(nombre)

            self.label_ocupado.setParent(self.widget_1)

            self.rb_ocupado.setParent(self.widget_1)

            self.label_ocupado.move(self.ultima_pos[0], self.ultima_pos[1])
            self.label_ocupado.show()

            self.rb_ocupado.move(self.ultima_pos[0] + 250, self.ultima_pos[1])
            self.rb_ocupado.show()

            self.lista_labels.append(self.label_ocupado)
            self.lista_entidades.append(self.rb_ocupado)

            self.ultima_pos = (
                self.ultima_pos[0], self.ultima_pos[1] + 15)
            if self.publicaciones >= 12:
                self.exceso_altura += 15

            self.widget_1.setFixedSize(360,200 + self.exceso_altura)
            self.publicaciones += 1

            self.scrollArea.ensureVisible(0, 200 + self.exceso_altura)





formulario_3 = uic.loadUiType("seleccion_datos.ui")


class SeleccionDatos(formulario_3[0], formulario_3[1]):
    def __init__(self, dict_listas,yt_modifier,menu_inicial):
        super().__init__()

        self.dict_listas=dict_listas

        self.yt_modifier=yt_modifier

        self.menu_inicial = menu_inicial

        self.setupUi(self)


        self.lista_labels = []
        self.lista_entidades = []

        self.widget_1 = QtGui.QWidget()
        self.widget_1.setFixedSize(360,220)
        self.ultima_pos = (0, 0)

        self.scrollArea.setWidget(self.widget_1)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setEnabled(True)

        self.publicaciones = 0
        self.exceso_altura = 0


        self.pushButton.clicked.connect(self.continuar)




    def continuar(self):
        self.hide()
        for i in range(len(self.lista_entidades)):
            if self.lista_entidades[i].isChecked():
                lista_canciones=list(self.yt_modifier.dict_ids[self.yt_modifier.nombre_lista_elegida][self.yt_modifier.id_lista_elegida].keys())
                self.yt_modifier.video_comentario_elegido=(0,0,0,self.yt_modifier.dict_ids[self.yt_modifier.nombre_lista_elegida][self.yt_modifier.id_lista_elegida][lista_canciones[i]])
                self.yt_modifier.nombre_video_datos=lista_canciones[i]
        self.menu_inicial.datos_video.actualizar()
        self.menu_inicial.datos_video.show()


    def actualizar(self):


        self.ultima_pos = (0, 0)
        self.publicaciones = 0
        self.exceso_altura = 0

        for label in self.lista_labels:
            label.setParent(None)
        for rb in self.lista_entidades:
            rb.setParent(None)

        self.lista_labels = []
        self.lista_entidades = []
        self.label_ocupado = None
        self.rb_ocupado = None

        for nombre, valor in self.yt_modifier.dict_ids[self.yt_modifier.nombre_lista_elegida][self.yt_modifier.id_lista_elegida].items():
            self.label_ocupado = QtGui.QLabel()

            self.rb_ocupado = QtGui.QRadioButton()

            if len(nombre)<35:
                nuevo_nombre=nombre

            else:
                nuevo_nombre=nombre[:35]+"..."

            self.label_ocupado.setText(nuevo_nombre)

            self.label_ocupado.setParent(self.widget_1)

            self.rb_ocupado.setParent(self.widget_1)

            self.label_ocupado.move(self.ultima_pos[0], self.ultima_pos[1])
            self.label_ocupado.show()

            self.rb_ocupado.move(self.ultima_pos[0] + 310, self.ultima_pos[1])
            self.rb_ocupado.show()

            self.lista_labels.append(self.label_ocupado)
            self.lista_entidades.append(self.rb_ocupado)

            self.ultima_pos = (
                self.ultima_pos[0], self.ultima_pos[1] + 15)
            if self.publicaciones >= 12:
                self.exceso_altura += 15

            self.widget_1.setFixedSize(360,220 + self.exceso_altura)
            self.publicaciones += 1

            self.scrollArea.ensureVisible(0, 220 + self.exceso_altura)


formulario_4 = uic.loadUiType("datos_video.ui")


class DatosVideos(formulario_4[0], formulario_4[1]):
    def __init__(self, dict_listas,yt_modifier,menu_inicial):
        super().__init__()

        self.dict_listas=dict_listas

        self.yt_modifier=yt_modifier

        self.menu_inicial = menu_inicial

        self.setupUi(self)



        self.pushButton.clicked.connect(self.continuar)




    def continuar(self):
        self.hide()
        self.menu_inicial.comentario_final.show()


    def actualizar(self):
        self.label_5.setText("")
        self.label_3.setText("")
        self.lineEdit.setText("")
        self.label_3.setText(self.yt_modifier.nombre_video_datos)
        link="https://www.youtube.com/watch?v="
        link+=self.yt_modifier.video_comentario_elegido[3]

        self.lineEdit.setText(link)




formulario_5 = uic.loadUiType("comentario_inicial.ui")


class ComentarioInicial(formulario_5[0], formulario_5[1]):
    def __init__(self, dict_listas,yt_modifier,menu_inicial):
        super().__init__()

        self.dict_listas=dict_listas

        self.yt_modifier=yt_modifier

        self.menu_inicial = menu_inicial

        self.setupUi(self)


        self.lista_info=[]

        self.lista_labels=[]

        self.lista_entidades=[]



        self.widget_1 = QtGui.QWidget()
        self.widget_1.setFixedSize(360, 220)
        self.ultima_pos = (0, 0)

        self.scrollArea.setWidget(self.widget_1)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setEnabled(True)

        self.publicaciones = 0
        self.exceso_altura = 0

        self.pushButton.clicked.connect(self.continuar)


    def continuar(self):
        self.hide()

        for i in range(len(self.lista_entidades)):
            if self.lista_entidades[i].isChecked() and self.lista_info:
                self.yt_modifier.video_comentario_elegido=self.lista_info[i]
                self.yt_modifier.nombre_video_datos=self.yt_modifier.video_comentario_elegido[0]
                self.menu_inicial.datos_video.actualizar()
                self.menu_inicial.comentario_final.show()

    def actualizar(self):


        for nombre, dict_id in self.yt_modifier.dict_ids.items():

            self.label_lista = QtGui.QLabel()

            if len(nombre) < 35:
                nuevo_nombre_lista = nombre

            else:
                nuevo_nombre_lista = nombre[:35] + "..."

            self.label_lista.setText(nuevo_nombre_lista)

            self.label_lista.setParent(self.widget_1)

            self.label_lista.move(self.ultima_pos[0], self.ultima_pos[1])

            self.label_lista.show()

            self.lista_labels.append(self.label_lista)


            for id_lista,dict_varios_videos in dict_id.items():

                for nombre_video,id_video in dict_varios_videos.items():




                    self.label_video = QtGui.QLabel()

                    self.rb_ocupado = QtGui.QRadioButton()



                    if len(nombre_video) < 20:
                        nuevo_nombre_video = nombre_video

                    else:
                        nuevo_nombre_video = nombre_video[:20] + "..."




                    self.label_video.setText(nuevo_nombre_video)


                    self.label_video.setParent(self.widget_1)

                    self.rb_ocupado.setParent(self.widget_1)

                    self.label_video.move(self.ultima_pos[0]+130, self.ultima_pos[1])

                    self.label_video.show()

                    self.rb_ocupado.move(self.ultima_pos[0] + 320, self.ultima_pos[1])
                    self.rb_ocupado.show()


                    self.lista_labels.append(self.label_video)

                    self.lista_entidades.append(self.rb_ocupado)

                    self.ultima_pos = (
                        self.ultima_pos[0], self.ultima_pos[1] + 15)
                    if self.publicaciones >= 12:
                        self.exceso_altura += 15

                    self.widget_1.setFixedSize(360, 200 + self.exceso_altura)
                    self.publicaciones += 1

                    self.scrollArea.ensureVisible(0, 200 + self.exceso_altura)

                    self.lista_info.append((nombre,id_lista,nombre_video,id_video))





formulario_6 = uic.loadUiType("comentario_final.ui")


class ComentarioFinal(formulario_6[0], formulario_6[1]):
    def __init__(self, dict_listas,yt_modifier,menu_inicial):
        super().__init__()

        self.dict_listas=dict_listas

        self.yt_modifier=yt_modifier

        self.menu_inicial = menu_inicial

        self.setupUi(self)



        self.pushButton.clicked.connect(self.continuar)




    def continuar(self):
        self.yt_modifier.texto_comentario=self.textEdit.toPlainText()
        self.yt_modifier.insert_comment()

        self.menu_inicial.datos_video.label_5.setText("¡COMENTARIO REALIZADO!")
        self.menu_inicial.datos_video.actualizar()

        self.hide()
        self.menu_inicial.datos_video.show()





formulario_7 = uic.loadUiType("parametro_est.ui")


class Parametros(formulario_7[0], formulario_7[1]):
    def __init__(self, dict_listas,yt_modifier,menu_inicial):
        super().__init__()

        self.dict_listas=dict_listas

        self.yt_modifier=yt_modifier

        self.menu_inicial=menu_inicial

        self.setupUi(self)

        self.pushButton.clicked.connect(self.continuar)

    def continuar(self):
        if self.radioButton.isChecked():
            self.yt_modifier.parametro = "Comentarios"

        elif self.radioButton_2.isChecked():
            self.yt_modifier.parametro = "Likes"

        elif self.radioButton_3.isChecked():
            self.yt_modifier.parametro = "Dislikes"

        elif self.radioButton_4.isChecked():
            self.yt_modifier.parametro = "Reproducciones"

        self.yt_modifier.get_statistics()
        self.menu_inicial.estadisticas.actualizar()
        self.hide()
        self.menu_inicial.estadisticas.show()





formulario_8 = uic.loadUiType("mostrar_estadisticas.ui")


class Estadisticas(formulario_8[0], formulario_8[1]):
    def __init__(self, dict_listas,yt_modifier,menu_inicial):
        super().__init__()

        self.dict_listas=dict_listas

        self.yt_modifier=yt_modifier

        self.menu_inicial=menu_inicial

        self.setupUi(self)


    def actualizar(self):
        self.label_10.setText(self.yt_modifier.parametro)



        if self.yt_modifier.parametro=="Comentarios":
            lista_aux=list(sorted(self.yt_modifier.lista_resultados_stats,key=lambda x: int(x[4])))
            elegido_mayor=lista_aux[-1]
            elegido_menor=lista_aux[0]
            valor_mayor=elegido_mayor[4]
            valor_menor = elegido_menor[4]
        elif self.yt_modifier.parametro == "Likes":
            lista_aux = list(sorted(self.yt_modifier.lista_resultados_stats, key=lambda x: int(x[2])))
            elegido_mayor = lista_aux[-1]
            elegido_menor = lista_aux[0]
            valor_mayor = elegido_mayor[2]
            valor_menor = elegido_menor[2]
        elif self.yt_modifier.parametro == "Dislikes":
            lista_aux = list(sorted(self.yt_modifier.lista_resultados_stats, key=lambda x: int(x[3])))
            elegido_mayor = lista_aux[-1]
            elegido_menor = lista_aux[0]
            valor_mayor = elegido_mayor[3]
            valor_menor = elegido_menor[3]
        else:
            lista_aux = list(sorted(self.yt_modifier.lista_resultados_stats, key=lambda x: int(x[5])))
            elegido_mayor = lista_aux[-1]
            elegido_menor = lista_aux[0]
            valor_mayor = elegido_mayor[5]
            valor_menor = elegido_menor[5]

        self.label_11.setText(elegido_mayor[0])
        link = "https://www.youtube.com/watch?v="
        link+=elegido_mayor[1]
        self.lineEdit_2.setText(link)
        self.label_13.setText(str(valor_mayor))

        self.label_15.setText(elegido_menor[0])
        link = "https://www.youtube.com/watch?v="
        link += elegido_menor[1]
        self.lineEdit.setText(link)

        self.label_14.setText(str(valor_menor))








formulario_8 = uic.loadUiType("seleccion_lista_est.ui")


class SeleccionListaEst(formulario_8[0], formulario_8[1]):
    def __init__(self, dict_listas,yt_modifier,menu_inicial):
        super().__init__()

        self.dict_listas=dict_listas

        self.yt_modifier=yt_modifier

        self.menu_inicial=menu_inicial

        self.setupUi(self)

        self.lista_labels = []
        self.lista_entidades = []

        self.widget_1 = QtGui.QWidget()
        self.widget_1.setFixedSize(360, 200)
        self.ultima_pos = (0, 0)

        self.scrollArea.setWidget(self.widget_1)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setEnabled(True)

        self.publicaciones = 0
        self.exceso_altura = 0

        self.pushButton.clicked.connect(self.continuar)

        self.actualizar()

    def continuar(self):

        for i in range(len(self.lista_entidades)):
            if self.lista_entidades[i].isChecked():
                self.yt_modifier.nombre_lista_elegida = self.lista_labels[i].text()


        lista_ini=list(self.yt_modifier.dict_ids[self.yt_modifier.nombre_lista_elegida].values())
        lista_aux=list(lista_ini[0].values())

        self.yt_modifier.lista_ids_stats=lista_aux


        self.hide()

        self.menu_inicial.parametros.show()

    def actualizar(self):

        self.ultima_pos = (0, 0)
        self.publicaciones = 0
        self.exceso_altura = 0

        for label in self.lista_labels:
            label.setParent(None)
        for rb in self.lista_entidades:
            rb.setParent(None)

        self.lista_labels = []
        self.lista_entidades = []
        self.label_ocupado = None
        self.rb_ocupado = None

        for nombre, valor in self.yt_modifier.dict_ids.items():
            self.label_ocupado = QtGui.QLabel()

            self.rb_ocupado = QtGui.QRadioButton()

            self.label_ocupado.setText(nombre)

            self.label_ocupado.setParent(self.widget_1)

            self.rb_ocupado.setParent(self.widget_1)

            self.label_ocupado.move(self.ultima_pos[0], self.ultima_pos[1])
            self.label_ocupado.show()

            self.rb_ocupado.move(self.ultima_pos[0] + 250, self.ultima_pos[1])
            self.rb_ocupado.show()

            self.lista_labels.append(self.label_ocupado)
            self.lista_entidades.append(self.rb_ocupado)

            self.ultima_pos = (
                self.ultima_pos[0], self.ultima_pos[1] + 15)
            if self.publicaciones >= 12:
                self.exceso_altura += 15

            self.widget_1.setFixedSize(360, 200 + self.exceso_altura)
            self.publicaciones += 1

            self.scrollArea.ensureVisible(0, 200 + self.exceso_altura)

        if self.lista_entidades:

            self.lista_entidades[0].setChecked(True)