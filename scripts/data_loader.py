import requests
import json
import os
import sys

# URL oficial del dataset
DATA_URL = "https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.4/download/municipios.json"

# Ruta donde guardaremos la "Base de Datos"
# Usamos rutas relativas para que funcione en cualquier OS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "nodes.json")

def ensure_directory_exists(path):
    """Crea el directorio si no existe (Práctica DevOps: Idempotencia)."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directorio creado: {path}")

def fetch_and_analyze_data():
    print(f"Iniciando descarga desde: {DATA_URL}...")
    
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status() # Lanza error si no es 200 OK
        
        data = response.json()
        
        # El JSON de gobierno suele venir envuelto en una clave raíz, a veces 'municipios'
        # Vamos a verificar eso.
        lista_municipios = data.get('municipios', [])
        total = data.get('cantidad', 0)

        print(f"Descarga exitosa. Total de registros detectados: {total}")
        
        if not lista_municipios:
            print("Alerta: La lista de municipios parece vacía o el formato cambió.")
            return

        # Análisis de Estructura (Schema Discovery)
        print("\n---ANÁLISIS DE ESTRUCTURA (Primer Elemento) ---")
        primer_nodo = lista_municipios[0]
        print(json.dumps(primer_nodo, indent=4, ensure_ascii=False))
        print("---------------------------------------------------\n")

        # Guardado en disco
        ensure_directory_exists(DATA_DIR)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(lista_municipios, f, indent=4, ensure_ascii=False)
        
        print(f"Base de datos inicial guardada en: {OUTPUT_FILE}")
        print("Listo para usar en el Servidor FastAPI.")

    except requests.exceptions.RequestException as e:
        print(f"Error de red: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: La respuesta no es un JSON válido.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_and_analyze_data()
    