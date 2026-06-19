-- Top 5 funds by composite score
SELECT fund, score, cagr_3yr, sharpe
FROM fund_scorecard
ORDER BY score DESC
LIMIT 5;

-- Funds with highest VaR (most risky)
SELECT fund, var_95_pct, cvar_95_pct, risk_grade
FROM var_cvar
ORDER BY var_95_pct ASC
LIMIT 10;

-- High alpha funds (beat benchmark)
SELECT fund, alpha_annualized, beta, r_squared
FROM alpha_beta
WHERE alpha_annualized > 0
ORDER BY alpha_annualized DESC;

-- Investor cohort summary
SELECT first_year,
       COUNT(DISTINCT investor_id) as investors,
       AVG(sip_amount) as avg_sip,
       SUM(sip_amount) as total_invested
FROM investor_data
GROUP BY first_year
ORDER BY first_year;