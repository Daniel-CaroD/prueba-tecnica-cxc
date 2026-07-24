SELECT
    name AS variable,
    type AS tipo,
    cid AS posicion,
    CASE
        WHEN "notnull" = 0 THEN 'Si'
        ELSE 'No'
    END AS acepta_nulos,
    CASE
        WHEN pk = 1 THEN 'Si'
        ELSE 'No'
    END AS llave_primaria,
    CASE
        WHEN name IN (
            'vlr_original',
            'vlr_pagado',
            'vlr_pendiente_pago'
        ) THEN 'Numerica'

        WHEN name IN (
            'cod_apli_prod',
            'descri_cod_apli_prod',
            'num_cta',
            'cod_trn',
            'descri_cod_trn'
        ) THEN 'Categorica'

        WHEN name IN (
            'f_creacion',
            'f_ultimo_pago',
            'year',
            'month',
            'day'
        ) THEN 'Temporal'

        ELSE 'Otra'
    END AS tipo_variable
FROM pragma_table_info('tabla1');