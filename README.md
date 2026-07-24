# Prueba Técnica – Mejora de Procesos

Este repositorio contiene la solución desarrollada para la prueba técnica del proceso de selección para el cargo de **Analista Semi-Senior de Evolución y Mejora de la Operación de Depósitos**.

El proyecto integra consultas SQL, un modelo de Machine Learning desarrollado en Python y una aplicación interactiva en Streamlit para el análisis de cuentas por cobrar. Como resultado, también se generan archivos que pueden utilizarse para construir un dashboard en Power BI.

---

## Tecnologías utilizadas

- Python
- SQLite
- Pandas
- NumPy
- Scikit-Learn
- Streamlit
- Matplotlib

---

## Estructura del proyecto

```text
.
├── .streamlit
│   ├── config.toml
├── docs
│   ├── informe_ejecutivo.docx
├── src
│   ├── data
│   │   └── fuente_cxc.db
│   ├── logica_python
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── preparador.py
│   │   ├── modelo.py
│   │   ├── evaluador.py
│   │   └── estimador.py
│   ├── resultados
│   └── sql
├── app.py
├── .gitignore
├── .requirements.txt
└── README.md
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd prueba-tecnica-mejora-de-procesos
```

### 2. Crear un entorno virtual

**Windows**

```bash
python -m venv .venv
```

**Linux / macOS**

```bash
python3 -m venv .venv
```

### 3. Activar el entorno virtual

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecución del proyecto

Una vez instaladas las dependencias, ejecutar la aplicación con:

```bash
streamlit run app.py
```

La aplicación abrirá automáticamente una ventana del navegador.

---

## Funcionamiento

La aplicación realiza automáticamente las siguientes etapas:

1. Conexión a la base de datos SQLite.
2. Ejecución de las consultas SQL para construir la tabla de modelado.
3. Preparación de los datos.
4. Entrenamiento del modelo de Machine Learning.
5. Evaluación del modelo mediante métricas de clasificación.
6. Estimación de probabilidades y cálculo del valor esperado.
7. Generación de los archivos de resultados para su análisis en Power BI.

---

## Archivos generados

Al finalizar la ejecución, se generan automáticamente archivos en:

```text
src/resultados/
```

Estos archivos contienen la información utilizada posteriormente para construir el dashboard en Power BI.

---

## Base de datos

La base de datos utilizada se encuentra en:

```text
src/data/fuente_cxc.db
```

No es necesario realizar ninguna configuración adicional para su funcionamiento.

---

## Dependencias principales

Las dependencias utilizadas se encuentran definidas en el archivo `requirements.txt`.

```

---

## Autor

**Daniel Steven Caro Durango**
