
# Importaciones
from __future__ import annotations
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

class Modelo:
    """
    Clase encargada de entrenar un modelo previamente preparado.
    """

    def __init__(self, modelo: BaseEstimator | None = None) -> None:
        self.modelo = modelo if modelo else LogisticRegression(max_iter=1000)
        self.pipeline: Pipeline | None = None

    def entrenar(self, X_train: pd.DataFrame, y_train: pd.Series, preprocesador: ColumnTransformer) -> None:
        """
        Entrena el modelo utilizando los datos de entrenamiento.
        """
        self.pipeline = Pipeline(
            steps=[
                ("preprocesador", preprocesador),
                ("modelo", self.modelo)
            ]
        )

        self.pipeline.fit(
            X_train,
            y_train
        )

    def predecir(self, X: pd.DataFrame):
        if self.pipeline is None:
            raise ValueError(
                "El modelo aún no ha sido entrenado."
            )
        return self.pipeline.predict(X)

    def predecir_probabilidades(self, X: pd.DataFrame):
        if self.pipeline is None:
            raise ValueError(
                "El modelo aún no ha sido entrenado."
            )
        return self.pipeline.predict_proba(X)

    def obtener_pipeline(self):
        return self.pipeline

    def resumen(self, X_train: pd.DataFrame, X_test: pd.DataFrame):
        return {
            "modelo": self.modelo.__class__.__name__,
            "observaciones_entrenamiento": len(X_train),
            "observaciones_prueba": len(X_test),
            "variables": X_train.shape[1]
        }