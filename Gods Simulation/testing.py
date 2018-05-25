import gui
from gui.kinds.human import Human
from gui.kinds.skull import Skull
from gui.kinds.orc import Orc
from gui.building import Building, Temple

from unidades import Guerrero, \
    Arquero, Mascota, Aldeano, Hero, \
    crear_guerrero_1, crear_guerrero_2, \
    crear_arquero_1, crear_arquero_2, \
    crear_mascota_1, crear_mascota_2

from movimiento import casi_igual, angulo_a_entidad, distancia, mover

from ataque import atacar, mas_cercano, muerte_1, muerte_2, \
    eliminar_aldeanos, ataque_cristian_1, ataque_cristian_2
from estadisticas import Estadisticas
from construir import construir_edificio_1, construir_edificio_2

import unittest


class TestMovimiento(unittest.TestCase):
    def setUp(self):
        guerrero_1_gui = Orc("warrior", pos=(1, 1), hp=50)
        self.guerrero = Guerrero(velocidad_mov=1.1,
                                 puntos_vida=50, puntos_daño=1, rango=5, gui=guerrero_1_gui)
        arquero_1_gui = Orc("archer", pos=(2, 1), hp=50)
        self.arquero = Arquero(velocidad_mov=1.1,
                               puntos_vida=50, puntos_daño=1, rango=5, gui=arquero_1_gui)

    def test_casi_igual(self):
        self.assertTrue(casi_igual(3, 4) == True)

    def test_angulo(self):
        self.assertEqual(angulo_a_entidad(self.arquero, self.arquero.gui.cord_x, self.arquero.gui.cord_y), 0)

    def test_distancia(self):
        self.assertEqual(distancia(self.arquero, self.guerrero), 1)

    def test_mover(self):
        mover(self.guerrero, self.arquero)

        self.assertTupleEqual((self.guerrero.gui.cord_x, self.guerrero.gui.cord_y), (2.1, 1))



class TestAtaque(unittest.TestCase):
    def setUp(self):
        guerrero_1_gui = Orc("warrior", pos=(1, 1), hp=50)
        self.guerrero = Guerrero(velocidad_mov=1.1,
                                 puntos_vida=50, puntos_daño=1, rango=5, gui=guerrero_1_gui)
        arquero_1_gui = Orc("archer", pos=(2, 1), hp=50)
        self.arquero = Arquero(velocidad_mov=1.1,
                               puntos_vida=50, puntos_daño=1, rango=5, gui=arquero_1_gui)


    def test_atacar(self):
        atacar(self.guerrero,self.arquero)
        self.assertEqual(self.arquero.puntos_vida,49)


Tsuite = unittest.TestSuite()
Tsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMovimiento))
Tsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAtaque))

unittest.TextTestRunner().run(Tsuite)
