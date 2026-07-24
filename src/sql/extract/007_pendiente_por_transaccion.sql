SELECT
    descri_cod_trn,
    SUM(vlr_pendiente_pago) AS total_pendiente
FROM tabla1
GROUP BY descri_cod_trn
ORDER BY total_pendiente DESC;