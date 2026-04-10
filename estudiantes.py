import json
import os
import re

DATA_FILE = "campers.json"

def cargar_datos():
    """Carga los datos desde el archivo JSON."""
    if not os.path.exists(DATA_FILE):
        return {"campers": [], "ultimo_id": 0}
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"campers": [], "ultimo_id": 0}

def guardar_datos(data):
    """Guarda los datos en el archivo JSON."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def validar_email(email):
    """Valida el formato de un correo electrónico."""
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, email) is not None

def registrar_camper():
    data = cargar_datos()
    print("\n--- Registro de Nuevo Camper ---")
    
    nombre = input("Nombre completo: ").strip()
    documento = input("Documento (solo números): ").strip()
    email = input("Email: ").strip()

    # Validaciones
    if not nombre or not documento or not email:
        print("Error: Ningún campo puede quedar vacío.")
        return

    if not documento.isdigit():
        print("Error: El documento debe ser numérico.")
        return

    if not validar_email(email):
        print("Error: Formato de email inválido.")
        return

    # Crear nuevo camper
    data["ultimo_id"] += 1
    nuevo_camper = {
        "id": data["ultimo_id"],
        "nombre": nombre,
        "documento": documento,
        "email": email,
        "estado": "Activo"
    }

    data["campers"].append(nuevo_camper)
    guardar_datos(data)
    print(f"Camper registrado con éxito. ID asignado: {nuevo_camper['id']}")

def listar_campers():
    data = cargar_datos()
    print("\n--- Lista de Campers ---")
    if not data["campers"]:
        print("No hay registros disponibles.")
        return

    for c in data["campers"]:
        print(f"ID: {c['id']} | Nombre: {c['nombre']} | Doc: {c['documento']} | Email: {c['email']} | Estado: {c['estado']}")

def actualizar_camper():
    data = cargar_datos()
    id_buscar = input("\nIngrese el ID del camper a actualizar: ")
    
    for c in data["campers"]:
        if str(c["id"]) == id_buscar:
            print(f"Editando a: {c['nombre']}")
            
            nuevo_nombre = input("Nuevo nombre (deje vacío para mantener): ").strip()
            nuevo_email = input("Nuevo email (deje vacío para mantener): ").strip()
            nuevo_estado = input("Nuevo estado (Activo/Inactivo - deje vacío para mantener): ").strip()

            if nuevo_nombre: c["nombre"] = nuevo_nombre
            if nuevo_email:
                if validar_email(nuevo_email):
                    c["email"] = nuevo_email
                else:
                    print("Email inválido. No se actualizó el correo.")
            if nuevo_estado in ["Activo", "Inactivo"]:
                c["estado"] = nuevo_estado
            
            guardar_datos(data)
            print("Datos actualizados correctamente.")
            return
    print("Camper no encontrado.")

def eliminar_camper():
    data = cargar_datos()
    id_buscar = input("\nIngrese el ID del camper a eliminar: ")
    
    inicial = len(data["campers"])
    data["campers"] = [c for c in data["campers"] if str(c["id"]) != id_buscar]
    
    if len(data["campers"]) < inicial:
        guardar_datos(data)
        print("Registro eliminado exitosamente.")
    else:
        print("ID no encontrado.")

def menu_principal2():
    while True:
        print("\n==============================")
        print("   SISTEMA DE GESTIÓN CAMPERS")
        print("==============================")
        print("1. Registrar Camper")
        print("2. Listar Campers")
        print("3. Actualizar Camper")
        print("4. Eliminar Camper")
        print("5. Salir al Menú Principal (Sistema)")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            registrar_camper()
        elif opcion == "2":
            listar_campers()
        elif opcion == "3":
            actualizar_camper()
        elif opcion == "4":
            eliminar_camper()
        elif opcion == "5":
            print("Regresando al menú principal del sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu_principal2()