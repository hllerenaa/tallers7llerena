"""
controlador/ctr_linea.py
=========================
El CONTROLADOR: es el "intermediario". Solo se encarga de GUARDAR y LEER las
lineas en el archivo. No muestra menus ni pide datos (de eso se encarga la
Vista) y no define que es una linea (de eso se encarga el Modelo).

La Linea es un catalogo INDEPENDIENTE de la Categoria: tiene su propio
archivo y no guarda ninguna referencia a otros catalogos.

Cada linea se guarda como una fila de texto separada por comas:
    id,nombre
Ejemplo:  1,Deportiva
"""

import os

from modelo.mdl_linea import Linea


class Controlador:

    def __init__(self):
        # Preparamos la ruta del archivo: media/lineas.txt
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        carpeta = os.path.join(raiz, "media")
        os.makedirs(carpeta, exist_ok=True)   # crea la carpeta si no existe
        self.archivo = os.path.join(carpeta, "lineas.txt")

    def listar(self):
        # Lee el archivo y devuelve una lista de objetos Linea.
        lineas = []

        try:
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                for l in archivo:
                    l = l.strip()
                    if l == "":
                        continue
                    # Cada fila trae 2 datos: id y nombre.
                    id, nombre = l.split(",")
                    # Pasamos el id para CONSERVAR el que ya tenia guardado.
                    linea = Linea(nombre, id)
                    lineas.append(linea)
        except FileNotFoundError:
            # Si el archivo todavia no existe, devolvemos la lista vacia.
            pass
        return lineas

    def guardar(self, lineas):
        # Escribe TODA la lista en el archivo (borra lo viejo y pone lo nuevo).
        with open(self.archivo, "w", encoding="utf-8") as archivo:
            for d in lineas:
                # Guardamos tambien el id al principio de cada fila.
                archivo.write(f"{d.id},{d.nombre}\n")

    def agregar(self, nombre):
        lineas = self.listar()
        # Pedimos el id nuevo al metodo del Modelo: el mas alto + 1.
        nuevo_id = Linea.siguiente_id(lineas)
        lineas.append(Linea(nombre, nuevo_id))
        self.guardar(lineas)

    def editar(self, id, nombre):
        # Buscamos la linea POR SU ID (no por su posicion en la lista).
        lineas = self.listar()
        for i in range(len(lineas)):
            if lineas[i].id == id:
                # La encontramos: la reemplazamos conservando el MISMO id.
                lineas[i] = Linea(nombre, id)
                self.guardar(lineas)
                return
        # Si el bucle termina sin encontrarla, avisamos con un error.
        # Ese error lo atrapara el try/except de la Vista.
        raise ValueError(f"No existe una linea con id {id}")

    def eliminar(self, id):
        # Buscamos la linea POR SU ID (no por su posicion en la lista).
        lineas = self.listar()
        for i in range(len(lineas)):
            if lineas[i].id == id:
                lineas.pop(i)          # la encontramos: la quitamos
                self.guardar(lineas)
                return
        # Si no aparece ningun id igual, lanzamos el error.
        raise ValueError(f"No existe una linea con id {id}")
