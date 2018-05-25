from unidades import TanqueCirculo, TanqueGrande, TanqueGuiador, TanqueQuieto
from elementos import ParedDura, ParedBlanda
from random import choice, randint


def poblar_etapas(mainwindow, num_etapa):
    if num_etapa == 1:
        quieto_1 = TanqueQuieto(mainwindow, (300, 500), "arriba")
        guiador_1 = TanqueGuiador(mainwindow, (400, 300))
        mainwindow.lista_enemigos.append(quieto_1)
        mainwindow.lista_enemigos.append(guiador_1)

    if num_etapa == 2:
        quieto_1 = TanqueQuieto(mainwindow, (300, 500), "derecha")
        guiador_1 = TanqueGuiador(mainwindow, (400, 100))
        guiador_2 = TanqueGuiador(mainwindow, (400, 500))

        pared_blanda_1 = ParedBlanda(mainwindow, (200, 300))
        pared_blanda_2 = ParedBlanda(mainwindow, (230, 300))
        pared_blanda_3 = ParedBlanda(mainwindow, (260, 300))

        mainwindow.lista_enemigos.append(quieto_1)
        mainwindow.lista_enemigos.append(guiador_1)
        mainwindow.lista_enemigos.append(guiador_2)

        mainwindow.lista_paredes_blandas.append(pared_blanda_1)
        mainwindow.lista_paredes_blandas.append(pared_blanda_2)
        mainwindow.lista_paredes_blandas.append(pared_blanda_3)

    if num_etapa == 3:
        quieto_1 = TanqueQuieto(mainwindow, (450, 350), "izquierda")
        quieto_2 = TanqueQuieto(mainwindow, (300, 100), "abajo")
        guiador_1 = TanqueGuiador(mainwindow, (400, 300))
        guiador_2 = TanqueGuiador(mainwindow, (400, 300))
        circulo_1 = TanqueCirculo(mainwindow, (150, 350))

        pared_dura_1 = ParedDura(mainwindow, (100, 200))
        pared_dura_2 = ParedDura(mainwindow, (130, 200))
        pared_dura_3 = ParedDura(mainwindow, (160, 200))

        mainwindow.lista_enemigos.append(quieto_1)
        mainwindow.lista_enemigos.append(quieto_2)

        mainwindow.lista_enemigos.append(guiador_1)
        mainwindow.lista_enemigos.append(guiador_2)

        mainwindow.lista_enemigos.append(circulo_1)

        mainwindow.lista_paredes_duras.append(pared_dura_1)
        mainwindow.lista_paredes_duras.append(pared_dura_2)
        mainwindow.lista_paredes_duras.append(pared_dura_3)

    if num_etapa == 4:
        guiador_1 = TanqueGuiador(mainwindow, (400, 200))
        guiador_2 = TanqueGuiador(mainwindow, (500, 280))
        guiador_3 = TanqueGuiador(mainwindow, (400, 100))
        circulo_1 = TanqueCirculo(mainwindow, (200, 380))
        circulo_2 = TanqueCirculo(mainwindow, (150, 380))

        pared_dura_1 = ParedDura(mainwindow, (100, 170))
        pared_dura_2 = ParedDura(mainwindow, (100, 200))

        pared_blanda_1 = ParedBlanda(mainwindow, (200, 300))
        pared_blanda_2 = ParedBlanda(mainwindow, (230, 300))
        pared_blanda_3 = ParedBlanda(mainwindow, (260, 300))

        mainwindow.lista_enemigos.append(guiador_1)
        mainwindow.lista_enemigos.append(guiador_2)
        mainwindow.lista_enemigos.append(guiador_3)

        mainwindow.lista_enemigos.append(circulo_1)
        mainwindow.lista_enemigos.append(circulo_2)

        mainwindow.lista_paredes_duras.append(pared_dura_1)
        mainwindow.lista_paredes_duras.append(pared_dura_2)

        mainwindow.lista_paredes_blandas.append(pared_blanda_1)
        mainwindow.lista_paredes_blandas.append(pared_blanda_2)
        mainwindow.lista_paredes_blandas.append(pared_blanda_3)

    if num_etapa == 5:
        quieto_1 = TanqueQuieto(mainwindow, (60, 60), "abajo")
        quieto_2 = TanqueQuieto(mainwindow, (500, 400), "izquierda")
        quieto_3 = TanqueQuieto(mainwindow, (500, 60), "abajo")

        guiador_1 = TanqueGuiador(mainwindow, (300, 60))
        guiador_2 = TanqueGuiador(mainwindow, (400, 250))
        guiador_3 = TanqueGuiador(mainwindow, (300, 200))

        circulo_1 = TanqueCirculo(mainwindow, (150, 380))
        circulo_2 = TanqueCirculo(mainwindow, (250, 380))

        pared_dura_1 = ParedDura(mainwindow, (100, 200))
        pared_dura_2 = ParedDura(mainwindow, (100, 230))

        pared_blanda_1 = ParedBlanda(mainwindow, (200, 300))
        pared_blanda_2 = ParedBlanda(mainwindow, (230, 300))
        pared_blanda_3 = ParedBlanda(mainwindow, (260, 300))

        pared_blanda_4 = ParedBlanda(mainwindow, (380, 300))
        pared_blanda_5 = ParedBlanda(mainwindow, (410, 300))

        mainwindow.lista_enemigos.append(quieto_1)
        mainwindow.lista_enemigos.append(quieto_2)
        mainwindow.lista_enemigos.append(quieto_3)

        mainwindow.lista_enemigos.append(guiador_1)
        mainwindow.lista_enemigos.append(guiador_2)
        mainwindow.lista_enemigos.append(guiador_3)

        mainwindow.lista_enemigos.append(circulo_1)
        mainwindow.lista_enemigos.append(circulo_2)

        mainwindow.lista_paredes_duras.append(pared_dura_1)
        mainwindow.lista_paredes_duras.append(pared_dura_2)

        mainwindow.lista_paredes_blandas.append(pared_blanda_1)
        mainwindow.lista_paredes_blandas.append(pared_blanda_2)
        mainwindow.lista_paredes_blandas.append(pared_blanda_3)
        mainwindow.lista_paredes_blandas.append(pared_blanda_4)
        mainwindow.lista_paredes_blandas.append(pared_blanda_5)

    if num_etapa == 6:
        tanque_grande_1 = TanqueGrande(mainwindow, (400, 150))

        pared_dura_1 = ParedDura(mainwindow, (100, 400))
        pared_dura_2 = ParedDura(mainwindow, (100, 430))

        pared_dura_3 = ParedDura(mainwindow, (430, 300))
        pared_dura_4 = ParedDura(mainwindow, (460, 300))
        pared_dura_5 = ParedDura(mainwindow, (490, 300))

        pared_blanda_1 = ParedBlanda(mainwindow, (200, 400))
        pared_blanda_2 = ParedBlanda(mainwindow, (230, 400))
        pared_blanda_3 = ParedBlanda(mainwindow, (260, 400))

        mainwindow.lista_enemigos.append(tanque_grande_1)

        mainwindow.lista_paredes_duras.append(pared_dura_1)
        mainwindow.lista_paredes_duras.append(pared_dura_2)
        mainwindow.lista_paredes_duras.append(pared_dura_3)
        mainwindow.lista_paredes_duras.append(pared_dura_4)
        mainwindow.lista_paredes_duras.append(pared_dura_5)

        mainwindow.lista_paredes_blandas.append(pared_blanda_1)
        mainwindow.lista_paredes_blandas.append(pared_blanda_2)
        mainwindow.lista_paredes_blandas.append(pared_blanda_3)

    if num_etapa == 7:
        quieto_1 = TanqueQuieto(mainwindow, (330, 500), "arriba")

        guiador_1 = TanqueGuiador(mainwindow, (400, 450))

        tanque_grande_1 = TanqueGrande(mainwindow, (300, 100))

        pared_blanda_1 = ParedBlanda(mainwindow, (200, 300))
        pared_blanda_2 = ParedBlanda(mainwindow, (230, 300))
        pared_blanda_3 = ParedBlanda(mainwindow, (260, 300))

        pared_blanda_4 = ParedBlanda(mainwindow, (400, 100))
        pared_blanda_5 = ParedBlanda(mainwindow, (430, 100))

        pared_blanda_6 = ParedBlanda(mainwindow, (100, 400))
        pared_blanda_7 = ParedBlanda(mainwindow, (130, 400))
        pared_blanda_8 = ParedBlanda(mainwindow, (160, 400))

        mainwindow.lista_enemigos.append(quieto_1)
        mainwindow.lista_enemigos.append(guiador_1)
        mainwindow.lista_enemigos.append(tanque_grande_1)

        mainwindow.lista_paredes_blandas.append(pared_blanda_1)
        mainwindow.lista_paredes_blandas.append(pared_blanda_2)
        mainwindow.lista_paredes_blandas.append(pared_blanda_3)
        mainwindow.lista_paredes_blandas.append(pared_blanda_4)
        mainwindow.lista_paredes_blandas.append(pared_blanda_5)
        mainwindow.lista_paredes_blandas.append(pared_blanda_6)
        mainwindow.lista_paredes_blandas.append(pared_blanda_7)
        mainwindow.lista_paredes_blandas.append(pared_blanda_8)

    if num_etapa == 8:
        quieto_1 = TanqueQuieto(mainwindow, (100, 100), "derecha")
        quieto_2 = TanqueQuieto(mainwindow, (500, 350), "izquierda")

        guiador_1 = TanqueGuiador(mainwindow, (400, 400))

        circulo_1 = TanqueCirculo(mainwindow, (150, 370))
        circulo_2 = TanqueCirculo(mainwindow, (110, 50))

        mainwindow.lista_enemigos.append(quieto_1)
        mainwindow.lista_enemigos.append(quieto_2)

        mainwindow.lista_enemigos.append(guiador_1)

        mainwindow.lista_enemigos.append(circulo_1)
        mainwindow.lista_enemigos.append(circulo_2)

        pared_dura_1 = ParedDura(mainwindow, (230, 200))
        pared_dura_2 = ParedDura(mainwindow, (260, 200))
        pared_dura_3 = ParedDura(mainwindow, (290, 200))

        pared_dura_4 = ParedDura(mainwindow, (300, 300))
        pared_dura_5 = ParedDura(mainwindow, (330, 300))

        pared_dura_6 = ParedDura(mainwindow, (400, 230))
        pared_dura_7 = ParedDura(mainwindow, (400, 260))
        pared_dura_8 = ParedDura(mainwindow, (400, 290))

        mainwindow.lista_paredes_duras.append(pared_dura_1)
        mainwindow.lista_paredes_duras.append(pared_dura_2)
        mainwindow.lista_paredes_duras.append(pared_dura_3)
        mainwindow.lista_paredes_duras.append(pared_dura_4)
        mainwindow.lista_paredes_duras.append(pared_dura_5)
        mainwindow.lista_paredes_duras.append(pared_dura_6)
        mainwindow.lista_paredes_duras.append(pared_dura_7)
        mainwindow.lista_paredes_duras.append(pared_dura_8)


def limpiar_etapa(mainwindow):
    for pared in mainwindow.lista_paredes_blandas:
        pared.hide()

    for pared in mainwindow.lista_paredes_duras:
        pared.hide()

    for elemento in mainwindow.lista_elementos:
        elemento.hide()

    for bala in mainwindow.lista_balas_disparadas:
        bala.hide()

    for explosion in mainwindow.lista_explosiones:
        explosion.hide()

    mainwindow.cuantos_portales_disparados = 0
    mainwindow.tanque_principal.cord_x = 70
    mainwindow.tanque_principal.cord_y = 300
    mainwindow.lista_enemigos = []
    mainwindow.lista_paredes_duras = []
    mainwindow.lista_paredes_blandas = []
    mainwindow.lista_balas_disparadas = []
    mainwindow.lista_elementos = []
    mainwindow.lista_explosiones = []

    mainwindow.puntaje += (int(mainwindow.constantes["tiempo_limite"]) - round(mainwindow.tiempo_juego)) * int(
        mainwindow.constantes["puntaje_por_tiempo_extra"])
    mainwindow.puntaje += mainwindow.tanque_principal.cañon.salud * (int(mainwindow.constantes["puntaje_por_salud"]))
    mainwindow.tiempo_juego = 0
    mainwindow.puntaje += mainwindow.tanque_principal.cañon.salud
    mainwindow.tanque_principal.cañon.salud = 200
    mainwindow.tanque_principal.cañon.tiene_barra(200)

    for i in range(int(mainwindow.constantes["balas_nuevas_por_etapa"])):
        mainwindow.mis_balas.append("n")


def poblar_supervivencia(mainwindow):
    posibilidades = ["quieto", "circular", "guiador", "grande"]
    nuevo_tanque = choice(posibilidades)

    enemigo = None

    if nuevo_tanque == "quieto":
        orientacion = choice(["derecha", "izquierda", "abajo", "arriba"])
        enemigo = TanqueQuieto(mainwindow, (randint(70, 530), randint(70, 530)), orientacion)

    elif nuevo_tanque == "circular":
        enemigo = TanqueCirculo(mainwindow, (randint(150, 400), randint(150, 400)))

    elif nuevo_tanque == "guiador":
        enemigo = TanqueGuiador(mainwindow, (randint(70, 530), randint(70, 530)))

    elif nuevo_tanque == "grande":
        enemigo = TanqueGrande(mainwindow, (randint(70, 530), randint(70, 530)))

    mainwindow.lista_enemigos.append(enemigo)


def inicial_supervivencia(mainwindow):
    if not mainwindow.inicial_supervivencia_listo:
        pared_dura = ParedDura(mainwindow, (randint(70, 530), randint(70, 530)))

        pared_blanda = ParedBlanda(mainwindow, (randint(70, 530), randint(70, 530)))

        mainwindow.lista_paredes_blandas.append(pared_blanda)
        mainwindow.lista_paredes_duras.append(pared_dura)

        enemigo = TanqueGuiador(mainwindow, (randint(70, 530), randint(70, 530)))

        mainwindow.lista_enemigos.append(enemigo)
