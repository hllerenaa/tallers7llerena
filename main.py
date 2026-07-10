"""
main.py
=======
Este es el archivo que se ejecuta para USAR el programa.

# Primero pregunta que quieres gestionar (dispositivos o clientes) y luego
# enciende la Vista correspondiente.
#
# Para ejecutar el programa, desde la carpeta del proyecto:
#     python main.py
"""

from vista.consola import Vista



def main():
    try:
        print("===== QUE QUIERES GESTIONAR? =====")
        print("1. Lineas")
        opcion = input("Elige una opcion: ")
        if opcion == "1":
            Vista().iniciar()
        else:
            print("Opcion no valida.")
    except Exception as ex:
        print(f"Error en el programa: {ex}")


if __name__ == "__main__":
    main()
