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
    # GET y SET: dan acceso controlado a los datos.
    #   - get_xxx  ->  LEE el dato
    #   - set_xxx  ->  CAMBIA el dato
    # Al final, property(...) une cada pareja para poder usarlos tambien
    # sin parentesis: linea.nombre  o  linea.nombre = "Deportiva".
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
