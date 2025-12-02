from fastapi import FastAPI
from app.models import Node

# Inicializamos la aplicación
# title y version aparecen en la documentación automática
app = FastAPI(
    title="ISP Node Manager API",
    description="API para gestión de nodos de red (Simulación TP Redes)",
    version="1.0.0"
)

@app.get("/")
def root():
    """Endpoint de bienvenida (Health Check)."""
    return {"system": "ISP Node Manager", "status": "running"}

# Endpoint de prueba para verificar que el modelo funciona
# (Lo borraremos después, es solo para que veas la magia de Pydantic hoy)
@app.post("/test-validation")
def test_validation(nodo: Node):
    """
    Envía un JSON aquí. Si cumple con el modelo Node, te lo devuelve.
    Si no, FastAPI te dará un error 422 detallado automáticamente.
    """
    return {"msg": "Nodo validado correctamente", "data": nodo}