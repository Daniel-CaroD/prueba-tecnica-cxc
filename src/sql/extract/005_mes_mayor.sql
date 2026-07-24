SELECT
    month,
    ROUND(SUM(vlr_pendiente_pago),2) AS total_pendiente
FROM tabla1
GROUP BY month
ORDER BY total_pendiente DESC
LIMIT 1;