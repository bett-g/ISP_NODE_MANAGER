# ISP Node Manager

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688?style=for-the-badge&logo=fastapi)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> **Proyecto Final - Redes de Datos (Tecnicatura en IA)**
> Simulación de un sistema de gestión de infraestructura de red (Cliente-Servidor).

## Descripción

**ISP Node Manager** es una aplicación RESTful diseñada para simular la administración de nodos (antenas/sitios) de un Proveedor de Servicios de Internet. El sistema permite a los administradores de red provisionar, monitorear y decomisionar nodos distribuidos geográficamente.

El proyecto utiliza datos reales del **Gobierno de la República Argentina** (Municipios) para simular la ubicación física de la infraestructura.

### Características Principales

* **Arquitectura MVC:** Separación clara entre Modelos, Lógica de Negocio (Servicio) y Controladores (API).
* **API RESTful con FastAPI:** Alto rendimiento y documentación automática (Swagger UI).
* **Persistencia JSON:** Base de datos documental basada en archivos (NoSQL simulation).
* **Seguridad:** Autenticación **HTTP Basic Auth** para operaciones críticas (Escritura/Borrado).
* **Rate Limiting:** Middleware personalizado para protección contra ataques de fuerza bruta o saturación (DDoS mitigation).
* **Validación de Datos:** Uso de **Pydantic** para asegurar la integridad de la información.

---

## Arquitectura del Proyecto

```text
isp-node-manager/
├── app/                    # Backend (FastAPI)
│   ├── main.py             # Entry point & Rutas
│   ├── models.py           # Esquemas de datos (Pydantic)
│   ├── service.py          # Lógica de negocio (CRUD JSON)
│   ├── auth.py             # Seguridad (Basic Auth)
│   └── rate_limiter.py     # Middleware de tráfico
├── client/                 # Cliente (Consola)
│   └── cli.py              # Interfaz de usuario CLI
├── data/                   # Persistencia
│   └── nodes.json          # DB (Ignorado en git)
├── scripts/                # Herramientas DevOps
│   └── data_loader.py      # ETL inicial de datos
├── requirements.txt        # Dependencias
└── README.md               # Documentación
