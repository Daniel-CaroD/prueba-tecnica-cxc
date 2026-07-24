DROP TABLE IF EXISTS cxc_modelo;
CREATE TABLE cxc_modelo AS
SELECT
    printf('%04d-%02d', year, month) AS periodo,
    descri_cod_apli_prod AS producto,
    date(
        substr(CAST(f_creacion AS TEXT),1,4) || '-' ||
        substr(CAST(f_creacion AS TEXT),5,2) || '-' ||
        substr(CAST(f_creacion AS TEXT),7,2)
    ) AS fecha_creacion,
    date(
        substr(CAST(f_ultimo_pago AS TEXT),1,4) || '-' ||
        substr(CAST(f_ultimo_pago AS TEXT),5,2) || '-' ||
        substr(CAST(f_ultimo_pago AS TEXT),7,2)
    ) AS fecha_ultimo_pago,
    vlr_original AS valor_original,
    vlr_pagado AS valor_pagado,
    vlr_pendiente_pago AS valor_pendiente,
    descri_cod_trn AS tipo_transaccion,
    CASE
        WHEN vlr_pendiente_pago = 0 THEN 1
        ELSE 0
    END AS pagada
FROM tabla1;