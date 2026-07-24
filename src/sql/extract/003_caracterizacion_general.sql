SELECT
    -- Periodo analizado
    MIN(month) AS mes_inicio,
    MAX(month) AS mes_fin,
    MIN(year) AS anio,

    -- Cantidad de registros
    COUNT(*) AS total_registros,

    -- Tipos de cuenta
    GROUP_CONCAT(DISTINCT descri_cod_apli_prod) AS tipos_cuenta,

    -- Valores monetarios
    ROUND(AVG(vlr_original), 2) AS promedio_vlr_original,
    ROUND(AVG(vlr_pagado), 2) AS promedio_vlr_pagado,
    ROUND(AVG(vlr_pendiente_pago), 2) AS promedio_vlr_pendiente,

    -- Estadísticos del saldo pendiente
    ROUND(MIN(vlr_pendiente_pago), 2) AS minimo_pendiente,
    ROUND(MAX(vlr_pendiente_pago), 2) AS maximo_pendiente,

    ROUND(
        SQRT(
            AVG(vlr_pendiente_pago * vlr_pendiente_pago)
            -
            AVG(vlr_pendiente_pago) * AVG(vlr_pendiente_pago)
        ),
        2
    ) AS desviacion_pendiente

FROM tabla1;