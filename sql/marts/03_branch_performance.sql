
CREATE OR REPLACE VIEW mart.branch_performance AS
SELECT
    b.branch_id,
    b.branch_name,
    f.currency,

    COUNT(f.transaction_key) AS total_transactions,

    SUM(f.amount) AS total_transaction_amount,

    AVG(f.amount) AS average_transaction_amount,

    COUNT(*) FILTER (
        WHERE LOWER(f.transaction_status) = 'successful'
    ) AS successful_transactions,

    COUNT(*) FILTER (
        WHERE LOWER(f.transaction_status) = 'failed'
    ) AS failed_transactions

FROM core.dim_branch b

LEFT JOIN core.fact_transactions f
    ON b.branch_key = f.branch_key

GROUP BY
    b.branch_id,
    b.branch_name,
    f.currency;
