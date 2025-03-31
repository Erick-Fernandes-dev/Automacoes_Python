-- 10 maiores despesas no último trimestre completo
WITH ultimo_trimestre AS (
    SELECT 
        date_trunc('quarter', CURRENT_DATE) - INTERVAL '3 months' AS inicio,
        date_trunc('quarter', CURRENT_DATE) - INTERVAL '1 day' AS fim
)
SELECT 
    o.razao_social,
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS total_despesas
FROM demonstracoes_contabeis d
JOIN operadoras o ON d.reg_ans = o.registro_ans
WHERE d.descricao ILIKE 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
AND d.data BETWEEN (SELECT inicio FROM ultimo_trimestre) 
                AND (SELECT fim FROM ultimo_trimestre)
GROUP BY o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;


-- 10 maiores despesas no último ano
SELECT 
    o.razao_social,
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS total_despesas
FROM demonstracoes_contabeis d
JOIN operadoras o ON d.reg_ans = o.registro_ans
WHERE d.descricao ILIKE 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
AND d.data BETWEEN (CURRENT_DATE - INTERVAL '1 year') AND CURRENT_DATE
GROUP BY o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;