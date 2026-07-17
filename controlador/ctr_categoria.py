"""
controlador/ctr_categoria.py
=============================
El CONTROLADOR: es el "intermediario". Solo se encarga de GUARDAR y LEER las
categorias en el archivo. No muestra menus ni pide datos (de eso se encarga
la Vista) y no define que es una categoria (de eso se encarga el Modelo).

Cada categoria se guarda como una fila de texto separada por comas:
    id,nombre
Ejemplo:  1,Calzado
"""

import os

from modelo.mdl_categoria import Categoria


class Controlador:

    def __init__(self):
        # Preparamos la ruta del archivo: media/categorias.txt
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        carpeta = os.path.join(raiz, "media")
        os.makedirs(carpeta, exist_ok=True)   # crea la carpeta si no existe
        self.archivo = os.path.join(carpeta, "categorias.txt")

    def listar(self):
        # Lee el archivo y devuelve una lista de objetos Categoria.
        categorias = []

        try:
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                for l in archivo:
                    l = l.strip()
                    if l == "":
                        continue
                    # Cada fila trae 2 datos: id y nombre.
                    id, nombre = l.split(",")
                    # Pasamos el id para CONSERVAR el que ya tenia guardado.
                    categoria = Categoria(nombre, id)
                    categorias.append(categoria)
        except FileNotFoundError:
            # Si el archivo todavia no existe, devolvemos la lista vacia.
            pass
        return categorias

    def guardar(self, categorias):
        # Escribe TODA la lista en el archivo (borra lo viejo y pone lo nuevo).
        with open(self.archivo, "w", encoding="utf-8") as archivo:
            for c in categorias:
                archivo.write(f"{c.id},{c.nombre}\n")

    def agregar(self, nombre):
        categorias = self.listar()
        # Pedimos el id nuevo al metodo del Modelo: el mas alto + 1.
        nuevo_id = Categoria.siguiente_id(categorias)
        categorias.append(Categoria(nombre, nuevo_id))
        self.guardar(categorias)

    def editar(self, id, nombre):
        # Buscamos la categoria POR SU ID (no por su posicion en la lista).
        categorias = self.listar()
        for i in range(len(categorias)):
            if categorias[i].id == id:
                # La encontramos: la reemplazamos conservando el MISMO id.
                categorias[i] = Categoria(nombre, id)
                self.guardar(categorias)
                return
        # Si el bucle termina sin encontrarla, avisamos con un error.
        raise ValueError(f"No existe una categoria con id {id}")

    def eliminar(self, id):
        # Buscamos la categoria POR SU ID (no por su posicion en la lista).
        categorias = self.listar()
        for i in range(len(categorias)):
            if categorias[i].id == id:
                categorias.pop(i)          # la encontramos: la quitamos
                self.guardar(categorias)
                return
        # Si no aparece ningun id igual, lanzamos el error.
        raise ValueError(f"No existe una categoria con id {id}")
