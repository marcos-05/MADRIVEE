import xgboost as xgb
import joblib
import pandas as pd
import os

# ─── Cargar el modelo y el scaler UNA ÚNICA VEZ al arrancar la API ───
try:
    model = xgb.XGBClassifier()
    model.load_model(os.path.join("ModelosIA", "xgboost_model.json"))
    scaler = joblib.load(os.path.join("ModelosIA", "scaler.pkl"))
    cols_scaler = scaler.feature_names_in_
except Exception as e:
    print(f"⚠️ Error cargando modelo ML: {e}")
    model = None
    scaler = None

def hacer_prediccion(input_data):
    """
    Recibe un diccionario con las variables necesarias y devuelve la predicción.
    """
    if model is None or scaler is None:
        raise RuntimeError("El modelo ML no está cargado correctamente.")

    # Convertir diccionario de entrada a DataFrame de una fila
    data = pd.DataFrame([input_data])

    # Normalizar solo las columnas que tocan
    scaled = scaler.transform(data[cols_scaler])
    scaled_df = pd.DataFrame(scaled, columns=cols_scaler)

    # Columnas que no se normalizan
    extra = data.drop(columns=cols_scaler)

    # Unir todo
    data_final = pd.concat([scaled_df, extra], axis=1)

    # Asegurar orden correcto de columnas que espera XGBoost
    data_final = data_final[model.get_booster().feature_names]

    # Predecir (XGBoost devuelve un array, cogemos el primer elemento)
    pred_array = model.predict(data_final)
    
    # Convertir a entero estándar (puede salir como numpy.int32)
    return int(pred_array[0])
