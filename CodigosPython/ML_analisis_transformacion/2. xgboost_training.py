import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, balanced_accuracy_score, f1_score
from xgboost import XGBClassifier
from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parent.parent.parent
output_csv   = _BASE_DIR / "CodigosPython" / "datasets" / "2. datasetNormalizado.csv"

df = pd.read_csv(output_csv, encoding="utf-8")

X = df.drop(columns=["id_entrada", "nivel_ocupacion"])
y = df["nivel_ocupacion"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = XGBClassifier(
    objective="multi:softprob",
    num_class=4,
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="mlogloss",
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Matriz de confusión:")
print(confusion_matrix(y_test, y_pred))

print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

model.save_model("xgboost_model.json")