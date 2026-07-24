"""
Modulo principal del proyecto
encargado de inicializar la aplicación y orquestar sus diferentes componentes
"""

# Importaciones
import streamlit as st
from src.logica_python.database import Database
from src.logica_python.preparador import PreparadorDatos
from src.logica_python.modelo import Modelo
from src.logica_python.evaluador import Evaluador
from src.logica_python.estimador import Estimador

# Rutas
DATABASE_PATH = "src/data/fuente_cxc.db"
SQL_EXTRACT_PATH = "src/sql/extract"
SQL_LOAD_PATH = "src/sql/load"

def main() -> None:
    """
    Funcion principal del proyecto.
    """

    # Iniciar conexion con la base de datos de "fuente_cxc"
    db = Database(DATABASE_PATH)

    # Configuracion de la pagina
    st.set_page_config(
        page_title="Prueba Técnica",
        layout="wide"
    )

    # Titulo y encabezado
    st.title("Prueba Técnica - Analista Semi-Senior Evolución y Mejora de la Operación Depósitos")

    st.markdown(
    """
    <h3 style="margin-bottom:0;">
        Sección Evolución Depósitos
    </h3>

    <h3 style="margin-top:0; margin-bottom:0;">
        Gerencia Operación Depósitos para Clientes
    </h3>

    <h4 style="color:gray; margin-top:10px;">
        Realizado por Daniel Steven Caro Durango
    </h4>

    <hr>
    """,
    unsafe_allow_html=True
)

    # Introduccion
    st.header("Introducción")

    st.markdown("""
    Esta aplicación presenta el proceso completo de obtención, transformación, exploración y análisis de la base de datos suministrada para la prueba técnica, la cual contiene información relacionada con las **Cuentas por Cobrar (CxC)**.

    A lo largo de la aplicación se documentan, de manera secuencial, las diferentes etapas del desarrollo, iniciando con la exploración y comprensión de los datos, seguida del proceso de transformación y preparación de la información para su análisis. Posteriormente, se presenta la metodología implementada para el desarrollo del modelo analítico, las métricas empleadas para evaluar su desempeño y los beneficios esperados para la operación.

    Finalmente, se presenta un **informe ejecutivo** que reúne el proceso de desarrollo realizado, la metodología aplicada, las hipótesis de negocio propuestas para ser abordadas mediante el modelo analítico, los principales hallazgos identificados durante el análisis, las métricas de evaluación del modelo, las visualizaciones desarrolladas para facilitar la interpretación de los resultados y un conjunto de conclusiones y recomendaciones orientadas a fortalecer la gestión operativa y apoyar la toma de decisiones basada en datos.
    """)

    # 1. Exploracion Inicial de los Datos
    st.header("1. Exploración Inicial de los Datos")

    st.markdown("""
    En esta sección se presenta una descripción general de la base de datos suministrada, mostrando su estructura, dimensiones y contenido inicial. El propósito es comprender las características de la información antes de iniciar cualquier proceso de transformación o análisis.
    """)

    # 1.1. Tabla principal
    st.subheader("1.1 Tabla principal")

    datos = db.consultar_dataframe(
        f"{SQL_EXTRACT_PATH}/000_obtener_tabla.sql"
    )

    st.write(f"**Número de registros:** {len(datos)}")
    st.write(f"**Número de variables:** {len(datos.columns)}")

    st.dataframe(
        datos,
        height=500,
        use_container_width=True
    )

    # 1.2. Resumen Mensual
    st.subheader("1.2 Resumen mensual")

    resumen = db.consultar_dataframe(
        f"{SQL_EXTRACT_PATH}/001_obtener_resumen_mensual.sql"
    )

    st.dataframe(
        resumen,
        height=350,
        use_container_width=True
    )

    grafica_trn = db.consultar_dataframe(
    f"{SQL_EXTRACT_PATH}/007_pendiente_por_transaccion.sql"
    )

    st.subheader("Saldo pendiente por tipo de transaccion")

    top = st.slider(
        "Numero de categorias a visualizar",
        min_value=5,
        max_value=len(grafica_trn),
        value=10,
        step=5
    )

    st.bar_chart(
        grafica_trn.head(top).set_index("descri_cod_trn")
    )

    # 1.3. Analisis de Variables
    st.subheader("1.3 Análisis de las Variables")

    variables = db.consultar_dataframe(
        f"{SQL_EXTRACT_PATH}/002_obtener_analisis_variables.sql"
    )

    st.dataframe(
        variables,
        use_container_width=True,
        hide_index=True
    )

    # 1.4 Caracterizacion general de la base de datos
    st.header("1.4 Caracterización General de la Base de Datos")

    st.info("""
    Esta sección resume las principales características identificadas durante la exploración inicial de la base de datos, proporcionando un contexto general sobre la información disponible antes de iniciar las etapas de preparación y análisis.
    """)

    # Consultas
    caracterizacion = db.consultar_dataframe(
        f"{SQL_EXTRACT_PATH}/003_caracterizacion_general.sql"
    )

    tipo_cobro = db.consultar_dataframe(
        f"{SQL_EXTRACT_PATH}/004_tipo_cobro_mayor.sql"
    )

    mes = db.consultar_dataframe(
        f"{SQL_EXTRACT_PATH}/005_mes_mayor.sql"
    )

    tipos_cuenta = db.consultar_dataframe(
        f"{SQL_EXTRACT_PATH}/006_resumen_cuentas.sql"
    )

    # Cada consulta devuelve una sola fila
    car = caracterizacion.iloc[0]
    cobro = tipo_cobro.iloc[0]
    mes_pendiente = mes.iloc[0]

    st.subheader("Resumen Ejecutivo")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Períodos Analizados",
            f"{car['mes_inicio']} - {car['mes_fin']} / {car['anio']}"
        )

    with col2:
        st.metric(
            "Tipos de Cuenta",
            car["tipos_cuenta"]
        )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Deuda Promedio",
            f"${car['promedio_vlr_original']:,.2f}"
        )

    with col2:
        st.metric(
            "Pago Promedio",
            f"${car['promedio_vlr_pagado']:,.2f}"
        )

    with col3:
        st.metric(
            "Pendiente Promedio",
            f"${car['promedio_vlr_pendiente']:,.2f}"
        )

    st.subheader("Descripción General")

    st.markdown(f"""
    La base de datos suministrada corresponde a la información de <b>Cuentas por Cobrar (CxC)</b> registrada durante los meses <b>{car['mes_inicio']}</b> y <b>{car['mes_fin']}</b> del año <b>{car['anio']}</b>.<br><br>

    Los registros incluyen obligaciones correspondientes a <b>{car['tipos_cuenta']}</b>, para las cuales se dispone del valor original de la obligación, el valor efectivamente pagado y el saldo pendiente de pago.<br><br>

    En promedio, cada obligación registra un valor inicial de <b>\${car['promedio_vlr_original']:,.2f}</b>. De este valor se recuperan, en promedio, <b>\${car['promedio_vlr_pagado']:,.2f}</b>, mientras que permanece un saldo pendiente promedio de <b>\${car['promedio_vlr_pendiente']:,.2f}</b>.
    """, unsafe_allow_html=True)

    st.subheader("Variabilidad del Saldo Pendiente")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Valor mínimo",
        f"${car['minimo_pendiente']:,.2f}"
    )

    col2.metric(
        "Valor máximo",
        f"${car['maximo_pendiente']:,.2f}"
    )

    col3.metric(
        "Desviación estándar",
        f"${car['desviacion_pendiente']:,.2f}"
    )

    st.markdown(f"""
    La variabilidad del saldo pendiente muestra que los valores registrados oscilan entre <b>\${car['minimo_pendiente']:,.2f}</b> y <b>\${car['maximo_pendiente']:,.2f}</b>, con una desviación estándar de <b>\${car['desviacion_pendiente']:,.2f}</b>. Estos resultados evidencian la dispersión existente en los saldos pendientes de las obligaciones analizadas.
    """, unsafe_allow_html=True)

    st.subheader("Distribución por Tipo de Cuenta")

    st.dataframe(
        tipos_cuenta,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Hallazgos Iniciales")

    st.success(f"""
    **Mayor saldo pendiente por tipo de cobro**

    - Tipo de cobro: **{cobro['descri_cod_trn']}**
    - Saldo pendiente acumulado: **${cobro['total_pendiente']:,.2f}**

    **Mes con mayor saldo pendiente**

    - Mes: **{mes_pendiente['month']}**
    - Saldo pendiente acumulado: **${mes_pendiente['total_pendiente']:,.2f}**
    """)

    st.warning(f"""
    Los resultados obtenidos permiten plantear una hipótesis inicial sobre el comportamiento de la cartera.

    El mayor saldo pendiente se concentra en el tipo de cobro **{cobro['descri_cod_trn']}**, mientras que el mayor valor pendiente acumulado se registra durante el mes **{mes_pendiente['month']}**.

    Estos resultados sugieren la conveniencia de analizar si durante dicho período se presentaron cambios operativos, modificaciones en productos o servicios, fricciones en el proceso de recaudo o factores externos de carácter económico, social o regulatorio que hayan influido en el comportamiento de pago.

    El modelo analítico propuesto permitirá complementar este análisis mediante la identificación de patrones asociados al incumplimiento y apoyar la formulación de estrategias orientadas a mejorar la gestión de la cartera.
    """)

    # 1.5 Preparacion de la base de datos para el modelo
    db.ejecutar_consulta(f"{SQL_LOAD_PATH}/008_cxc_modelo.sql")
    db.ejecutar_consulta(f"{SQL_LOAD_PATH}/009_resumen_modelo.sql")

    st.header("1.5 Preparación de la Base de Datos para el Modelo")

    st.markdown("""
    Con el propósito de facilitar la construcción del modelo analítico y garantizar la calidad de la información utilizada durante el entrenamiento, se generaron nuevas tablas a partir de la base de datos original.

    Durante este proceso se realizó una transformación de los datos que incluyó el cambio de nombres de las variables por nombres más descriptivos, la conversión del formato de las fechas, la eliminación de atributos que no aportan información al modelo y la creación de una estructura orientada al análisis predictivo.

    Como resultado se obtuvieron las siguientes tablas, las cuales serán utilizadas en las etapas posteriores del desarrollo del modelo.
    """)

    modelo = db.consultar_dataframe(f"{SQL_EXTRACT_PATH}/010_obtener_cxc_modelo.sql")

    st.subheader("Base de datos preparada para el modelo")

    st.dataframe(
        modelo,
        use_container_width=True
    )

    resumen_modelo = db.consultar_dataframe(f"{SQL_EXTRACT_PATH}/011_obtener_resumen_modelo.sql")

    st.subheader("Resumen mensual preparado")

    st.dataframe(
        resumen_modelo,
        use_container_width=True
    )

    st.success("""
    **Transformaciones realizadas**

    - Se reemplazaron los nombres técnicos de las variables por nombres descriptivos.
    - Se convirtieron las fechas al formato `YYYY-MM-DD` para facilitar su interpretación y procesamiento.
    - Se consolidó la información relevante en una única tabla preparada para el entrenamiento del modelo analítico.
    - Se definió la variable objetivo **pagada**, que identifica si la obligación fue saldada completamente (`1`) o si mantiene saldo pendiente (`0`).
    - Se construyó una tabla resumen con estadísticas agregadas por período, producto y tipo de transacción para apoyar el análisis exploratorio y la validación de resultados.
    """)

    # 2. Construccion del modelo analitico
    st.header("2. Construcción del Modelo Analítico")

    modelo_df = db.consultar_dataframe(f"{SQL_EXTRACT_PATH}/010_obtener_cxc_modelo.sql")

    # 2.1 Definicoón del modelo
    st.subheader("2.1 Definición del Modelo")

    st.markdown("""
    Para estimar la probabilidad de que una cuenta por cobrar sea pagada se implementó
    un modelo de **Regresión Logística**.

    Este algoritmo permite resolver problemas de clasificación binaria, donde la variable
    objetivo toma los valores:

    - **1:** Cuenta pagada.
    - **0:** Cuenta con saldo pendiente.
    """)

    st.write("Vista previa de la base utilizada para el entrenamiento:")

    st.dataframe(
        modelo_df.head(),
        use_container_width=True
    )

    # 2.2 Preparacion de datos
    st.subheader("2.2 Preparación de los Datos")

    preparador = PreparadorDatos(

        columna_objetivo="pagada",

        columnas_fecha=[
            "fecha_creacion",
            "fecha_ultimo_pago"
        ],

        columnas_categoricas=[
            "producto",
            "tipo_transaccion"
        ],

        columnas_numericas=[
            "valor_original",
            "valor_pagado",
            "valor_pendiente"
        ]
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
        df_train,
        df_test,
        preprocesador
    ) = preparador.preparar(modelo_df)

    col1, col2 = st.columns(2)

    col1.metric(
        "Observaciones entrenamiento",
        len(X_train)
    )

    col2.metric(
        "Observaciones prueba",
        len(X_test)
    )

    st.success("Preparación de datos completada correctamente.")

    # 2.3 Entrenamiento
    st.subheader("2.3 Entrenamiento")
    modelo = Modelo()

    modelo.entrenar(
        X_train,
        y_train,
        preprocesador
    )

    st.success("Modelo entrenado correctamente.")

    # Predicciones
    y_pred = modelo.predecir(X_test)
    y_prob = modelo.predecir_probabilidades(X_test)[:, 1]

    # 2.4 Evaluacion
    st.subheader("2.4 Evaluación")

    evaluador = Evaluador()

    metricas = evaluador.evaluar(
        y_test,
        y_pred,
        y_prob
    )
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Accuracy",
        f"{metricas['accuracy']:.3f}"
    )

    c2.metric(
        "Precision",
        f"{metricas['precision']:.3f}"
    )

    c3.metric(
        "Recall",
        f"{metricas['recall']:.3f}"
    )

    c4.metric(
        "F1",
        f"{metricas['f1']:.3f}"
    )

    c5.metric(
        "ROC AUC",
        f"{metricas['roc_auc']:.3f}"
    )

    st.subheader("Matriz de Confusión")

    st.dataframe(metricas["matriz_confusion"])

    st.subheader("Reporte de Clasificación")

    st.text(metricas["classification_report"])

    # 2.5 Estimacion
    st.subheader("2.5 Estimación")

    estimador = Estimador()

    estimaciones = estimador.estimar(
        pipeline=modelo.obtener_pipeline(),
        X=X_test,
        df_original=df_test,
        columna_valor="valor_original"
    )

    st.dataframe(
        estimaciones,
        use_container_width=True
    )

    st.subheader("Valor esperado por producto")

    resumen_producto = estimador.resumir(
        estimaciones,
        columna_grupo="producto"
    )

    st.dataframe(
        resumen_producto,
        use_container_width=True
    )

    st.subheader("Valor esperado por tipo de transacción")

    resumen_tipo = estimador.resumir(
        estimaciones,
        columna_grupo="tipo_transaccion"
    )

    st.dataframe(
        resumen_tipo,
        use_container_width=True
    )

    # 2.6 Conclusiones
    st.subheader("2.6 Conclusiones")

    total_cuentas = len(estimaciones)

    cuentas_pagadas = (
        estimaciones["probabilidad"] >= 0.5
    ).sum()

    cuentas_pendientes = total_cuentas - cuentas_pagadas

    valor_esperado = estimaciones["valor_esperado"].sum()

    st.success(f"""
    ### Principales resultados

    El modelo de Regresión Logística obtuvo los siguientes indicadores de desempeño:

    - Accuracy: **{metricas['accuracy']:.3f}**
    - Precision: **{metricas['precision']:.3f}**
    - Recall: **{metricas['recall']:.3f}**
    - F1 Score: **{metricas['f1']:.3f}**
    - ROC AUC: **{metricas['roc_auc']:.3f}**

    ### Estimación para el siguiente período

    De acuerdo con las probabilidades estimadas por el modelo para las **{total_cuentas} cuentas** evaluadas:

    - Se espera que aproximadamente **{cuentas_pagadas} cuentas** sean pagadas completamente.
    - Aproximadamente **{cuentas_pendientes} cuentas** podrían mantener saldo pendiente.
    - El **valor esperado de recaudo** estimado es de **${valor_esperado:,.2f}**.

    Estas estimaciones permiten priorizar la gestión de cobranza sobre aquellas cuentas con menor probabilidad de pago y facilitan la planeación operativa para el siguiente período.
    """)


    # Cerrar conexion
    db.cerrar_conexion()

if __name__ == "__main__":
    main()