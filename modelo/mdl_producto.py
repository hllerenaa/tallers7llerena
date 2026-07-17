"""
modelo/mdl_producto.py
=======================
El MODELO: aqui solo definimos QUE es un producto.
El modelo NO pide datos por teclado ni muestra menus.

Campos: id_producto (PK), nombre, id_marca (FK), id_categoria (FK),
        id_linea (FK), precio, stock, estado.

Las FK (id_marca, id_categoria, id_linea) son los ids de los otros
catalogos. Aqui solo guardamos el NUMERO; comprobar que ese id exista
es trabajo de la Vista/Controlador, no del modelo.
"""


class Producto:

    def __init__(self, nombre, id_marca, id_categoria, id_linea, precio, stock, estado, id):
        """
        Constructor: se ejecuta al hacer Producto(...). Solo GUARDA los datos.
        El id ya viene calculado desde fuera.
        """
        self._id = int(id)
        self._nombre = nombre
        self._id_marca = int(id_marca)
        self._id_categoria = int(id_categoria)
        self._id_linea = int(id_linea)
        self._precio = float(precio)
        self._stock = int(stock)
        self._estado = estado

    @staticmethod
    def siguiente_id(productos):
        """
        Devuelve el id que le toca a un producto NUEVO:
        el id mas alto que ya existe + 1 (si no hay ninguno, empieza en 1).
        """
        mayor = 0
        for producto in productos:
            if producto.id > mayor:
                mayor = producto.id
        return mayor + 1

    # -------------------------------------------------------------------
    # GET y SET: dan acceso controlado a los datos.
    #   - get_xxx  ->  LEE el dato
    #   - set_xxx  ->  CAMBIA el dato
    # Al final, property(...) une cada pareja para poder usarlos tambien
    # sin parentesis: producto.precio  o  producto.precio = 59.99.
    # -------------------------------------------------------------------

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, valor):
        self._nombre = valor

    def get_id_marca(self):
        return self._id_marca

    def set_id_marca(self, valor):
        self._id_marca = int(valor)

    def get_id_categoria(self):
        return self._id_categoria

    def set_id_categoria(self, valor):
        self._id_categoria = int(valor)

    def get_id_linea(self):
        return self._id_linea

    def set_id_linea(self, valor):
        self._id_linea = int(valor)

    def get_precio(self):
        return self._precio

    def set_precio(self, valor):
        self._precio = float(valor)

    def get_stock(self):
        return self._stock

    def set_stock(self, valor):
        self._stock = int(valor)

    def get_estado(self):
        # Guarda "activo" o "inactivo".
        return self._estado

    def set_estado(self, valor):
        self._estado = valor

    # property(get, set): conecta cada pareja de funciones.
    # OJO: id solo tiene get (NO tiene set): es de SOLO LECTURA,
    # asi el id no se puede cambiar desde fuera y siempre es unico.
    id = property(get_id)
    nombre = property(get_nombre, set_nombre)
    id_marca = property(get_id_marca, set_id_marca)
    id_categoria = property(get_id_categoria, set_id_categoria)
    id_linea = property(get_id_linea, set_id_linea)
    precio = property(get_precio, set_precio)
    stock = property(get_stock, set_stock)
    estado = property(get_estado, set_estado)
