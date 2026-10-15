# ─────────────────────────────────────────────────────────────────
# MADRIVE — Dockerfile
# Imagen base: Python 3.10 slim (mínimo peso, compatible con YOLO y XGBoost)
# ─────────────────────────────────────────────────────────────────

FROM python:3.10-slim

# Evita que Python genere archivos .pyc y que el output salga en tiempo real (sin buffer)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias para OpenCV/YOLO y mysql
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    gcc \
    default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# 1. Copiar solo el requirements.txt primero (aprovecha la caché de Docker)
#    Si no cambias las librerías, Docker no las reinstala en cada build
COPY requirements.txt .

# 2. Instalar todas las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar todo el código del proyecto al contenedor
COPY . .

# Exponer el puerto que usa Flask
EXPOSE 5000

# Comando de arranque: lanzar la API Flask
CMD ["python", "api.py"]
