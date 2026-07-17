"""
vista/view_categoria.py
========================
La VISTA: muestra el menu, pide los datos por teclado y muestra los
resultados. Es la parte que "se ve". Cuando hay que guardar o leer datos,
le pide ayuda al Controlador.
"""

from controlador.ctr_categoria import Controlador


class Vista:

    def __init__(self):
        # La Vista usa un Controlador para guardar y leer los datos.
        self.controlador = Controlador()

    def iniciar(self):
        # Este es el menu principal: se repite hasta que el usuario elige salir.
        while True:
            print("\n----- SISTEMA DE CATEGORIAS -----")
            print("1. Agregar categoria")
            print("2. Listar categorias")
            print("3. Editar categoria")
            print("4. Eliminar categoria")
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

    def mostrar(self, categorias):
        # Muestra la lista numerada. El "id" es el identificador real y unico.
        if len(categorias) == 0:
            print("\nNo hay categorias guardadas.")
            return
        print("\n----- CATEGORIAS -----")
        numero = 1
        for c in categorias:
            print(f"{numero}). (id: {c.id}) {c.nombre} | Estado: {c.estado}")
            numero = numero + 1

    def pedir_estado(self):
        # Pide el estado y devuelve "activo", "inactivo" o None si es invalido.
        estado = input("Estado (activo/inactivo): ").strip().lower()
        if estado not in ("activo", "inactivo"):
            print("El estado debe ser 'activo' o 'inactivo'.")
            return None
        return estado

    def agregar(self):
        nombre = input("Nombre: ").strip()
        if nombre == "":
            print("Nombre no puede estar vacio.")
            return

        estado = self.pedir_estado()
        if estado is None:
            return

        # try / except: si al guardar algo falla, NO se cae el programa.
        try:
            self.controlador.agregar(nombre, estado)
            print("\nCategoria agregada.")
        except Exception as ex:
            print(f"\nNo se pudo agregar la categoria: {ex}")

    def listar(self):
        categorias = self.controlador.listar()
        self.mostrar(categorias)

    def editar(self):
        categorias = self.controlador.listar()
        self.mostrar(categorias)
        if len(categorias) == 0:
            return

        # Pedimos el ID del registro (el numero entre parentesis).
        id = input("\nId de la categoria a editar: ")
        if not id.isdigit():
            print("El id debe ser un numero.")
            return
        id = int(id)

        print("Escribe los datos nuevos:")
        nombre = input("Nombre: ").strip()
        if nombre == "":
            print("Nombre no puede estar vacio.")
            return
        estado = self.pedir_estado()
        if estado is None:
            return

        # try / except: si el id NO existe, el controlador lanza un error.
        try:
            self.controlador.editar(id, nombre, estado)
            print("\nCategoria actualizada.")
        except Exception as ex:
            print(f"\nNo se pudo editar la categoria: {ex}")

    def eliminar(self):
        categorias = self.controlador.listar()
        self.mostrar(categorias)
        if len(categorias) == 0:
            return

        # Pedimos el ID del registro (el numero entre parentesis).
        id = input("\nId de la categoria a eliminar: ")
        if not id.isdigit():
            print("El id debe ser un numero.")
            return
        id = int(id)

        confirm = input(f"Confirma eliminar la categoria con id {id}? (s/n): ").strip().lower()
        if confirm != 's':
            print("Operacion cancelada.")
            return

        # try / except: si el id NO existe, el controlador lanza un error.
        try:
            self.controlador.eliminar(id)
            print("\nCategoria eliminada.")
        except Exception as ex:
            print(f"\nNo se pudo eliminar la categoria: {ex}")
