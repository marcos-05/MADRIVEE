# MADRIVEE · Análisis de congestión en Madrid

**Proyecto universitario desarrollado en equipo.** Esta es mi copia personal para mostrar el trabajo completo y explicar con claridad mi aportación. El [repositorio grupal original](https://github.com/RickVicente/Proyecto-de-Computaci-n-I) permanece independiente.

MADRIVEE utiliza imágenes de cámaras públicas de la DGT para estimar el nivel de tráfico y mostrarlo en un mapa. El sistema también permite consultar una predicción para una cámara y una fecha/hora, y guardar un historial de esas consultas.

> **English summary:** Team project that combines public traffic-camera data, computer vision and a congestion classifier with a Flask API, MariaDB and a web map. My work focused on the database, backend API and integration of the application.

## Cómo funciona

```mermaid
flowchart LR
    DGT[Cámaras y metadatos DGT] --> ETL[Descarga y preparación de datos]
    ETL --> YOLO[YOLOv8: vehículos y ocupación visual]
    YOLO --> DS[Datos de entrenamiento]
    DS --> XGB[XGBoost: nivel de congestión]
    XGB --> API[API Flask]
    API <--> DB[(MariaDB: usuarios, zonas, predicciones)]
    API --> UI[Mapa y vistas web]
```

Los cuatro niveles que muestra la aplicación son **fluido**, **denso**, **atasco** y **muy congestionado**. YOLO analiza las imágenes; XGBoost utiliza los datos preparados para clasificar la congestión. La API conecta esos módulos con la base de datos y la interfaz.

## Mi aportación

- Diseño e implementación de la base de datos para usuarios, zonas/cámaras e historial de predicciones.
- Desarrollo e integración de la API Flask: acceso a datos, registro e inicio de sesión, consulta de cámaras, predicciones y registros.
- Integración del backend con las vistas y resolución de conflictos de integración durante el trabajo en equipo.

**Créditos del equipo:** el desarrollo de los modelos de visión y clasificación correspondió principalmente a Ricardo. El mapa y las vistas fueron un trabajo compartido por otros integrantes; esta copia conserva el código del proyecto para que se entienda la solución completa. Los nombres y el historial de contribuciones pueden consultarse en el [repositorio grupal](https://github.com/RickVicente/Proyecto-de-Computaci-n-I). No presento el entrenamiento de YOLO o XGBoost como una contribución individual mía.

## Contenido del repositorio

| Ruta | Función |
| --- | --- |
| [`api.py`](api.py) | API Flask y conexión con base de datos, frontend y modelos. |
| [`init.sql`](init.sql) | Esquema SQL y ubicaciones de cámaras públicas de ejemplo. |
| [`CodigosPython/`](CodigosPython/) | Descarga, transformación, análisis de imágenes y entrenamiento. |
| [`ModelosIA/`](ModelosIA/) | Artefactos pequeños del clasificador y preprocesamiento. |
| Archivos `.html` | Inicio de sesión, registro, mapa y vistas de usuario/administración. |
| [`docker-compose.yml`](docker-compose.yml) | Arranque local de API y MariaDB. |

La copia **no incluye** la base de datos de usuarios, contraseñas reales, imágenes descargadas, vídeos de demostración, archivos compilados ni el peso YOLO `yolov8x-seg.pt` (aprox. 144 MB). El fichero SQL contiene solo la estructura y metadatos de cámaras públicas. Las claves de la API y de MariaDB se configuran mediante variables de entorno; no hay valores de producción en el repositorio.

## Probarlo en local

Requiere Docker y Docker Compose. Copia [`.env.example`](.env.example) a `.env` y asigna valores propios a las tres variables. Después:

```bash
docker compose up --build
```

La aplicación quedará disponible en `http://localhost:5000`. Puedes registrarte desde la interfaz. La visualización y descarga de imágenes necesitan acceso a los servicios públicos de la DGT. El análisis visual necesita `yolov8x-seg.pt`; al usar esa función, Ultralytics puede obtener el peso si está disponible en su origen oficial, o puedes situarlo en la raíz del proyecto para una ejecución local.

El proyecto es un **prototipo académico**. Antes de usarlo en producción habría que sustituir el hash SHA-256 de contraseñas por un algoritmo específico para contraseñas, reforzar la validación y los permisos de los endpoints, añadir pruebas automatizadas y revisar el tratamiento de los datos de las cámaras. Las modificaciones de esta copia se limitan a retirar datos privados, separar la configuración sensible y evitar algunos accesos no autorizados evidentes.

## Fuente de datos y alcance

Los metadatos e imágenes provienen de las cámaras públicas de la [Dirección General de Tráfico](https://www.dgt.es/). Las predicciones reflejan un ejercicio universitario y no deben utilizarse para decisiones de circulación en tiempo real.
