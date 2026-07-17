"""
main.py
=======
Este es el archivo que se ejecuta para USAR el programa.

# Primero pregunta que catalogo quieres gestionar (marcas, categorias,
# lineas o productos) y luego enciende la Vista correspondiente.
#
# Para ejecutar el programa, desde la carpeta del proyecto:
#     python main.py
"""

from vista.view_marca import Vista as VistaMarca
from vista.view_categoria import Vista as VistaCategoria
from vista.view_linea import Vista as VistaLinea
from vista.view_producto import Vista as VistaProducto


def main():
    try:
        # Menu general: se repite hasta que el usuario elige salir.
        while True:
            print("\n===== QUE QUIERES GESTIONAR? =====")
            print("1. Marcas")
            print("2. Categorias")
            print("3. Lineas")
            print("4. Productos")
            print("5. Salir")
            opcion = input("Elige una opcion: ")

            if opcion == "1":
                VistaMarca().iniciar()
            elif opcion == "2":
                VistaCategoria().iniciar()
            elif opcion == "3":
                VistaLinea().iniciar()
            elif opcion == "4":
                VistaProducto().iniciar()
            elif opcion == "5":
                print("\nHasta luego.")
                break
            else:
                print("\nOpcion no valida. Elige del 1 al 5.")
    except Exception as ex:
        print(f"Error en el programa: {ex}")


if __name__ == "__main__":
    main()
