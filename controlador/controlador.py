"""
controlador/controlador.py
=========================
El CONTROLADOR: solo se encarga de GUARDAR y LEER las lineas en el
archivo. No muestra menus ni pide datos (de eso se encarga la Vista).

# Cada linea se guarda como una linea de texto separada por comas:
#   NombreLinea,orden
"""

import os

from modelo.linea import Linea


class Controlador:

    def __init__(self):
        # Preparamos la ruta del archivo: media/basededatos.txt
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        carpeta = os.path.join(raiz, "media")
        os.makedirs(carpeta, exist_ok=True)   # crea la carpeta si no existe
        self.archivo = os.path.join(carpeta, "tiendavirtual.txt")

    def listar(self):
        # Lee el archivo y devuelve una lista de lineas.
        lineas = []

        try:
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                for l in archivo:
                    l = l.strip()
                    if l == "":
                        continue
                    nombre, orden = l.split(",")
                    linea = Linea(nombre, orden)
                    lineas.append(linea)
        except FileNotFoundError:
            # Si el archivo todavia no existe, devolvemos la lista vacia.
            pass
        return lineas

    def guardar(self, lineas):
        # Escribe TODA la lista en el archivo (borra lo viejo y pone lo nuevo).
        with open(self.archivo, "w", encoding="utf-8") as archivo:
            for d in lineas:
                archivo.write(f"{d.nombre},{d.orden}\n")

    def agregar(self, nombre, orden):
        lineas = self.listar()
        lineas.append(Linea(nombre, orden))
        self.guardar(lineas)

    def editar(self, numero, nombre, orden):
        lineas = self.listar()
        lineas[numero - 1] = Linea(nombre, orden)  # -1: las listas empiezan en 0
        self.guardar(lineas)

    def eliminar(self, numero):
        lineas = self.listar()
        lineas.pop(numero - 1)   # -1: las listas empiezan en 0
        self.guardar(lineas)
