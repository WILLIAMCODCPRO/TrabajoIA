import json
import os

DATA_FILE = "computadoras.json"

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return {"computadores": [], "ultimo_id": 0}
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"computadores": [], "ultimo_id": 0}

def guardar_datos(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def seleccionar_estado():
    """Permite seleccionar el estado mediante números."""
    print("\nSeleccione el estado del equipo:")
    print("1. Disponible")
    print("2. Ocupado")
    print("3. Dañado")
    opc = input("Opción: ")
    estados = {"1": "Disponible", "2": "Ocupado", "3": "Dañado"}
    return estados.get(opc, None)

def registrar_computador():
    data = cargar_datos()
    print("\n--- Registro de Nuevo Computador ---")
    
    inventario = input("Número de inventario: ").strip()
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    estado = seleccionar_estado()

    # Validaciones
    if not inventario or not marca or not modelo or not estado:
        print("Error: Todos los campos son obligatorios y el estado debe ser válido.")
        return

    if not inventario.isdigit() or int(inventario) < 0:
        print("Error: El número de inventario debe ser un entero positivo.")
        return

    data["ultimo_id"] += 1
    nuevo_equipo = {
        "id": data["ultimo_id"],
        "inventario": int(inventario),
        "marca": marca,
        "modelo": modelo,
        "estado": estado
    }

    data["computadores"].append(nuevo_equipo)
    guardar_datos(data)
    print(f"Equipo registrado con éxito. ID: {nuevo_equipo['id']}")

def listar_computadores():
    data = cargar_datos()
    print("\n--- Inventario de Computadores ---")
    if not data["computadores"]:
        print("No hay equipos registrados.")
        return

    print(f"{'ID':<5} | {'Inventario':<12} | {'Marca':<12} | {'Modelo':<12} | {'Estado'}")
    print("-" * 60)
    for c in data["computadores"]:
        print(f"{c['id']:<5} | {c['inventario']:<12} | {c['marca']:<12} | {c['modelo']:<12} | {c['estado']}")

def actualizar_computador():
    data = cargar_datos()
    id_buscar = input("\nIngrese el ID del computador a editar: ")
    
    for c in data["computadores"]:
        if str(c["id"]) == id_buscar:
            print(f"Editando equipo ID {id_buscar} ({c['marca']} {c['modelo']})")
            
            nueva_marca = input("Nueva Marca (vacío para mantener): ").strip()
            nuevo_modelo = input("Nuevo Modelo (vacío para mantener): ").strip()
            print("¿Desea cambiar el estado?")
            nuevo_estado = seleccionar_estado()

            if nueva_marca: c["marca"] = nueva_marca
            if nuevo_modelo: c["modelo"] = nuevo_modelo
            if nuevo_estado: c["estado"] = nuevo_estado
            
            guardar_datos(data)
            print("Equipo actualizado correctamente.")
            return
    print("ID no encontrado.")

def eliminar_computador():
    data = cargar_datos()
    id_buscar = input("\nIngrese el ID del equipo a eliminar: ")
    
    original_count = len(data["computadores"])
    data["computadores"] = [c for c in data["computadores"] if str(c["id"]) != id_buscar]
    
    if len(data["computadores"]) < original_count:
        guardar_datos(data)
        print("Equipo eliminado del inventario.")
    else:
        print("ID no encontrado.")

def menu_computadores():
    while True:
        print("\n================================")
        print("   GESTIÓN DE COMPUTADORES")
        print("================================")
        print("1. Registrar Computador")
        print("2. Listar Inventario")
        print("3. Actualizar Computador")
        print("4. Eliminar Computador")
        print("5. Volver al Menú Principal")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            registrar_computador()
        elif opcion == "2":
            listar_computadores()
        elif opcion == "3":
            actualizar_computador()
        elif opcion == "4":
            eliminar_computador()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")