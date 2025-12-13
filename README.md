# ISP Node Manager

> **Proyecto Final - Redes de Datos (Tecnicatura en IA)**  
> Simulación de un sistema de gestión de infraestructura de red (Cliente-Servidor).

## Descripción

**ISP Node Manager** es una aplicación RESTful diseñada para simular la administración de nodos (antenas/sitios) de un Proveedor de Servicios de Internet. El sistema permite a los administradores de red provisionar, monitorear y decomisionar nodos distribuidos geográficamente.

El proyecto utiliza datos reales del **Gobierno de la República Argentina** (municipios) para simular la ubicación física de la infraestructura.

## Características principales

- **Arquitectura MVC:** separación clara entre modelos, lógica de negocio (servicio) y controladores (API).
- **API RESTful con FastAPI:** alto rendimiento y documentación automática (Swagger UI).
- **Persistencia JSON:** base de datos documental basada en archivos (simulación NoSQL).
- **Seguridad:** autenticación **HTTP Basic Auth** para operaciones críticas (escritura y borrado).
- **Rate limiting:** middleware personalizado para protección contra saturación (10 requests por minuto).
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
├── scripts/                # Herramientas DevOps
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

### 2. Levantar la API (servidor)

Mantener esta terminal abierta.

```powershell
python -m uvicorn app.main:app --reload
```

- URL base: http://127.0.0.1:8000  
- Documentación: http://127.0.0.1:8000/docs

### 3. Ejecutar el cliente

En una nueva terminal (activar el entorno virtual previamente):

```powershell
python client/cli.py
```

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

**Nota:** la API posee un límite de seguridad de 10 peticiones por minuto por IP. Al superarlo, retorna HTTP 429.

---

## Ejecución en red local (modo laboratorio)

### Comandos resumidos

```powershell
ipconfig
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Notas:
- Utilizar la dirección IPv4 de la PC servidor para acceder desde otros equipos.
- Permitir el acceso cuando Windows Firewall solicite autorización (red privada y pública).
- El servicio escucha en el puerto 8000.

