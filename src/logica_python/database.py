# Importaciones
import sqlite3 as sql
import pandas as pd

class Database:
    """
    Clase encargada de realizar la conexion a la base de datos y ejecutar consultas SQL.
    Atributos:
        - conexion (sql.Connection): Objeto de conexion a la base de datos SQLite.
        - cursor (sql.Cursor): Cursor para ejecutar sentencias SQL.
    """

    def __init__(self, db_ruta: str) -> None:
        """
        Argumentos:
            - db_ruta (str): Ruta del archivo de la base de datos SQLite.
        """
        self.conexion = sql.connect(db_ruta)
        self.cursor = self.conexion.cursor()

    def consultar_dataframe(self, ruta_sql: str, params: tuple = ()) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL desde un archivo y devuelve el resultado como un DataFrame de pandas.
        Argumentos:
            - ruta_sql (str): Ruta del archivo SQL que contiene la consulta.
            - params (tuple, opcional): Parametros opcionales para la consulta SQL.
        """
        with open(ruta_sql, 'r', encoding='utf-8') as archivo_sql:
            consulta = archivo_sql.read()

        return pd.read_sql_query(sql=consulta, con=self.conexion, params=params)

    def ejecutar_consulta(self, ruta_sql: str) -> None:
        """
        Ejecuta un script SQL.
        Argumentos:
            - ruta_sql (str): Ruta del archivo SQL que contiene la consulta.
        """
        with open(ruta_sql, "r", encoding="utf-8") as archivo:
            script = archivo.read()

        self.cursor.executescript(script)
        self.conexion.commit()

    def cerrar_conexion(self) -> None:
        """
        Cierra la conexión a la base de datos.
        """
        self.conexion.close()