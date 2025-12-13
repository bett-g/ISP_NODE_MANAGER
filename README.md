# ISP Node Manager

> **Proyecto Final - Redes de Datos (Tecnicatura en IA)**  
> Simulación de un sistema de gestión de infraestructura de red (Cliente-Servidor).

## Descripción

**ISP Node Manager** es una aplicación RESTful diseñada para simular la administración de nodos (antenas/sitios) de un Proveedor de Servicios de Internet. El sistema permite a los administradores de red provisionar, monitorear y decomisionar nodos distribuidos geográficamente.

El proyecto utiliza datos reales del **Gobierno de la República Argentina** (municipios) con aproximadamente 2000 registros para simular la ubicación física de la infraestructura.

## Características principales

- **Arquitectura MVC:** separación clara entre modelos, lógica de negocio (servicio) y controladores (API).
- **API RESTful con FastAPI:** alto rendimiento y documentación automática (Swagger UI).
- **Persistencia JSON:** base de datos documental basada en archivos (simulación NoSQL).
- **Seguridad:** autenticación **HTTP Basic Auth** para operaciones críticas (escritura y borrado).
- **Rate limiting:** middleware personalizado para protección contra saturación.
- **Validación de datos:** uso de **Pydantic** para asegurar la integridad de la información.

---

## Arquitectura del proyecto

```text
isp-node-manager/
├── app/                    # Backend (FastAPI)
│   ├── main.py             # Entry point y rutas
│   ├── models.py           # Esquemas de datos (Pydantic)
│   ├── service.py          # Lógica de negocio (CRUD JSON)
│   ├── auth.py             # Seguridad (Basic Auth)
│   └── rate_limiter.py     # Middleware de tráfico
├── client/                 # Cliente (consola)
│   └── cli.py              # Interfaz de usuario CLI
├── data/                   # Persistencia
│   └── nodes.json          # Base de datos (ignorada en git)
├── scripts/                # Herramientas de poblado
│   └── data_loader.py      # ETL inicial de datos
├── requirements.txt        # Dependencias
└── README.md               # Documentación
```

---

## Guía de despliegue rápido (cheat sheet)

Seguir los comandos en orden para levantar el entorno completo en Windows (PowerShell).

### 1. Configuración inicial (solo la primera vez)

```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python scripts/data_loader.py
```

### 2. Levantar la API (servidor área local)

Mantener esta terminal abierta.

```powershell
ipconfig
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- URL base: http://127.0.0.1:8000  
- Documentación: http://127.0.0.1:8000/docs
- Configurar o deshabilitar Firewall (red privada y pública).


### 3. Ejecutar el cliente

En la terminal de otra PC (activar el entorno virtual previamente):

```powershell
python client/cli.py
```

- Utilizar la dirección IPv4 de la PC servidor para acceder a la API desde otro equipo en la red.

---

## Referencia de la API

Credenciales de administrador:

- Usuario: `admin`
- Contraseña: `admin123`

| Método | Endpoint        | Descripción                          | Auth |
|--------|-----------------|--------------------------------------|------|
| GET    | /nodes          | Lista los nodos (paginado)            | No   |
| GET    | /nodes/{id}     | Detalle de un nodo específico         | No   |
| POST   | /nodes          | Crea un nuevo nodo                    | Sí   |
| DELETE | /nodes/{id}     | Elimina un nodo existente             | Sí   |

**Nota:** la API posee un límite de seguridad de 5 peticiones cada 30 segundos por IP. Al superarlo, retorna HTTP 429.

---


