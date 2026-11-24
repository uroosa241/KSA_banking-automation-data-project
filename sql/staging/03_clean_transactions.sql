
DROP TABLE IF EXISTS staging.transactions;

CREATE TABLE staging.transactions AS
WITH cleaned AS (
    SELECT
        TRIM(transaction_id) AS transaction_id,
        TRIM(account_id) AS account_id,
        TRIM(customer_id) AS customer_id,
        INITCAP(TRIM(transaction_type)) AS transaction_type,
        amount,
        UPPER(TRIM(currency)) AS currency,
        transaction_date,
        INITCAP(TRIM(transaction_status)) AS transaction_status,
        TRIM(branch_id) AS branch_id,
        loaded_at,
        ROW_NUMBER() OVER (
            PARTITION BY TRIM(transaction_id)
            ORDER BY loaded_at DESC
        ) AS row_num
    FROM raw.transactions
    WHERE transaction_id IS NOT NULL
      AND TRIM(transaction_id) <> ''
)
SELECT
    transaction_id,
    account_id,
    customer_id,
    transaction_type,
    amount,
    currency,
    transaction_date,
    transaction_status,
    branch_id,
    loaded_at
FROM cleaned
WHERE row_num = 1;
