SELECT
    descri_cod_trn,
    ROUND(SUM(vlr_pendiente_pago), 2) AS total_pendiente
FROM tabla1
GROUP BY descri_cod_trn
ORDER BY total_pendiente DESC
LIMIT 1;