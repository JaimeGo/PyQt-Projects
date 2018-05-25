from etapas import poblar_etapas, poblar_supervivencia, inicial_supervivencia, limpiar_etapa
from elementos import crear_powerup
from tienda import Tienda
from sys import exit
from registro_puntaje import MenuRegistro

from PyQt4 import QtGui


def run(main_window):
    if main_window.modo == "survival":
        run_supervivencia(main_window)

    elif main_window.modo == "etapas":
        run_etapas(main_window)


def run_etapas(main_window):
    if not main_window.pauseado:

        main_window.tiempo_juego += 0.025
        main_window.refrescar_balas()

        main_window.refrescar_labels()

        if main_window.etapa_superada:
            poblar_etapas(main_window, main_window.etapa)
            main_window.etapa_superada = False

        if main_window.control == "mouse":
            main_window.tanque_principal.refrescar_imagen_total()

        else:
            main_window.tanque_principal.refrescar_cañon()

        main_window.tanque_principal.manejar_colision()

        for tanque_enemigo in main_window.lista_enemigos:
            tanque_enemigo.mover()
            tanque_enemigo.recuperar_velocidad()

            if tanque_enemigo.__class__.__name__ == "TanqueQuieto":
                tanque_enemigo.disparar_quieto()

            if round(main_window.tiempo_juego, 4) % 2 == 0:
                tanque_enemigo.disparar()

            if tanque_enemigo.salud == 0:
                main_window.lista_enemigos.remove(tanque_enemigo)
                tanque_enemigo.hide()
                crear_powerup(main_window, (tanque_enemigo.cord_x, tanque_enemigo.cord_y))
                main_window.puntaje += tanque_enemigo.recompensa

        for bala in main_window.lista_balas_disparadas:
            bala.mover_bala()
            bala.manejar_colision()

        for explosion in main_window.lista_explosiones:
            explosion.hacer_desaparer()

        for elemento in main_window.lista_elementos:
            elemento.manejar_colision()

        for bomba in main_window.lista_bombas:
            bomba.tick()

        for portal in main_window.lista_portales:
            portal.hacer_disponible()

        if main_window.tanque_principal.cord_x >= 450 and main_window.tanque_principal.cord_y >= 450 and main_window.tiempo_tienda <= 0:
            main_window.pauseado = True
            main_window.tienda.label_13.setText(str(main_window.puntaje))
            main_window.tienda.show()

        if main_window.tiempo_tienda > 0:
            main_window.tiempo_tienda -= 0.025

        if not main_window.lista_enemigos:
            limpiar_etapa(main_window)
            main_window.etapa += 1
            if main_window.etapa == 9:
                main_window.resultado = "gano"
                main_window.puntaje += int(main_window.constantes["recompensa_por_ganar"])
                main_window.se_acabo = True
            else:
                poblar_etapas(main_window, main_window.etapa)
                main_window.pauseado = True
                main_window.tienda.label_13.setText(str(main_window.puntaje))
                main_window.tienda.show()

        if main_window.tanque_principal.cañon.salud <= 0 or main_window.tiempo_juego >= int(
                main_window.constantes["tiempo_limite"]):
            main_window.resultado = "perdio"
            main_window.se_acabo = True

        if main_window.escudo:
            main_window.escudo.proteger()


def run_supervivencia(main_window):
    inicial_supervivencia(main_window)
    main_window.inicial_supervivencia_listo = True

    main_window.refrescar_balas()
    main_window.refrescar_labels()

    if not main_window.pauseado:
        main_window.tiempo_juego += 0.025

        modificador = 0.25 if round(main_window.tiempo_juego, 4) % 5 == 0 else 0

        main_window.parametro_aparicion -= modificador

        if main_window.parametro_aparicion <= 0.5:
            main_window.parametro_aparicion = 0.5
        if round(main_window.tiempo_juego, 4) % main_window.parametro_aparicion == 0:
            poblar_supervivencia(main_window)

        if main_window.control == "mouse":
            main_window.tanque_principal.refrescar_imagen_total()

        else:
            main_window.tanque_principal.refrescar_cañon()

        for tanque_enemigo in main_window.lista_enemigos:
            tanque_enemigo.mover()
            tanque_enemigo.recuperar_velocidad()

            if tanque_enemigo.__class__.__name__ == "TanqueQuieto":
                tanque_enemigo.disparar_quieto()

            if round(main_window.tiempo_juego, 4) % 2 == 0:
                tanque_enemigo.disparar()

            if tanque_enemigo.salud == 0:
                main_window.lista_enemigos.remove(tanque_enemigo)
                tanque_enemigo.hide()
                crear_powerup(main_window, (tanque_enemigo.cord_x, tanque_enemigo.cord_y))
                main_window.puntaje += tanque_enemigo.recompensa

        for bala in main_window.lista_balas_disparadas:
            bala.mover_bala()
            bala.manejar_colision()

        for explosion in main_window.lista_explosiones:
            explosion.hacer_desaparer()

        for elemento in main_window.lista_elementos:
            elemento.manejar_colision()

        for bomba in main_window.lista_bombas:
            bomba.tick()

        for portal in main_window.lista_portales:
            portal.hacer_disponible()

        main_window.tanque_principal.manejar_colision()

        if main_window.tanque_principal.cord_x >= 450 and main_window.tanque_principal.cord_y >= 450 and main_window.tiempo_tienda <= 0:
            main_window.pauseado = True
            main_window.tienda.label_13.setText(str(main_window.puntaje))
            main_window.tienda.show()

        if main_window.tiempo_tienda > 0:
            main_window.tiempo_tienda -= 0.025

        if main_window.escudo:
            main_window.escudo.proteger()

        if main_window.tanque_principal.cañon.salud <= 0:
            puntaje = main_window.puntaje
            main_window.hide()
            main_window.pauseado = True
            main_window.menu_registro = MenuRegistro(puntaje)
