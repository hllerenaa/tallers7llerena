"""
controlador/ctr_marca.py
=========================
El CONTROLADOR: es el "intermediario". Solo se encarga de GUARDAR y LEER las
marcas en el archivo. No muestra menus ni pide datos (de eso se encarga la
Vista) y no define que es una marca (de eso se encarga el Modelo).

Cada marca se guarda como una fila de texto separada por comas:
    id,nombre
Ejemplo:  1,Nike
"""

import os

from modelo.mdl_marca import Marca


class Controlador:

    def __init__(self):
        # Preparamos la ruta del archivo: media/marcas.txt
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        carpeta = os.path.join(raiz, "media")
        os.makedirs(carpeta, exist_ok=True)   # crea la carpeta si no existe
        self.archivo = os.path.join(carpeta, "marcas.txt")

    def listar(self):
        # Lee el archivo y devuelve una lista de objetos Marca.
        marcas = []

        try:
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                for l in archivo:
                    l = l.strip()
                    if l == "":
                        continue
                    # Cada fila trae 2 datos: id y nombre.
                    id, nombre = l.split(",")
                    # Pasamos el id para CONSERVAR el que ya tenia guardado.
                    marca = Marca(nombre, id)
                    marcas.append(marca)
        except FileNotFoundError:
            # Si el archivo todavia no existe, devolvemos la lista vacia.
            pass
        return marcas

    def guardar(self, marcas):
        # Escribe TODA la lista en el archivo (borra lo viejo y pone lo nuevo).
        with open(self.archivo, "w", encoding="utf-8") as archivo:
            for m in marcas:
                archivo.write(f"{m.id},{m.nombre}\n")

    def agregar(self, nombre):
        marcas = self.listar()
        # Pedimos el id nuevo al metodo del Modelo: el mas alto + 1.
        nuevo_id = Marca.siguiente_id(marcas)
        marcas.append(Marca(nombre, nuevo_id))
        self.guardar(marcas)

    def editar(self, id, nombre):
        # Buscamos la marca POR SU ID (no por su posicion en la lista).
        marcas = self.listar()
        for i in range(len(marcas)):
            if marcas[i].id == id:
                # La encontramos: la reemplazamos conservando el MISMO id.
                marcas[i] = Marca(nombre, id)
                self.guardar(marcas)
                return
        # Si el bucle termina sin encontrarla, avisamos con un error.
        raise ValueError(f"No existe una marca con id {id}")

    def eliminar(self, id):
        # Buscamos la marca POR SU ID (no por su posicion en la lista).
        marcas = self.listar()
        for i in range(len(marcas)):
            if marcas[i].id == id:
                marcas.pop(i)          # la encontramos: la quitamos
                self.guardar(marcas)
                return
        # Si no aparece ningun id igual, lanzamos el error.
        raise ValueError(f"No existe una marca con id {id}")
