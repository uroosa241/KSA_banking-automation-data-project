
CREATE OR REPLACE VIEW mart.executive_kpis AS
SELECT
    currency,

    COUNT(*) AS total_transactions,

    COUNT(DISTINCT customer_key) AS total_customers,

    SUM(amount) AS total_transaction_amount,

    AVG(amount) AS average_transaction_amount,

    COUNT(*) FILTER (
        WHERE LOWER(transaction_status) = 'successful'
    ) AS successful_transactions,

    COUNT(*) FILTER (
        WHERE LOWER(transaction_status) = 'failed'
    ) AS failed_transactions,

    COUNT(*) FILTER (
        WHERE LOWER(transaction_status) = 'pending'
    ) AS pending_transactions,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE LOWER(transaction_status) = 'successful'
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS success_rate_percentage

FROM core.fact_transactions

GROUP BY currency;
