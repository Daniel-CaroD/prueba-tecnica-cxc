SELECT
    descri_cod_apli_prod AS tipo_cuenta,
    COUNT(*) AS cantidad_cuentas,
    ROUND(AVG(vlr_original),2) AS deuda_promedio,
    ROUND(AVG(vlr_pendiente_pago),2) AS pendiente_promedio
FROM tabla1
GROUP BY descri_cod_apli_prod;