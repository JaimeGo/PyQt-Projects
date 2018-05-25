from PyQt4 import QtGui, uic, QtCore

formulario_1 = uic.loadUiType("seleccion_amigos.ui")


class SeleccionAmigos(formulario_1[0], formulario_1[1]):
    def __init__(self, ind_o_grup, cliente):
        super().__init__()

        self.ind_o_grup = ind_o_grup

        self.cliente = cliente

        self.setupUi(self)

        self.lista_amigos = []

        self.lista_labels = []
        self.lista_entidades = []

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

        self.mini_chat_grup = MiniChatGrupal(self.cliente)
        self.mini_chat_ind = MiniChatInd(self.cliente)

        self.pushButton.clicked.connect(self.enviar)

        self.pushButton_2.clicked.connect(self.amigo_desde_seleccion)

    def amigo_desde_seleccion(self):
        self.cliente.menu.chat_grupal.usuario_amigo = self.lineEdit.text()
        self.cliente.menu.chat_grupal.hacer_amigo()
        self.actualizar()

    def enviar(self):
        lista_chateadores = []
        for i in range(len(self.lista_entidades)):
            if self.lista_entidades[i].isChecked():
                lista_chateadores.append(self.lista_amigos[i])

        self.cliente.lista_en_minichat = lista_chateadores
        self.hide()
        if self.ind_o_grup == "ind":
            self.mini_chat_ind.show()

        else:
            self.mini_chat_grup.show()

    def actualizar(self):
        self.lista_amigos = self.cliente.menu.chat_grupal.lista_amigos

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

        for amigo in self.lista_amigos:
            self.label_ocupado = QtGui.QLabel()
            self.rb_ocupado = None
            if self.ind_o_grup == "ind":
                self.rb_ocupado = QtGui.QRadioButton()

            else:
                self.rb_ocupado = QtGui.QCheckBox()

            self.label_ocupado.setText(amigo)

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
            if self.publicaciones >= 9:
                self.exceso_altura += 15

            self.widget_1.setFixedSize(290, 150 + self.exceso_altura)
            self.publicaciones += 1

            self.scrollArea.ensureVisible(0, 150 + self.exceso_altura)


formulario_2 = uic.loadUiType("chat_individual.ui")


class MiniChatInd(formulario_2[0], formulario_2[1]):
    def __init__(self, cliente):
        super().__init__()

        self.cliente = cliente

        self.setupUi(self)

        self.lista_amigos = []

        self.lista_labels = []
        self.lista_entidades = []

        self.widget_1 = QtGui.QWidget()
        self.widget_1.setFixedSize(210, 140)
        self.ultima_pos = (0, 0)

        self.scrollArea.setWidget(self.widget_1)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setEnabled(True)

        self.publicaciones = 0
        self.exceso_altura = 0

        self.pushButton.clicked.connect(self.enviar)
        self.pushButton_2.clicked.connect(self.enviar_mensajeria)

        print(self.scrollArea.width())
        print(self.scrollArea.height())

    def publicar_chat(self, mensaje):

        self.label_ocupado_1 = QtGui.QLabel()
        self.label_ocupado_2 = QtGui.QLabel()

        usuario = mensaje[:mensaje.find(":")]
        nuevo_mensaje = mensaje[mensaje.find(":") + 1:]

        lista_mensaje = [usuario, nuevo_mensaje]

        if lista_mensaje[1].strip() == ":)":
            self.label_ocupado_1.setText(lista_mensaje[0] + ":")
            self.label_ocupado_2.setPixmap(QtGui.QPixmap("emojis/sonrisa").scaled(15, 15))


        elif lista_mensaje[1].strip() == ":(":
            self.label_ocupado_1.setText(lista_mensaje[0] + ":")
            self.label_ocupado_2.setPixmap(QtGui.QPixmap("emojis/triste").scaled(15, 15))

        elif lista_mensaje[1].strip() == ":o":
            self.label_ocupado_1.setText(lista_mensaje[0] + ":")
            self.label_ocupado_2.setPixmap(QtGui.QPixmap("emojis/sorpresa").scaled(20, 20))

        elif lista_mensaje[1].strip() == "-_-":
            self.label_ocupado_1.setText(lista_mensaje[0] + ":")
            self.label_ocupado_2.setPixmap(QtGui.QPixmap("emojis/impasible").scaled(20, 20))

        else:
            self.label_ocupado_1.setText(lista_mensaje[0] + ":")
            self.label_ocupado_2.setText(lista_mensaje[1])

        self.label_ocupado_1.setParent(self.widget_1)
        self.label_ocupado_2.setParent(self.widget_1)

        self.label_ocupado_1.move(self.ultima_pos[0], self.ultima_pos[1])
        self.label_ocupado_2.show()

        self.label_ocupado_2.move(self.ultima_pos[0] + 7 * len(lista_mensaje[0]),
                                  self.ultima_pos[1])
        self.label_ocupado_1.show()

        self.lista_entidades.append(self.label_ocupado_1)
        self.lista_entidades.append(self.label_ocupado_2)

        self.ultima_pos = (
            self.ultima_pos[0], self.ultima_pos[1] + 15)
        if self.publicaciones >= 9:
            self.exceso_altura += 15

        self.widget_1.setFixedSize(210, 140 + self.exceso_altura)
        self.publicaciones += 1

        self.scrollArea.ensureVisible(0, 140 + self.exceso_altura)

    def enviar(self):
        mensaje = self.lineEdit_2.text()
        self.publicar_chat(self.cliente.usuario + ": " + mensaje)
        self.cliente.chatear_desde_minichat(self.cliente.usuario + ":::" + "ind" + ":::" + mensaje)

    def enviar_mensajeria(self):
        texto = self.plainTextEdit.toPlainText()
        destino = ","
        mensaje_total = texto
        mensaje_total += ":::" + destino.join(self.cliente.lista_en_minichat) + ":::" + "ind"

        self.cliente.send_message_to_server("texto_minichat:::" + mensaje_total)

    def publicar_texto(self, mensaje):
        self.plainTextEdit.setPlainText(mensaje)


formulario_3 = uic.loadUiType("mini_chat_grupal.ui")


class MiniChatGrupal(formulario_3[0], formulario_3[1]):
    def __init__(self, cliente):
        super().__init__()

        self.cliente = cliente

        self.setupUi(self)

        self.lista_amigos = []

        self.lista_labels = []
        self.lista_entidades = []

        self.widget_1 = QtGui.QWidget()
        self.widget_1.setFixedSize(210, 140)
        self.ultima_pos = (0, 0)

        self.scrollArea.setWidget(self.widget_1)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setEnabled(True)

        self.publicaciones = 0
        self.exceso_altura = 0

        self.pushButton.clicked.connect(self.enviar)
        self.pushButton_2.clicked.connect(self.enviar_mensajeria)

    def publicar_chat(self, mensaje):

        self.label_ocupado_1 = QtGui.QLabel()
        self.label_ocupado_2 = QtGui.QLabel()

        usuario = mensaje[:mensaje.find(":")]
        nuevo_mensaje = mensaje[mensaje.find(":") + 1:]

        lista_mensaje = [usuario, nuevo_mensaje]
        print(lista_mensaje[1].strip())
        if lista_mensaje[1].strip() == ":)":
            self.label_ocupado_1.setText(lista_mensaje[0] + ":")
            self.label_ocupado_2.setPixmap(QtGui.QPixmap("emojis/sonrisa").scaled(15, 15))
            print("hasta aqui llega")

        elif lista_mensaje[1].strip() == ":(":
            self.label_ocupado_1.setText(lista_mensaje[0] + ":")
            self.label_ocupado_2.setPixmap(QtGui.QPixmap("emojis/triste").scaled(15, 15))

        elif lista_mensaje[1].strip() == ":o":
            self.label_ocupado_1.setText(lista_mensaje[0] + ":")
            self.label_ocupado_2.setPixmap(QtGui.QPixmap("emojis/sorpresa").scaled(20, 20))

        elif lista_mensaje[1].strip() == "-_-":
            self.label_ocupado_1.setText(lista_mensaje[0] + ":")
            self.label_ocupado_2.setPixmap(QtGui.QPixmap("emojis/impasible").scaled(20, 20))

        else:
            self.label_ocupado_1.setText(lista_mensaje[0] + ":")
            self.label_ocupado_2.setText(lista_mensaje[1])

        self.label_ocupado_1.setParent(self.widget_1)
        self.label_ocupado_2.setParent(self.widget_1)

        self.label_ocupado_1.move(self.ultima_pos[0], self.ultima_pos[1])
        self.label_ocupado_2.show()

        self.label_ocupado_2.move(self.ultima_pos[0] + 7 * len(lista_mensaje[0]),
                                  self.ultima_pos[1])
        self.label_ocupado_1.show()

        self.lista_entidades.append(self.label_ocupado_1)
        self.lista_entidades.append(self.label_ocupado_2)

        self.ultima_pos = (
            self.ultima_pos[0], self.ultima_pos[1] + 15)
        if self.publicaciones >= 9:
            self.exceso_altura += 15

        self.widget_1.setFixedSize(210, 140 + self.exceso_altura)
        self.publicaciones += 1

        self.scrollArea.ensureVisible(0, 140 + self.exceso_altura)

    def enviar(self):
        mensaje = self.lineEdit_2.text()
        self.publicar_chat(self.cliente.usuario + ": " + mensaje)
        self.cliente.chatear_desde_minichat(self.cliente.usuario + ":::" + "grup" + ":::" + mensaje)

    def enviar_mensajeria(self):
        texto = self.plainTextEdit.toPlainText()
        destino = ","
        mensaje_total = texto
        mensaje_total += ":::" + destino.join(self.cliente.lista_en_minichat) + ":::" + "grup"

        self.cliente.send_message_to_server("texto_minichat:::" + mensaje_total)

    def publicar_texto(self, mensaje):
        self.plainTextEdit.setPlainText(mensaje)

    def empezar_partida(self):
        self.hide()
        self.cliente.chat_grupal.hide()
        self.cliente.sala = "sala_3:::"
        self.cliente.send_message_to_server("partida_grupal_con:" + ",".join(self.cliente.lista_en_minichat))
        self.cliente.chat_grupal.show()
