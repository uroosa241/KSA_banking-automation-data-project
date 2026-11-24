
DROP TABLE IF EXISTS staging.accounts;

CREATE TABLE staging.accounts AS
WITH cleaned AS (
    SELECT
        TRIM(account_id) AS account_id,
        TRIM(customer_id) AS customer_id,
        INITCAP(TRIM(account_type)) AS account_type,
        TRIM(iban) AS iban,
        balance,
        UPPER(TRIM(currency)) AS currency,
        INITCAP(TRIM(account_status)) AS account_status,
        opening_date,
        loaded_at,
        ROW_NUMBER() OVER (
            PARTITION BY TRIM(account_id)
            ORDER BY loaded_at DESC
        ) AS row_num
    FROM raw.accounts
    WHERE account_id IS NOT NULL
      AND TRIM(account_id) <> ''
)
SELECT
    account_id,
    customer_id,
    account_type,
    iban,
    balance,
    currency,
    account_status,
    opening_date,
    loaded_at
FROM cleaned
WHERE row_num = 1;
