"""
modelo/mdl_linea.py
=====================
El MODELO: aqui solo definimos QUE es una linea.
El modelo NO pide datos por teclado ni muestra menus.

Campos: id_linea (PK), nombre, estado.
La Linea es un catalogo INDEPENDIENTE de la Categoria: no guarda ninguna
referencia a ella. Quien las relaciona es el Producto (con sus FK).

Novedad de este ejercicio: el campo "id".
    - Es AUTOINCREMENTABLE: cada linea nueva recibe el siguiente numero
      automaticamente, sin que el usuario lo escriba.
    - Para generarlo usamos un metodo sencillo (siguiente_id) dentro de la
      clase, en vez de meter esa logica dentro del constructor.
"""


class Linea:

    def __init__(self, nombre, estado, id):
        """
        Constructor: se ejecuta al hacer Linea(...). Solo GUARDA los datos.
        El id ya viene calculado desde fuera (por eso el constructor queda
        cortito y claro).
        """
        self._id = int(id)
        self._nombre = nombre
        self._estado = estado

    @staticmethod
    def siguiente_id(lineas):
        """
        Devuelve el id que le toca a una linea NUEVA.

        Regla (muy sencilla): es el id mas alto que ya existe + 1.
        Si todavia no hay ninguna linea, empezamos en 1.

        Ejemplo: si ya existen los ids 1, 2 y 5 -> devuelve 6.

        Es @staticmethod porque NO necesita una linea concreta (no usa 'self'):
        solo mira la lista completa. Por eso se llama con Linea.siguiente_id(...).
        """
        mayor = 0
        for linea in lineas:
            if linea.id > mayor:
                mayor = linea.id
        return mayor + 1

    # -------------------------------------------------------------------
    # PROPERTIES (los "def property"): dan acceso controlado a los datos
    # -------------------------------------------------------------------

    @property
    def id(self):
        """
        Property de solo LECTURA para el id.
        Al escribir 'linea.id' se ejecuta esto y devuelve el numero.
        Como NO tiene un @id.setter, el id NO se puede cambiar desde fuera:
        asi el id siempre es unico y no se modifica por error.
        """
        return self._id

    @property
    def nombre(self):
        # Al escribir 'linea.nombre' se devuelve el nombre guardado.
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        # Al escribir 'linea.nombre = "algo"' se guarda el nuevo valor aqui.
        self._nombre = valor

    @property
    def estado(self):
        # Al escribir 'linea.estado' se devuelve el estado guardado
        # ("activo" o "inactivo").
        return self._estado

    @estado.setter
    def estado(self, valor):
        # Al escribir 'linea.estado = "activo"' se guarda el nuevo valor aqui.
        self._estado = valor
