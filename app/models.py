from pydantic import BaseModel, Field
from typing import Optional

# --- Sub-modelos (Objetos anidados) ---
# Sirven para validar los objetos dentro del objeto principal

class Coordinates(BaseModel):
    lat: float = Field(..., description="Latitud geográfica de la antena")
    lon: float = Field(..., description="Longitud geográfica de la antena")

class Province(BaseModel):
    id: str
    nombre: str

# --- Modelo Principal ---

class Node(BaseModel):
    # Usamos Field para añadir documentación automática a la API
    id: str = Field(..., description="Identificador único del Nodo (ID Municipio)")
    nombre: str = Field(..., description="Nombre del Nodo o Sitio")
    provincia: Province
    centroide: Coordinates
    
    # Añadimos un campo extra que NO viene en el JSON original pero que nos sirve para simular el estado de la red.
    # default="online" significa que si no se envía, se asume online.
    status: str = Field(default="online", description="Estado operativo: online, offline, maintenance")

    class Config:
        # Esto genera un ejemplo en la documentación automática
        json_schema_extra = {
            "example": {
                "id": "060588",
                "nombre": "Nodo Nueve de Julio",
                "provincia": {
                    "id": "06",
                    "nombre": "Buenos Aires"
                },
                "centroide": {
                    "lat": -35.44,
                    "lon": -60.88
                },
                "status": "online"
            }
        }