"""
modelo/mdl_producto.py
=======================
El MODELO: aqui solo definimos QUE es un producto.
El modelo NO pide datos por teclado ni muestra menus.

Campos: id_producto (PK), nombre, id_marca (FK), id_categoria (FK),
        id_linea (FK), precio, stock.

Las FK (id_marca, id_categoria, id_linea) son los ids de los otros
catalogos. Aqui solo guardamos el NUMERO; comprobar que ese id exista
es trabajo de la Vista/Controlador, no del modelo.
"""


class Producto:

    def __init__(self, nombre, id_marca, id_categoria, id_linea, precio, stock, id):
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
    # PROPERTIES: dan acceso controlado a los datos.
    # @property = para LEER (producto.precio) y @precio.setter = para
    # CAMBIAR (producto.precio = 59.99). Se usan SIN parentesis.
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
    def id_marca(self):
        return self._id_marca

    @id_marca.setter
    def id_marca(self, valor):
        self._id_marca = int(valor)

    @property
    def id_categoria(self):
        return self._id_categoria

    @id_categoria.setter
    def id_categoria(self, valor):
        self._id_categoria = int(valor)

    @property
    def id_linea(self):
        return self._id_linea

    @id_linea.setter
    def id_linea(self, valor):
        self._id_linea = int(valor)

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._precio = float(valor)

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        self._stock = int(valor)
