"""
vista/view_linea.py
================
La VISTA: muestra el menu, pide los datos por teclado y muestra los
resultados. Es la parte que "se ve". Cuando hay que guardar o leer datos,
le pide ayuda al Controlador.
"""

from controlador.ctr_linea import Controlador


class Vista:

    def __init__(self):
        # La Vista usa un Controlador para guardar y leer los datos.
        self.controlador = Controlador()

    def iniciar(self):
        # Este es el menu del catalogo: se repite hasta que el usuario elige regresar.
        while True:
            print("\n----- SISTEMA DE LINEAS -----")
            print("1. Agregar linea")
            print("2. Listar lineas")
            print("3. Editar linea")
            print("4. Eliminar linea")
            print("5. Regresar")
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
                # Regresa al menu principal (solo rompe ESTE menu).
                print("\nRegresando al menu principal...")
                break
            else:
                print("\nOpcion no valida. Elige del 1 al 5.")

    def mostrar(self, lineas):
        # Muestra la lista numerada (1, 2, 3...).
        # OJO: el "numero" de la lista es solo la posicion en pantalla para
        # elegir; el "id" es el identificador real y unico de cada linea
        # (lo genero el Modelo de forma automatica) y no cambia aunque borres.
        if len(lineas) == 0:
            print("\nNo hay lineas guardadas.")
            return
        print("\n----- LINEAS -----")
        numero = 1
        for d in lineas:
            print(f"{numero}). (id: {d.id}) {d.nombre} | Estado: {d.estado}")
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

        # try / except: si al guardar algo falla (por ejemplo, no se puede
        # escribir el archivo), NO se cae el programa. Mostramos el error y
        # el menu sigue funcionando.
        try:
            self.controlador.agregar(nombre, estado)
            print("\nLinea agregada.")
        except Exception as ex:
            print(f"\nNo se pudo agregar la linea: {ex}")

    def listar(self):
        lineas = self.controlador.listar()
        self.mostrar(lineas)

    def editar(self):
        lineas = self.controlador.listar()
        self.mostrar(lineas)
        if len(lineas) == 0:
            return

        # Ahora pedimos el ID del registro (el numero que sale entre parentesis),
        # no la posicion en la lista.
        id = input("\nId de la linea a editar: ")
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

        # try / except: si el id NO existe, el controlador lanza un error
        # y aqui lo atrapamos para mostrar el mensaje sin caernos.
        try:
            self.controlador.editar(id, nombre, estado)
            print("\nLinea actualizada.")
        except Exception as ex:
            print(f"\nNo se pudo editar la linea: {ex}")

    def eliminar(self):
        lineas = self.controlador.listar()
        self.mostrar(lineas)
        if len(lineas) == 0:
            return

        # Pedimos el ID del registro (el numero entre parentesis), no la posicion.
        id = input("\nId de la linea a eliminar: ")
        if not id.isdigit():
            print("El id debe ser un numero.")
            return
        id = int(id)

        confirm = input(f"Confirma eliminar la linea con id {id}? (s/n): ").strip().lower()
        if confirm != 's':
            print("Operacion cancelada.")
            return

        # try / except: si el id NO existe, el controlador lanza un error
        # y aqui lo atrapamos para mostrar el mensaje sin caernos.
        try:
            self.controlador.eliminar(id)
            print("\nLinea eliminada.")
        except Exception as ex:
            print(f"\nNo se pudo eliminar la linea: {ex}")
