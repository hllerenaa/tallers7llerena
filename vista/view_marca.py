"""
vista/view_marca.py
====================
La VISTA: muestra el menu, pide los datos por teclado y muestra los
resultados. Es la parte que "se ve". Cuando hay que guardar o leer datos,
le pide ayuda al Controlador.
"""

from controlador.ctr_marca import Controlador


class Vista:

    def __init__(self):
        # La Vista usa un Controlador para guardar y leer los datos.
        self.controlador = Controlador()

    def iniciar(self):
        # Este es el menu principal: se repite hasta que el usuario elige salir.
        while True:
            print("\n----- SISTEMA DE MARCAS -----")
            print("1. Agregar marca")
            print("2. Listar marcas")
            print("3. Editar marca")
            print("4. Eliminar marca")
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

    def mostrar(self, marcas):
        # Muestra la lista numerada. El "id" es el identificador real y unico.
        if len(marcas) == 0:
            print("\nNo hay marcas guardadas.")
            return
        print("\n----- MARCAS -----")
        numero = 1
        for m in marcas:
            print(f"{numero}). (id: {m.id}) {m.nombre} | Estado: {m.estado}")
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
            print("\nMarca agregada.")
        except Exception as ex:
            print(f"\nNo se pudo agregar la marca: {ex}")

    def listar(self):
        marcas = self.controlador.listar()
        self.mostrar(marcas)

    def editar(self):
        marcas = self.controlador.listar()
        self.mostrar(marcas)
        if len(marcas) == 0:
            return

        # Pedimos el ID del registro (el numero entre parentesis).
        id = input("\nId de la marca a editar: ")
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
            print("\nMarca actualizada.")
        except Exception as ex:
            print(f"\nNo se pudo editar la marca: {ex}")

    def eliminar(self):
        marcas = self.controlador.listar()
        self.mostrar(marcas)
        if len(marcas) == 0:
            return

        # Pedimos el ID del registro (el numero entre parentesis).
        id = input("\nId de la marca a eliminar: ")
        if not id.isdigit():
            print("El id debe ser un numero.")
            return
        id = int(id)

        confirm = input(f"Confirma eliminar la marca con id {id}? (s/n): ").strip().lower()
        if confirm != 's':
            print("Operacion cancelada.")
            return

        # try / except: si el id NO existe, el controlador lanza un error.
        try:
            self.controlador.eliminar(id)
            print("\nMarca eliminada.")
        except Exception as ex:
            print(f"\nNo se pudo eliminar la marca: {ex}")
