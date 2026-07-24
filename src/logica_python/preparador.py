# Importaciones
from __future__ import annotations
from typing import List, Optional
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class PreparadorDatos:
    """
    Clase encargada de preparar los datos para el entrenamiento del modelo.
    """

    def __init__(
        self,
        columna_objetivo: str,
        columnas_fecha: Optional[List[str]] = None,
        columnas_categoricas: Optional[List[str]] = None,
        columnas_numericas: Optional[List[str]] = None,
        columnas_eliminar: Optional[List[str]] = None,
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> None:

        self.columna_objetivo = columna_objetivo
        self.columnas_fecha = columnas_fecha or []
        self.columnas_categoricas = columnas_categoricas or []
        self.columnas_numericas = columnas_numericas or []
        self.columnas_eliminar = columnas_eliminar or []

        self.test_size = test_size
        self.random_state = random_state

    def validar_columnas(self, df: pd.DataFrame) -> None:
        """
        Verifica que todas las columnas existan.
        """

        columnas = (
            self.columnas_fecha
            + self.columnas_categoricas
            + self.columnas_numericas
            + self.columnas_eliminar
            + [self.columna_objetivo]
        )

        faltantes = [c for c in columnas if c not in df.columns]

        if faltantes:
            raise ValueError(
                f"Las siguientes columnas no existen en el DataFrame: {faltantes}"
            )

    def convertir_fechas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convierte las columnas de fecha a datetime.
        """

        for columna in self.columnas_fecha:
            df[columna] = pd.to_datetime(
                df[columna],
                errors="coerce"
            )

        return df

    def crear_variables_fecha(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Genera variables temporales a partir de las columnas de fecha.
        """

        for columna in self.columnas_fecha:

            anio = f"{columna}_anio"
            mes = f"{columna}_mes"
            dia = f"{columna}_dia"

            df[anio] = df[columna].dt.year
            df[mes] = df[columna].dt.month
            df[dia] = df[columna].dt.day

            for nueva in [anio, mes, dia]:
                if nueva not in self.columnas_numericas:
                    self.columnas_numericas.append(nueva)

        return df

    def eliminar_columnas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Elimina columnas no utilizadas.
        """

        columnas = [
            columna
            for columna in self.columnas_eliminar
            if columna in df.columns
        ]

        return df.drop(columns=columnas)

    def separar_variables(
        self,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.Series]:
        """
        Separa las variables predictoras y la variable objetivo.
        """

        X = df.drop(columns=[self.columna_objetivo])

        y = df[self.columna_objetivo]

        return X, y

    def obtener_preprocesador(self) -> ColumnTransformer:
        """
        Construye el preprocesador de Scikit-Learn.
        """

        pipeline_numerico = Pipeline(
            steps=[
                ("scaler", StandardScaler())
            ]
        )

        pipeline_categorico = Pipeline(
            steps=[
                (
                    "encoder",
                    OneHotEncoder(
                        handle_unknown="ignore"
                    )
                )
            ]
        )

        preprocesador = ColumnTransformer(
            transformers=[
                (
                    "numericas",
                    pipeline_numerico,
                    self.columnas_numericas
                ),
                (
                    "categoricas",
                    pipeline_categorico,
                    self.columnas_categoricas
                )
            ],
            remainder="drop"
        )

        return preprocesador
    
    def preparar(
        self,
        df: pd.DataFrame
    ):

        df = df.copy()
        self.validar_columnas(df)
        df = self.convertir_fechas(df)
        df = self.crear_variables_fecha(df)
        df = self.eliminar_columnas(df)
        X, y = self.separar_variables(df)
        preprocesador = self.obtener_preprocesador()
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=y
        )
        df_train = df.loc[X_train.index].copy()
        df_test = df.loc[X_test.index].copy()
        return (
            X_train,
            X_test,
            y_train,
            y_test,
            df_train,
            df_test,
            preprocesador
        )