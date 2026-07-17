"""
controlador/ctr_producto.py
============================
El CONTROLADOR: es el "intermediario". Solo se encarga de GUARDAR y LEER los
productos en el archivo. No muestra menus ni pide datos (de eso se encarga
la Vista) y no define que es un producto (de eso se encarga el Modelo).

Cada producto se guarda como una fila de texto separada por comas:
    id,nombre,id_marca,id_categoria,id_linea,precio,stock,estado
Ejemplo:  1,Zapatilla Air,1,2,1,59.99,10,activo

Las columnas id_marca, id_categoria e id_linea son las FK: apuntan a los
ids de los catalogos de Marca, Categoria y Linea.
"""

import os

from modelo.mdl_producto import Producto


class Controlador:

    def __init__(self):
        # Preparamos la ruta del archivo: media/productos.txt
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        carpeta = os.path.join(raiz, "media")
        os.makedirs(carpeta, exist_ok=True)   # crea la carpeta si no existe
        self.archivo = os.path.join(carpeta, "productos.txt")

    def listar(self):
        # Lee el archivo y devuelve una lista de objetos Producto.
        productos = []

        try:
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                for l in archivo:
                    l = l.strip()
                    if l == "":
                        continue
                    # Cada fila trae 8 datos, en el mismo orden en que se guardan.
                    id, nombre, id_marca, id_categoria, id_linea, precio, stock, estado = l.split(",")
                    producto = Producto(nombre, id_marca, id_categoria, id_linea,
                                        precio, stock, estado, id)
                    productos.append(producto)
        except FileNotFoundError:
            # Si el archivo todavia no existe, devolvemos la lista vacia.
            pass
        return productos

    def guardar(self, productos):
        # Escribe TODA la lista en el archivo (borra lo viejo y pone lo nuevo).
        with open(self.archivo, "w", encoding="utf-8") as archivo:
            for p in productos:
                archivo.write(f"{p.id},{p.nombre},{p.id_marca},{p.id_categoria},"
                              f"{p.id_linea},{p.precio},{p.stock},{p.estado}\n")

    def agregar(self, nombre, id_marca, id_categoria, id_linea, precio, stock, estado):
        productos = self.listar()
        # Pedimos el id nuevo al metodo del Modelo: el mas alto + 1.
        nuevo_id = Producto.siguiente_id(productos)
        productos.append(Producto(nombre, id_marca, id_categoria, id_linea,
                                  precio, stock, estado, nuevo_id))
        self.guardar(productos)

    def editar(self, id, nombre, id_marca, id_categoria, id_linea, precio, stock, estado):
        # Buscamos el producto POR SU ID (no por su posicion en la lista).
        productos = self.listar()
        for i in range(len(productos)):
            if productos[i].id == id:
                # Lo encontramos: lo reemplazamos conservando el MISMO id.
                productos[i] = Producto(nombre, id_marca, id_categoria, id_linea,
                                        precio, stock, estado, id)
                self.guardar(productos)
                return
        # Si el bucle termina sin encontrarlo, avisamos con un error.
        raise ValueError(f"No existe un producto con id {id}")

    def eliminar(self, id):
        # Buscamos el producto POR SU ID (no por su posicion en la lista).
        productos = self.listar()
        for i in range(len(productos)):
            if productos[i].id == id:
                productos.pop(i)          # lo encontramos: lo quitamos
                self.guardar(productos)
                return
        # Si no aparece ningun id igual, lanzamos el error.
        raise ValueError(f"No existe un producto con id {id}")
