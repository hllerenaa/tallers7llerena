"""
vista/consola.py
================
La VISTA: muestra el menu, pide los datos por teclado y muestra los
resultados. Es la parte que "se ve". Cuando hay que guardar o leer datos,
le pide ayuda al Controlador.
"""

from controlador.controlador import Controlador


class Vista:

    def __init__(self):
        # La Vista usa un Controlador para guardar y leer los datos.
        self.controlador = Controlador()

    def iniciar(self):
        # Este es el menu principal: se repite hasta que el usuario elige salir.
        while True:
            print("\n----- SISTEMA DE LINEAS -----")
            print("1. Agregar linea")
            print("2. Listar lineas")
            print("3. Editar linea")
            print("4. Eliminar linea")
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

    def mostrar(self, lineas):
        # Muestra la lista numerada (1, 2, 3...).
        if len(lineas) == 0:
            print("\nNo hay lineas guardadas.")
            return
        print("\n----- LINEAS -----")
        numero = 1
        for d in lineas:
            print(f"{numero}). {d.nombre} | Orden: {d.orden}")
            numero = numero + 1

    def agregar(self):
        nombre = input("Nombre: ").strip()
        if nombre == "":
            print("Nombre no puede estar vacio.")
            return

        orden = input("Orden (numero): ").strip()
        if not orden.isdigit():
            print("Orden debe ser un numero.")
            return

        self.controlador.agregar(nombre, orden)
        print("\nLinea agregada.")

    def listar(self):
        lineas = self.controlador.listar()
        self.mostrar(lineas)

    def editar(self):
        lineas = self.controlador.listar()
        self.mostrar(lineas)
        if len(lineas) == 0:
            return

        numero = input("\nNumero de la linea a editar: ")
        if not numero.isdigit():
            print("Eso no es un numero.")
            return
        numero = int(numero)
        if numero < 1 or numero > len(lineas):
            print("Ese numero no esta en la lista.")
            return

        print("Escribe los datos nuevos:")
        nombre = input("Nombre: ").strip()
        if nombre == "":
            print("Nombre no puede estar vacio.")
            return
        orden = input("Orden (numero): ").strip()
        if not orden.isdigit():
            print("Orden debe ser un numero.")
            return

        self.controlador.editar(numero, nombre, orden)
        print("\nLinea actualizada.")

    def eliminar(self):
        lineas = self.controlador.listar()
        self.mostrar(lineas)
        if len(lineas) == 0:
            return

        numero = input("\nNumero de la linea a eliminar: ")
        if not numero.isdigit():
            print("Eso no es un numero.")
            return
        numero = int(numero)
        if numero < 1 or numero > len(lineas):
            print("Ese numero no esta en la lista.")
            return

        confirm = input(f"Confirma eliminar la linea {numero}? (s/n): ").strip().lower()
        if confirm != 's':
            print("Operacion cancelada.")
            return

        self.controlador.eliminar(numero)
        print("\nLinea eliminada.")
