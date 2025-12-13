from fastapi import FastAPI, HTTPException, Query, Depends, status 
from typing import List
from app.models import Node
from app import service, auth # Importamos nuestro nuevo módulo de seguridad
from app.rate_limiter import RateLimiter

app = FastAPI(
    title="ISP Node Manager API",
    description="API para gestión de nodos de red (Simulación TP Redes)",
    version="1.0.0"
)

public_limiter = RateLimiter(requests_limit=3, time_window=10)

@app.get("/")
def root():
    return {"system": "ISP Node Manager", "status": "active", "docs": "/docs"}

# --- ENDPOINTS PÚBLICOS ---

@app.get("/nodes", response_model=List[Node], dependencies=[Depends(public_limiter)])
def list_nodes(limit: int = Query(10, ge=1, le=100)):
    """
    Obtiene el listado de nodos (Antenas).
    
    - **limit**: Filtra la cantidad de resultados (Por defecto 10 para no saturar).
    """
    all_nodes = service.get_nodes()
    
    # Implementamos una paginación simple (Slicing de listas)
    return all_nodes[:limit]

@app.get("/nodes/{node_id}", response_model=Node, dependencies=[Depends(public_limiter)])
def get_node_by_id(node_id: str):
    """Busca un nodo específico por su ID."""
    all_nodes = service.get_nodes()
    
    # Búsqueda lineal
    for node in all_nodes:
        if node.id == node_id:
            return node
            
    raise HTTPException(status_code=404, detail="Nodo no encontrado")

@app.post("/nodes", status_code=status.HTTP_201_CREATED, response_model=Node)
def create_node(node: Node, username: str = Depends(auth.get_current_username)):
    """
    [ADMIN] Provisionar un nuevo nodo.
    Requiere Auth Basic.
    """
    try:
        return service.create_node(node)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/nodes/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_node(node_id: str, username: str = Depends(auth.get_current_username)):
    """
    [ADMIN] Decomisionar (eliminar) un nodo.
    Requiere Auth Basic.
    """
    success = service.delete_node(node_id)
    if not success:
        raise HTTPException(status_code=404, detail="Nodo no encontrado")
    
    return None # 204 No Content no devuelve cuerpo

