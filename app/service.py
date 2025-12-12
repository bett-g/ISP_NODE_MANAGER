import json
import os
from typing import List
from app.models import Node

# Calculamos la ruta absoluta al archivo JSON (igual que en el loader)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "nodes.json")

def load_data() -> List[dict]:
    """Lee el JSON crudo del disco."""
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data: List[dict]):
    """Escribe la lista completa al disco (Persistencia)."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_nodes() -> List[Node]:
    """
    Obtiene todos los nodos y los convierte al modelo Pydantic 'Node'.
    Aquí simulamos que todos arrancan 'online' ya que el JSON original no tiene estado.
    """
    raw_data = load_data()
    nodes = []
    
    for item in raw_data:
        # Validamos y convertimos cada diccionario del JSON a un objeto Node
        # Si el JSON tiene campos extra, Pydantic los ignora si así se configura,
        # pero aquí los campos coinciden (id, nombre, provincia, centroide).
        # El campo 'status' tomará su valor por defecto ('online').
        node = Node(**item) 
        nodes.append(node)
        
    return nodes

# ... (imports y funciones anteriores load_data, save_data, get_nodes)

def create_node(new_node: Node) -> Node:
    """Agrega un nuevo nodo a la lista y guarda en disco."""
    nodes = get_nodes()
    
    # Validación de unicidad: No queremos IDs repetidos
    for node in nodes:
        if node.id == new_node.id:
            raise ValueError(f"El nodo con ID {new_node.id} ya existe.")
    
    # Convertimos el objeto Node a diccionario para guardarlo
    # model_dump() es el método moderno de Pydantic v2 (o .dict() en v1)
    nodes_data = [n.model_dump() for n in nodes]
    nodes_data.append(new_node.model_dump())
    
    save_data(nodes_data)
    return new_node

def delete_node(node_id: str) -> bool:
    """Elimina un nodo por ID. Retorna True si lo borró, False si no existía."""
    nodes = get_nodes()
    initial_count = len(nodes)
    
    # Filtramos la lista: dejamos todos los que NO sean el ID a borrar
    filtered_nodes = [n for n in nodes if n.id != node_id]
    
    if len(filtered_nodes) == initial_count:
        return False # No se borró nada
        
    # Guardamos la nueva lista
    nodes_data = [n.model_dump() for n in filtered_nodes]
    save_data(nodes_data)
    
    return True

