"""
modelo/mdl_categoria.py
========================
El MODELO: aqui solo definimos QUE es una categoria.
El modelo NO pide datos por teclado ni muestra menus.

Campos: id_categoria (PK), nombre, estado.
El id es AUTOINCREMENTABLE: se calcula con el metodo siguiente_id.
"""


class Categoria:

    def __init__(self, nombre, estado, id):
        """
        Constructor: se ejecuta al hacer Categoria(...). Solo GUARDA los datos.
        El id ya viene calculado desde fuera.
        """
        self._id = int(id)
        self._nombre = nombre
        self._estado = estado

    @staticmethod
    def siguiente_id(categorias):
        """
        Devuelve el id que le toca a una categoria NUEVA:
        el id mas alto que ya existe + 1 (si no hay ninguna, empieza en 1).
        """
        mayor = 0
        for categoria in categorias:
            if categoria.id > mayor:
                mayor = categoria.id
        return mayor + 1

    # -------------------------------------------------------------------
    # PROPERTIES: dan acceso controlado a los datos
    # -------------------------------------------------------------------

    @property
    def id(self):
        # Solo LECTURA: no tiene setter, el id no se puede cambiar desde fuera.
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def estado(self):
        # Guarda "activo" o "inactivo".
        return self._estado

    @estado.setter
    def estado(self, valor):
        self._estado = valor
