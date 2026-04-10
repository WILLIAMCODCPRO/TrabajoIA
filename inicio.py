import os
from estudiantes import  menu_principal2
from computadores import menu_computadores

def limpiar_pantalla():
    # Limpia la consola según el sistema operativo (nt es Windows, posix es Linux/Mac)
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu_principal():
    limpiar_pantalla()
    print("========================================")
    print("           MENÚ PRINCIPAL              ")
    print("========================================")
    print("1. Gestionar Campers")
    print("2. Gestionar Computadores")
    print("3. Salir")
    print("----------------------------------------")

def menu_principal():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción (1-3): ")

        if opcion == "1":
            limpiar_pantalla()
            print(">>> Módulo de Gestión de Campers <<<")
            menu_principal2()
            input("\nPresione Enter para volver al Menú Principal...")
        
        elif opcion == "2":
            limpiar_pantalla()
            print(">>> Módulo de Gestión de Computadores <<<")
            menu_computadores()
            input("\nPresione Enter para volver al Menú Principal...")
        
        elif opcion == "3":
            print("\nSaliendo del sistema... ¡Hasta pronto!")
            break
        
        else:
            print("\n[!] Opción no válida. Por favor, intente de nuevo.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()