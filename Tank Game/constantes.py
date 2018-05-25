class Constantes:
    def __init__(self):
        self.diccionario = {}
        with open("constantes.txt") as archivo:
            for linea in archivo.readlines():
                lista_linea = linea.strip().split("=")
                self.diccionario.update({lista_linea[0]: lista_linea[1]})
