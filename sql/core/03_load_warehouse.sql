
-- =========================================
-- 1. LOAD CUSTOMER DIMENSION
-- =========================================

INSERT INTO core.dim_customer (
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    gender,
    date_of_birth,
    registration_date
)
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    gender,
    date_of_birth,
    registration_date
FROM staging.customers
ON CONFLICT (customer_id)
DO UPDATE SET
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    email = EXCLUDED.email,
    phone = EXCLUDED.phone,
    city = EXCLUDED.city,
    gender = EXCLUDED.gender,
    date_of_birth = EXCLUDED.date_of_birth,
    registration_date = EXCLUDED.registration_date;


-- =========================================
-- 2. LOAD ACCOUNT DIMENSION
-- =========================================

INSERT INTO core.dim_account (
    account_id,
    customer_key,
    account_type,
    iban,
    balance,
    currency,
    account_status,
    opening_date
)
SELECT
    a.account_id,
    c.customer_key,
    a.account_type,
    a.iban,
    a.balance,
    a.currency,
    a.account_status,
    a.opening_date
FROM staging.accounts a
LEFT JOIN core.dim_customer c
    ON a.customer_id = c.customer_id
ON CONFLICT (account_id)
DO UPDATE SET
    customer_key = EXCLUDED.customer_key,
    account_type = EXCLUDED.account_type,
    iban = EXCLUDED.iban,
    balance = EXCLUDED.balance,
    currency = EXCLUDED.currency,
    account_status = EXCLUDED.account_status,
    opening_date = EXCLUDED.opening_date;


-- =========================================
-- 3. LOAD BRANCH DIMENSION
-- =========================================

INSERT INTO core.dim_branch (
    branch_id,
    branch_name
)
SELECT DISTINCT
    branch_id,
    'Branch ' || branch_id
FROM staging.transactions
WHERE branch_id IS NOT NULL
  AND TRIM(branch_id) <> ''
ON CONFLICT (branch_id)
DO UPDATE SET
    branch_name = EXCLUDED.branch_name;


-- =========================================
-- 4. LOAD DATE DIMENSION
-- =========================================

INSERT INTO core.dim_date (
    date_key,
    full_date,
    day_number,
    month_number,
    month_name,
    quarter_number,
    year_number,
    day_name,
    is_weekend
)
SELECT
    TO_CHAR(d::DATE, 'YYYYMMDD')::INTEGER,
    d::DATE,
    EXTRACT(DAY FROM d)::INTEGER,
    EXTRACT(MONTH FROM d)::INTEGER,
    TO_CHAR(d, 'FMMonth'),
    EXTRACT(QUARTER FROM d)::INTEGER,
    EXTRACT(YEAR FROM d)::INTEGER,
    TO_CHAR(d, 'FMDay'),
    EXTRACT(ISODOW FROM d)::INTEGER IN (6, 7)
FROM generate_series(
    (SELECT MIN(transaction_date)::DATE
     FROM staging.transactions
     WHERE transaction_date IS NOT NULL),
    (SELECT MAX(transaction_date)::DATE
     FROM staging.transactions
     WHERE transaction_date IS NOT NULL),
    INTERVAL '1 day'
) AS dates(d)
ON CONFLICT (date_key)
DO NOTHING;


-- =========================================
-- 5. LOAD TRANSACTION FACT TABLE
-- =========================================

INSERT INTO core.fact_transactions (
    transaction_id,
    customer_key,
    account_key,
    branch_key,
    date_key,
    transaction_type,
    amount,
    currency,
    transaction_date,
    transaction_status
)
SELECT
    t.transaction_id,
    c.customer_key,
    a.account_key,
    b.branch_key,
    d.date_key,
    t.transaction_type,
    t.amount,
    t.currency,
    t.transaction_date,
    t.transaction_status
FROM staging.transactions t

LEFT JOIN core.dim_customer c
    ON t.customer_id = c.customer_id

LEFT JOIN core.dim_account a
    ON t.account_id = a.account_id

LEFT JOIN core.dim_branch b
    ON t.branch_id = b.branch_id

LEFT JOIN core.dim_date d
    ON t.transaction_date::DATE = d.full_date

ON CONFLICT (transaction_id)
DO UPDATE SET
    customer_key = EXCLUDED.customer_key,
    account_key = EXCLUDED.account_key,
    branch_key = EXCLUDED.branch_key,
    date_key = EXCLUDED.date_key,
    transaction_type = EXCLUDED.transaction_type,
    amount = EXCLUDED.amount,
    currency = EXCLUDED.currency,
    transaction_date = EXCLUDED.transaction_date,
    transaction_status = EXCLUDED.transaction_status,
    loaded_at = CURRENT_TIMESTAMP;
