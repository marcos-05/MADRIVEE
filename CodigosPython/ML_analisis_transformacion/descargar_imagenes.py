import os
import time
import csv
import cv2
import requests
import numpy as np
from datetime import datetime
from pathlib import Path
from ultralytics import YOLO

JSON_URL = "https://www.dgt.es/.content/.assets/json/camaras.json"

CAMERAS = {
    "169709": "https://infocar.dgt.es/etraffic/data/camaras/169709.jpg?t=1759834159649",
    "169708": "https://infocar.dgt.es/etraffic/data/camaras/169708.jpg?t=1759834159649",
    "826": "https://infocar.dgt.es/etraffic/data/camaras/826.jpg?t=1759834225500",
    "1160": "https://infocar.dgt.es/etraffic/data/camaras/1160.jpg?t=1759834275729",
    "1676": "https://infocar.dgt.es/etraffic/data/camaras/1676.jpg?t=1759834314977",
    "1690": "https://infocar.dgt.es/etraffic/data/camaras/1690.jpg?t=1759834314977",
    "696": "https://infocar.dgt.es/etraffic/data/camaras/696.jpg?t=1759834334403",
    "598": "https://infocar.dgt.es/etraffic/data/camaras/598.jpg?t=1759833949373",
    "972": "https://infocar.dgt.es/etraffic/data/camaras/972.jpg?t=1759834549446",
    "967": "https://infocar.dgt.es/etraffic/data/camaras/967.jpg?t=1759834616716",
    "866": "https://infocar.dgt.es/etraffic/data/camaras/866.jpg?t=1759834632512",
    "877": "https://infocar.dgt.es/etraffic/data/camaras/877.jpg?t=1759834647410",
    "169741": "https://infocar.dgt.es/etraffic/data/camaras/169741.jpg?t=1759834658332",
    "864": "https://infocar.dgt.es/etraffic/data/camaras/864.jpg?t=1759834676245",
    "971": "https://infocar.dgt.es/etraffic/data/camaras/971.jpg?t=1759834562471",
    "651": "https://infocar.dgt.es/etraffic/data/camaras/651.jpg?t=1759834201645",
    "771": "https://infocar.dgt.es/etraffic/data/camaras/771.jpg?t=1759836052767",
    "773": "https://infocar.dgt.es/etraffic/data/camaras/773.jpg?t=1759836066876",
    "926": "https://infocar.dgt.es/etraffic/data/camaras/926.jpg?t=1759836128476",
    "1010": "https://infocar.dgt.es/etraffic/data/camaras/1010.jpg?t=1759836140679",
    "1004": "https://infocar.dgt.es/etraffic/data/camaras/1004.jpg?t=1759836140679",
    "731": "https://infocar.dgt.es/etraffic/data/camaras/731.jpg?t=1759836179328",
    "1125": "https://infocar.dgt.es/etraffic/data/camaras/1125.jpg?t=1759836204192",
    "791": "https://infocar.dgt.es/etraffic/data/camaras/791.jpg?t=1759836223066",
    "799": "https://infocar.dgt.es/etraffic/data/camaras/799.jpg?t=1759836245366",
    "169372": "https://infocar.dgt.es/etraffic/data/camaras/169372.jpg?t=1759836024932",
    "634": "https://infocar.dgt.es/etraffic/data/camaras/634.jpg?t=1760080607575",
    "660": "https://infocar.dgt.es/etraffic/data/camaras/660.jpg?t=1760080639359",
    "668": "https://infocar.dgt.es/etraffic/data/camaras/668.jpg?t=1760080677092",
    "798": "https://infocar.dgt.es/etraffic/data/camaras/798.jpg?t=1760080721584",
    "866": "https://infocar.dgt.es/etraffic/data/camaras/866.jpg?t=1760081080580",
    "872": "https://infocar.dgt.es/etraffic/data/camaras/872.jpg?t=1760081121352",
    "868": "https://infocar.dgt.es/etraffic/data/camaras/868.jpg?t=1760081126624",
    "873": "https://infocar.dgt.es/etraffic/data/camaras/873.jpg?t=1760081077226",
    "1161": "https://infocar.dgt.es/etraffic/data/camaras/1161.jpg?t=1760081224769",
    "1162": "https://infocar.dgt.es/etraffic/data/camaras/1162.jpg?t=1760081228225",
    "1158": "https://infocar.dgt.es/etraffic/data/camaras/1158.jpg?t=1760081233373",
    "897": "https://infocar.dgt.es/etraffic/data/camaras/897.jpg?t=1760081239666",
    "174942": "https://infocar.dgt.es/etraffic/data/camaras/174942.jpg?t=1760081301918",
    "174943": "https://infocar.dgt.es/etraffic/data/camaras/174943.jpg?t=1760081369602",
    "174945": "https://infocar.dgt.es/etraffic/data/camaras/174945.jpg?t=1760081332946",
    "673": "https://infocar.dgt.es/etraffic/data/camaras/673.jpg?t=1760081474663",
    "677": "https://infocar.dgt.es/etraffic/data/camaras/677.jpg?t=1760081492738",
    "1097": "https://infocar.dgt.es/etraffic/data/camaras/1097.jpg?t=1760081497164",
    "705": "https://infocar.dgt.es/etraffic/data/camaras/705.jpg?t=1760081557152",
    "726": "https://infocar.dgt.es/etraffic/data/camaras/726.jpg?t=1760081590777",
    "175471": "https://infocar.dgt.es/etraffic/data/camaras/175471.jpg?t=1760174424650",
}

JSON_URL = "https://www.dgt.es/.content/.assets/json/camaras.json"

INTERVALO = 17.5 * 60

# Rutas relativas al proyecto (compatibles con cualquier máquina)
_BASE_DIR = Path(__file__).resolve().parent.parent.parent  # raíz del proyecto

DATASET_CSV = _BASE_DIR / "CodigosPython" / "datasets" / "1. datasetCompleto.csv"

CLASSES = ["car", "truck", "bus", "bike"]

def obtener_camaras_bbdd():
    from api import get_mysql_connection

    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id_zona FROM zonas")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [str(row["id_zona"]) for row in rows]

def obtener_siguiente_id(dataset_csv):
    if not dataset_csv.exists():
        return 1

    try:
        with open(dataset_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            ids = [int(row["id_entrada"]) for row in reader if row["id_entrada"].isdigit()]
            return max(ids) + 1 if ids else 1
    except Exception as e:
        print("No se pudo leer id_entrada, usando 1:", e)
        return 1

def cargar_json():
    import requests

    JSON_URL = "https://www.dgt.es/.content/.assets/json/camaras.json"

    try:
        r = requests.get(JSON_URL, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {str(c["id"]): c for c in data.get("camaras", [])}
    except Exception as e:
        print("Error JSON:", e)
        return {}

def calcular_ocupacion(result):
    if result.masks is None:
        return 0.0

    masks = result.masks.data.cpu().numpy()
    cls_ids = result.boxes.cls.cpu().numpy()

    combined = np.zeros(masks.shape[1:], dtype=bool)
    for i, cls in enumerate(cls_ids):
        if result.names[int(cls)] in CLASSES:
            combined |= masks[i] > 0.5

    return np.sum(combined) / combined.size


def nivel_ocupacion(area):
    if area < 0.02:
        return 0
    elif area < 0.07:
        return 1
    elif area < 0.15:
        return 2
    else:
        return 3


def procesar_camara_con_modelo(cam_id, url, cam_data, id_entrada, model):
    try:
        meta = cam_data.get(cam_id, {})
        carretera = meta.get("carretera", "")
        lat = meta.get("latitud", "")
        lon = meta.get("longitud", "")

        now = datetime.now()
        fecha = now.strftime("%Y-%m-%d")
        hora = now.strftime("%H:%M:%S")

        img = requests.get(url, timeout=10).content
        img_array = np.frombuffer(img, np.uint8)
        img_cv2 = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        result = model(img_cv2)[0]

        counts = {c: 0 for c in CLASSES}
        for box in result.boxes:
            cls = result.names[int(box.cls[0])]
            if cls in counts:
                counts[cls] += 1

        area = calcular_ocupacion(result)
        nivel = nivel_ocupacion(area)

        with open(DATASET_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                id_entrada,
                cam_id,
                carretera,
                lat,
                lon,
                fecha,
                hora,
                counts["car"],
                counts["truck"],
                counts["bus"],
                counts["bike"],
                sum(counts.values()),
                nivel
            ])

        print(f"{cam_id} | Vehículos: {sum(counts.values())} | Nivel: {nivel}")

    except Exception as e:
        print(f"Error cámara {cam_id}:", e)

def ejecutar_descarga():
    import csv
    from ultralytics import YOLO
    from pathlib import Path

    print("Ejecutando descarga manual...\n")

    _BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATASET_CSV = _BASE_DIR / "CodigosPython" / "datasets" / "1. datasetCompleto.csv"

    if not DATASET_CSV.exists():
        DATASET_CSV.parent.mkdir(parents=True, exist_ok=True)
        with open(DATASET_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id_entrada", "id_camara", "carretera", "latitud", "longitud",
                "fecha_descarga", "hora_descarga",
                "cars", "trucks", "buses", "bikes", "total", "nivel_ocupacion"
            ])

    model = YOLO("yolov8x-seg.pt")
    model.conf = 0.25

    id_entrada = obtener_siguiente_id(DATASET_CSV)
    cam_data = cargar_json()

    # 🔥 Obtener cámaras desde BBDD
    from api import get_mysql_connection

    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id_zona FROM zonas")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    ids_bbdd = [str(row["id_zona"]) for row in rows]

    for cam_id in ids_bbdd:

        cam = cam_data.get(cam_id)

        if not cam:
            continue

        url = cam.get("url") or cam.get("imagen")

        if not url:
            continue

        procesar_camara_con_modelo(
            cam_id,
            url,
            cam_data,
            id_entrada,
            model
        )

        id_entrada += 1

    print("Descarga finalizada\n")

'''
if __name__ == "__main__":
    main()
'''