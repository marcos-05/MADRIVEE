import numpy as np
from ultralytics import YOLO
import os

model = None


def get_model():
    global model
    if model is None:
        model = YOLO(os.getenv("MADRIVEE_YOLO_WEIGHTS", "yolov8x-seg.pt"))
        model.conf = 0.25
    return model

class_names = ["car", "truck", "bus", "bike"]

def calcular_ocupacion_visual(result):
    masks = result.masks
    if masks is None:
        return 0.0

    mask_array = masks.data.cpu().numpy()
    cls_ids = result.boxes.cls.cpu().numpy()

    combined_mask = np.zeros(mask_array.shape[1:], dtype=bool)

    for i, cls_id in enumerate(cls_ids):
        cls_name = result.names[int(cls_id)]
        if cls_name in class_names:
            combined_mask |= mask_array[i] > 0.5

    return np.sum(combined_mask) / combined_mask.size

def nivel_ocupacion_por_area(area_ratio):
    if area_ratio < 0.02:
        return 0
    elif area_ratio < 0.07:
        return 1
    elif area_ratio < 0.15:
        return 2
    else:
        return 3

def calcular_nivel_trafico(img_path):
    result = get_model()(img_path)[0]

    area_ratio = calcular_ocupacion_visual(result)
    nivel = nivel_ocupacion_por_area(area_ratio)

    return nivel, area_ratio
