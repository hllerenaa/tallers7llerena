"""
vista/view_producto.py
=======================
La VISTA: muestra el menu, pide los datos por teclado y muestra los
resultados. Es la parte que "se ve". Cuando hay que guardar o leer datos,
le pide ayuda al Controlador.

El Producto es el que RELACIONA los catalogos: guarda el id de una Marca,
el id de una Categoria y el id de una Linea (las FK). Por eso esta Vista
tambien usa los controladores de esos tres catalogos: para mostrar las
opciones disponibles y comprobar que el id elegido exista de verdad.
"""

from controlador.ctr_producto import Controlador
from controlador.ctr_marca import Controlador as ControladorMarca
from controlador.ctr_categoria import Controlador as ControladorCategoria
from controlador.ctr_linea import Controlador as ControladorLinea


class Vista:

    def __init__(self):
        # La Vista usa un Controlador para guardar y leer los productos...
        self.controlador = Controlador()
        # ...y los controladores de los catalogos para validar las FK.
        self.ctr_marca = ControladorMarca()
        self.ctr_categoria = ControladorCategoria()
        self.ctr_linea = ControladorLinea()

    def iniciar(self):
        # Este es el menu principal: se repite hasta que el usuario elige salir.
        while True:
            print("\n----- SISTEMA DE PRODUCTOS -----")
            print("1. Agregar producto")
            print("2. Listar productos")
            print("3. Editar producto")
            print("4. Eliminar producto")
            print("5. Salir")
            opcion = input("Elige una opcion: ")

            if opcion == "1":
                self.agregar()
            elif opcion == "2":
                self.listar()
            elif opcion == "3":
                self.editar()
            elif opcion == "4":
                self.eliminar()
            elif opcion == "5":
                print("\nHasta luego.")
                break
            else:
                print("\nOpcion no valida. Elige del 1 al 5.")

    def nombre_por_id(self, lista, id):
        # Busca en un catalogo (marcas, categorias o lineas) el nombre
        # que corresponde a un id. Si no existe, lo avisa en pantalla.
        for item in lista:
            if item.id == id:
                return item.nombre
        return f"(id {id} no existe)"

    def mostrar(self, productos):
        # Muestra la lista numerada. Para que se entienda, en vez de mostrar
        # solo los numeros de las FK, buscamos el NOMBRE de cada catalogo.
        if len(productos) == 0:
            print("\nNo hay productos guardados.")
            return

        marcas = self.ctr_marca.listar()
        categorias = self.ctr_categoria.listar()
        lineas = self.ctr_linea.listar()

        print("\n----- PRODUCTOS -----")
        numero = 1
        for p in productos:
            marca = self.nombre_por_id(marcas, p.id_marca)
            categoria = self.nombre_por_id(categorias, p.id_categoria)
            linea = self.nombre_por_id(lineas, p.id_linea)
            print(f"{numero}). (id: {p.id}) {p.nombre} | Marca: {marca} | "
                  f"Categoria: {categoria} | Linea: {linea} | "
                  f"Precio: {p.precio} | Stock: {p.stock} | Estado: {p.estado}")
            numero = numero + 1

    def pedir_fk(self, lista, titulo):
        """
        Muestra un catalogo (marcas, categorias o lineas) y pide elegir un id.
        Devuelve el id elegido (int) o None si algo esta mal.
        Asi garantizamos que la FK apunte a un registro que SI existe.
        """
        if len(lista) == 0:
            print(f"No hay {titulo} registradas. Registra primero en ese catalogo.")
            return None

        print(f"\n{titulo.upper()} disponibles:")
        for item in lista:
            print(f"   (id: {item.id}) {item.nombre} | Estado: {item.estado}")

        id = input(f"Id de la {titulo[:-1]}: ").strip()
        if not id.isdigit():
            print("El id debe ser un numero.")
            return None
        id = int(id)

        # Comprobamos que el id elegido exista en el catalogo.
        for item in lista:
            if item.id == id:
                return id
        print(f"No existe ese id en {titulo}.")
        return None

    def pedir_estado(self):
        # Pide el estado y devuelve "activo", "inactivo" o None si es invalido.
        estado = input("Estado (activo/inactivo): ").strip().lower()
        if estado not in ("activo", "inactivo"):
            print("El estado debe ser 'activo' o 'inactivo'.")
            return None
        return estado

    def pedir_datos(self):
        """
        Pide TODOS los datos de un producto y los devuelve en una tupla.
        Si algun dato es invalido, devuelve None y no se guarda nada.
        Se usa tanto en agregar como en editar (para no repetir codigo).
        """
        nombre = input("Nombre: ").strip()
        if nombre == "":
            print("Nombre no puede estar vacio.")
            return None

        # Las tres FK: se eligen viendo el catalogo correspondiente.
        id_marca = self.pedir_fk(self.ctr_marca.listar(), "marcas")
        if id_marca is None:
            return None
        id_categoria = self.pedir_fk(self.ctr_categoria.listar(), "categorias")
        if id_categoria is None:
            return None
        id_linea = self.pedir_fk(self.ctr_linea.listar(), "lineas")
        if id_linea is None:
            return None

        precio = input("Precio: ").strip()
        try:
            precio = float(precio)
            if precio < 0:
                print("El precio no puede ser negativo.")
                return None
        except ValueError:
            print("El precio debe ser un numero (ej: 59.99).")
            return None

        stock = input("Stock (numero entero): ").strip()
        if not stock.isdigit():
            print("El stock debe ser un numero entero.")
            return None
        stock = int(stock)

        estado = self.pedir_estado()
        if estado is None:
            return None

        return nombre, id_marca, id_categoria, id_linea, precio, stock, estado

    def agregar(self):
        datos = self.pedir_datos()
        if datos is None:
            return

        # try / except: si al guardar algo falla, NO se cae el programa.
        try:
            self.controlador.agregar(*datos)
            print("\nProducto agregado.")
        except Exception as ex:
            print(f"\nNo se pudo agregar el producto: {ex}")

    def listar(self):
        productos = self.controlador.listar()
        self.mostrar(productos)

    def editar(self):
        productos = self.controlador.listar()
        self.mostrar(productos)
        if len(productos) == 0:
            return

        # Pedimos el ID del registro (el numero entre parentesis).
        id = input("\nId del producto a editar: ")
        if not id.isdigit():
            print("El id debe ser un numero.")
            return
        id = int(id)

        print("Escribe los datos nuevos:")
        datos = self.pedir_datos()
        if datos is None:
            return

        # try / except: si el id NO existe, el controlador lanza un error.
        try:
            self.controlador.editar(id, *datos)
            print("\nProducto actualizado.")
        except Exception as ex:
            print(f"\nNo se pudo editar el producto: {ex}")

    def eliminar(self):
        productos = self.controlador.listar()
        self.mostrar(productos)
        if len(productos) == 0:
            return

        # Pedimos el ID del registro (el numero entre parentesis).
        id = input("\nId del producto a eliminar: ")
        if not id.isdigit():
            print("El id debe ser un numero.")
            return
        id = int(id)

        confirm = input(f"Confirma eliminar el producto con id {id}? (s/n): ").strip().lower()
        if confirm != 's':
            print("Operacion cancelada.")
            return

        # try / except: si el id NO existe, el controlador lanza un error.
        try:
            self.controlador.eliminar(id)
            print("\nProducto eliminado.")
        except Exception as ex:
            print(f"\nNo se pudo eliminar el producto: {ex}")
