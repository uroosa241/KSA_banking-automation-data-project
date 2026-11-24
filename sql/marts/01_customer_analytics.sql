
CREATE SCHEMA IF NOT EXISTS mart;

CREATE OR REPLACE VIEW mart.customer_analytics AS
SELECT
    c.customer_key,
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    c.gender,
    c.registration_date,

    COUNT(DISTINCT a.account_key) AS total_accounts,

    COUNT(DISTINCT f.transaction_key) AS total_transactions,

    COALESCE(SUM(f.amount), 0) AS total_transaction_amount,

    COUNT(DISTINCT f.currency) AS currencies_used

FROM core.dim_customer c

LEFT JOIN core.dim_account a
    ON c.customer_key = a.customer_key

LEFT JOIN core.fact_transactions f
    ON c.customer_key = f.customer_key

GROUP BY
    c.customer_key,
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    c.gender,
    c.registration_date;
