# Importaciones
from __future__ import annotations
import pandas as pd
from sklearn.pipeline import Pipeline


class Estimador:
    """
    Clase encargada de generar estimaciones a partir de un
    modelo de clasificación.
    """
    def __init__(self) -> None:
        pass

    def estimar(self, pipeline: Pipeline, X: pd.DataFrame, 
                df_original: pd.DataFrame, columna_valor: str,
                nombre_probabilidad: str = "probabilidad",
                nombre_valor_esperado: str = "valor_esperado") -> pd.DataFrame:

        if columna_valor not in df_original.columns:
            raise ValueError(
                f"La columna '{columna_valor}' no existe."
            )

        probabilidades = pipeline.predict_proba(X)[:, 1]
        resultado = df_original.copy()
        resultado[nombre_probabilidad] = probabilidades
        resultado[nombre_valor_esperado] = (resultado[columna_valor] * resultado[nombre_probabilidad])

        return resultado

    def resumir(self,df: pd.DataFrame, columna_grupo: str, columna_valor: str = "valor_esperado") -> pd.DataFrame:

        if columna_grupo not in df.columns:
            raise ValueError(
                f"La columna '{columna_grupo}' no existe."
            )

        if columna_valor not in df.columns:
            raise ValueError(
                f"La columna '{columna_valor}' no existe."
            )
        
        resumen = (
            df.groupby(columna_grupo, as_index=False)
            .agg({columna_valor: "sum"})
        )

        return resumen

    def porcentaje(
        self,
        df: pd.DataFrame,
        columna_valor: str,
        columna_total: str,
        nombre_columna: str = "porcentaje") -> pd.DataFrame:

        if columna_valor not in df.columns:
            raise ValueError(
                f"La columna '{columna_valor}' no existe."
            )

        if columna_total not in df.columns:
            raise ValueError(
                f"La columna '{columna_total}' no existe."
            )

        resultado = df.copy()

        resultado[nombre_columna] = (
            resultado[columna_valor]
            / resultado[columna_total]) * 100

        return resultado