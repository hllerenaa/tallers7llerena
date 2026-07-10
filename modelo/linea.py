"""
modelo/linea.py
=====================
El MODELO: aqui solo definimos QUE es una linea de texto en el archivo y como saber si una
linea es valida. Nada mas: no pide datos ni muestra menus.
"""

class Linea:
    def __init__(self, nombre, orden):
        self.nombre = nombre
        self.orden = orden
