# Importaciones
from __future__ import annotations
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

class Evaluador:
    """
    Clase encargada de evaluar modelos de clasificación.
    """
    def __init__(self) -> None:
        pass

    def accuracy(self, y_real: pd.Series, y_pred: pd.Series) -> float:
        return float(accuracy_score(y_real, y_pred))

    def precision(self, y_real: pd.Series, y_pred: pd.Series) -> float:
        return float(precision_score(y_real, y_pred))

    def recall(self, y_real: pd.Series, y_pred: pd.Series) -> float:
        return float(recall_score(y_real, y_pred))

    def f1(self, y_real: pd.Series, y_pred: pd.Series) -> float:
        return float(f1_score(y_real, y_pred))

    def roc_auc(self, y_real: pd.Series, probabilidades: pd.Series) -> float:
        return float(roc_auc_score(y_real, probabilidades))

    def matriz_confusion(self, y_real: pd.Series, y_pred: pd.Series):
        return confusion_matrix(y_real, y_pred)

    def reporte(self, y_real: pd.Series, y_pred: pd.Series) -> str:
        return str(classification_report(y_real, y_pred))
    
    def evaluar(self, y_real: pd.Series, y_pred: pd.Series, probabilidades) -> dict:
        return {
            "accuracy": self.accuracy(y_real, y_pred),
            "precision": self.precision(y_real, y_pred),
            "recall": self.recall(y_real,y_pred),
            "f1": self.f1(y_real,y_pred),
            "roc_auc": self.roc_auc(y_real,probabilidades),
            "matriz_confusion": self.matriz_confusion(y_real, y_pred),
            "classification_report":self.reporte(y_real,y_pred)
        }