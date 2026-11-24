
CREATE SCHEMA IF NOT EXISTS fraud;

CREATE OR REPLACE VIEW fraud.fraud_indicators AS

SELECT
    f.transaction_id,
    f.customer_key,
    f.account_key,
    f.branch_key,
    f.transaction_type,
    f.amount,
    f.currency,
    f.transaction_date,
    f.transaction_status,

    CASE
        WHEN f.amount >= 40000 THEN 'HIGH AMOUNT'

        WHEN LOWER(f.transaction_status) = 'failed'
            THEN 'FAILED TRANSACTION'

        WHEN f.amount < 0
            THEN 'NEGATIVE AMOUNT'

        ELSE 'NORMAL'
    END AS risk_indicator,

    CASE
        WHEN f.amount >= 40000 THEN 'HIGH'

        WHEN LOWER(f.transaction_status) = 'failed'
            THEN 'MEDIUM'

        WHEN f.amount < 0
            THEN 'MEDIUM'

        ELSE 'LOW'
    END AS risk_level

FROM core.fact_transactions f

WHERE
    f.amount >= 40000
    OR LOWER(f.transaction_status) = 'failed'
    OR f.amount < 0;
