def normalizar_dataset():
    import pandas as pd
    import joblib
    from sklearn.preprocessing import MinMaxScaler, LabelEncoder
    from pathlib import Path
    import os

    _BASE_DIR = Path(__file__).resolve().parent.parent.parent
    metadata_csv = _BASE_DIR / "CodigosPython" / "datasets" / "1. datasetCompleto.csv"
    output_csv   = _BASE_DIR / "CodigosPython" / "datasets" / "2. datasetNormalizado.csv"

    model_dir = _BASE_DIR / "ModelosIA"
    model_dir.mkdir(exist_ok=True)

    scaler_path = model_dir / "scaler.pkl"
    encoder_path = model_dir / "encoder.pkl"

    df = pd.read_csv(metadata_csv, encoding='utf-8')

    if output_csv.exists():
        df_existing = pd.read_csv(output_csv)
        df = df.iloc[len(df_existing):]

    # Separar fecha y hora
    df[['anio', 'mes', 'dia']] = df['fecha_descarga'].str.split('-', expand=True)
    df[['hora', 'minuto', 'segundo']] = df['hora_descarga'].str.split(':', expand=True)

    # Extraer letra y número de carretera
    df['carretera_letra'] = df['carretera'].str.extract(r'([A-Z]+)')
    df['carretera_numero'] = df['carretera'].str.extract(r'(\d+)')

    # Convertir columnas numéricas a int
    df[['anio','mes','dia','hora','minuto','segundo','carretera_numero']] = df[['anio','mes','dia','hora','minuto','segundo','carretera_numero']].astype(int)

    # One-hot encoding para la letra de la carretera
    df = pd.get_dummies(df, columns=['carretera_letra'])
    cols_one_hot_letras = ['carretera_letra_A', 'carretera_letra_M', 'carretera_letra_N']
    for col in cols_one_hot_letras:
        if col not in df.columns:
            df[col] = 0
    df[cols_one_hot_letras] = df[cols_one_hot_letras].astype(int)

    # Crear categorías de franjas horarias
    def franja_horaria(hora):
        if 6 <= hora <= 11:
            return 'mañana'
        elif 12 <= hora <= 17:
            return 'tarde'
        elif 18 <= hora <= 23:
            return 'noche'
        else:
            return 'madrugada'

    df['franja_horaria'] = df['hora'].apply(franja_horaria)

    df = pd.get_dummies(df, columns=['franja_horaria'])
    cols_one_hot_franjas = ['franja_horaria_mañana','franja_horaria_noche','franja_horaria_tarde', 'franja_horaria_madrugada']
    for col in cols_one_hot_franjas:
        if col not in df.columns:
            df[col] = 0
    df[cols_one_hot_franjas] = df[cols_one_hot_franjas].astype(int)

    df = df.drop(columns=['cars','trucks','buses','bikes','total','carretera','fecha_descarga','hora_descarga','segundo'])

    variables = ['id_camara','latitud','longitud','anio','mes','dia','hora','minuto','carretera_numero']

    if not scaler_path.exists() or not encoder_path.exists():
        label_encoder = LabelEncoder()
        scalerX = MinMaxScaler()

        df['carretera_numero'] = label_encoder.fit_transform(df['carretera_numero'])
        df[variables] = scalerX.fit_transform(df[variables])

        joblib.dump(scalerX, scaler_path)
        joblib.dump(label_encoder, encoder_path)

        df = df.sample(frac=1).reset_index(drop=True)

        df.to_csv(output_csv, index=False)

    else:
        scalerX = joblib.load(scaler_path)
        label_encoder = joblib.load(encoder_path)

        df['carretera_numero'] = df['carretera_numero'].apply(
            lambda x: label_encoder.transform([x])[0] if x in label_encoder.classes_ else -1
        )
        df[variables] = scalerX.transform(df[variables])

        df = df.sample(frac=1).reset_index(drop=True)

        if not output_csv.exists():
            df.to_csv(output_csv, index=False)
        else:
            df.to_csv(output_csv, mode='a', header=False, index=False)