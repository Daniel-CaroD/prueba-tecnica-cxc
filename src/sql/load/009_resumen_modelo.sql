DROP TABLE IF EXISTS resumen_modelo;
CREATE TABLE resumen_modelo AS
SELECT
    printf('%04d-%02d', year, month) AS periodo,
    descri_cod_apli_prod AS producto,
    descri_cod_trn AS tipo_transaccion,
    COUNT(*) AS num_registros,
    SUM(vlr_original) AS valor_original,
    SUM(vlr_pagado) AS valor_pagado,
    SUM(vlr_pendiente_pago) AS valor_pendiente
FROM tabla1
GROUP BY
    periodo,
    producto,
    tipo_transaccion
ORDER BY
    periodo,
    producto,
    tipo_transaccion;