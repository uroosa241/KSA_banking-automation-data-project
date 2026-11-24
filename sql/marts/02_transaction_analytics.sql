
CREATE OR REPLACE VIEW mart.transaction_analytics AS
SELECT
    EXTRACT(YEAR FROM transaction_date)::INTEGER AS transaction_year,
    EXTRACT(MONTH FROM transaction_date)::INTEGER AS transaction_month,
    TO_CHAR(transaction_date, 'FMMonth') AS month_name,
    currency,
    transaction_type,
    transaction_status,

    COUNT(*) AS total_transactions,

    SUM(amount) AS total_transaction_amount,

    AVG(amount) AS average_transaction_amount,

    MIN(amount) AS minimum_transaction_amount,

    MAX(amount) AS maximum_transaction_amount

FROM core.fact_transactions

GROUP BY
    EXTRACT(YEAR FROM transaction_date),
    EXTRACT(MONTH FROM transaction_date),
    TO_CHAR(transaction_date, 'FMMonth'),
    currency,
    transaction_type,
    transaction_status;
