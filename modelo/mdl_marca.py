"""
modelo/mdl_marca.py
====================
El MODELO: aqui solo definimos QUE es una marca.
El modelo NO pide datos por teclado ni muestra menus.

Campos: id_marca (PK), nombre, estado.
El id es AUTOINCREMENTABLE: se calcula con el metodo siguiente_id.
"""


class Marca:

    def __init__(self, nombre, estado, id):
        """
        Constructor: se ejecuta al hacer Marca(...). Solo GUARDA los datos.
        El id ya viene calculado desde fuera.
        """
        self._id = int(id)
        self._nombre = nombre
        self._estado = estado

    @staticmethod
    def siguiente_id(marcas):
        """
        Devuelve el id que le toca a una marca NUEVA:
        el id mas alto que ya existe + 1 (si no hay ninguna, empieza en 1).
        """
        mayor = 0
        for marca in marcas:
            if marca.id > mayor:
                mayor = marca.id
        return mayor + 1

    # -------------------------------------------------------------------
    # GET y SET: dan acceso controlado a los datos.
    #   - get_xxx  ->  LEE el dato
    #   - set_xxx  ->  CAMBIA el dato
    # Al final, property(...) une cada pareja para poder usarlos tambien
    # sin parentesis: marca.nombre  o  marca.nombre = "Nike".
    # -------------------------------------------------------------------

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, valor):
        self._nombre = valor

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
    estado = property(get_estado, set_estado)
