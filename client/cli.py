import requests
import sys
import getpass

API_URL = "http://localhost:8000"

def get_credentials():
    print("--- Autenticacion Requerida ---")
    username = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")
    return (username, password)

def print_error(response):
    if response.status_code == 429:
        print("AVISO: El servidor esta ocupado, intente nuevamente en unos segundos.")
    elif response.status_code == 401:
        print("Error: Credenciales invalidas.")
    elif response.status_code == 404:
        print("Error: Nodo no encontrado.")
    else:
        print(f"Error desconocido: {response.status_code}")

def list_nodes():
    try:
        response = requests.get(f"{API_URL}/nodes")
        if response.status_code == 200:
            nodes = response.json()
            print("\n--- Listado de Nodos ---")
            for node in nodes:
                print(f"[{node['id']}] {node['nombre']} - {node['status']}")
        else:
            print_error(response)
    except requests.exceptions.RequestException:
        print("Error: No se pudo conectar al servidor.")

def get_node_details():
    node_id = input("Ingrese ID del Nodo: ")
    try:
        response = requests.get(f"{API_URL}/nodes/{node_id}")
        if response.status_code == 200:
            node = response.json()
            print("\n--- Detalle del Nodo ---")
            print(f"ID: {node['id']}")
            print(f"Nombre: {node['nombre']}")
            print(f"Estado: {node['status']}")
            print(f"Provincia: {node['provincia']['nombre']} (ID: {node['provincia']['id']})")
            print(f"Coordenadas: Lat {node['centroide']['lat']}, Lon {node['centroide']['lon']}")
        else:
            print_error(response)
    except requests.exceptions.RequestException:
        print("Error: No se pudo conectar al servidor.")

def create_node():
    auth = get_credentials()
    
    print("\n--- Crear Nuevo Nodo ---")
    node_id = input("ID: ")
    name = input("Nombre: ")
    prov_name = input("Nombre de Provincia: ")
    
    # Simple validacion para lat/lon
    try:
        lat = float(input("Latitud: "))
        lon = float(input("Longitud: "))
    except ValueError:
        print("Error: Latitud y Longitud deben ser numeros.")
        return

    payload = {
        "id": node_id,
        "nombre": name,
        "provincia": {
            "id": "00", # Hardcoded as per prompt implication (or user didn't specify asking for ID, just Name, but API needs ID. I'll prompt for 00 or maybe I should ask? Prompt said "Name, Province Name". I will use 00 as placeholder or ask? "Province Name" was requested. I will default ID to "00" as example showed "id": "00")
            "nombre": prov_name
        },
        "centroide": {
            "lat": lat,
            "lon": lon
        },
        "status": "online"
    }

    try:
        response = requests.post(f"{API_URL}/nodes", json=payload, auth=auth)
        if response.status_code == 201:
            print("Nodo creado exitosamente.")
        else:
            print_error(response)
    except requests.exceptions.RequestException:
        print("Error: No se pudo conectar al servidor.")

def delete_node():
    auth = get_credentials()
    node_id = input("Ingrese ID del Nodo a eliminar: ")
    
    try:
        response = requests.delete(f"{API_URL}/nodes/{node_id}", auth=auth)
        if response.status_code == 204:
            print("Nodo eliminado exitosamente.")
        else:
            print_error(response)
    except requests.exceptions.RequestException:
        print("Error: No se pudo conectar al servidor.")

def main():
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Listar Nodos")
        print("2. Ver Detalle de un Nodo")
        print("3. Crear Nodo")
        print("4. Eliminar Nodo")
        print("5. Salir")
        
        choice = input("Seleccione una opcion: ")
        
        if choice == '1':
            list_nodes()
        elif choice == '2':
            get_node_details()
        elif choice == '3':
            create_node()
        elif choice == '4':
            delete_node()
        elif choice == '5':
            print("Saliendo...")
            break
        else:
            print("Opcion invalida.")

if __name__ == "__main__":
    main()
